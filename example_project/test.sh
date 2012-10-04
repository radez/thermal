#!/bin/sh
coverage -e
coverage -x manage.py test
coverage -r -m --html ../src/thermal/*.py ../src/thermal/db/*.py ../src/thermal/templatetags/*.py ../src/thermal/tests/*.py
