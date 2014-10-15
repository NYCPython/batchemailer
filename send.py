import re
import smtplib

import config

FIELD_DELIMITER = "|"
PARAM_PATTERN = "{{([a-z_0-9]*)}}"
REPLACE_PATTERN = "{{%s}}"


def remove_junk(text):
    return re.sub(r"[\x80-\xff]", ' ', text).strip()


def get_recipients(names, emails):
    names_list = names.split(',')
    full_emails = ["%s <%s>" % (names_list[i], x) for i, x in enumerate(emails.split(','))]
    return ', '.join(full_emails)


def get_first_names(names):
    first_names = [x.split(" ")[0] for x in names.split(',')]
    return ', '.join(first_names)


def lookup_key(key, entry_values):
    if key in entry_values:
        return entry_values[key]
    elif key in config.MSG_KEYS:
        return config.MSG_KEYS[key]
    elif key == 'first_name':
        return get_first_names(entry_values['email_name'])


def replace_keys(phrase, entry_values):
    phrase_keys = re.findall(PARAM_PATTERN, phrase)
    for key in phrase_keys:
        param_value = lookup_key(key, entry_values)
        phrase = re.sub(REPLACE_PATTERN % key, param_value, phrase)
    return phrase

# ===============================================================
#   BEGIN SCRIPT
# ===============================================================

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(config.SMTP_EMAIL, config.SMTP_PWD)

with open('body.txt', 'r') as f:
    BODY_TEMPLATE = f.read()
with open('recipients.txt', 'r') as f:
    mailing_list = f.read().split('\n')

mailing_keys = [x.strip() for x in mailing_list[0].split(FIELD_DELIMITER)]

# a list of key:value dicts for each mailing_list entry
mailing_recipients = [{mailing_keys[i]:remove_junk(y)
                       for i, y in enumerate(x.split(FIELD_DELIMITER))}
                      for x in mailing_list[1:]]

for entry in mailing_recipients:
    if 'email' in entry:
        if config.PREVIEW_MODE:
            entry['email'] = ','.join([config.PREVIEW_EMAILS[i]
                                       for i, x in enumerate(entry['email'].split(','))])
        subject = replace_keys(config.MSG_SUBJECT, entry)
        body = replace_keys(BODY_TEMPLATE, entry)
        recipient = get_recipients(entry['email_name'], entry['email'])

        headers = ["From: " + config.MSG_FROM,
                   "Subject: " + subject,
                   "CC: " + config.MSG_CC,
                   "To: " + recipient,
                   "mime-version: 1.0",
                   "content-type: text/plain"]
        headers = "\r\n".join(headers)

        print headers
        print body[:70], "..."
        confirm = raw_input("Do you really want to send this to %s? " % entry['email'].split(','))
        if confirm == 'y':
            server.sendmail(config.MSG_FROM,
                            entry['email'].split(',') + [config.MSG_CC],
                            headers + "\r\n\r\n" + body)

server.quit()
