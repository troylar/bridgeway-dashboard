cd /home/troy/dev/bridgeway-dashboard
. ./venv/bin/activate
kill `pidof uwsgi`
uwsgi --processes 1 --threads 1 --socket 10.20.5.50:8050 --protocol=http -w wsgi &
