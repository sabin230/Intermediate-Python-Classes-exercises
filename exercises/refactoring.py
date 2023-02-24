"""Refactoring exercises"""
from email.parser import Parser
try:
    # Some versions of Anaconda are missing IMAP4_SSL
    from imaplib import IMAP4_SSL
except ImportError:
    pass


class Weekday:
    """Class with attributes representing weekdays."""


class NextDate:
    """Answers questions about the next Monday/Tuesday/etc."""


def next_date():
    """Returns next Monday/Tuesday/etc."""


def days_until():
    """Returns days until next Monday/Tuesday/etc."""


def next_tuesday():
    """Returns date of next Tuesday."""


def days_to_tuesday():
    """Returns days until next Tuesday."""


class IMAPChecker:
    """Facilitate connection to IMAP server."""

# Refactor the below functions into IMAPChecker methods


def get_connection(host, username, password):
    """Initialize IMAP server and login"""
    server = IMAP4_SSL(host)
    server.login(username, password)
    server.select("inbox")
    return server


def close_connection(server):
    server.close()
    server.logout()


def get_message_uids(server):
    """Return unique identifiers for each message"""
    return server.uid("search", None, "ALL")[1][0].split()


def get_message(server, uid):
    """Get email message identified by given UID"""
    result, data = server.uid("fetch", uid, "(RFC822)")
    (_, message_text), _ = data
    message = Parser().parsestr(message_text)
    return message
