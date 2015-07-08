import config
import re
import smtplib


FIELD_DELIMITER = "\t"
PARAM_PATTERN = "{{([a-z_0-9]*)}}"
REPLACE_PATTERN = "{{%s}}"


def remove_junk(text):
    return re.sub(r"[\x80-\xff]", ' ', text).strip()


def extract_just_emails(emails):
    just_emails = []
    for full_email in emails:
        just_email = re.compile("<(.*)>").findall(full_email)
        if just_email:
            just_emails.append(just_email[0])
        elif '@' in full_email:
            just_emails.append(full_email)
    return just_emails

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
    elif key in config.EXTRA_PARAM_KEYS:
        return config.EXTRA_PARAM_KEYS[key]
    elif key == 'first_name':
        return get_first_names(entry_values['email_names'])


def replace_keys(phrase, entry_values):
    phrase_keys = re.findall(PARAM_PATTERN, phrase)
    for key in phrase_keys:
        param_value = lookup_key(key, entry_values)
        phrase = re.sub(REPLACE_PATTERN % key, param_value, phrase)
    return phrase

# ===============================================================
#   BEGIN SCRIPT
# ===============================================================

server = smtplib.SMTP(config.SMTP_SERVER)
server.ehlo()
server.starttls()
server.login(config.SMTP_EMAIL, config.SMTP_PWD)

with open(config.FILENAME_BODY, 'r') as f:
    BODY_TEMPLATE = f.read()
with open(config.FILENAME_SUBJECT, 'r') as f:
    SUBJECT_TEMPLATE = f.read().split('\n')[0]
with open(config.FILENAME_RECIPIENTS_TSV, 'r') as f:
    mailing_list = f.read().split('\n')

mailing_keys = [x.strip() for x in mailing_list[0].split(FIELD_DELIMITER)]

# a list of key:value dicts for each mailing_list entry
mailing_recipients = [{mailing_keys[i]:remove_junk(y)
                       for i, y in enumerate(x.split(FIELD_DELIMITER))}
                      for x in mailing_list[1:]]

msg = "PREVIEW_MODE is " + str(config.PREVIEW_MODE) + "."
if not config.PREVIEW_MODE:
    msg += " **** THIS IS THE REAL THING!!! **** "
confirm = raw_input(msg + " Enter y to continue: ")
if confirm != 'y':
    exit(0)

for entry in mailing_recipients:
    cc_emails = config.MSG_CC[:] or []
    if config.HEADER_PARAM_EMAIL in entry:
        if config.PREVIEW_MODE:
            entry[config.HEADER_PARAM_EMAIL] = ','.join(config.PREVIEW_EMAILS)
            entry.pop(config.HEADER_PARAM_CC, None)
        subject = replace_keys(SUBJECT_TEMPLATE, entry)
        body = replace_keys(BODY_TEMPLATE, entry)
        if config.HEADER_PARAM_CC in entry:
            cc_emails.append(entry[config.HEADER_PARAM_CC])

        headers = ["From: " + config.MSG_FROM,
                   "To: " + entry[config.HEADER_PARAM_EMAIL],
                   "Subject: " + subject,
                   "mime-version: 1.0",
                   "content-type: text/plain"]

        if cc_emails:
            headers.append("CC: " + ', '.join(cc_emails))

        headers = "\r\n".join(headers)

        print "============================================="
        print headers
        print body[:70], "..."
        print "============================================="
        confirm = raw_input("Do you really want to send this to %r? " % entry[config.HEADER_PARAM_EMAIL])
        if confirm == 'y':
            #collect all emails in To, From, and CC fields
            send_to_emails = entry[config.HEADER_PARAM_EMAIL] + ',' + config.MSG_FROM + ',' \
                + ','.join(cc_emails)
            send_to_emails = extract_just_emails(send_to_emails.split(','))
            server.sendmail(config.MSG_FROM,
                            send_to_emails,
                            headers + "\r\n\r\n" + body)

server.quit()
