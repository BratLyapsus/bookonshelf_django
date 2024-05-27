from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_notification_email(subject, message, recipient_list, html_message=None):
    email = EmailMultiAlternatives(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list
    )
    if html_message:
        email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)