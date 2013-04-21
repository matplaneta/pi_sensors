A quick installation guide of Raspberry Pi sensors system

1. Download files into /home/pi/sensors folder
2. Define your sensors in sensors.cfg
3. Create sqlite tables in sensors.db file using sample script tools/create_sensor_db.sql
4. Instal RTC if needed with script tools/rtc/install_i2c-hwclock.sh
5. add to the cron sensors monitor:
crontab -e
*/10 * * * * sudo python /home/pi/sensors/scan.py
6. add auto-start scripts to the /etc/rc.local
python /home/pi/sensors/webserver.py &
python /home/pi/sensors/welcome.py
7. reboot Pi
