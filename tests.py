"""
Test the identification of email metadata. For the sake of sharing and browsing,  all of the project's code tests included in this file.
"""
import unittest
import urllib2
import time
import json
import datetime
import urllib


from pymail import Email
import phrase
import parse
import configuration
import interface


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

EMAIL_EXAMPLE = {'email':
                 {'subject': 'Automobile production information.',
                  'html':'Between Canada, Japan and Mexico, in 2015 the most cars are expected to be manufactured in Mexico.'
                  , 'from_line': '<John Doe> info@irrelevantinformation.com'
                  , 'finished_at': '2014-10-01 12:33 PM'
                  , 'country_parser':  parse.PopularityParser(possible_phrases=['Japan',
                                                                                'Mexico',
                                                                                'Canada'])},
                 'metadata': {'country': 'mexico', 'signer': 'john doe'}}

class TestPhraseListFileFactory(unittest.TestCase):
    def setUp(self):
        self.factory = phrase.PhraseListFileFactory
        self.expected_phrase_list = phrase.PhraseList(['canada',
                                                       'united states',
                                                       'new zealand'])

    def runTest(self):
        self.assertListEqual(self.factory.factory('./test_files/phrase_list.csv',
                                                  {'line_separator': '\n'}),
                             self.expected_phrase_list)


class TestPhraseListConfiguration(unittest.TestCase):
    def setUp(self):
        self.expected_configuration_parameters = {'line_separator': '\n'}
        self.configuration = configuration.PhraseListConfiguration(None,
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
            Email(**EMAIL_EXAMPLE['email'])
        except:
            self.encountered_error = True

    def runTest(self):
        self.assertFalse(self.encountered_error)

        
class TestAssignmentOfSubject(unittest.TestCase):
    def setUp(self):
        self.email = Email(**EMAIL_EXAMPLE['email'])

    def runTest(self):
        self.assertEqual(self.email.subject,
                         EMAIL_EXAMPLE['email']['subject'])


class TestAssignmentofCountry(unittest.TestCase):
    def setUp(self):
        self.email = Email(**EMAIL_EXAMPLE['email'])

    def runTest(self):
        self.assertEqual(self.email.country,
                         EMAIL_EXAMPLE['metadata']['country'])


class TestCountryParserSpecification(unittest.TestCase):
    pass


class TestSigner(unittest.TestCase):
    def setUp(self):
        self.email = Email(**EMAIL_EXAMPLE['email'])

    def runTest(self):
        self.assertEqual(self.email.signer,
                         EMAIL_EXAMPLE['metadata']['signer'])


class TestUIInitialization(unittest.TestCase):
    def setUp(self):
        interface_duration = 3
        self.encountered_error = False
        self.interface = interface.TemporaryWebInterface(interface_duration)
        try:
            self.interface.open_interface()
            sleep_until_interface_has_initialized(self.interface)
            self.interface.shutdown()
        except Exception:
            self.encountered_error = True

    def runTest(self):
        self.assertFalse(self.encountered_error)


def sleep_until_interface_has_initialized(interface):
    while not interface.server.initialized:
        time.sleep(.5)


def url_from_interface_and_path(interface, path):
    url = 'http://localhost:' + str(interface.server.port) + path
    return url


class TestWebInterface(unittest.TestCase):
    interface_duration = 15

    @classmethod
    def setUpClass(cls):
        cls.interface = interface.TemporaryWebInterface(cls.interface_duration)
        cls.interface.open_interface()
        sleep_until_interface_has_initialized(cls.interface)

    def test_non_cgi_page_retrieval(self):
        url = url_from_interface_and_path(self.interface, '/test_files/test.html')
        response = urllib2.urlopen(url, timeout=4)
        with open('./test_files/test.html') as f:
            self.file_content  = f.read()
        self.retrieved_content = response.read()
        self.assertEqual(self.retrieved_content.rstrip(), self.file_content.rstrip())

    def test_cgi_page_retrieval(self):
        url = url_from_interface_and_path(self.interface, '/__init__.py')
        response = urllib2.urlopen(url, timeout=4)
        self.response_code = response.getcode()
        self.assertEqual(self.response_code, 200)

    def test_access_to_parse_interface(self):
        encountered_error = False
        try:
            url = url_from_interface_and_path(self.interface, '/parse_it.py')
            urllib2.urlopen(url, timeout=4)
        except Exception:
            encountered_error = True
        self.assertFalse(encountered_error)

    def test_interface_parsing(self):
        encountered_error = False
        try:
            url = url_from_interface_and_path(self.interface, '/parse_it.py')
            email = {'subject': 'subject',
                     'html': 'the country of haiti',
                     'finished_at': str(datetime.date(2014,11,12)),
                     'from_line': '<ablert> albert@alb.com'}
            co = urllib.urlencode(email)
            r = urllib2.Request(url, co)
            u = urllib2.urlopen(r, timeout=4)
            content = u.read()
            j = json.loads(content)
        except Exception:
            encountered_error = True
        self.assertEqual(j['country'], 'haiti')
        self.assertFalse(encountered_error)

    @classmethod
    def tearDownClass(cls):
        cls.interface.shutdown()


class TestPersistance(unittest.TestCase):
    def test_persister_instantiation(self):
        from persister import SQLPersister, SQLLiteDriver
        encountered_error = False
        sqlite = SQLLiteDriver('')
        try:
            SQLPersister(sqlite, fields=['bob'])
        except:
            encountered_error = True
        self.assertFalse(encountered_error)

    def test_converter(self):
        from persister import SQLConverter
        email = Email(**EMAIL_EXAMPLE['email'])
        expected_phrase = ('subject', "'" + email.subject + "'")
        self.assertEqual(expected_phrase, SQLConverter.convert(email, ['subject']))

    def test_sqlite_driver_instantiation(self):
        from persister import SQLLiteDriver
        loc = r'C:\Users\gareth\Documents\code\repos\identify_email_metadata\identify_email_metadata\test_files\test.db'
        self.assertTrue(SQLLiteDriver(loc))

    def test_send_to_persister(self):
        email = Email(**EMAIL_EXAMPLE['email'])
        from persister import SQLPersister, awaiting_persistance, SQLDebugDriver
        loc = r'C:\Users\gareth\Documents\code\repos\identify_email_metadata\identify_email_metadata\test_files\test.db'
        driver = SQLDebugDriver(loc)
        db = SQLPersister(driver, fields=['subject', 'country', 'signer'])
        awaiting_persistance.append(email)
        db.record_results(awaiting_persistance)
        expected_sql = "INSERT INTO email_metadata (signer, country, subject) values ('{0.signer}', '{0.country}', '{0.subject}')".format(email)
        self.assertEqual(expected_sql, driver.captured_command)


if __name__ == '__main__':
    unittest.main()
