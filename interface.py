""" Provide a user interface via a local webserver """
import CGIHTTPServer
from  BaseHTTPServer import HTTPServer
import random
import threading


class ThreadedHTTPServer(threading.Thread):
    daemon = True
    def __init__(self):
        self.initialized = False
        super(ThreadedHTTPServer, self).__init__()
        
    def run(self):
        self.host = ""
        self.port = random.randrange(8000, 8100)
        print 'listening on port ' + str(self.port)
        server = HTTPServer
        handler = CGIHTTPServer.CGIHTTPRequestHandler
        handler.cgi_directories = ["/", ]
        self.httpd = server((self.host, self.port), handler)
        self.initialized = True
        self.httpd.serve_forever()


class WebInterface(object):
    def __init__(self):
        self.server = ThreadedHTTPServer()
    
    def open_interface(self):
        self.server.start()

    def shutdown(self):
        self.server.httpd.shutdown()


class TemporaryWebInterface(WebInterface):
    def __init__(self, duration_in_seconds=10):
        self.duration_in_seconds = duration_in_seconds
        super(TemporaryWebInterface, self).__init__()

    def initiate_timeout(self):
        self.server.join(self.duration_in_seconds)
        self.shutdown()


class PersistantWebInterface(WebInterface):
    def open_interface(self):
        self.server.start()
        self.server.join()
        self.server.httpd.shutdown()


if __name__ == '__main__':
    iface = TemporaryWebInterface(120)
    # iface = PersistantWebInterface()
    iface.open_interface()
    iface.initiate_timeout()
