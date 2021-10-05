from flask import Flask, request, Response, make_response, render_template
from werkzeug.exceptions import abort
from werkzeug.routing import Rule
from http import HTTPStatus
from urllib.parse import urlparse
from socket import gaierror, gethostbyname
import os
import requests

app = Flask(__name__)
app.url_map.add(Rule('/bypass', endpoint='corsbypass'))

def preflight_response(request):
  response = make_response()
  response.headers.add("Access-Control-Allow-Origin", request.origin)
  response.headers.add('Access-Control-Allow-Headers', "*")
  response.headers.add('Access-Control-Allow-Methods', "*")
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

@app.route('/')
def index():
  return render_template("index.html")

@app.endpoint('corsbypass')
def bypass():
  if not request.args["url"]:
    abort(HTTPStatus.BAD_REQUEST, "No url specified")
  if request.method == "OPTIONS":
    return preflight_response(request)

  requested_domain = urlparse(request.args["url"]).netloc
  if ':' in requested_domain:
    requested_domain = requested_domain[:requested_domain.index(':')]
  try:
    requested_host = gethostbyname(requested_domain)
  except gaierror as e:
    abort(HTTPStatus.BAD_REQUEST, "Invalid url host specified")
    
  if requested_host == "0.0.0.0" or requested_host == "127.0.0.1":
    abort(HTTPStatus.FORBIDDEN, "Not allowed")

  resp = requests.request(
    method=request.method,
    url=request.args["url"],
    headers={key: value for (key, value) in request.headers if key != 'Host'},
    data=request.get_data(),
    cookies=request.cookies,
    allow_redirects=False)

  excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
  headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers and not name.lower().startswith('access-control')]
  response = Response(resp.content, resp.status_code, headers)
  response.headers.add("Access-Control-Allow-Origin", request.origin or '*')
  return response

@app.route("/flag")
def flag():
  if request.remote_addr != "127.0.0.1":
    abort(HTTPStatus.FORBIDDEN, "Only for local use")
  return os.getenv("FLAG")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=(os.getenv("PORT") or "8000"), debug=False)
