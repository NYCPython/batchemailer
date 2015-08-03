import argparse
import configparser
import csv
import os
import smtplib


def main(dry_run=True):
    if not dry_run:
        SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '').strip()
        if not SMTP_PASSWORD:
            print('Must set SMTP_PASSWORD environment variable')

    # Parse and select config
    config = configparser.ConfigParser()

    cwd = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(cwd, 'batch-emailer.ini')
    if not os.path.exists(config_file):
        raise RuntimeError('Please create and populate a batch-emailer.ini file')

    print('Reading configs from {}'.format(config_file))
    config.read(config_file)

    if not config.sections():
        msg = 'Please create a least one customized section in the batch-emailer.ini file'
        raise ValueError(msg)

    print('Emails available for sending:')
    for i, sec in enumerate(config.sections()):
        print('{}: {}'.format(i, sec))
    section_index = input('Enter the number of the email you would like to send: ')
    section_index = int(section_index.strip())
    section = config.sections()[section_index]

    # Load constants from config
    SMTP_SERVER = config[section].get('smtp_server')
    SMTP_EMAIL = config[section].get('smtp_email')

    REPLY_ADDRESS = config[section].get('reply_address')
    CC_ADDRESSES = config[section].get('cc_addresses')
    if CC_ADDRESSES:
        CC_ADDRESSES = CC_ADDRESSES.strip().split(',')
    SUBJECT_TEMPLATE = config[section].get('subject')
    BODY_FILENAME = config[section].get('body_filename')
    RECIPIENTS_FILENAME = config[section].get('recipients_filename')

    # Load templates
    with open(BODY_FILENAME) as f:
        BODY_TEMPLATE = f.read()

    with open(RECIPIENTS_FILENAME) as f:
        reader = csv.DictReader(f)
        RECIPIENT_DICTS = [d for d in reader]

    if not dry_run:
        # Start server
        server = smtplib.SMTP(SMTP_SERVER)
        server.ehlo()
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

    # Build and send emails
    for count, recipient_dict in enumerate(RECIPIENT_DICTS, start=1):
        subject_line = SUBJECT_TEMPLATE.format(**recipient_dict)
        headers = ["From: {}".format(REPLY_ADDRESS),
                   "To: {email_address}".format(**recipient_dict),
                   "Subject: {}".format(subject_line),
                   "mime-version: 1.0",
                   "content-type: text/plain"]
        if CC_ADDRESSES:
            headers.append("CC: " + ', '.join(CC_ADDRESSES))
        headers = "\r\n".join(headers)
        body = BODY_TEMPLATE.format(**recipient_dict)
        msg = headers + "\r\n\r\n" + body

        if dry_run:
            print(msg, '\n\n')
        else:
            print('Sending email #{}: "{}" to <{email_address}>'
                  ''.format(count, subject_line, **recipient_dict))
            confirm = input('Confirm [y/n]: ')
            confirm = confirm.strip()
            if 'y' not in confirm:
                continue
            destination_emails = [recipient_dict['email_address']] + CC_ADDRESSES
            server.sendmail(REPLY_ADDRESS, destination_emails, msg.encode('utf-8'))
            print('...sent.')

    if not dry_run:
        server.quit()
    print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to send emails.')
    parser.add_argument('--nodry',
                        dest='dry',
                        action='store_false',
                        default=True,
                        help='Send emails. Do not run in dry test mode')
    args = parser.parse_args()
    main(dry_run=args.dry)

