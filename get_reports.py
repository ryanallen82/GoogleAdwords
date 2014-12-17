
"""
A script that connects to the Google AdWords API and pulls reports based on report definition
(see:
    * https://developers.google.com/adwords/api/docs/appendix/reports
    * https://github.com/googleads/googleads-python-lib/blob/master/examples/adwords/v201409/reporting/download_criteria_report.py )
"""
from googleads import adwords
import pandas as pd
import fileinput
import os


def initialize_api():
    """This function initializes the connection to the AdWords API and returns the client object,
     a report downloader object, and a list of customer IDs

    :rtype : object
    :param None.:
    :returns:  report_downloader, list of customer IDs, client object
    """
    client = adwords.AdWordsClient.LoadFromStorage('C:\Python_workspace\GoogleAdWords\googleads.yaml')

    mcs = client.GetService('ManagedCustomerService' , version='v201409')
    selector = {'fields':['CustomerId']}

    accounts = mcs.get(selector)
    report_downloader = client.GetReportDownloader(version='v201409')

    ids = []
    for account in accounts['entries']:
        ids.append(account['customerId'])

    return report_downloader, ids, client


def get_report(report, client, ids, report_downloader):
    """This function takes a report definitions, a client object, the customer IDs, and a report downloader object.
    It pulls a report based on the report definition, iterates through all of the client ids to pull individual reports,
    and puts those reports into a temporary csv file. It then removes any duplicate lines, and puts the csv file into
     a pandas dataframe. Any non-alphanumeric characters are removed from the keywords column, and the dataframe is returned.

    :param report: A an xml dictionary with the report definition
    :type report: dict.
    :param client: A Google API client object
    :type client: Google API client object.
    :param ids: A list of client ids.
    :type ids: List.
    :param report_downloader: A Google report download object
    :type report_downloader: Object.

    :returns:  Pandas DataFrame
    """
    if os.path.isfile('test_dump.csv'):
        os.remove('test_dump.csv')
    file = open('test_dump.csv', 'a')
    for i in ids:
        client.SetClientCustomerId(i)
        try:
            report_downloader.DownloadReport(report, file, skip_report_header=True, skip_report_summary=True)
            #report_downloader.DownloadReportWithAwql(report, 'CSV', file, skip_report_header=True, skip_report_summary=True)
        except Exception, e:
            print str(e)
            pass

    file.close()

    seen = set()
    for line in fileinput.FileInput('test_dump.csv', inplace=1):
        if line in seen: continue

        seen.add(line)
        print line,

    df = pd.read_csv('test_dump.csv')
    if 'Keyword' in df.columns:
        df['Keyword'] = df['Keyword'].map(lambda x: str(x).replace('+',''))
    if 'Cost' in df.columns:
        df['Cost'] = df['Cost'].map(lambda x: fix_cost(x))
    return df

def fix_cost(cost):
    cost/=1000000.
    return cost

