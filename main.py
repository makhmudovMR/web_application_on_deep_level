import socket
from views import *


URLS = {
    '/': index,
    '/blog': blog,
}


def parse_requset(request):
    parse = request.split()
    method = parse[0]
    url = parse[1]
    return (method, url)

def generate_content(code, url):
    if code == 404:
        return '<h1>404 Not Found</h1>'
    return URLS[url]()

def generate_headers(method, url):
    if  method != 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    
    if url not in URLS:
        return ('HTTP/1.1 404 Not Found found\n\n', 404)
    
    return ('HTTP/1.1 200 OK\n\n', 200)

def generate_response(request):
    method, url = parse_requset(request)
    headers, code = generate_headers(method, url)
    response = generate_content(code, url)
    return (headers + response).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # определённые настройки
    server_socket.bind(('localhost', 5000)) # ждем обращение на этот адресс
    server_socket.listen()
    print('Server is run, go to: localhost:5000')

    while True:
        client_socket, addr = server_socket.accept() # принимаем запрос клиента
        request = client_socket.recv(1024) # получаем запрос (по пакетам в размере 1024)
        print(request)
        print('-' * 10)
        print(addr)

        response = generate_response(request.decode('utf-8')) # генерируем ответ

        client_socket.sendall(response) # отправляем ответ
        client_socket.close()# закрываем соединение




if __name__ == '__main__':
    run()