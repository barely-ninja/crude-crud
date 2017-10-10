from urllib.parse import parse_qs
from os.path import exists
from sqlite3 import connect
from routes import resolve

_DB = "db/comment.db"
_INIT = "db/init.sql"

def db_conn(db_name):
    conn = connect(db_name)
    conn.text_factory = str
    return conn

class CommentServer:
    """WSGI server for comment app"""
    def __init__(self, environ, start_response):
        path_elements = environ['PATH_INFO'].split('/')
        self.route = resolve(environ['REQUEST_METHOD'], path_elements)()
        self.params = parse_qs(environ['QUERY_STRING'])
        self.params['resource_id'] = path_elements[-1]
        self.start = start_response

        if exists(_DB):
            self.conn = db_conn(_DB)
        else:
            self.conn = db_conn(_DB)
            cursor = self.conn.cursor()
            with open(_INIT) as init_file:
                cursor.executescript(init_file.read())


    def __iter__(self):
        status, headers, content = self.route.model(self.conn, self.params).render()
        self.start(status, headers)
        yield content

