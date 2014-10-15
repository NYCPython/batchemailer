batchemailer
============

Simple script to send batch emails

============================ SETUP ============================

1) config.py should have the following set:

	PREVIEW_MODE 	- if set to True, then script will replace the emails listed in
					  recipients.tab with the emails listed in PREVIEW_EMAILS
	PREVIEW_EMAILS	- dummy emails used to send emails in preview (test) mode

	SMTP_EMAIL	 	- the email you'll use to authenticate to the SMTP server
	SMTP_PWD	 	- your email password
	MSG_FROM	 	- for the email that gets sent, this will be the "To"
	MSG_CC			- for the email that gets sent, this will be the "Cc". Note that a
					  cc is currently required.

	MSG_SUBJECT 	- Subject for you email. This can use {{params}} (see note below)
	MSG_KEYS		- contains values for {{params}} [not specified via recipients.tab]

2) recipients.tab 	- a pipe delimited file mailing list values.
					
					** Required Fields **

					The following entries are required:
						email 		- comma-delimited list of emails to send to
						email_name 	- comma-delmited list of Full Names corresponding 
									  to the email list above

					Any other fields that you add can be used to replace any
					{{params}} in the email body or subject

3) body.txt - email body (in text format)

4) {{params}}	- params (denoted like {{this}}) can be placed anywhere in
				  the config.MSG_SUBJECT or body.txt.

				- if a {{param}} is found, the script looks to see if this is
				  defined in:
				  1) recipients.tab
				  2) config.MSG_KEYS

				** Special Keys **

				{{first_name}} - will take the first name from email_name
								 specified in recipients.tab. If there are 
								 multiple emails, the first_name will be a 
								 comma-delimited list of those first names

============================ EXECUTION ============================

1) set PREVIEW_MODE (as well as the other variables) in config.py
2) to run: python send.py
	- in order to send, you'll need to confirm each one by typing 'y'
