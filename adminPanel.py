import pyrebase

class admin:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyDknVRA5s71ILA3aiFPYzrlKunQbGyXfDE",
            "authDomain": "cse-result.firebaseapp.com",
            "databaseURL": "https://cse-result.firebaseio.com",
            "projectId": "cse-result",
            "storageBucket": "cse-result.appspot.com",
            "messagingSenderId": "589177772091"
        }
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()

    def login(self, email, passwd):
        try:
            self.auth.sign_in_with_email_and_password(email, passwd)
            return True
        except Exception as e:
            import json
            return json.loads(e.args[-1])


    def add_new(self, email, passwd):
        user = self.auth.create_user_with_email_and_password(email, passwd)
    
    def remove(self, email):
        pass

# admin().login("ikbalnayem000@gmail.com", "welcome back")