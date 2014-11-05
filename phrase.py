"""
PhraseLists merely extend the list built-in to provide a relevantly named class.
"""

from configuration import PhraseListConfigurationConnectionError

class PhraseList(list):
    pass


class PhraseListFileFactory(object):
    factory_subject = PhraseList

    @classmethod
    def factory(cls, connection_string, parameters):
        source_data = cls.retrieve_source_data(connection_string)
        lowercase_filecontents = source_data.lower()
        return cls.factory_subject(lowercase_filecontents.split(parameters['line_separator']))

    @staticmethod
    def retrieve_source_data(connection_string):
        try:
            with open(connection_string) as f:
                return f.read()
        except IOError:
            raise PhraseListConfigurationConnectionError('Error reading from PhraseList data source.')


