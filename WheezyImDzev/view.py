from wheezy.web.handlers import BaseHandler
from config import session
from Tutorial import Greeting
from repository import Repository
from validation import greeting_validator

class ListHandler(BaseHandler):

    def get(self):
        with session() as db:
            repo = Repository(db)
            greetings = repo.list_greetings()
        return self.render_response('list_html',
                greetings=greetings)


class AddHandler(BaseHandler):

    def get(self, greeting = None):
        greeting = greeting or Greeting()
        return self.render_response('add_html', greeting = greeting)
    
    def post(self):
        greeting = Greeting()
        if (not self.try_update_model(greeting)
                or not self.validate(greeting, greeting_validator)):
            return self.get(greeting)
        with session() as db:
            repo = Repository(db)
            if not repo.add_greeting(greeting):
                self.error('Sorry, can not add your greeting.')
                return self.get(greeting)
            db.commit()
        return self.see_other_for('list')

    
