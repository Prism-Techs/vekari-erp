from django.core.mail import EmailMessage
import os
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives,send_mail
import random
from django.template import Context
from django.template.loader import render_to_string
from vekaria_erp.settings import EMAIL_FROM

class Util:

    @staticmethod
    def send_reset_password_email(data):
        
        d = Context({ 'data': data }) 
        print(d['data'],"0000000000000000000000000000000000000")
        htmly     = render_to_string('EmailTemplate.html',d['data'])
        html_content = htmly 
        msg = EmailMultiAlternatives(data['subject'], data['body'], os.environ.get('EMAIL_FROM'), [data['to_email']] )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
