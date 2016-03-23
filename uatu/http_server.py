#!/usr/bin/env python
import mimetypes
import os
import socket


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCK_ADDRESS = ('127.0.0.1', 9000)


def get_404():
    return '''HTTP/1.0 404 Not Found
        Content-Type: text/html

        Not Found
    '''


def request_parse(text):
    lines = [l.rstrip('\r\n') for l in text.splitlines()]
    request_method = lines[0].split()
    server_name = lines[1].split()

    return {
        'REQUEST_METHOD': request_method[0],
        'PATH_INFO': request_method[1],
        'SERVER_NAME': server_name[1],
        'SERVER_PORT': SOCK_ADDRESS[1],
    }


def content_type_header(path_info):
    """
    Return the content type header.
    """
    if path_info == '/':
        path_info = '/index.html'

    filename = path_info.split('/')[-1]
    mimetype = mimetypes.guess_type(filename)

    return 'Content-Type: {0}'.format(mimetype[0])


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(SOCK_ADDRESS)

    sock.listen(1)

    response_pattern = '''HTTP/1.0 200 OK
        {content_type}

        <h1>Example</h1>'''

    while 1:
        connection, address = sock.accept()
        request = connection.recv(1024)

        environ = request_parse(request)
        print(environ)

        if not request:
            break

        response = response_pattern.format(
            content_type=content_type_header(environ['PATH_INFO'])
        )
        connection.sendall(response)
        connection.close()
