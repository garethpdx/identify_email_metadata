""" Tests to ensure the operation of the code ample, not to be included """
import unittest
from pymail import Email
import parse

email_stub = {'subject': 'Donate now!',
              'html':'are we talking about niger? or canada or somewhere else?. No, niger.'
              , 'from_line': '<John Doe> newsleltter@mercycorps.org'
              , 'finished_at': '2014-10-01 12:33 PM'
              , 'country_parser':  parse.PopularityParser}
stub_metadata = {'country': 'niger', 'signer': 'John Doe'}



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
        self.parser = parse.PopularityParser(self.parseable_string)

    def runTest(self):
        self.assertEqual(self.parser.parse(), self.expected_country)


class TestChronologyCountryParser(unittest.TestCase):
    def setUp(self):
        self.parseable_string = 'the countries of niger and england, but niger is newer'
        self.expected_country = 'niger'
        self.parser = parse.ChronologicalParser(self.parseable_string)

    def runTest(self):
        self.assertEqual(self.parser.parse(), self.expected_country)


if __name__ == '__main__':
    unittest.main()
