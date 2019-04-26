import pyrebase
from conf import login

class admin:
    def __init__(self):
        firebase = pyrebase.initialize_app(login.CONFIG)
        self.auth = firebase.auth()
        self.ex = False

    def login(self, email, passwd):
        try:
            self.auth.sign_in_with_email_and_password(email, passwd)
            self.ex = True
        except Exception as e:
            import json
            self.ex = json.loads(e.args[1])['error']['message']
        finally:
            return self.ex


    def add_new(self, email, passwd):
        user = self.auth.create_user_with_email_and_password(email, passwd)
    
    def remove(self, email):
        pass
