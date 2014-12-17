import get_reports
import parse_url
import pandas as pd
from datetime import date
import string
import time

total_start = time.time()
start = time.time()
dictfile = 'C:\Python_workspace\GoogleAdWords\dictionary.txt'

report = {
      'reportName': 'KEYWORDS_PERFORMANCE_REPORT',
      'dateRangeType': 'LAST_MONTH',
      'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
      'downloadFormat': 'CSV',
      'selector': {
          'fields': ['AccountDescriptiveName','CampaignName','Date','KeywordText','ExternalCustomerId','CampaignStatus','Status',
                     'AdGroupStatus','Clicks','Impressions','Cost','DayOfWeek', 'Slot', 'Ctr', 'AveragePosition', 'DestinationUrl']},
         }
#report = "SELECT AccountDescriptiveName, KeywordText, Clicks, Impressions, DestinationUrl FROM KEYWORDS_PERFORMANCE_REPORT DURING YESTERDAY"
print "Initializing"
downloader, ids, client = get_reports.initialize_api()

elapsed = (time.time() - start)/60
print "Run time: " + str(elapsed)
start = time.time()

print "Getting reports"
df = get_reports.get_report(report, client, ids, downloader)
dictionary = parse_url.init_dictionary(dictfile)

elapsed = (time.time() - start)/60
print "Run time: " + str(elapsed)
start = time.time()

print "Creating headers"
df, urlparams = parse_url.create_headers(df)

elapsed = (time.time() - start)/60
print "Run time: " + str(elapsed)
start = time.time()

print "Parsing URL"
df = parse_url.parse_url(df)

elapsed = (time.time() - start)/60
print "Run time: " + str(elapsed)
start = time.time()

print "Checking values"
df = parse_url.typo_correct(urlparams, df, dictionary)
today = "".join(l for l in str(date.today()) if l not in string.punctuation and l not in " ")
filename = report['reportType'] + today + '.csv'

df.to_csv(filename)
elapsed = (time.time() - start)/60
print "Run time: " + str(elapsed)

total_elapsed = (time.time() - total_start)/60

print "Total run time: " + str(total_elapsed)


