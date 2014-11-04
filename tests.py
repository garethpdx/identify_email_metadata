""" Tests to ensure the operation of the code ample, not to be included """
import unittest
from pymail import Email
import phrase
import parse
import config

COUNTRIES = phrase.PhraseListFileFactory.factory(connection_string=config.COUNTRYLIST_SOURCE.connection_string, parameters=config.COUNTRYLIST_SOURCE.parameters)

email_stub = {'subject': 'Donate now!',
              'html':'are we talking about niger? or canada or somewhere else?. No, niger.'
              , 'from_line': '<John Doe> newsleltter@mercycorps.org'
              , 'finished_at': '2014-10-01 12:33 PM'
              , 'country_parser':  parse.PopularityParser(possible_phrases=COUNTRIES)}
stub_metadata = {'country': 'niger', 'signer': 'John Doe'}


class TestPhraseListFileFactory(unittest.TestCase):
    def setUp(self):
        self.factory = phrase.PhraseListFileFactory
        self.expected_phrase_list = phrase.PhraseList(['canada', 'united states', 'new zealand'])

    def runTest(self):
        self.assertListEqual(self.factory.factory('./test_files./phrase_list.csv',{'line_separator': '\n'}), self.expected_phrase_list)


class TestPhraseListConfiguration(unittest.TestCase):
    def setUp(self):
        self.expected_configuration_parameters = {'line_separator': '\n'}
        self.configuration = config.PhraseListConfiguration(None, None, line_separator='\n')
    def runTest(self):
        self.assertDictEqual(self.expected_configuration_parameters, self.configuration.parameters)


class TestIdentificationOfPhrases(unittest.TestCase):
    def setUp(self):
        self.possible_phrases = phrase.PhraseList(['china', 'france', 'germany', 'ireland', 'england', 'mali'])
        self.expected_phrases_to_find = ['england', 'france']
        self.parser = parse.PhraseParser('The countries of England, Somalia, and Francis -- er, I mean france.', self.possible_phrases)

    @unittest.expectedFailure
    def runTest(self):
        self.assertListEqual(sorted(self.expected_phrases_to_find),
                             sorted(self.parser.phrases_in_parseable()))


class TestPopularityCounter(unittest.TestCase):
    def setUp(self):
        self.possible_phrases = phrase.PhraseList(['england'])
        self.parser = parse.PopularityParser('The countries of England, Somalia, and Francis -- er, I mean france.', self.possible_phrases)
        self.instances_of_phrase = self.parser.count_instances(self.possible_phrases[0])
        self.expected_instances_of_phrase = 1

    def runTest(self):
        self.assertEqual(self.expected_instances_of_phrase, self.instances_of_phrase)


class TestEmailInstantiationUsingDefaults(unittest.TestCase):
    def setUp(self):
        self.encountered_error = False
        try:
            Email(**email_stub)
        except:
            self.encountered_error = True

    def runTest(self):
        self.assertFalse(self.encountered_error)
        
class TestSubject(unittest.TestCase):
    def setUp(self):
        self.email = Email(**email_stub)

    def runTest(self):
        self.assertEqual(self.email.subject, email_stub['subject'])


class TestCountry(unittest.TestCase):
    def setUp(self):
        self.email = Email(**email_stub)

    def runTest(self):
        self.assertEqual(self.email.country, stub_metadata['country'])


class TestSigner(unittest.TestCase):
    def setUp(self):
        self.email = Email(**email_stub)

    def runTest(self):
        self.assertEqual(self.email.signer, stub_metadata['signer'])


class TestPopularityCountryParser(unittest.TestCase):
    def setUp(self):
        self.parseable_string = 'the countries of niger and england, but niger is newer'
        self.expected_country = 'niger'
        self.parser = parse.PopularityParser(parseable=self.parseable_string, possible_phrases=COUNTRIES)

    def runTest(self):
        self.assertEqual(self.parser.parse(), self.expected_country)


class TestChronologyCountryParser(unittest.TestCase):
    def setUp(self):
        self.parseable_string = 'the countries of niger and england, but niger is newer'
        self.expected_country = 'niger'
        self.parser = parse.ChronologicalParser(parseable=self.parseable_string, possible_phrases=COUNTRIES)

    def runTest(self):
        self.assertEqual(self.parser.parse(), self.expected_country)


if __name__ == '__main__':
    unittest.main()
