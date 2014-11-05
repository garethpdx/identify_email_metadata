from configuration import PhraseListConfiguration

COUNTRYLIST_SOURCE = PhraseListConfiguration(method='file',
                                             connection_string='./mc_countries.csv',
                                             line_separator = '\n')
