## Introduction
Create Short URLs, QR Codes in simple and easy way. This application also supports API requests.

## Features


- Create Short URLs
- Create QR Codes of type: URL, Me-Card, WIFI
- Acces using API created using Django Rest Framework
- User Dashboard
- Pricing Section
- Beautiful API Docs## Tech Stack

**Client Side:** HTML, CSS, SCSS, TailwindCSS, JavaScript, JQuery

**Server Side:** Python, Django, Django Rest Framework

**Database:** SQLite

**Integrations:** Instamojo Payment Gateway

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Django settings

`DEBUG = TRUE`

`SECRET_KEY = "django-insecure-yqz=6w&d3zshvkyl%1e41p%5p9$#&ag0ljzj!@-f4l@(#8xy7j"`


- For sending emails
`EMAIL_HOST_USER = "email address from which email will be send"`

`EMAIL_HOST_PASSWORD = "its app password"`

Note : You have to create app password for the email you are using in `EMAIL_HOST_USER` and put it in `EMAIL_HOST_PASSWORD`

- For instamojo payment gateway
`API_KEY = "YOUR_API_KEY"`

`AUTH_TOKEN = "YOUR_AUTH_TOKEN"`

`ENDPOINT = "https://test.instamojo.com/api/1.1/"`

Note : For instamojo you have to create an account on instamojo: https://www.instamojo.com/. Change the `API_KEY`, `AUTH_TOKEN`, `ENDPOINT="https://instamojo.com/api/1.1/"` for production.


## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/SBCare

```
or simply download this project from https://github.com/Mr-Atanu-Roy/SBCare

In project directory Create a virtual environment of any name(say env)

```bash
  virtualenv env

```
Activate the virtual environment

For windows:
```bash
  env\Script\activate

```
Install dependencies
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands
```bash
  py manage.py makemigrations
  py manage.py migrate

```

Create a super user
```bash
  py manage.py createsuperuser

```
Then add some data into database


To run the project in your localserver
```bash
  py manage.py runserver

```
## Authors

- [@Atanu Roy](https://github.com/Mr-Atanu-Roy)

