from urllib.parse import urlencode
from sqlite3 import Error as dbError
from response import Response, escape
from db.init import comment_schema

class CreateComment(Response):
    '''Create comment route'''
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        def extract_value(src, key):
            try:
                value = src[key][0]
            except KeyError:
                value = None
            return value
        schema_order = comment_schema()[1:]
        ordered = [extract_value(params['body'],key) for key in schema_order]
        esc_rules = ['name']*3+['phone', 'email']+['id']*2+['text']
        ord_pairs = zip(esc_rules, ordered)
        values = tuple([escape(rule, value) for rule, value in ord_pairs])
        query = 'INSERT INTO comments ('+', '.join(schema_order)+') VALUES (?,?,?,?,?,?,?,?)'
        cursor = conn.cursor()
        try:
            cursor.execute(query, values)
        except dbError as err:       
            self.props['error'] = err
        else:
            conn.commit()
        return self

    def render(self, assets):
        content = 'OK'.encode()
        status = self.status['redirect']
        headers = self.headers('TXT', content)
        if self.props['error'] == '':
            redirectURL = '/view'
        else:
            redirectURL = '/comment?%s' % urlencode({'error': self.props['error']})
        headers.append(('Location', redirectURL))
        return status, headers, content
