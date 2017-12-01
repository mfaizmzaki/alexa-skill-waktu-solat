# Changelog

All changes to this project will be documented in this file.

Date format: YYYY-MM-DD

## [0.1.0] - 2017-11-24
### Added
- First deployment of Prayer Time Alexa Skill.
- Added README.md as simple guide.
- Added lambda_function.py which is the main code file.
- Added intent.json which is list of intents used in the skill.

## [0.2.0] - 2017-11-27
### Added
- Renamed Subuh and Isyak to Dawn and Night respectively in lambda_function.py.
- Replaced Subuh and Isyak prayer names to Dawn and Night respectively in README.md
- Added new feature GetTimeRemaining which informs the time remaining until a specific prayer time.
- Added new utterances to support the new GetTimeRemaining feature.
- Added comma and new line to GetAllPrayerTimes card to slow down Alexa's speech.

## [0.3.0] - 2017-12-01
### Added
- Added new feature to get the time remaining to the nearest next prayer.
- Added new utterances to support the new feature.
- Added a code workaround to check if a slot is filled.
- Minor fix: Added 'Thank you' and 'Thanks' as utterances to allow the skill to stop running.

## [0.3.1] - 2017-12-02
### Fixed
- Fixed bug could not identify the next prayer because of now() method by replacing it with time() method.
