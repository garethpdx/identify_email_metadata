import sqlite3


class Persister(object):
    def record_results(self, record_queue):
        for record in record_queue:
            self.persist(record)


class SQLConverter(object):

    @classmethod
    def convert(cls, record, fields):
        to_insert = {}
        for field in fields:
            raw_data = cls.sanitize_input(getattr(record, field))
            to_insert[field] = raw_data
        columns = ', '.join(to_insert.keys())
        values = "'" + "', '".join(to_insert.values()) + "'"
        return columns, values

    @classmethod
    def sanitize_input(cls, inp):
        if not inp:
            return ''
        return inp.replace("'", "''")


class SQLPersister(Persister):
    def __init__(self, driver, fields):
        self.driver = driver
        self.fields = fields

    def persist(self, record):
        cols, vals = SQLConverter.convert(record, self.fields)
        command = ("INSERT INTO email_metadat" +
                   "a ({0}) values ({1})").format(cols, vals)
        self.driver.execute_command(command)


class SQLDriver(object):
    def __init__(self, file_location):
        self.file_location = file_location

    def execute_command(self, command):
        pass


class SQLLiteDriver(SQLDriver):

    def execute_command(self, command):
        conn = sqlite3.connect(self.file_location)
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()


class SQLDebugDriver(SQLDriver):
    def __init__(self, *args, **kwargs):
        self.captured_command = None
        super(SQLDebugDriver, self).__init__(*args, **kwargs)

    def capture_command(self, command):
        self.captured_command = command

    def execute_command(self, command):
        self.capture_command(command)
        super(SQLDebugDriver, self).execute_command(command)


awaiting_persistance = []
