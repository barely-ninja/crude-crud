from response import Response, escape

class CreateComment(Response):
    '''Create comment route'''
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        print('***', params['body'])
        schema_order = ['name', 'last_name', 'middle_name', 'phone', 'email', 'city_id', 'region_code', 'comment']
        ordered = [params['body'][key.encode()].decode() for key in schema_order]
        esc_rules = ['name']*3+['phone', 'email']+['id']*2+['text']
        ord_pairs = zip(esc_rules, ordered)
        values = [escape(rule, value) for rule, value in ord_pairs]

        query = 'INSERT INTO comments VALUES({0},{1},{2},{3},{4},{5},{6},{7})'.format(*values)
        print(query)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return self

    def render(self, assets):
        content = ''
        status = self.status['redirect']
        headers = self.headers('TXT', content).append(('Location', '/comments'))
        return status, headers, content
