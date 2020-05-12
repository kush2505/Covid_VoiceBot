# COVID-19_VoiceAssistant
## This is a basic scraper based voice assistant tool to check out the Aggregate/Daily/Countrywise stats for COVID-19.

*This project is made using Regex, pyaudio and pyttsx3 (Python Text 2 Speech) libraries in python./*

*The stats that are displayed by the project are not static and can change whenever we speak 'update'*

The script reads the data file through an API retrieved using Parsehub.
https://www.parsehub.com/quickstart

It can also be done using a suitable JSON file but that would defy the basic purpose of the dynamic problem at hand.

The website from which the data was scraped is https://www.worldometers.info/coronavirus/

**The tool can be used to output the data in 3 forms:**
- Total Global Coronavirus Cases/Deaths Just by saying say....'Total number of cases/deaths'
- *Daily Coronavirus Cases/Deaths for a Country* You can go like ' Cases today in Palestine' oops xD
- *Total Coronavirus Cases/Deaths for a Country* You can say ' Number of deaths in Iraq' 

The END_PHRASE constant can be made to change as per requirement to exit out of the loop.
