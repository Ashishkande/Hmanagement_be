from app.celery_worker import celery
from app.service.email_service import send_email

@celery.task
def send_otp_email(email, otp):

    print("TASK RECEIVED")
    print(email)
    print(otp)

    send_email(email, otp)

    print("EMAIL TASK FINISHED")