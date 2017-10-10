class Response:
    """Generic response interface for a route"""
    def __init__(self):
        self.props = {}
        self.status = {
            'OK': "200 OK",
            'server-error': "500 Server Error",
            'not-found': "404 Resource not found"
        }
    def headers(self, ct_type, ct):
        def content_type(ctt):
            MIME_table = {
                'HTML': 'text/html',
                'JSON': 'text/json',
                'ico': 'image/x-icon',
                'txt': 'text/plain'
            }
            if ctt in MIME_table:
                return MIME_table[ctt]
            else:
                return 'application/octet-stream'

        return [('Content-type', content_type(ct_type)), ('Content-length', str(len(ct)))]

    def model(self, conn, params):
        """Populate props from model"""
        pass

    def render(self):
        """Render view from props"""
        pass
