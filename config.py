

class PhraseListConfiguration(object):
    def __init__(self, method, connection_string, **kwargs):
        self.method = method
        self.connection_string = connection_string
        self.parameters = {}
        for kw in kwargs:
            self.parameters[kw] = kwargs[kw]


COUNTRYLIST_SOURCE = PhraseListConfiguration(method='file',
                                             connection_string='./mc_countries.csv',
                                             line_separator = '\n')
