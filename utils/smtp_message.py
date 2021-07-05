import smtplib
from abc import ABC, abstractclassmethod
from email.message import EmailMessage
from utils.db_operator import Course, Participant


class SMTPMessage(ABC):
    def __init__(self, server_name, port, email, password, db=None):
        self.server_name = server_name
        self.port = port
        self.email = email
        self.password = password
        self.db = db

        self.server = smtplib.SMTP_SSL(self.server_name, self.port)
        self.server.login(self.email, self.password)

    def send_mail(self, to, ctx=None):
        msg = EmailMessage()

        msg["Subject"] = "SoutienProg | Participation au soutien"
        msg["From"] = self.email
        msg["To"] = to
        msg.set_content(self.message(ctx))

        self.server.send_message(msg)

    @property
    @abstractclassmethod
    def message(self, ctx):
        pass


class SMTPMessageOnCourseBegin(SMTPMessage):
    def __init__(self, server, email, password, db, port=465):
        super().__init__(server, port, email, password, db)

    def message(self, ctx: Participant):
        course = Course(self.db)
        participant_course = course.find_course_by_id(ctx[3])
        formated_datetime = participant_course[2].strftime("%H h %M")
        
        return f"{participant_course[6]} va commencer à {formated_datetime}.\nSuivez le lien suivant afin d'assister au soutien : {participant_course[7]}"
