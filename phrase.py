from config import COUNTRYLIST_SOURCE

class PhraseList(list):
    pass


class PhraseListFileFactory(object):
    relevant_class = PhraseList
    
    @classmethod
    def factory(cls, connection_string):
        source_data = cls.retrieve_source_data(connection_string)
        lowercase_filecontents = source_data.lower()
        return cls.relevant_class(lowercase_filecontents.split(COUNTRYLIST_SOURCE['parameters']['line_separator']))

    @staticmethod
    def retrieve_source_data(connection_string):
        with open(connection_string) as f:
            return f.read()

