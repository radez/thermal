ther·mal
merriam-webster.com: of, relating to, or caused by heat

Thermal is a django web application intended to expose heat-api's cli
functionality via web user interface.

To get started you must have django installed
in the example_projects directory link in the thermal src code and 
the heat_mock directory:

ln -s ../src/thermal
ln -s ../heat_mock heat

then run the builtin development webserver with one of the following
commands:

./manage.py runserver # http://localhost:8000
./manage.py runserver 8001 http://localhost:8001
./manage.py runserver 0.0.0.0:8002 http://{machine's ip}:8002
