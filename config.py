"""
Edit this script to configure new phrase data sources.

"""

from configuration import PhraseListConfiguration

COUNTRYLIST_SOURCE = PhraseListConfiguration(method='file',
                                             connection_string='./phraselist.csv',
                                             line_separator = '\n')
