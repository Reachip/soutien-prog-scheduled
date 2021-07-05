import logging

from os import environ
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import db_operator, smtp_message, database

sched = BlockingScheduler()

try:
    db = database.PostgresDB(
        environ["DB_HOST"],
        environ["DB_NAME"],
        environ["DB_LOGIN"],
        environ["DB_PASSWORD"],
    )

except KeyError:
    raise RuntimeError(
        "Need DB_NAME, DB_HOST, DB_LOGIN and DB_PASSWORD variables to work"
    )

try:
    mailer = smtp_message.SMTPMessageOnCourseBegin(
        environ["SMTP_SERVER"], environ["SMTP_MAIL"], environ["SMTP_PASSWORD"], db
    )

except KeyError:
    raise RuntimeError("Need SMTP_SERVER, SMTP_MAIL, SMTP_PASSWORD variables to work")

course = db_operator.Course(db)
participant = db_operator.Participant(db)

logging.basicConfig(level=logging.INFO)

@sched.scheduled_job("interval", minutes=1)
def fetch_old_courses():
    logging.info("Fetch old courses ...")

    for id in course.fetch_old_courses():
        logging.info(f"Delete course(s) with id(s) : {id}")
        course.delete_courses(id)
        logging.info(f"{id} deleted succesfully !")

    else:
        logging.info("Find nothing ...")


@sched.scheduled_job("interval", minutes=1)
def fetch_courses_which_start_about_in_5_minutes():
    logging.info("Fetch courses which start about in 5 minutes ...")

    for courses_id in course.fetch_courses_which_start_about_in_5_minutes():
        logging.info(f"Find course(s) with id : {courses_id}")

        for unotified_participant in participant.fetch_unotified_participants(
            courses_id
        ):
            logging.info(f"Send mail to {unotified_participant[1]}")
            participant.send_mail_to_participant(unotified_participant, mailer)

            logging.info(f"Set {unotified_participant[1]} as notified")
            participant.set_notified(unotified_participant)

    else:
        logging.info("Find nothing ...")
        
sched.start()
