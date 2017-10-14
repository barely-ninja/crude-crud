from string import Template
from response import Response, fill_template

class StaticServer(Response):
    """Serves static assets"""
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        """model"""
        self.name_parts = params['resource_id'].split('.')
        return self

    def render(self, assets):
        """view"""
        if 'body' in assets:
            asset_type = 'HTML'
            content = fill_template(assets['body'], assets).encode()
            status = self.status['OK']
        else:
            try:
                res_path = 'static/'
                asset_type = self.name_parts[1].capitalize()
                asset_name = res_path + self.name_parts[0]
                with open(asset_name, mode='rb') as static_file:
                    content = static_file.read()
                status = self.status['OK']             
            except IndexError:
                asset_type = 'TXT'
                content = 'Content not available'
                status = self.status['not-found']

        return status, self.headers(asset_type, content), content
