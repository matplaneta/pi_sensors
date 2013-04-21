#!/bin/bash

sed -i 's/^blacklist i2c-bcm2708/# &/' /etc/modprobe.d/raspi-blacklist.conf

cp sbin/i2c-hwclock /sbin
chmod +x /sbin/i2c-hwclock
cp etc/init.d/i2c-hwclock /etc/init.d
chmod +x /etc/init.d/i2c-hwclock

update-rc.d fake-hwclock remove
update-rc.d i2c-hwclock defaults
