# TA Metrics

## Team Members

**Daniel Brott**

**Monika Davies**

**Alejandro Rivera**

**Andy Nguyen**

**Natalija Germek**

## Project Description

This project is a full-stack application which aims to help Code Fellows administrators and teaching assistants (TAs) visualize metrics regarding help ticket velocity (how many help tickets each TA is taking everyday, how long is each TA spending on a ticket, which classes have the most number of tickets at any given time, etc.). Through this project, Code Fellows administrators are able to identify how to best allocate TAs to help students as well as identify possible areas of improvement with Code Fellows' course curriculums.

## Tools Used

- Trello
- PyCharm
- Django
- Python
- NextJS
- React
- JavaScript

## Links and Models

- [Trello](https://trello.com/b/jz4OJzfn/ta-metrics)

- [Domain Model](documentation/domain_model.png)

- [Table Wireframe](documentation/TableWireframe.png)

- [Application Wireframe](documentation/Wireframe.png)

## Functions and Methods

| Function or Method        | Summary                                                                                                                           | Example                                          | 
|:--------------------------|:----------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|
| call_api()                | Makes call to Code Fellows API and returns JSON data from specified start date                                                    | call_api(start_date)                             |
| get_request()             | Gets start and end date query parameters and converts them to datetime objects                                                    | get_request(request)                             |
| fields_to_pacific_dates() | Takes single ticket entry JSON data from Code Fellows API and converts date string fields to datetime objects in Pacific timezone | fields_to_pacific_dates(day)                     |
| pop_day_container()       | Populates day container                                                                                                           | pop_day_container(container, day, date_idx)      |
| get_hour_str()            | Converts hour to string for dictionary look up in container                                                                       | get_hour_str(time)                               |
| to_pacific_time()         | Converts string to datetime object in Pacific timezone                                                                            | to_pacific_time(time)                            |
| create_day_container()    | Creates empty container for get_tickets_and_wait function                                                                         | create_day_container(start_date, end_date)       |
| daily_tickets_waits()     | Populates container with mean, median and average data on number of tickets and total wait times                                  | daily_tickets_waits(request)                     |
| get_summary_stats()       | Returns summary statistics on wait times for a range of dates                                                                     | get_summary_stats(request)                       |
| pop_ta_day_container()    | Populates day container for TA stats                                                                                              | pop_ta_day_container(container, day, date_idx)   |
| daily_ta_data()           | Populates day container for TA stats                                                                                              | daily_ta_data(request)                           |
| ta_summary_stats()        | Populates data per TA, specifically total tickets, total time and unique students                                                 | ta_summary_stats(request)                        |
| formatData              | format’s the data to populate date, time, hourlyTickets, hourlyWait, totalTickets, totalWait for the Admin Chart | ta_summary_stats(request)                        |

| Function or Method | Summary                                                                                                                          | Example                 | 
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------|:------------------------|
| oauth_start()      | Set state for OAuth                                                                                                              | oauth_start(request)    |
| oauth_callback()   | Populates day container                                                                                                          | oauth_callback(request) |
| id_token(request)  | generates expired login error if time out occurs                                                                                 | id_token(request)       |

## Setup

Install Redis locally:

```bash
brew install redis
```

Then run redis in a terminal window:

```bash
redis-server
```

Install `mkcert` to self-sign certificates and run HTTPS locally: https://github.com/FiloSottile/mkcert

Run `mkcert -install` to install local certificate authority

Then, in the root of the project, run the following command to generate a certificate:

```bash
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```

Create a `.env` file in the `ta_metrics_project` directory with the following variables:

```dotenv
SLACK_CLIENT_ID=<YOUR_SLACK_CLIENT_ID>
SLACK_CLIENT_SECRET=<YOUR_SLACK_CLIENT_SECRET>
SLACK_REDIRECT_URL=<YOUR_SLACK_REDIRECT_URL>
```

To create a local virtual environment in the root of the project:

```bash
python -m venv .venv
```

To activate the virtual environment:

```bash
source .venv/bin/activate
```

To deactivate the virtual environment:

```bash
deactivate
```

To install dependencies:

```bash
pip install -r requirements.txt
```

To run locally with https:

```bash
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```

Reference: 

[Django Development Server Certificate](https://timonweb.com/django/https-django-development-server-ssl-certificate/)

## Reference for Slack OAuth

[Slack OAuth](https://github.com/slackapi/python-slack-sdk/blob/main/integration_tests/samples/openid_connect/flask_example.py)

## Change log

- Crated Wireframes, Domain Model, updated README.md - 07 March 2023.

### Version

*Version 1.0* Created team agreement, Trello board, README - March 6, 2023

*Version 1.1* Continued to completed call_api() function - 08 March 2023

*Version 2.0* Refactor API call functions. Refactor date/time function to access date based on client date range input. - 09 March 2023

*Version 2.1* Completed Functions for API calculation and data gathering, updated README.md. - 11 March 2023

*Version 2.2* Updated README.md, initial creation of tests. - 14 March 2023

*Version 2.3* Updated README.md, created more tests, integrated OAuth, Updated views, updated requirements.txt. - 15 March 2023

*Version 2.4* Added more tests, refactored some tests, updated README.md and added to TAView logic. - 16 March 2023

*Version 2.5* Testing refactoring. - 17 March 2023