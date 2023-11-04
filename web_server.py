import os
import socket
import mimetypes
import subprocess 

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((self.host, self.port))
        sock_server.listen()
        print("Web Server SIAP...!!!")
        print("Cara Akses Web Server : http://"+str(self.host)+":"+str(self.port))
        while True:
            sock_client, client_address = sock_server.accept()
            request = sock_client.recv(1024).decode()
            print("Dari Client :"+request)

            if(request and request.strip()):
                response = self.handle_request(request)
                sock_client.send(response)

            sock_client.close()
        #endwhile
        sock_server.close()

    def handle_request(self, request):
        return request
#Akhir dari class TCPServer

class HTTPServer (TCPServer):
    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_request(self, request):
        request_message = str(request).split("\r\n")
        request_line = request_message[0]
        words = request_line.split()
        method = words[0]
        uri = words[1].strip("/")
        
        http_version = words[2]
        if(uri == ''):
            uri = 'index.html'
        if(method == 'GET'):
            response = self.handle_get(uri, http_version)
        elif(method == "POST"):
            response = self.handle_post(uri, http_version)
        return response

    def handle_get(self, uri, http_version):
        uri_elem = uri
        url = "%s"%(uri_elem)
        if os.path.exists(url) and not os.path.isdir(url): 
            response_line = b''.join([http_version.encode(), b'200', b'OK'])
            content_type = mimetypes.guess_type(url)[0] or 'text/html'
            entity_header = b''.join([b'Content-type: ', content_type.encode()])

            file = open(url, 'rb')
            message_body = file.read()
            file.close()
        else :
            response_line = b''.join([http_version.encode(), b'404', b'Not Found'])
            entity_header = b'Content-Type: text/html'
            message_body = b'<h1>404 Not Found</h1>'
        crlf = b'\r\n'
        response = b''.join([response_line, crlf, entity_header, crlf, crlf, message_body])
        return response

    def handle_post(self, uri,http_version):
        response_line = b''.join([http_version.encode(), b'200', b'OK'])
        entity_header = b'Content-Type: text/html'
        message_body = b'<h1>Ini testing POST</h1>'
        crlf = b'\r\n'
        response = b''.join([response_line, crlf, entity_header, crlf, crlf, message_body])
        return response

    
#Akhir class HTTPServer
    
if __name__ == '__main__':
    server = HTTPServer('127.0.0.1', 8080)
    server.start()    