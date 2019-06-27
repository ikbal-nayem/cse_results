import pyrebase, json
from conf import login

class admin:
    def __init__(self):
        firebase = pyrebase.initialize_app(login.CONFIG)
        self.auth = firebase.auth()
        self.db = firebase.database()
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

    def get_log(self):
        data = self.db.child('log').get().val()
        new_data = []
        for date in data:
            for time in data[date]:
                dic = {
                    'admin': data[date][time]['admin'],
                    'semester': data[date][time]['semester'],
                    'session': data[date][time]['session'],
                    'year': data[date][time]['year'],
                    'date': '{} ({})'.format(date, time),
                }
                new_data.append(dic)
        return new_data

    def post_log(self, data):
        import datetime
        dt = datetime.datetime.now()
        self.db.child('log').child(dt.date()).child(str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second)).set(data)

    def get_last_result(self):
        data = self.db.child('log').get().val()
        li, ti = [], []
        for date in data:
            for time in data[date]:
                li.append(date)
        for time in data[sorted(li)[-1]]:
            ti.append(time)
        d = data[sorted(li)[-1]][sorted(ti)[-1]]
        return d['semester'], d['year']