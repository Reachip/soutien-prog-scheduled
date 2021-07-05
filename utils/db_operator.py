from datetime import datetime, timedelta
from os import environ
from abc import ABC


class DBOperator(ABC):
    def __init__(self, database):
        self.cursor = database.cursor
        self.connector = database.connector


class Course(DBOperator):
    def __init__(self, database):
        super().__init__(database)

    def find_course_by_id(self, id):
        request = f"select * from course_course where id = {id}"
        self.cursor.execute(request)

        return self.cursor.fetchall()[0]

    def fetch_old_courses(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = f"select * from course_course where starting_at <= '{now}'"
        self.cursor.execute(request)

        return [field[0] for field in self.cursor.fetchall()]

    def delete_courses(self, id):
        self.cursor.execute(
            f"delete from participant_participant where course_id = {id}"
        )
        self.cursor.execute(f"delete from course_course where id = {id}")

    def fetch_courses_which_start_about_in_5_minutes(self):
        now_plus_5_minutes = (datetime.now() + timedelta(minutes=5)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = f"select * from course_course where starting_at between '{now}' and '{now_plus_5_minutes}'"
        self.cursor.execute(request)

        return [str(field[0]) for field in self.cursor.fetchall()]


class Participant(DBOperator):
    def __init__(self, database) -> None:
        super().__init__(database)

    def fetch_unotified_participants(self, course_id):
        participants = []

        set_notified_req = f"select * from participant_participant where course_id = '{course_id}' and notified = false"
        self.cursor.execute(set_notified_req)

        for participant in self.cursor.fetchall():
            participants.append(participant)

        return participants

    def send_mail_to_participant(self, participant, mailer):
        mailer.send_mail(participant[2], participant)

    def set_notified(self, participant):
        update_req = f"update participant_participant set notified = true where id = '{participant[0]}'"
        self.cursor.execute(update_req)
        self.connector.commit()
