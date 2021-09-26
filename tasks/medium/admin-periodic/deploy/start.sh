#!/bin/sh

/usr/sbin/cron
exec /usr/sbin/sshd -D
