import pyrebase, json
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
            self.ex = json.loads(e.args[1])['error']['message']
        finally:
            return self.ex


    def add_new(self, email, passwd):
        try:
            user = self.auth.create_user_with_email_and_password(email, passwd)
            self.auth.send_email_verification(user['idToken'])
            self.ex = True
        except Exception:
            self.ex = False
        finally:
            return self.ex
            

