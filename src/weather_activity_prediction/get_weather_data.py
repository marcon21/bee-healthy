import csv
import codecs
import urllib.request
import urllib.error
import sys

# This is the core of our weather query URL
BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

ApiKey='YOUR_API_KEY' # can be generated from visual crossing website by making an account
#UnitGroup sets the units of the output - us or metric
UnitGroup='metric'

#Location for the weather data
Location=urllib.parse.quote('Ekkehardusstraße 2, 97717 Aura an der Saale, Germany')
Location_csv_name = "Aura_an_der_Saale"
#Optional start and end dates
#If nothing is specified, the forecast is retrieved. 
#If start date only is specified, a single historical or forecast day will be retrieved
#If both start and and end date are specified, a date range will be retrieved
# IMPORTANT: there is a daily 1000 token limit
StartDate = '2017-01-01'
EndDate='2017-01-31'

#JSON or CSV 
#JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
#CSV format requires an 'include' parameter below to indicate which table section is required
ContentType="csv"

#include sections
#values include days,hours,current,alerts
Include="hours" # Hourly is 24 tokens a day daily is one token a day

# Output file name
output_file = f"data/weather/{Location_csv_name}_{StartDate}_{EndDate}.csv"

print('')
print(' - Requesting weather : ')

# Url is completed. Now add query parameters (could be passed as GET or POST)
params = "?"

# append each parameter as necessary
if len(UnitGroup):
    params += "&unitGroup=" + UnitGroup

if len(ContentType):
    params += "&contentType=" + ContentType

if len(Include):
    params += "&include=" + Include

params += "&key=" + ApiKey

ApiQuery = f"{BaseURL}{Location}/{StartDate}/{EndDate}?{params}"
print(' - Running query URL: ', ApiQuery)
print()

try: 
    CSVBytes = urllib.request.urlopen(ApiQuery)
except urllib.error.HTTPError as e:
    ErrorInfo = e.read().decode() 
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()
except urllib.error.URLError as e:
    ErrorInfo = e.read().decode() 
    print('Error code: ', e.code,ErrorInfo)
    sys.exit()

# Parse the results as CSV
CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))

# Open a file for writing
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    RowIndex = 0

    for Row in CSVText:
        writer.writerow(Row) 
        RowIndex += 1

print()
print(f"Weather data saved to '{output_file}'.")
