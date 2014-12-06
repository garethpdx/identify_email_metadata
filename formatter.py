"""

Normalize and format content to match parsing requirements.

"""

class ContentFormatter(object):
    """
    Convert content to match the basic formatter requirement: lowercase
    """
    @classmethod
    def format(cls, to_format):
        formatted_parseable = to_format
        try:
            formatted_parseable = to_format.lower()
        except AttributeError as e:
            cls.handle_unexpected_type(to_format, e)
        return formatted_parseable

    @classmethod
    def handle_unexpected_type(cls, to_format, exception):
        raise FormatTypeError('Expected to format a string-like object implementing a lower() method')

class FormatTypeError(TypeError):
    pass
