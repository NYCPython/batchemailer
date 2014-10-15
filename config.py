import os

# setting this to true will set recipient emails to MSG_KEYS['preview_email']
PREVIEW_MODE = True
# if you have an entry with 4 emails, then PREVIEW_EMAILS should have at least 
# 4 unique emails
PREVIEW_EMAILS =['your.email+1@gmail.com', 'your.email+2@gmail.com']

# this email and password should be what you use to log into gmail
SMTP_EMAIL = 'your-email@nycpython.org'
SMTP_PWD = os.environ['YOUR_EMAIL_PASSWORD']

# what's listed in the "From" field. Ideally should match what you entered
# for SMTP_EMAIL, otherwise you risk getting marked as 'spam'
MSG_FROM = 'Your Name <your-email@nycpython.org>'
MSG_CC = 'my-groups@googlegroups.com,my-friend@gmail.com'

# see README on {{params}}
MSG_SUBJECT = 'Thank you to {{company_name}} for supporting PyGotham 2014!'

## {{params}} that may be in either body or subject
MSG_KEYS = {
    'sender_name': 'Celia'
}