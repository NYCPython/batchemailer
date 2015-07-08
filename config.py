import sys

# setting this to true will set recipient emails to MSG_KEYS['preview_email']
PREVIEW_MODE = False

# if PREVIEW_MODE is True, the email receipient is replaced with PREVIEW_EMAILS
PREVIEW_EMAILS =['!!your email address!!']

# SMTP settings
SMTP_SERVER = 'smtp.gmail.com:587'
SMTP_EMAIL = '!!your email address!!'
SMTP_PWD = '!!your password!!'

# what's listed in the "From" field. Ideally should match what you entered
# for SMTP_EMAIL, otherwise you risk getting marked as 'spam'
MSG_FROM = 'My full name <your-email@your-company.com>'
MSG_CC = ['Your colleague <their-email@your-company.com>']

# these are any extra params that aren't in recipients.tsv, but that you want to use
# in either the body or subject
EXTRA_PARAM_KEYS = {
    'sender_name': '!!Your Name Goes Here!!'
}

# these are the param values from recipients.tsv that contains the 'to' and 'cc' values
HEADER_PARAM_EMAIL = 'email'    # this value is required
HEADER_PARAM_CC = 'cc'          # cc values are optional

# on the command line, specify the folder that contains your batch files
FOLDER_NAME = sys.argv[1]
FILENAME_BODY = FOLDER_NAME + '/body.txt'
FILENAME_SUBJECT = FOLDER_NAME + '/subject.txt'
FILENAME_RECIPIENTS_TSV = FOLDER_NAME + '/recipients.tsv'
