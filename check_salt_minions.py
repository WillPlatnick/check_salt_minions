#!/usr/bin/env python
'''
Project     :       Icinga/Nagios salt-minion down check
Version     :       0.1
Author      :       Will Platnick <wplatnick@gmail.com>
Summary     :       This program is an icinga/nagios plugin that is run from the salt-master to return a list of down minions
Dependency  :       Python 2.6, Linux, Icinga/Nagios

Usage :
```````
shell> python check_salt_minions.py
'''

import os
import sys
import subprocess
from optparse import OptionParser
import yaml
import re


# Command Line Parsing Arguements
cmd_parser = OptionParser(version = "0.1")
cmd_parser.add_option("-e", "--exclude", type="string", action = "store", dest = "exclude", help = "Exclude regex", metavar = "Exclude")
(cmd_options, cmd_args) = cmd_parser.parse_args()

command = [ 'salt-run', 'manage.status' ]
down_servers = ""

try:
  child = subprocess.Popen(command, stdout=subprocess.PIPE)
  output = child.communicate()[0]
except OSError, e:
  print "UNKNOWN: salt doesn't appear to be installed"
  exit(3)

yaml_out = yaml.load(output)

try:
  if not yaml_out['down'] and not yaml_out['up']:
    print "UNKNOWN: Server has no minions attached to it"
    exit(3)
except:
  print "UNKNOWN: Invalid JSON detected"
  exit(3)

try:
  for server in yaml_out['down']:
    if cmd_options.exclude:
      match = re.match(cmd_options.exclude, server)
      if match is None:
        down_servers += server + " "
    else:
      down_servers += server + " "
except:
  print "OK"
  exit(3)

if down_servers:
  print "CRITICAL: " + down_servers
  exit(2)
else:
  print "OK"
  exit(0)

