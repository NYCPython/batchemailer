batchemailer
============

Simple script to batch send text emails.

How to use
==========
Calling:

	unix% python send.py my-folder

will send to all emails specified in the my-folder/recipients.tsv, using
my-folder/body.txt and my-folder/subject.txt as your body and subject template.

In order to send, you'll need to confirm each one by typing 'y'.

How it works
============

The scripts looks for double-bracketed params ({{sender_name}}) in body.txt and subject.txt
and replace it with values found in either recipients.tsv or EXTRA_PARAM_KEYS (in config.py).

The script expects recipients.tsv to be a tab-delimited file:
	- It expects an 'email' column, which will be the email recipient.
	- 'email' can contain multiple emails, separated by commas.
	- if a 'cc' column is found, these emails get added to the CC field, along with any emails
	  specified in MSG_CC (config.py).

Step 1: configure config.py
===========================
Open config.py and set the following:

SMTP_SERVER - should be your smtp server
SMTP_EMAIL - replace with your email address
SMTP_PWD - replace with your email password

MSG_FROM - what will be displayed in the From field
MSG_CC - list of emails to be included in the CC field. Note that additional CC recipients can also
	be specified in FILENAME_RECIPIENTS_TSV.

EXTRA_PARAM_KEYS['sender_name'] - set to your name, if your body template contains {{sender_name}}

	== Optional ==
	There is a PREVIEW_MODE setting, which if set to True, will send your emails to those listed
	in PREVIEW_EMAILS, instead of your real recipients in FILENAME_RECIPIENTS_TSV

Step 2: add data to recipients.tsv
==================================
The script recipients.tsv to be a tab-delimited file. It expects an 'email' column, which will
be the email recipient. 'email' can contain multiple emails, separated by commas. Add any other
columns that you want to use as params in either the body or subject templates.

Step 3: tweak body.txt and subject.txt as needed
================================================
Denote any params you want to use with double-brackets: {{my-param}}
