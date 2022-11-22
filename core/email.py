from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_code_email(name, email, code):

    context = {
        'name' : name,
        'email' : email,
        'code' : code
    }

    email_subject = "Fitness Verification Code"
    email_body = render_to_string('email_code_message.txt', context)

    email=EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email, ]
    )

    return email.send(fail_silently=True)

def send_change_password_email(name, email, change_password_link):

    #change_password_link =  request.build_absolute_uri('/bands/?print=true')
    context = {
        'name': name,
        'email': email,
        'change_password_link': change_password_link
    }

    email_subject = "Fitness Change Password"
    email_body = render_to_string('email_change_password.txt', context)

    email=EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email, ]
    )

    return email.send(fail_silently=True)