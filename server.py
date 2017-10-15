from re import sub
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

def get_file(fn):
    try:
        with open(fn) as somefile:
            return somefile.read()
    except FileNotFoundError:
        return ''

class CommentServer:
    """WSGI server for comment app"""
    def __init__(self, environ, start_response):
        path_elements = environ['PATH_INFO'].split('/')
        #Find controller based on request method and path
        controller_class, asset_path, asset_files = resolve(environ['REQUEST_METHOD'], path_elements)
        self.controller = controller_class()
        #Collect useful params
        self.params = {}
        if environ['REQUEST_METHOD'] == 'GET':
            self.params['body'] = parse_qs(environ['QUERY_STRING'], encoding='utf-8')
        else:
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size).decode()
            self.params['body'] = parse_qs(request_body, encoding='utf-8')
        self.params['resource_id'] = path_elements[-1]
        #Init DB
        if exists(_DB):
            self.conn = db_conn(_DB)
        else:
            self.conn = db_conn(_DB)
            cursor = self.conn.cursor()
            with open(_INIT) as init_file:
                cursor.executescript(init_file.read())
        #Collect required files
        try:
            body = list(asset_files.keys())[0]
            self.assets = {
                'body': get_file(sub(r"\.\/", asset_path, body))
            }
            for k, v in asset_files[body].items():
                self.assets[k] = get_file(sub(r"\.\/", asset_path, v))
        except IndexError:
            self.assets = {}

        self.start = start_response

    def __iter__(self):
        status, headers, content = self.controller.model(self.conn, self.params).render(self.assets)
        self.start(status, headers)
        yield content

