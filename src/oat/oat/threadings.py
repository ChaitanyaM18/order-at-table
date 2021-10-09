import threading
import logging

from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.mail import send_mail as core_send_mail


# Create your views here.
logger = logging.getLogger('embassy.custom')


class EmailThread(threading.Thread):
    def __init__(self, subject, template_object, from_email, to,
                 resume, fail_silently):
        super(EmailThread, self).__init__()
        self.subject = subject
        self.to = to
        self.from_email = from_email
        self.template_object = template_object
        self.resume = resume
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject, self.template_object, self.from_email, self.to)
        msg.content_subtype = "html"
        # if self.resume:
        #     msg.attach(self.resume.name, self.resume.read())
        try:
            msg.send()
        except Exception as e:
            logger.warning('Email with subject %s error %s', (self.subject,str(e)))


def send_mails(subject, template_object, from_email, to, resume,
              fail_silently=False, *args, **kwargs):
    EmailThread(subject, template_object, from_email,
                to, resume, fail_silently).start()
