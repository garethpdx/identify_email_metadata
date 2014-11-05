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
>>>     unparsed_email['country_parser'] = parse.ChronologicalParser(possible_phrases=pymail.DEFAULT_PHRASE_LIST)
>>>     email = pymail.Email(**unparsed_email)
>>>     print('The email was signed by {0.signer}. {0.country} is the first referenced country.'.format(email))

The modules are organized flatly and without a setup script to enable inspection and execution with minimal configuration or installation.
No 3rd party libraries are required to run the demo. With Python 2.7 installed, the demo should run with either of the following commands, depending
on whether the Python executable is available via path 1) or not 2). 1) python demo.py, 2) demo.py.
