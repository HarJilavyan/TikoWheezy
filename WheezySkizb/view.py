from wheezy.web.handlers import BaseHandler
from wheezy.security import Principal
from wheezy.web import authorize
from datetime import datetime
import json
from main import Notes, Users


class HomeHandler(BaseHandler):

    def get(self):
        page = "0"
        return self.render_response('home.html',
                    notes=Notes().get_all(5, 0), page=page,count="1"
            )


class NotesHandler(BaseHandler):

    def get(self):
        notes = Notes()
        page = int(self.route_args.get("page"))*5
        next_page = ((int(self.route_args.get("page"))+1)*5)
        next_page_bool = notes.get_all(5, next_page).fetchone()
        return self.render_response(
                'home.html', notes=notes.get_all(5, page),
                page=self.route_args.get("page"), count=next_page_bool
            )


class SignUpHandler(BaseHandler):

    def get(self):
        return self.render_response('signup.html')


class SignUserHandler(BaseHandler):
    def post(self):
        form = self.request.form
        new_user_name = form['login'][0]
        new_user_password = form['password'][0]
        if new_user_password != form['verify'][0]:
            return self.json_response(
                    {
                        "status": "Fail",
                        "message": "Passwords dont match",
                        "field": "verify"
                    }
                )
        if Users().check_username(new_user_name):
            return self.json_response(
                    {
                        "status": "Fail",
                        "message": "username exists",
                        "field": "login"
                    }
                )
        Users().sign_up(new_user_name, new_user_password)
        return self.json_response({"status": "ok"})


class LoginHandler(BaseHandler):

    def post(self):
        users = Users()
        
        user = users.login(
            self.request.form['login'][0], self.request.form['password'][0]
        )
        print(self.request.form['login'][0])
        if not user:
            return self.json_response(
                    {
                        "status": "Fail"
                    }
                )
        else:
            self.principal = Principal(id=str(user[0]))
            print(self.principal)
            return self.json_response(
                {
                    "status": "ok"
                }
            )


class SuccessLoginHandler(BaseHandler):
    def get(self):
        notes = Notes()
        user_id = self.principal.id
        notes = notes.get_by_user_id(user_id)
        return self.render_response('loginSuccess.html', notes=notes)


class LogoutHandler(BaseHandler):
    def get(self):
        del self.principal
        return self.redirect_for('home')


class NoteFormHandler(BaseHandler):
    def get(self):
        note_id = self.route_args.get("note_id")
        note = Notes().get_by_id(note_id)
        print(note)
        return self.render_response(
            'edit_note_form.html', note=note
        )


class AddHandler(BaseHandler):
    @authorize()
    def post(self):
        notes = Notes()
        new_note = self.request.form["add"][0]
        notes.insert(new_note, int(self.principal.id))
        return self.redirect_for('success')


class EditNoteHandler(BaseHandler):
    @authorize()
    def post(self):
        notes = Notes()
        edited_note = self.request.form["edit"][0]
        note_id = self.route_args.get("note_id")
        notes.edit_note(note_id, edited_note)
        return self.redirect_for('success')


class DeleteHandler(BaseHandler):
    @authorize()
    def get(self):
        notes = Notes()
        note_id = self.route_args.get("note_id")
        notes.deletenote(note_id)
        return self.redirect_for('success')



