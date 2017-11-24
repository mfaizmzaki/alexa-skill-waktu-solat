# alexa-skill-waktu-solat
Amazon's Alexa Skill for Amazon Echo/Echo Dot. This skill allows Alexa to return prayer times (waktu solat) based on voice prompt by user. At the moment, this skill is written to return a preset/local prayer times. The prayer times are queried through API written by @zaimramlan, https://github.com/zaimramlan/waktu-solat-api

# Tech stack
- AWS Lambda
- Python 2.7

# Utterences
GetAllPrayerTimes prayer times
GetAllPrayerTimes what are the prayer times
GetAllPrayerTimes prayers
GetPrayerTime what time is {Prayer}
GetPrayerTime {Prayer} at what time
GetPrayerTime {Prayer}
GetPrayerTime When is {Prayer}

# Prayer Times
- Imsak
- Subuh
- Syuruk
- Zohor
- Asar
- Maghrib
- Isyak

# Still needed
- Time until next prayer 
- Prayer times for all location based on voice prompt
- Push notification when it's time for prayer

