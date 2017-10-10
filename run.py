from server import CommentServer
from wsgiref import simple_server

def main():
    comment_server = simple_server.make_server('localhost', 8888, CommentServer)
    comment_server.serve_forever()

if __name__ == '__main__':
    main()
