
import os
from django.template import Context
from django.core.mail import EmailMultiAlternatives,send_mail

from django.template import Context
from django.template.loader import render_to_string
from vekaria_erp.settings import EMAIL_FROM

class Utils:

    @staticmethod
    def send_vendor_email(data)->bool:
        try:
            if data.get('to_email') is not None and data.get('to_email')!="":
                d = Context({ 'data': data }) 
                print(d['data'],"0000000000000000 send email 000000000000000000000")
                htmly = render_to_string('vendor_templates.html',d['data'])
                html_content = htmly 
                msg = EmailMultiAlternatives(data['subject'], data['body'], os.environ.get('EMAIL_FROM'), [data['to_email']] )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return True
            return False  
        except Exception as e:
            print(e)
            return False
