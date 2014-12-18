Identify Email Metadata
=====

Parse emails to determine who symbolically sent the message and what country is the focus of the email using either a Python API or an HTTP API.

Two country parsers are included, enabling the email's country to be determined based on the frequency of references or by the order of appearance.

HTTP
----

To initiate the HTTP interface, execute interface.py. It will initate a CGIHTTPServer that listens on a port between 8000 and 8099. To use the web-interface, navigate to /static/html/parse_form.html using your browser. If the webserver runs on port 8080, open http://localhost:8080/static/html/parse_form.html.

Python
----


Example (Using default: Determine country by frequency):

    from __future__ import print_function

    import pymail
    import examples

    for unparsed_email in examples.emails:
        email = pymail.Email(**unparsed_email)
        print('The email was signed by {0.signer} and {0.country} is the most-referenced country.'.format(email))

Example (Determine country by order of appearance instead of frequency):

    from __future__ import print_function

    import pymail
    import parse
    import examples

    for unparsed_email in examples.emails:
        unparsed_email['country_parser'] = parse.ChronologicalParser(possible_phrases=pymail.DEFAULT_PHRASE_LIST)
        email = pymail.Email(**unparsed_email)
        print('The email was signed by {0.signer}. {0.country} is the first referenced country.'.format(email))

The modules are organized flatly and without setup.py to enable inspection and execution with minimal configuration or installation.
No 3rd party libraries are required to run the demo. With Python 2.7 installed, the demo should run with either of the following commands, "python demo.py" or "demo.py", depending
on whether the Python executable is available via path or not, respectively.
