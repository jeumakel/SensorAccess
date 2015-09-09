import cgi
import Cookie
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SensorAccess import SensorAccess

class MainHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_headers('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        is_json = False
        param_type = ''
        if self.path == '/favicon.ico':
            return
        p = self.path.split("?")
        path = p[0][1:].split("/")
        params = {}
        if len(p) > 1:
            params = cgi.parse_qs(p[1], True, True)
            if ('json' in params and params.get('json')[0] == '1') or ('all' in params and params.get('all')[0] == '1'):
                is_json = True
            for param in params:
                if  (param == 'cpu_temp' or \
                    param == 'cpu_usage' or \
                    param == 'all' or \
                    param == 'net_sent' or \
                    param == 'net_recv') and params.get(param)[0] == '1':
                    param_type = param
                    break
            if param_type == '':
                #if no correct param type, return default page
                self._get_index()
            else:
                self._get_requested_data(param_type, is_json)
        else:
            #if no parameters on the url, return default page
            self._get_index()

    def _get_index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate') # HTTP 1.1.
        self.send_header('Pragma', 'no-cache') # HTTP 1.0.
        self.send_header('Expires', '0') # Proxies.
        self.end_headers()
        self.wfile.write('<html>')
        self.wfile.write('<head><title>Sensor Web Access</title></head>')
        self.wfile.write('<body>')
        self.wfile.write('<h1>Sensor Web Access</h1>')
        self.wfile.write('Individual responses:')
        self.wfile.write('<ul>')
        self.wfile.write('<li><a href="?cpu_usage=1">CPU usage percentage</a></li>')
        self.wfile.write('<li><a href="?cpu_temp=1">CPU temperature</a></li>')
        self.wfile.write('<li><a href="?net_sent=1">Network bytes sent</a></li>')
        self.wfile.write('<li><a href="?net_recv=1">Network bytes received</a></li>')
        self.wfile.write('</ul>')
        self.wfile.write('JSON responses:')
        self.wfile.write('<ul>')
        self.wfile.write('<li><a href="?all=1&json=1">All parameters</a></li>')
        self.wfile.write('<li><a href="?cpu_usage=1&json=1">CPU usage percentage</a></li>')
        self.wfile.write('<li><a href="?cpu_temp=1&json=1">CPU temperature</a></li>')
        self.wfile.write('<li><a href="?net_sent=1&json=1">Network bytes sent</a></li>')
        self.wfile.write('<li><a href="?net_recv=1&json=1">Network bytes received</a></li>')
        self.wfile.write('</ul>')
        self.wfile.write('</br><p>You accessed path: %s</p>' % self.path)
        self.wfile.write('</body>')
        self.wfile.write('</html>')

    def _get_requested_data(self, param_type, is_json):
        self.send_response(200)
        if is_json:
            self.send_header('Content-type', 'application/json')
        else:
            self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate') # HTTP 1.1.
        self.send_header('Pragma', 'no-cache') # HTTP 1.0.
        self.send_header('Expires', '0') # Proxies.
        self.end_headers()
        self.wfile.write(self._get_data(param_type, is_json))

    def _get_data(self, param_type, is_json):
        sensor_access = SensorAccess()
        if param_type == 'all':
            return sensor_access.get_all_json()
        if param_type == 'cpu_temp':
            return sensor_access.get_cpu_temperature(is_json)
        if param_type == 'cpu_usage':
            return sensor_access.get_cpu_usage(is_json)
        if param_type == 'net_sent':
            return sensor_access.get_bytes_sent(is_json)
        if param_type == 'net_recv':
            return sensor_access.get_bytes_received(is_json)
        if is_json:
            return '{}'
        return ''

def main(port):
    try:
        server = HTTPServer(('', int(port)), MainHandler)
        print 'started httpserver on port %s... CTRL+C stops httpserver' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '13234'
    main(port)
