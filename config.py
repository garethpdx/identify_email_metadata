"""
Edit this script to configure new phrase data sources and persistence options.

"""

from configuration import PhraseListConfiguration

COUNTRYLIST_SOURCE = PhraseListConfiguration(method='file',
                                             connection_string='./phraselist.csv',
                                             line_separator = '\n')

RECORD_API_RESULTS = False
SQLITE_DB = ''
