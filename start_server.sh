#! /bin/bash
clear

if [ "${1}"x == "ssl"x ]; then
	type="ssl"
	param="0.0.0.0:8000"
	sudo python manage.py "run${type}server" $param
fi

python manage.py "runserver"