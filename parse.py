import collections
import re

from config import COUNTRYLIST_LOCATION, LINE_SEPARATOR

class Parser(object):
    def parse(self, parseable):
        raise NotImplemented('Method "parse" must be implemented by subclass.')

def _retrieve_possible_phrases():
    with open(COUNTRYLIST_LOCATION) as f:
        file_content = f.read()
        lower_file_content = file_content.lower()
        return lower_file_content.split(LINE_SEPARATOR)


class PhraseParser(Parser):
    def __init__(self, possible_phrases = _retrieve_possible_phrases()):
        self.possible_phrases = possible_phrases

    def phrases_in_html(self, html):
        phrases_present = []
        formatted_html = self.format_html(html)
        for phrase in self.possible_phrases:
            if phrase in formatted_html:
                phrases_present.append(phrase)
        return phrases_present
    
    @staticmethod
    def format_html(html):
        return html.lower()
       

class ChronologicalParser(PhraseParser):

    def parse(self, html):
        leader = self.Tracker()
        for phrase in self.phrases_in_html(html):
            index = html.find(phrase)
            if self.found_needle(index):
                leader.update(phrase, index)
                # We're only interested in phrases that come before, not after
                html = html[:index]
        return leader.name
    
    class Tracker(object):
        def __init__(self, name=None, value=None):
            self.update(name, value)

        def update(self, name, value):
            self.name = name
            self.value = value

    @staticmethod
    def found_needle(index):
        # string.find returns -1 when it doesn't find the needle in the haystack
        return index >= 0


class PopularityCounter(collections.Counter):
    @property
    def most_common_key(self):
        # Counter.most_common(int) -> List of tuplues (key, count) sorted in descending order by count
        most_common = self.most_common(1)
        leader = most_common.pop()
        return leader[0]


class PopularityParser(PhraseParser):
    def parse(self, html):
        phrase_instances = {}
        for phrase in self.phrases_in_html(html):
            phrase_instances[phrase] = self.count_instances(html, phrase)
        self.raise_error_if_empty(phrase_instances)
        most_common = max(phrase_instances, key=lambda x: phrase_instances[x]) # PopularityCounter(phrase_instances)
        return most_common

    @staticmethod
    def count_instances(html, phrase):
        return len(re.findall(phrase, html, flags=re.IGNORECASE))

    @staticmethod
    def raise_error_if_empty(phrase_instances):
        if len(phrase_instances) == 0:
            raise ParserValueError('HTML contained no relevant countries.')


class SignerParser(Parser):

    def parse(self, parseable):
        pattern_matching_first_bracketed_characters = '<.*?>'
        first_bracketed_pattern = re.search(pattern_matching_first_bracketed_characters, parseable)
        try:
            signer_with_surrounding_brackets = first_bracketed_pattern.group()
        except AttributeError:
            raise ParserValueError('Signer expected in format <name> but none found.')
        return self.strip_first_and_last_character(signer_with_surrounding_brackets)
        
    @classmethod
    def strip_first_and_last_character(cls, bracketed_signer):
        return bracketed_signer[1:-1]

class ParserValueError(ValueError):
    pass
