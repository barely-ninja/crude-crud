from string import Template
from response import Response

class StaticServer(Response):
    """Serves static assets"""
    def __init__(self):
        super().__init__()
        self.res_path = 'static/'

    def model(self, conn, params):
        """model"""
        self.props['asset_name'] = params['resource_id']
        return self

    def render(self):
        """view"""
        try:
            try:
                asset_type = self.props['asset_name'].split('.')[1]
                with open(self.res_path+self.props['asset_name'], mode='rb') as static_file:
                    content = static_file.read()
                status = self.status['OK']
                return status, self.headers(asset_type,content), content

            except FileNotFoundError:
                asset_type = 'txt'
                content = 'Content not available'
                status = self.status['not-found']
                return status, self.headers(asset_type,content), content

        except IndexError:
            asset_type = 'HTML'
            self.res_path = 'res/comment/create_form/'
            with open(self.res_path+'form.html') as template_file:
                template_text = template_file.read()
            with open(self.res_path+'form.js') as script_file:
                script_text = script_file.read()
            template = Template(template_text)
            content = template.substitute(script=script_text).encode()
            status = self.status['OK']
            return status, self.headers(asset_type,content), content        