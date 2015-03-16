import cgi

from pymail import Email
from config import SQLITE_DB, RECORD_API_RESULTS
from interface import ParseInterfaceResponse, SuccessfulParseResponse, FailedParseResponse
from persister import SQLLiteDriver, SQLPersister, awaiting_persistance

header = "Content-type:application/json\r\n\r\n"
print header

input_data = cgi.FieldStorage()


def log_successful_parse(email):
    db_driver = SQLLiteDriver(SQLITE_DB)
    persister = SQLPersister(db_driver, ['subject', 'country', 'signer'])
    awaiting_persistance.append(email)
    persister.record_results(awaiting_persistance)

if input_data:
    try:
        e = Email(input_data['subject'].value,
                  input_data['html'].value,
                  input_data['finished_at'].value,
                  input_data['from_line'].value)
        response = SuccessfulParseResponse(e)
        if RECORD_API_RESULTS:
            log_successful_parse(e)
    except Exception as e:
        response = FailedParseResponse()
        response.render_response()
        raise e
else:
    response = ParseInterfaceResponse()

response.render_response()
