import parse

class Email(object):

    def __init__(self, subject, html, finished_at, from_line, country_parser=parse.PopularityParser(), signer_parser=parse.SignerParser()):
        self.subject = subject
        self.html = html
        self.finished_at = finished_at
        self.from_line = from_line
        self.country_parser = country_parser
        self.signer_parser = signer_parser

    @property
    def signer(self):
        return self.signer_parser.parse(self.from_line)

    @property
    def country(self):
        return self.country_parser.parse(self.html)
        


