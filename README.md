# temperature_monitor

# How to use it

1. Open the source code of the arduino and write the server url.
2. Launch the web server.
3. Deploy the raspberry script to an IoT device that can execute python.

**To run the server, use the following commands:**

To start the web server:
```
$ python manage.py runserver 0.0.0.0:8000
```

To start the worker that manages the logic of the notifications:
```
$ python manage.py runworker parse-temperature
```
