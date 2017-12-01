# alexa-skill-waktu-solat
Amazon's Alexa Skill for Amazon Echo/Echo Dot. This skill allows Alexa to return prayer times (waktu solat) based on voice prompt by user. At the moment, this skill is written to return a preset/local prayer times. The prayer times are queried through API written by @zaimramlan, https://github.com/zaimramlan/waktu-solat-api

# Tech stack
- AWS Lambda
- Python 2.7

# Utterances
- AMAZON.StopIntent Thank you
- AMAZON.StopIntent Thanks
- GetAllPrayerTimes prayer times
- GetAllPrayerTimes what are the prayer times
- GetPrayerTime what time is {Prayer}
- GetPrayerTime {Prayer} at what time
- GetPrayerTime {Prayer}
- GetPrayerTime When is {Prayer}
- GetTimeRemaining Time until {PrayerTime}
- GetTimeRemaining How long until {PrayerTime}
- GetTimeRemaining How long until next prayer
- GetTimeRemaining Next prayer

# Prayer Times
- Imsak
- Dawn (Subuh)
- Syuruk
- Zohor
- Asar
- Maghrib
- Night (Isyak)

# Still needed
- More variety of sample utterances
- Prayer times for all location based on voice prompt
- Push notification when it's time for prayer
