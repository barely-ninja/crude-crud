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
                value = ''
            return value
        schema_order = comment_schema()[1:]
        ordered = [extract_value(params['body'],key) for key in schema_order]
        esc_rules = ['name']*3+['phone', 'email']+['id']*2+['text']
        ord_pairs = zip(esc_rules, ordered)
        values = tuple([escape(rule, value) for rule, value in ord_pairs])
        query = 'INSERT INTO comments ('+', '.join(schema_order)+') VALUES (?,?,?,?,?,?,?,?)'
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return self

    def render(self, assets):
        content = 'OK'.encode()
        status = self.status['redirect']
        headers = self.headers('TXT', content)
        headers.append(('Location', '/view'))
        return status, headers, content
