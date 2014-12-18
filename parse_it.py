import cgi

from pymail import Email
from interface import ParseInterfaceResponse, SuccessfulParseResponse, FailedParseResponse

header = "Content-type:application/json\r\n\r\n"
print header

input_data = cgi.FieldStorage()

if input_data:
    try:
        e = Email(input_data['subject'].value,
                  input_data['html'].value,
                  input_data['finished_at'].value,
                  input_data['from_line'].value)
        response = SuccessfulParseResponse(e)
    except Exception as e:
        response = FailedParseResponse()
        response.render_response()
        raise e
else:
    response = ParseInterfaceResponse()

response.render_response()
