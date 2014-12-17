import json
import cgi
import datetime

from pymail import Email

header = "Content-type:application/json\r\n\r\n"
print header

input_data = cgi.FieldStorage()
if input_data:
    e = Email(input_data['subject'].value,
              input_data['html'].value,
              input_data['finished_at'].value,
              input_data['from_line'].value)
    response = {'country': e.country, 'signer': e.signer}
    print json.dumps(response)
else:
    print ""
