"""
Send a message by email to one or more recipients (by SMTP or sendmail).
"""

# Copyright (c) 2009-2024, UChicago Argonne, LLC.  See LICENSE file.

import os
import sys

SMTP_TIMEOUT = 10


class MailerError(Exception):
    pass


def sendMail_sendmail(
    subject, message, recipients, sendmail_cfg, sender=None, logger=None
):
    """
    Send an email message using sendmail (linux only).

    :param str subject: short text for email subject
    :param str message: full text of email body
    :param [str] recipients: list of email addresses to receive the message
    :param dict sendmail_cfg: such as returned from :mod:`PvMail.ini_config.Config.get`

        :user: required - (*str*) username to for sendmail (or similar) program

    :param str sender: "From" address, if *None* use *smtp_cfg['user']* value
    :param obj logger: optional message logging method

    EXAMPLE::

        >>> import PvMail.ini_config
        >>> sendmail_cfg = PvMail.ini_config.Config().get()
        >>> recipients = ['joe@gmail.com', 'sally@example.org']
        >>> subject = 'sendmail test message'
        >>> message = PvMail.ini_config.__doc__
        >>> sendMail_sendmail(subject, message, recipients, sendmail_cfg)

    """

    if sys.platform not in ("linux2"):
        raise MailerError(f"Cannot use this method on {sys.platform=!r}")

    sender = sender or sendmail_cfg["user"]
    if isinstance(recipients, str):
        recipients = [
            recipients,
        ]

    def _sendmail_handler(email_program, from_addr, recipients, subject, message):
        to_addr = str(" ".join(recipients))
        mail_command = "%s -F %s -t %s" % (email_program, from_addr, to_addr)
        mail_message = [
            mail_command,
        ]
        for who in recipients:
            mail_message.append("To: " + who)
        mail_message.append("Subject: " + subject)
        mail_message.append(message)
        cmd = """cat << +++ | %s\n+++""" % "\n".join(mail_message)
        return mail_command, cmd

    def _mail_handler(email_program, from_addr, recipients, subject, message):
        # to_addr = str(" ".join(recipients))
        # mail_command = "%s %s" % (email_program, to_addr)
        # mail_message = "%s\n%s" % (subject, message)
        # # TODO: needs to do THIS
        # """
        # cat /tmp/message.txt | mail jemian@anl.gov
        # """
        # # cmd = '''echo %s | %s''' % (mail_message, mail_command)
        # # return mail_command, cmd    # lgtm [py/unreachable-statement]
        raise MailerError("code needs improvement here")

    cmd = None
    for email_program, handler in (
        ("/usr/lib/sendmail", _sendmail_handler),
        ("/usr/bin/sendmail", _sendmail_handler),
        ("/usr/bin/mail", _mail_handler),
    ):
        if os.path.exists(email_program):
            results = handler(email_program, sender, recipients, subject, message)
            mail_command, cmd = results
            break

    if cmd is None:
        raise MailerError("Cannot find mail transport agent for sendmail.")

    if logger is not None:
        logger("sending email to: " + str(recipients))
        logger("email program: " + email_program)
        logger("mail command: " + mail_command)
        logger("email From: " + sender)

    try:
        if logger is not None:
            logger("email command:\n" + cmd)
        if os.path.exists(email_program):
            os.popen(cmd)  # send the message
        else:
            if logger is not None:
                logger("email program (%s) does not exist" % email_program)
    except Exception as reason:
        # err_msg = traceback.format_exc()
        final_msg = f"{cmd=!r}\ntraceback: {reason}"
        logger(final_msg)
        raise MailerError(final_msg)

    if logger is not None:
        logger("sendmail sent")


def sendMail_SMTP(subject, message, recipients, smtp_cfg, sender=None, logger=None):
    """
    send email message through SMTP server

    :param str subject: short text for email subject
    :param str message: full text of email body
    :param [str] recipients: list of email addresses to receive the message
    :param dict smtp_cfg: such as returned from :mod:`PvMail.ini_config.Config.get`

        :server:               required - (*str*) SMTP server
        :user:                 required - (*str*) username to login to SMTP server
        :port:                 optional - (*str*) SMTP port
        :password:             optional - (*str*) password for username
        :connection_security:  optional - (*str*) **STARTTLS** (the only choice, if specified)

    :param str sender: "From" address, if *None* use *smtp_cfg['user']* value

    EXAMPLE::

        >>> import PvMail.ini_config
        >>> smtp_cfg = PvMail.ini_config.Config().get()
        >>> recipients = ['joe@gmail.com', 'sally@example.org']
        >>> subject = 'SMTP test message'
        >>> message = PvMail.ini_config.__doc__
        >>> sendMail_SMTP(subject, message, recipients, smtp_cfg)

    """
    import email
    import smtplib

    host = smtp_cfg.get("server", None)
    if host is None:
        raise MailerError("must define an SMTP host to be used")
    port = smtp_cfg.get("port", None)
    username = smtp_cfg.get("user", None)
    if username is None:
        raise MailerError("must define a username for the SMTP server")
    if sender is None:
        sender = username
    password = smtp_cfg.get("password", None)
    connection_security = smtp_cfg.get("connection_security", None)
    if connection_security not in (None, "STARTTLS"):
        msg = "connection_security must be: STARTTLS or not defined, found: "
        raise MailerError(msg + connection_security)

    msg = email.message.Message()
    if isinstance(recipients, str):
        msg["To"] = recipients
    else:
        for who in recipients:
            msg["To"] = who
    msg["From"] = sender
    msg["Subject"] = subject
    msg.set_payload(message)

    if logger is not None:
        logger("sending email to: " + str(recipients))
        logger("SMTP server: " + host)
        logger("SMTP user: " + username)
        logger("email From: " + sender)

    smtpserver = smtplib.SMTP(timeout=SMTP_TIMEOUT)
    # smtpserver.set_debuglevel(1)
    if port is None:
        smtpserver.connect(host)
    else:
        smtpserver.connect(host, int(port))
    if logger is not None:
        logger("SMTP connected")

    smtpserver.ehlo()
    if smtp_cfg.get("connection_security", None) == "STARTTLS":
        smtpserver.starttls()
        smtpserver.ehlo()
        if logger is not None:
            logger("SMTP STARTTLS")

    if password is not None:
        smtpserver.login(username, password)
        if logger is not None:
            logger("SMTP authenticated")

    smtpserver.sendmail(username, recipients, str(msg))
    smtpserver.close()
    if logger is not None:
        logger("SMTP complete")


def send_message(subject, message, recipients, config):
    """
    send an email message

    :param str subject: short text for email subject
    :param str message: full text of email body
    :param [str] recipients: list of email addresses to receive the message
    :param dict config: such as returned from :mod:`PvMail.ini_config.Config`
    """
    email_agent_dict = dict(sendmail=sendMail_sendmail, SMTP=sendMail_SMTP)
    agent = email_agent_dict[config.mail_transfer_agent]
    agent(subject, message, recipients, config.get())


def main():
    """
    User on-demand test of the mailer module and configuration.
    """
    import argparse

    from . import DOCS_URL
    from . import __version__
    from . import ini_config

    doc = f"Test the email sender from PvMail {__version__}"
    parser = argparse.ArgumentParser(description=doc)
    msg = "email address(es), whitespace-separated if more than one"
    parser.add_argument("recipient", action="store", nargs="+", help=msg, default="")
    results = parser.parse_args()
    print(doc)

    cfg = ini_config.Config()
    print("Using configuration from: " + cfg.ini_file)
    print("Using user name: " + cfg.get()["user"])

    recipients = results.recipient
    print("Sending email(s) to: " + str(" ".join(recipients)))
    print("mail transfer agent: " + cfg.mail_transfer_agent)

    subject = "PvMail mailer test message: " + cfg.mail_transfer_agent
    message = f"{doc}\nFor more help, see: {DOCS_URL}"

    send_message(subject, message, recipients, cfg)
