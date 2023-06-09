from wheezy.routing import url
from wheezy.web.handlers import file_handler
from view import AddHandler
from view import ListHandler

all_urls = [
    url('', ListHandler, name='list'),
    url('add', AddHandler, name='add'),
    url('static/{path:any}',
        file_handler(root='static/'),
        name='static')
]