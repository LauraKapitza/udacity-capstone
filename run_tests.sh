# /bin/bash
export TEST_RUNNING=1

dropdb dance_test
createdb -U postgres dance_test

flask db upgrade

python test_flaskr.py
python -m unittest discover tests