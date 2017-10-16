from string import Template
from response import Response, fill_template

class CreateCommentForm(Response):
    """Serves static assets"""
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        """model"""
        if 'error' in params['body']:
            self.props['error'] = params['body']['error']
        return self

    def render(self, assets):
        """view"""
        asset_type = 'HTML'
        content = fill_template(assets['body'], {
            'error': self.props['error'],
            'header': assets['header'],
            'script': assets['script']
            }).encode()
        status = self.status['OK']
        return status, self.headers(asset_type,content), content        