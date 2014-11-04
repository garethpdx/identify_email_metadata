"""
Test the behavior of pyemail code. For the sake of sharing and browsing,  all of the project's code tests included in this file, instead of an additional package.
"""
import unittest

from pymail import Email
import phrase
import parse
import config


PHRASE_EXAMPLES = []
PHRASE_EXAMPLES.append({'text':'From 1995 to 2005, Africa\'s rate of economic growth increased, averaging 5% in 2005. Some countries experienced still higher growth rates, notably Equatorial Guinea, Angola, and Sudan, all three of which had recently begun extracting their petroleum reserves or had expanded their oil extraction capacity. Angola has vast mineral and petroleum reserves, and its economy has on average grown at a double-digit pace since the 1990s, especially since the end of the civil war.',
                     'phrase_list': ['angola',
                                     'equatorial guinea',
                                     'sudan'],
                     'most_popular_relevant_phrase': 'angola',
                     'first_phrase_mentioned': 'equatorial guinea'})
PHRASE_EXAMPLES.append({'text': """India, officially the Republic of India,[12][c] is a country in South Asia. It is the seventh-largest country by area, the second-most populous country with over 1.2 billion people, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the south-west, and the Bay of Bengal on the south-east, it shares land borders with Pakistan to the west; China, Nepal, and Bhutan to the north-east; and Burma and Bangladesh to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; in addition, India's Andaman and Nicobar Islands share a maritime border with Thailand and Indonesia.""",
                     'phrase_list': ['india',
                                     'bangladesh',
                                     'Nepal',
                                     'Bhutan',
                                     'Pakistan',
                                     'Thailand',
                                     'Indonesia'],
                     'most_popular_relevant_phrase': 'india', 
                     'first_phrase_mentioned': 'india'})

EMAIL_EXAMPLE = {'example_email':
              {'subject': 'Automobile production information.',
               'html':'Between Canada, Japan and Mexico, in 2015 the most cars are expected to be manufactured in Mexico.'
               , 'from_line': '<John Doe> info@irrelevantinformation.com'
               , 'finished_at': '2014-10-01 12:33 PM'
               , 'country_parser':  parse.PopularityParser(possible_phrases=['Japan',
                                                                             'Mexico',
                                                                             'Canada'])},
              'metadata': {'country': 'mexico', 'signer': 'John Doe'}}

class TestPhraseListFileFactory(unittest.TestCase):
    def setUp(self):
        self.factory = phrase.PhraseListFileFactory
        self.expected_phrase_list = phrase.PhraseList(['canada',
                                                       'united states',
                                                       'new zealand'])

    def runTest(self):
        self.assertListEqual(self.factory.factory('./test_files./phrase_list.csv',
                                                  {'line_separator': '\n'}),
                             self.expected_phrase_list)


class TestPhraseListConfiguration(unittest.TestCase):
    def setUp(self):
        self.expected_configuration_parameters = {'line_separator': '\n'}
        self.configuration = config.PhraseListConfiguration(None,
                                                            None,
                                                            line_separator='\n')
    def runTest(self):
        self.assertDictEqual(self.expected_configuration_parameters,
                             self.configuration.parameters)


class TestIdentificationOfPhrases(unittest.TestCase):
    def setUp(self):
        self.possible_phrases = phrase.PhraseList(['china',
                                                   'france',
                                                   'germany',
                                                   'ireland',
                                                   'england'])
        self.expected_phrases_to_find = ['england',
                                         'france']
        self.parser = parse.PhraseParser('The countries of England, Somalia, and Francis -- er, make that France.',
                                         self.possible_phrases)

    def runTest(self):
        self.assertListEqual(sorted(self.expected_phrases_to_find),
                             sorted(self.parser.phrases_in_parseable()))


class TestPopularityCounter(unittest.TestCase):
    def setUp(self):
        self.possible_phrases = phrase.PhraseList(['england'])
        self.parser = parse.PopularityParser('The countries of England, Somalia, and Francis -- er, I mean france.',
                                             self.possible_phrases)
        self.instances_of_phrase = self.parser.count_instances(self.possible_phrases[0])
        self.expected_instances_of_phrase = 1

    def runTest(self):
        self.assertEqual(self.expected_instances_of_phrase,
                         self.instances_of_phrase)

class TestParserAccuracy(unittest.TestCase):
    examples = []
    relevant_test_key = None

    def setUp(self):
        self.parse_results = []
        for text in self.examples:
            possible_phrases = phrase.PhraseList(text['phrase_list'])
            parser = parse.PopularityParser(text['text'],
                                            possible_phrases)
            self.parse_results.append((parser.parse(),
                                       text[self.relevant_test_key]))
    
    def runTest(self):
        for comparison in self.parse_results:
            self.assertEqual(comparison[0], comparison[1])
            
class TestPopularityParserAccuracy(TestParserAccuracy):
    relevant_test_key = 'most_popular_relevant_phrase'
    examples = PHRASE_EXAMPLES

class TestChronologyCountryParserAccuracy(unittest.TestCase):
    relevant_test_key = 'first_phrase_mentioned'
    examples = PHRASE_EXAMPLES

class TestEmailInstantiationUsingDefaults(unittest.TestCase):
    def setUp(self):
        self.encountered_error = False
        try:
            Email(**EMAIL_EXAMPLE['example_email'])
        except:
            self.encountered_error = True

    def runTest(self):
        self.assertFalse(self.encountered_error)
        
class TestAssignmentOfSubject(unittest.TestCase):
    def setUp(self):
        self.email = Email(**EMAIL_EXAMPLE['example_email'])

    def runTest(self):
        self.assertEqual(self.email.subject,
                         EMAIL_EXAMPLE['example_email']['subject'])


class TestSigner(unittest.TestCase):
    def setUp(self):
        self.email = Email(**EMAIL_EXAMPLE['example_email'])

    def runTest(self):
        self.assertEqual(self.email.signer,
                         EMAIL_EXAMPLE['metadata']['signer'])


if __name__ == '__main__':
    unittest.main()
