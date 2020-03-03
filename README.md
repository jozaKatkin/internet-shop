# internet-shop

My final project - a simple bakery store.

## Features
- sending emails (order confirmation, user verification)
- authentication (allauth)
- signals
- pagination

## Installation

Linux:

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install requirements.txt
```

## Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Testing Emails

To output an account verification message to a console use this in your settings.py file:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
To send order confirmations use:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

## Built With
- Django
- Bootstrap