#
# responder sample app
#
# see: https://responder.kennethreitz.org/en/latest/quickstart.html
#
import responder

api = responder.API(
    templates_dir = "app/templates"
)


@api.route("/")
def root_path(req, resp):
    resp.html = api.template('index.html')

@api.route("/hello/{who}")
def hello_to(req, resp, *, who):
    resp.text = f"Hello, {who}! how are you?"

@api.route("/hello/{who}/html")
def hello_html(req, resp, *, who):
    resp.html = api.template('hello.html', who=who)

if __name__ == '__main__':
    api.run()

