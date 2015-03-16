"""
Parse string-like objects for the identification of relevant information.

For phrases of relevant words, use either a popularity or a chronological
method. For from-line's, extract the first bracketed set of characters.

"""

import re

from formatter import ContentFormatter

class Parser(object):
    formatter = ContentFormatter

    def __init__(self, parseable=None):
        self.parseable = self.format(parseable)

    def parse(self):
        raise NotImplemented('Method "parse" must be implemented by subclass.')

    @classmethod
    def format(cls, to_format):
        if to_format:
            return cls.formatter.format(to_format)


class PhraseParser(Parser):
    def __init__(self, parseable=None, possible_phrases=None):
        super(PhraseParser, self).__init__(parseable)
        self.possible_phrases = [self.format(phrase) for phrase in possible_phrases]
        self.leader = self.Tracker()

    def phrases_in_parseable(self):
        phrases_present = []
        for phrase in self.possible_phrases:
            if phrase in self.parseable:
                phrases_present.append(phrase)
        return phrases_present

    def parse(self):
        for phrase in self.phrases_in_parseable():
            parse_result  = self.parse_parseable(phrase)
            if self.is_new_leader(parse_result):
                self.update_leader(phrase, parse_result)
                self.optimize_parseable()
        return self.leader.name

    @staticmethod
    def format(text):
        formatted_text = None
        try:
            formatted_text = text.lower()
        except AttributeError:
            pass
        return formatted_text

    def optimize_parseable(self):
        pass

    def update_leader(self, name, value):
        self.leader.name = name
        self.leader.value = value

    class Tracker(object):
        def __init__(self, name=None, value=None):
            self.update(name, value)

        def update(self, name, value):
            self.name = name
            self.value = value


class ChronologicalParser(PhraseParser):

    def parse_parseable(self, phrase):
        return self.parseable.find(phrase)

    def is_new_leader(self, index):
        if self.found_needle(index):
            return True
        
    def optimize_parseable(self):
        # Discards excess string
        self.parseable = self.parseable[:self.leader.value]

    @staticmethod
    def found_needle(index):
        # string.find returns -1 when it doesn't find the needle in the haystack
        return index >= 0

class PopularityParser(PhraseParser):

    def parse_parseable(self, phrase):
        return self.count_instances(phrase)

    def is_new_leader(self, value):
        return value > self.leader.value

    def count_instances(self, phrase):
        return len(re.findall(phrase, self.parseable, flags=re.IGNORECASE))

    @staticmethod
    def raise_error_if_empty(phrase_instances):
        if len(phrase_instances) == 0:
            raise ParserValueError('HTML contained no relevant countries.')


class SignerParser(Parser):

    def parse(self):
        pattern_matching_first_bracketed_characters = '<.*?>'
        first_bracketed_pattern = re.search(pattern_matching_first_bracketed_characters, self.parseable)
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
