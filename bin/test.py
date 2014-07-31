#!/usr/bin/env python


import sys
import nose

sys.path.append('')

from meatbot.status import connect
connect()
nose.main()
