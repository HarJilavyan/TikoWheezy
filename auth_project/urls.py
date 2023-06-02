from view import (
    LoginHandler, HomeHandler, AddHandler, NotesHandler, DeleteHandler,
    SuccessLoginHandler, SignUpHandler, SignUserHandler, EditNoteHandler,
    NoteFormHandler, LogoutHandler
    )
from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.web.handlers import file_handler
from wheezy.routing import url
from datetime import timedelta
from wheezy.http import CacheProfile
from wheezy.http.cache import etag_md5crc32

static_cache_profile = CacheProfile(
    "public",
    duration=timedelta(minutes=15),
    vary_environ=["HTTP_ACCEPT_ENCODING"],
    namespace="static",
    http_vary=["Accept-Encoding"],
    etag_func=etag_md5crc32,
    enabled=True
)

static_files = response_cache(static_cache_profile)(
    response_transforms(gzip_transform(compress_level=6))(
        file_handler(
            root='static/')))

all_urls = [
    url('', HomeHandler, name='home'),
    url('{page:i}', NotesHandler, name="notes"),
    url('login', LoginHandler, name="login"),
    url('signup', SignUpHandler, name="sign_up"),
    url('logout', LogoutHandler, name="logout"),
    url('signup/user', SignUserHandler, name='sign_user'),
    url('dashboard', SuccessLoginHandler, name="success"),
    url('addnote', AddHandler, name="addnote"),
    url('deletenote/{note_id:i}', DeleteHandler,
        name="deletenote"
        ),
    url('notes/{note_id:i}', NoteFormHandler, name="note_form"),
    url('editnote/{note_id:i}', EditNoteHandler, name="edit"),
    # static urls
    url('static/{path:any}', static_files, name='static')
]
