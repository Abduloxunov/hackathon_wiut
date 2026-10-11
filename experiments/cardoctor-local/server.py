"""Local-only HTTP service for the CarDoctor experiment."""
import core
import json,mimetypes,re,secrets
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit
TOKEN=secrets.token_urlsafe(32)
MAX_REQUEST=12*1024*1024

class Handler(BaseHTTPRequestHandler):
    def send(self,body,status=200,kind='application/json; charset=utf-8'):
        if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False,allow_nan=False).encode()
        self.send_response(status);self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','no-store');self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self' data: blob:; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers();self.wfile.write(body)
    def valid_host(self):
        return self.headers.get('Host') in {'127.0.0.1:8765','localhost:8765'}
    def do_GET(self):
        if not self.valid_host():return self.send({'error':'Invalid local host.'},400)
        path=urlsplit(self.path).path
        if path=='/api/health':
            lib=core.library()
            return self.send({'token':TOKEN,'model_available':core.MODEL_FILE.exists(),'references':len(lib['references']),'notes':len(lib['notes']),'storage':str(core.RUNTIME),'damage_detector_trained':False,'feature_version':core.FEATURE_VERSION})
        if path=='/api/library':return self.send(core.library())
        static={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/favicon.svg':'favicon.svg'}
        if path in static:
            file=core.BASE/'static'/static[path]
            return self.send(file.read_bytes(),kind=mimetypes.guess_type(str(file))[0] or 'text/plain')
        match=re.fullmatch(r'/media/([a-f0-9]{32}\.png)',path)
        if match:
            file=core.RUNTIME/'images'/match[1]
            if file.exists():return self.send(file.read_bytes(),kind='image/png')
        return self.send({'error':'Not found.'},404)
    def do_POST(self):
        if not self.valid_host():return self.send({'error':'Invalid local host.'},400)
        if self.headers.get('X-CarDoctor-Token')!=TOKEN:return self.send({'error':'Reload the local app before submitting.'},403)
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send({'error':'Send JSON.'},415)
        try:size=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.send({'error':'Invalid request length.'},400)
        if not 0<size<=MAX_REQUEST:return self.send({'error':'Request is too large or empty.'},413)
        try:
            data=json.loads(self.rfile.read(size))
            if not isinstance(data,dict):raise ValueError('Expected a JSON object.')
            path=urlsplit(self.path).path
            if path=='/api/analyze':return self.send(core.analyze(data))
            if path=='/api/references':return self.send(core.add_reference(data),201)
            if path=='/api/notes':return self.send(core.add_note(data),201)
            if path=='/api/export':
                # Recompute from the image rather than trusting client-supplied results.
                result=core.analyze(data)
                from reports import markdown_report
                target=core.RUNTIME/'reports'/(result['case_id']+'.md')
                target.write_text(markdown_report(result),encoding='utf-8')
                return self.send({'path':str(target),'report':markdown_report(result)})
            return self.send({'error':'Not found.'},404)
        except (ValueError,KeyError,TypeError,UnicodeDecodeError) as e:return self.send({'error':str(e)},400)
        except Exception as e:
            print(type(e).__name__,str(e))
            return self.send({'error':'The analysis could not complete. Check the local server log.'},500)
    def log_message(self,format,*args):print(format%args)

if __name__=='__main__':
    print('CarDoctor local experiment: http://127.0.0.1:8765')
    print('Storage:',core.RUNTIME)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
