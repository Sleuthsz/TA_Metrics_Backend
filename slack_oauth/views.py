import logging
import time

import jwt
import redis
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from slack_sdk import WebClient
from slack_sdk.oauth import OpenIDConnectAuthorizeUrlGenerator, RedirectUriPageRenderer
from slack_sdk.oauth.state_store import FileOAuthStateStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

client_id = settings.SLACK_CLIENT_ID
client_secret = settings.SLACK_CLIENT_SECRET
redirect_uri = settings.SLACK_REDIRECT_URL
scopes = ['openid', 'email', 'profile']

state_store = FileOAuthStateStore(
    expiration_seconds=300,
    base_dir='/tmp'
)
authorization_url_generator = OpenIDConnectAuthorizeUrlGenerator(
    client_id=client_id,
    scopes=scopes,
    redirect_uri=redirect_uri
)

redirect_page_renderer = RedirectUriPageRenderer(
    install_path='/slack/install',
    redirect_uri_path='/slack/oauth_redirect'
)

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)


def auth_check(func):
    def wrapper(*args, **kwargs):
        token = args[0].META.get('HTTP_AUTHORIZATION').split()[1]
        claims = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
        expiration_time = int(claims.get('exp'))
        current_time = int(time.time())
        if expiration_time < current_time:
            redis_client.delete(token)
            return JsonResponse({
                'expired': True
            })
        else:
            retrieved_id_token = redis_client.get(token)
            if retrieved_id_token is not None:
                result = func(*args, **kwargs)
                return result
            else:
                return JsonResponse({
                    'expired': True
                })

    return wrapper


@api_view(['GET'])
def oauth_start(request):
    state = state_store.issue()
    url = authorization_url_generator.generate(state=state)
    return JsonResponse({'redirect_url': url})


@api_view(['GET'])
def oauth_callback(request):
    code = request.GET.get('code')
    if code is not None:
        state = request.GET.get('state')
        if state_store.consume(state):
            try:
                token_response = WebClient().openid_connect_token(
                    client_id=client_id,
                    client_secret=client_secret,
                    code=code
                )
                token = token_response.get("id_token")
                claims = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
                exp_time = claims.get("exp")
                new_exp_time = exp_time + 3600
                claims["exp"] = new_exp_time
                new_token = jwt.encode(payload=claims, key='ta_metrics')
                # new_claims = jwt.decode(new_token, options={"verify_signature": False}, algorithms=["RS256"])
                redis_client.set(new_token, new_token)
                return redirect(f'{settings.FRONTEND_URL}/redirect/?id_token={new_token}')
            except Exception as e:
                logger.exception('Failed to perform openid.connect.token API call\n')
                logger.error(f'{e}\n')
                return redirect_page_renderer.render_failure_page('Failed to perform openid.connect.token API call')
        else:
            return redirect_page_renderer.render_failure_page('The state value is already expired')
    else:
        error = request.GET.get('error')
        return HttpResponseBadRequest(f'Something is wrong with the installation (error: {error})')


@api_view(['GET'])
def logout(request):
    token = request.META.get('HTTP_AUTHORIZATION').split()[1]
    redis_client.delete(token)
    return JsonResponse({
        'expired': True
    })
