"""
Edit this script to configure new phrase data sources.

"""

from configuration import PhraseListConfiguration

COUNTRYLIST_SOURCE = PhraseListConfiguration(method='file',
                                             connection_string='./phraselist.csv',
                                             line_separator = '\n')

RECORD_API_RESULTS = False
SQLITE_DB = r'C:\Users\\gareth\Documents\code\\repos\\identify_email_metadata\\identify_email_metadata\test.db'
