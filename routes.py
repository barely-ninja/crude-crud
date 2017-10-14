from static.static_server import StaticServer
from res.region.list_reg import ViewRegion
from res.comment.create_form import CreateCommentForm
from res.comment.create import CreateComment
from res.comment.list_all import ListComments

def resolve(method, path_elements):
    routes = {
        ('GET', ''): (StaticServer, 'static/', {
            './page.html': {
                'header': './header.html'
            }
        }),
        ('GET', 'comment'): (CreateCommentForm, 'res/comment/create_form/', {
            './form.html': {
                'header': 'static/header.html',
                'script': './form.js'
            }
        }),
        ('POST', 'comment'): (CreateComment, '', {}),
        ('GET', 'view'): (ListComments, 'res/comment/list_all/', {
            './list.html': {
                'row': './comment.html',
                'header': 'static/header.html'
            }
        }),
        ('GET', 'regions'): (ViewRegion, '', {}),
    }

    resource = path_elements[1]

    try:
        route = routes[(method, resource)]
    except KeyError:
        route = (StaticServer, '', {})

    return route
