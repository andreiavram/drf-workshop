gunicorn -b :8090 --workers=4 --env DJANGO_SETTINGS_MODULE=device_rest_api.settings device_rest_api.wsgi
