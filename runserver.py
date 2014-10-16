#!/usr/local/bin/python2.7

import sys

from datetime import date
from main import app
from upload_s3 import set_metadata
from flask_frozen import Freezer

# cron is called with 3 arguments, should only run in the first week of month
cron_condition = len(sys.argv) == 3 and date.today().day < 8
force_update = len(sys.argv) == 2 and sys.argv[1] == 'freeze'

if len(sys.argv) > 1:  # if runserver is passed an argument
    if cron_condition or force_update:
        freezer = Freezer(app)
        freezer.freeze()
        set_metadata()
else:
    app.run()
