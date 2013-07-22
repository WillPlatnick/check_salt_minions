check_salt_minions
==================

Icinga/Nagios plugin for checking down salt minions.

It is meant to be run from the salt-master and uses 'salt-run manage.status' to grab what servers are down.

This needs to be re-written at some point, but it works, so I'm probably not going to get around to it soon.  What I didn't realize about using salt-run is that non-privileged users don't run it so well, so I added a line like below to our sudoers, to allow nrpe to sudo this command.


```
nagios   ALL=NOPASSWD: /usr/lib/nagios/plugins/contrib/check_salt_minions.py
```

