"""Tests for refactoring exercises"""
from contextlib import contextmanager
from datetime import date
from unittest.mock import call, patch, sentinel
import unittest

from refactoring import IMAPChecker, Weekday


class NextDateTests(unittest.TestCase):

    """Tests for NextDate."""

    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_date_for_changing_time(self):
        monday = NextDate(Weekday.MONDAY)
        tuesday = NextDate(Weekday.TUESDAY)
        wednesday = NextDate(Weekday.WEDNESDAY)
        thursday = NextDate(Weekday.THURSDAY)
        friday = NextDate(Weekday.FRIDAY)
        saturday = NextDate(Weekday.SATURDAY)
        sunday = NextDate(Weekday.SUNDAY)
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(monday.date(), date(2019, 9, 9))
        self.assertEqual(tuesday.date(), date(2019, 9, 3))
        self.assertEqual(wednesday.date(), date(2019, 9, 4))
        self.assertEqual(thursday.date(), date(2019, 9, 5))
        self.assertEqual(friday.date(), date(2019, 9, 6))
        self.assertEqual(saturday.date(), date(2019, 9, 7))
        self.assertEqual(sunday.date(), date(2019, 9, 8))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(monday.date(), date(2019, 9, 9))
        self.assertEqual(tuesday.date(), date(2019, 9, 10))
        self.assertEqual(wednesday.date(), date(2019, 9, 11))
        self.assertEqual(thursday.date(), date(2019, 9, 5))
        self.assertEqual(friday.date(), date(2019, 9, 6))
        self.assertEqual(saturday.date(), date(2019, 9, 7))
        self.assertEqual(sunday.date(), date(2019, 9, 8))

    def test_days_until(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(NextDate(Weekday.MONDAY).days_until(), 6)
        self.assertEqual(NextDate(Weekday.TUESDAY).days_until(), 0)
        self.assertEqual(NextDate(Weekday.WEDNESDAY).days_until(), 1)


class NextDateFunctionTests(unittest.TestCase):

    """Tests for next_date."""

    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_next_date(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(next_date(Weekday.MONDAY), date(2019, 9, 9))
        self.assertEqual(next_date(Weekday.TUESDAY), date(2019, 9, 3))
        self.assertEqual(next_date(Weekday.WEDNESDAY), date(2019, 9, 4))
        self.assertEqual(next_date(Weekday.THURSDAY), date(2019, 9, 5))
        self.assertEqual(next_date(Weekday.FRIDAY), date(2019, 9, 6))
        self.assertEqual(next_date(Weekday.SATURDAY), date(2019, 9, 7))
        self.assertEqual(next_date(Weekday.SUNDAY), date(2019, 9, 8))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(next_date(Weekday.MONDAY), date(2019, 9, 9))
        self.assertEqual(next_date(Weekday.TUESDAY), date(2019, 9, 10))
        self.assertEqual(next_date(Weekday.WEDNESDAY), date(2019, 9, 11))
        self.assertEqual(next_date(Weekday.THURSDAY), date(2019, 9, 5))
        self.assertEqual(next_date(Weekday.FRIDAY), date(2019, 9, 6))
        self.assertEqual(next_date(Weekday.SATURDAY), date(2019, 9, 7))
        self.assertEqual(next_date(Weekday.SUNDAY), date(2019, 9, 8))


class DaysUntilFunctionTests(unittest.TestCase):

    """Tests for days_until."""

    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_days_until(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(days_until(Weekday.MONDAY), 6)
        self.assertEqual(days_until(Weekday.TUESDAY), 0)
        self.assertEqual(days_until(Weekday.WEDNESDAY), 1)
        self.assertEqual(days_until(Weekday.THURSDAY), 2)
        self.assertEqual(days_until(Weekday.FRIDAY), 3)
        self.assertEqual(days_until(Weekday.SATURDAY), 4)
        self.assertEqual(days_until(Weekday.SUNDAY), 5)
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(days_until(Weekday.MONDAY), 4)
        self.assertEqual(days_until(Weekday.TUESDAY), 5)
        self.assertEqual(days_until(Weekday.WEDNESDAY), 6)
        self.assertEqual(days_until(Weekday.THURSDAY), 0)
        self.assertEqual(days_until(Weekday.FRIDAY), 1)
        self.assertEqual(days_until(Weekday.SATURDAY), 2)
        self.assertEqual(days_until(Weekday.SUNDAY), 3)


class DaysToTuesdayTests(unittest.TestCase):

    """Tests for days_to_tuesday."""

    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_days_to_tuesday(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(days_to_tuesday(), 0)
        self.assertEqual(days_to_tuesday(after_today=True), 7)
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(days_to_tuesday(), 5)
        self.assertEqual(days_to_tuesday(after_today=True), 5)


class NextTuesdayTests(unittest.TestCase):

    """Tests for next_tuesday."""

    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_next_tuesday(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(next_tuesday(), date(2019, 9, 3))
        self.assertEqual(next_tuesday(after_today=True), date(2019, 9, 10))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(next_tuesday(), date(2019, 9, 10))
        self.assertEqual(next_tuesday(after_today=True), date(2019, 9, 10))


def NextDate(*args, **kwargs):
    """Call a fresh import of the nextdate.NextDate class."""
    from importlib import reload
    import refactoring
    reload(refactoring)
    return refactoring.NextDate(*args, **kwargs)


def next_date(*args, **kwargs):
    """Call a fresh import of the nextdate.next_date function."""
    from importlib import reload
    import refactoring
    reload(refactoring)
    return refactoring.next_date(*args, **kwargs)


def days_until(*args, **kwargs):
    """Call a fresh import of the nextdate.days_until function."""
    from importlib import reload
    import refactoring
    reload(refactoring)
    return refactoring.days_until(*args, **kwargs)


def days_to_tuesday(*args, **kwargs):
    """Call a fresh import of the nextdate.days_to_tuesday function."""
    from importlib import reload
    import refactoring
    reload(refactoring)
    return refactoring.days_to_tuesday(*args, **kwargs)


def next_tuesday(*args, **kwargs):
    """Call a fresh import of the nextdate.next_tuesday function."""
    from importlib import reload
    import refactoring
    reload(refactoring)
    return refactoring.next_tuesday(*args, **kwargs)


@contextmanager
def patch_date(year, month, day, hour=0, minute=0):
    """Monkey patch the current time to be the given time."""
    import datetime
    from unittest.mock import patch

    date_args = year, month, day
    time_args = hour, minute

    class FakeDate(datetime.date):
        """A datetime.date class with mocked today method."""

        @classmethod
        def today(cls):
            return cls(*date_args)

    class FakeDateTime(datetime.datetime):
        """A datetime.datetime class with mocked today, now methods."""

        @classmethod
        def today(cls):
            return cls(*date_args, *time_args)

        @classmethod
        def now(cls):
            return cls.today()

    def set_date(year, month, day, *rest):
        nonlocal date_args, time_args
        date_args = year, month, day
        time_args = rest

    with patch('datetime.datetime', FakeDateTime):
        with patch('datetime.date', FakeDate):
            yield set_date


class IMAPCheckerTests(unittest.TestCase):

    """Tests for IMAPChecker."""

    def test_initialization(self):
        host = 'example.com'
        with patch('classes.IMAP4_SSL', autospec=True) as imap_mock:
            IMAPChecker(host)
        self.assertEqual(imap_mock.mock_calls, [call(host)])

    def test_authentication(self):
        host = 'example.com'
        username = 'user@example.com'
        password = 'password'
        with patch('classes.IMAP4_SSL', autospec=True) as imap_mock:
            checker = IMAPChecker(host)
            checker.authenticate(username, password)
        self.assertEqual(imap_mock.mock_calls, [
            call(host),
            call().login(username, password),
            call().select('inbox'),
        ])

    def test_get_message_uids(self):
        host = 'example.com'
        with patch('classes.IMAP4_SSL', autospec=True) as imap_mock:
            checker = IMAPChecker(host)
            uids = checker.get_message_uids()
        imap_mock.assert_has_calls([call().uid('search', None, 'ALL')])
        self.assertEqual(
            uids,
            (imap_mock.return_value.uid.return_value.__getitem__.return_value
             .__getitem__.return_value.split.return_value),
        )

    def test_get_message(self):
        host = 'example.com'
        uid = 'uid1'
        with patch('classes.IMAP4_SSL', autospec=True) as imap_mock:
            with patch('classes.Parser', autospec=True) as parser_mock:
                imap_mock.return_value.uid.return_value = [
                    '',
                    (('', sentinel.MessageText), ''),
                ]
                parser_mock.return_value.parsestr.return_value = sentinel.M
                checker = IMAPChecker(host)
                message = checker.get_message(uid)
        self.assertEqual(imap_mock.mock_calls, [
            call(host),
            call().uid('fetch', uid, '(RFC822)')
        ])
        self.assertEqual(parser_mock.mock_calls, [
            call(),
            call().parsestr(sentinel.MessageText),
        ])
        self.assertEqual(message, sentinel.M)


if __name__ == "__main__":
    from helpers import error_message
    error_message()
