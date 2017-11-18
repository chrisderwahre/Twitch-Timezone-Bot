import pytwitcherapi, webbrowser, time
import queue
import threading
import json
from datetime import datetime, timedelta
import pytz
from pytz import timezone

session = pytwitcherapi.TwitchSession()
url = session.get_auth_url()

session.start_login_server()
webbrowser.open(url)

while not session.authorized:
    time.sleep(1)

time.sleep(2)

print("Authorized.")

session.shutdown_login_server()

channel = session.get_channel("Dein Channel Name")


client = pytwitcherapi.IRCClient(session, channel)

t = threading.Thread(target=client.process_forever)
t.start()

vIn = "In "
vIs = " ist es "
vOt = " am "

timeCode = '%H:%M'
dateCode = '%d.%m.%Y'

commandInfo = "!infozeit"
command = "!zeit"

error = "Fehler!"

# Beispiel: In World/World ist es Stunde:Minute am Tag.Monat.Jahr


print("Connected.")

while True:
    try:
        m = client.messages.get(False)

        if m.text.split(' ')[0] == "fdw":

            if m.text.split(' ')[1] == commandInfo:
                client.send_msg("!time <stadt> Alle zonen/städte: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

            if m.text.split(' ')[1] == command:
                try:
                    timeV = timezone(m.text.split(' ',3)[2])
                    timeV_time = datetime.now(timeV)
                    client.send_msg(vIn + m.text.split(' ',3)[2] + vIs + timeV_time.strftime('%H:%M') + vOt + timeV_time.strftime('%d.%m.%Y'))
                except:
                    client.send_msg(error)
                    
            
    except queue.Empty:
        time.sleep(1)
            
