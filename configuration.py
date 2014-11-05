"""
Configurations for phrase parsing data sources.
"""

class PhraseListConfiguration(object):
    def __init__(self, method, connection_string, **kwargs):
        self.method = method
        self.connection_string = connection_string
        self.parameters = {}
        for kw in kwargs:
            self.parameters[kw] = kwargs[kw]


class PhraseListConfigurationConnectionError(IOError):
    pass
