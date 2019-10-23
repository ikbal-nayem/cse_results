from db_operation import database
from operation import backend
from conf import email_info
import smtplib, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mail:
    def __init__(self):
        self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.smtp.login(email_info.EMAIL, email_info.PASSWORD)

    def send(self, semester, year):
        time.sleep(5)
        addresses = database().find_email(semester, str(year))
        for address in addresses:
            print('Sending mail to '+address[1]+'...', end=' ')
            data = backend().generate_API(address[0], semester)
            template = self.create_template(data)
            msg = self.generate_msg(semester, address[1], template)
            self.smtp.sendmail(email_info.EMAIL, address[1], msg.as_string())
            print('Done')
        self.smtp.quit()
            
    def generate_msg(self, semester, send_to, template):
        msg = MIMEMultipart("alternative")
        msg['Subject'] = semester+" Semester result"
        msg['From'] = email_info.EMAIL
        msg['To'] = send_to
        text = "Your "+semester+" Semester result has been published.\n To see go to our site (http://iku.pythonanywhere.com/)"
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(template, 'html')
        msg.attach(part1)
        msg.attach(part2)
        return msg


    def create_template(self, info):
        from main import app, render_template
        with app.app_context():
            return render_template('admin/email_template.html', info=info)


