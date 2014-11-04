from parse import PopularityParser
from parse import SignerParser
import phrase

from config import COUNTRYLIST_SOURCE
DEFAULT_PHRASE_LIST = phrase.PhraseListFileFactory.factory(connection_string=COUNTRYLIST_SOURCE.connection_string,
                                                           parameters=COUNTRYLIST_SOURCE.parameters)
DEFAULT_COUNTRY_PARSER = PopularityParser(possible_phrases=DEFAULT_PHRASE_LIST)
DEFAULT_SIGNER_PARSER = SignerParser()

class Email(object):

    def __init__(self, subject, html, finished_at, from_line, country_parser=DEFAULT_COUNTRY_PARSER, signer_parser=DEFAULT_SIGNER_PARSER):
        self.subject = subject
        self.html = html
        self.finished_at = finished_at
        self.from_line = from_line
        self.country_parser = country_parser
        self.country_parser.parseable = self.html
        self.signer_parser = signer_parser
        self.signer_parser.parseable = self.from_line

    @property
    def signer(self):
        return self.signer_parser.parse()

    @property
    def country(self):
        return self.country_parser.parse()
