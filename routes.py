from static.static_server import StaticServer
from res.region.list_reg import ListCitiesInRegion
from res.comment.create import CreateComment
from res.comment.list_all import ListComments

def resolve(method, path_elements):
    routes = {}
    routes[('GET', '')] = StaticServer
    routes[('GET', 'comment')] = StaticServer
    routes[('POST', 'comment')] = CreateComment
    routes[('GET', 'view')] = ListComments
    routes[('GET', 'region')] = ListCitiesInRegion
    
    resource = path_elements[1]

    try:
        route = routes[(method, resource)]
    except KeyError:
        route = StaticServer

    return route
