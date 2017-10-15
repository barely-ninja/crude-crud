from response import Response, escape

class DeleteComment(Response):
    '''Create comment route'''
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        comment_id = escape('id', params['resource_id'])
        query = 'DELETE FROM comments WHERE comment_id={0}'.format(comment_id)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return self

    def render(self, assets):
        content = 'OK'.encode()
        status = self.status['redirect']
        headers = self.headers('TXT', content)
        headers.append(('Location', '/view'))
        return status, headers, content
