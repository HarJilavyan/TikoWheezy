from wheezy.http import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory
from wheezy.web.templates import WheezyTemplate
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from urls import all_urls
import sqlite3


searchpath = ['templates']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[
        CoreExtension(),
        WidgetExtension(),
    ])
engine.global_vars.update({
    'h': html_escape
})
options = {'render_template': WheezyTemplate(engine)}
main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory
    ],
    options=options
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
