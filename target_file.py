import pytz
from datetime import datetime

timezones = ['Europe/Paris']
for tz in timezones:
    p = pytz.timezone(tz)
    now = datetime.now(p)
    print(now.strftime('%Y-%m-%d %H:%M:%S %Z%z'))