Pymail
-----

Parse emails to determine who symbolically sent the message and what country is the focus of the email.

Two country parsers are included, enabling the email's country to be determined
based on the frequency of references or by the order of appearance.

Example (Using default: Determine country by frequency)

>>> from __future__ import print_function

>>> import pymail
>>> import examples

>>> for unparsed_email in examples.emails:
>>>     email = pymail.Email(**unparsed_email)
>>>     print('The email was signed by {0.signer} and {0.country} is the most-referenced country.'.format(email))

Example (Determine country by order of appearance instead of frequency):

>>> from __future__ import print_function

>>> import pymail
>>> import parse
>>> import examples

>>> for unparsed_email in examples.emails:
>>> 	unparsed_email['country_parser'] = parse.ChronologicalParser()
>>>     email = pymail.Email(**unparsed_email)
>>>     print('The email was signed by {0.signer}. {0.country} is the first referenced country.'.format(email))
