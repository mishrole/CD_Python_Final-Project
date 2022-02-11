from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask( __name__ )
app.secret_key = "coding-dojo"

CORS( app, resources={r"/api/*" : {"origins": "*"}} )

# SMTP Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USER')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASS')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
# mail = Mail()
# mail.init_app(app)
