from re import sub
from string import Template

def escape(name, item):
    re_table = {
        'name': r'[^\d|\w| |\.]',
        'phone': r'[^\d| |\(|\)]',
        'email': r'[^\d|\w|\.|\-|@]',
        'id': r'[^\d]',
        'text': r'[;]'
    }
    try:
        val = sub(re_table[name], '', item)
    except TypeError:
        val = None
    return val

def fill_template(container, props):
    """Helper method for filling templates from self.props"""
    template = Template(container)
    props_list = [(k, v if v is not None else '') for k,v in props.items()]
    clean_props = dict(props_list)
    content = template.substitute(clean_props)
    return content

class Response:
    """Generic response interface for a route"""
    def __init__(self):
        self.props = {'error': ''}
        self.status = {
            'OK': "200 OK",
            'server-error': "500 Server Error",
            'not-found': "404 Not Found",
            'redirect': "303 See Other"
        }
    def headers(self, ct_type, ct):
        def content_type(ctt):
            MIME_table = {
                'HTML': 'text/html; charset=utf-8',
                'JSON': 'text/json',
                'ICO': 'image/x-icon',
                'TXT': 'text/plain'
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
