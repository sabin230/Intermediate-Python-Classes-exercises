"""Tests for classes exercises"""
from contextlib import contextmanager
from datetime import date, timedelta
from itertools import cycle, permutations
from locale import setlocale, LC_TIME
import random
from string import ascii_uppercase
from timeit import default_timer
import unittest


from classes import (
    BankAccount,
    SuperMap,
    MinHeap,
    Flavor,
    Size,
    IceCream,
    Month,
    MonthDelta,
    Row,
)


random.seed(0)

names = permutations(ascii_uppercase, 6)
colors = cycle([
    'purple', 'green', 'pink', 'blue', 'black', 'orange', 'yellow',
])


class BankAccountTests(unittest.TestCase):

    """Tests for BankAccount."""

    def test_new_account_balance_default(self):
        account = BankAccount()
        self.assertEqual(account.balance, 0)

    def test_opening_balance(self):
        account = BankAccount(balance=100)
        self.assertEqual(account.balance, 100)

    def test_deposit(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.balance, 100)

    def test_withdraw(self):
        account = BankAccount(balance=100)
        account.withdraw(40)
        self.assertEqual(account.balance, 60)

    def test_repr(self):
        account = BankAccount()
        self.assertEqual(repr(account), 'BankAccount(balance=0)')
        account.deposit(200)
        self.assertEqual(repr(account), 'BankAccount(balance=200)')

    def test_transfer(self):
        mary_account = BankAccount(balance=100)
        dana_account = BankAccount(balance=0)
        mary_account.transfer(dana_account, 20)
        self.assertEqual(mary_account.balance, 80)
        self.assertEqual(dana_account.balance, 20)

    @unittest.skip("BankAccount Transactions")
    def test_transactions_open(self):
        expected_transactions = [
            ('OPEN', 100, 100),
        ]
        account = BankAccount(balance=100)
        self.assertEqual(account.transactions, expected_transactions)

    @unittest.skip("BankAccount Transactions")
    def test_transactions_deposit(self):
        expected_transactions = [
            ('OPEN', 0, 0),
            ('DEPOSIT', 100, 100),
        ]
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.transactions, expected_transactions)

    @unittest.skip("BankAccount Transactions")
    def test_transactions_withdraw(self):
        expected_transactions = [
            ('OPEN', 100, 100),
            ('WITHDRAWAL', -40, 60),
        ]
        account = BankAccount(balance=100)
        account.withdraw(40)
        self.assertEqual(account.transactions, expected_transactions)

    @unittest.skip("BankAccount Transactions")
    def test_transactions_scenario(self):
        expected_transactions = [
            ('OPEN', 0, 0),
            ('DEPOSIT', 100, 100),
            ('WITHDRAWAL', -40, 60),
            ('DEPOSIT', 95, 155),
        ]
        account = BankAccount()
        account.deposit(100)
        account.withdraw(40)
        account.deposit(95)
        self.assertEqual(account.transactions, expected_transactions)

    @unittest.skip("Truthy BankAccount")
    def test_truthy_accounts(self):
        account = BankAccount()
        self.assertIs(bool(account), False)
        account.deposit(100)
        self.assertIs(bool(account), True)

    @unittest.skip("Comparable BankAccount")
    def test_account_comparisons(self):
        account1 = BankAccount()
        account2 = BankAccount()
        self.assertTrue(account1 == account2)
        self.assertTrue(account1 >= account2)
        self.assertTrue(account1 <= account2)
        account1.deposit(100)
        account2.deposit(10)
        self.assertTrue(account1 != account2)
        self.assertTrue(account2 < account1)
        self.assertTrue(account1 > account2)
        self.assertTrue(account2 < account1)
        self.assertTrue(account1 >= account2)
        self.assertTrue(account2 <= account1)

    @unittest.skip("Read-Only BankAccount")
    def test_balance_cannot_be_written(self):
        account1 = BankAccount()
        account2 = BankAccount(100)
        self.assertEqual(account1.balance, 0)
        with self.assertRaises(Exception):
            account1.balance = 50
        self.assertEqual(account1.balance, 0)
        self.assertEqual(account2.balance, 100)
        with self.assertRaises(Exception):
            account2.balance = 50
        self.assertEqual(account2.balance, 100)
        account1.deposit(100)
        account2.deposit(10)
        self.assertEqual(account1.balance, 100)
        self.assertEqual(account2.balance, 110)
        with self.assertRaises(Exception):
            account2.balance = 500
        self.assertEqual(account2.balance, 110)
        account2.transfer(account1, 50)
        self.assertEqual(account1.balance, 150)
        self.assertEqual(account2.balance, 60)

    @unittest.skip("Hidden Balance")
    def test_dir_does_not_show_balance_attribute(self):
        account = BankAccount()
        account.deposit(100)
        self.assertNotIn('_balance', dir(account))
        allowed = {
            'accounts',
            'balance',
            'deposit',
            'withdraw',
            'transfer',
            'transactions',
            'name',
        } | set(dir(type('', (), {})()))
        self.assertEqual(set(dir(account)) - allowed, set())


class Item:

    __slots__ = ('id', 'name', 'color', 'version')

    def __init__(self, id, name, color, version):
        self.id = id
        self.name = name
        self.color = color
        self.version = version

    @property
    def _values(self):
        return (self.id, self.name, self.color, self.version)

    def __hash__(self):
        return hash(self._values)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self._values == other._values

    def __repr__(self):
        return f"Item{self._values!r}"


class SuperMapTests(unittest.TestCase):

    """Tests for SuperMap."""

    def test_where_method(self):
        few_items = [
            Item(i, "".join(next(names)), next(colors), random.randint(0, 5))
            for i in range(10_000, 10_100)
        ]
        mapping = SuperMap(few_items, indexes=('id', 'color'))
        matches = mapping.where('color', "pink")
        self.assertEqual(set(matches), {
            item
            for item in few_items
            if item.color == "pink"
        })
        matches = mapping.where('id', 4)
        self.assertEqual(len(matches), 0)
        matches = mapping.where('id', 10_050)
        self.assertEqual(len(matches), 1)

    def test_time_efficient_lookups(self):
        many_items = [
            Item(i, "".join(next(names)), next(colors), random.randint(0, 5))
            for i in range(2_000)
        ]
        mapping = SuperMap(many_items, indexes=('id', 'color'))
        with Timer() as manual_lookup:
            items1 = {
                item
                for item in many_items
                if item.color == "pink"
            }
        with Timer() as lookup_from_map:
            items2 = mapping.where('color', "pink")
        self.assertEqual(len(items1), len(items2))
        self.assertEqual(set(items1), items2)
        self.assertGreater(
            manual_lookup.elapsed,
            lookup_from_map.elapsed * 5,
        )


class MinHeapTests(unittest.TestCase):

    """Tests for MinHeap."""

    @classmethod
    def setUpClass(cls):
        cls.big_numbers = [
            3748, 7250, 140, 7669, 5711, 2284, 3322, 6435, 8138, 6920, 9634, 7511,
            5295, 5456, 7458, 5618, 102, 7747, 4638, 46, 4532, 1483, 944, 3542, 6641,
            9091, 693, 836, 3099, 3385, 7798, 758, 8407, 4756, 8801, 3936, 5301, 5744,
            6454, 1156, 7686, 5664, 2568, 6414, 3469, 2867, 8875, 6097, 2546, 4658,
            7027, 9437, 755, 8536, 8186, 9539, 661, 6706, 265, 2254, 2402, 3355, 9141,
            5091, 1727, 6739, 4599, 5599, 9007, 2925, 2894, 5333, 9586, 7409, 916,
            6420, 8493, 9531, 5083, 5350, 3346, 1378, 6260, 3143, 7216, 684, 170, 6721,
            418, 7013, 7729, 7484, 5355, 4850, 8073, 1389, 2084, 1856, 9740, 2747,
        ]

    def test_create_heap(self):
        MinHeap([322, 76, 4, 7, 2, 123, 47, 1, 18, 3, 29, 199, 11])
        MinHeap(self.big_numbers)

    def test_peek_at_smallest(self):
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        h = MinHeap(numbers)
        self.assertEqual(h.peek(), 1)
        i = MinHeap(self.big_numbers)
        self.assertEqual(i.peek(), 46)

    def test_pop_from_heap(self):
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        h = MinHeap(numbers)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(h.pop(), 4)
        self.assertEqual(h.pop(), 7)
        self.assertEqual(h.pop(), 11)
        i = MinHeap(self.big_numbers)
        self.assertEqual(i.pop(), 46)

    def test_push_onto_heap(self):
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        i = MinHeap(self.big_numbers)
        i.push(17)
        self.assertEqual(i.peek(), 17)
        i.push(24)
        self.assertEqual(i.pop(), 17)
        self.assertEqual(i.pop(), 24)
        self.assertEqual(i.pop(), 46)
        h = MinHeap(numbers)
        h.push(6)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(h.pop(), 4)
        self.assertEqual(h.pop(), 6)

    def test_faster_than_sorting(self):
        many_big_numbers = [random.randint(100, 1000) for n in range(10000)]
        with Timer() as sort_timer:
            sorted(many_big_numbers)
        heap = MinHeap(many_big_numbers)
        with Timer() as min_heap_timer:
            heap.push(150)
            heap.push(950)
            heap.push(400)
            heap.push(760)
            heap.push(280)
            heap.push(870)
            heap.push(330)
            heap.push(1000)
            heap.push(50)
            heap.push(500)
            items = [heap.pop() for _ in range(10)]
        self.assertEqual(len(items), 10)
        self.assertLess(min_heap_timer.elapsed, sort_timer.elapsed)


class FlavorTests(unittest.TestCase):

    """Tests for Flavor."""

    def test_name_attribute(self):
        flavor = Flavor("vanilla")
        self.assertEqual(flavor.name, "vanilla")

    def test_specifying_ingredients(self):
        flavor = Flavor("vanilla", ingredients=["milk", "sugar", "vanilla"])
        self.assertEqual(flavor.ingredients, ["milk", "sugar", "vanilla"])
        flavor = Flavor("chocolate",
                        ingredients=["milk", "sugar", "vanilla", "chocolate"])
        self.assertEqual(
            flavor.ingredients,
            ["milk", "sugar", "vanilla", "chocolate"],
        )

    def test_modifying_ingredients(self):
        original_ingredients = ["milk", "sugar", "vanilla"]
        flavor = Flavor("vanilla", ingredients=original_ingredients)
        flavor.ingredients.append("red bean")
        self.assertEqual(original_ingredients, ["milk", "sugar", "vanilla"])

    def test_has_dairy_attribute(self):
        flavor = Flavor("vanilla")
        self.assertIs(flavor.has_dairy, True)
        flavor = Flavor("vanilla", has_dairy=True)
        self.assertIs(flavor.has_dairy, True)
        flavor = Flavor("vanilla", has_dairy=False)
        self.assertIs(flavor.has_dairy, False)

    def test_string_representation(self):
        flavor = Flavor("chocolate", has_dairy=False)
        self.assertEqual(repr(flavor), "Flavor(name='chocolate', ingredients=[], has_dairy=False)")
        flavor = Flavor("vanilla", ingredients=["milk", "sugar", "vanilla"])
        self.assertEqual(
            repr(flavor),
            "Flavor(name='vanilla', ingredients=['milk', 'sugar', 'vanilla'], has_dairy=True)",
        )


class SizeTests(unittest.TestCase):

    """Tests for Size."""

    def test_initializer(self):
        size = Size(quantity=1, unit="gram", price="5.00")
        self.assertEqual(size.quantity, 1)
        self.assertEqual(size.unit, "gram")
        self.assertEqual(size.price, "5.00")

    def test_human_string_representation(self):
        size = Size(quantity=1, unit="gram", price="5.00")
        self.assertEqual(str(size), "1 gram")
        size = Size(quantity=1, unit="scoop", price="5.00")
        self.assertEqual(str(size), "1 scoop")

    def test_pluralization(self):
        size = Size(quantity=3, unit="pint", price="9.00")
        self.assertEqual(str(size), "3 pints")
        size = Size(quantity=3, unit="scoop", price="4.00")
        self.assertEqual(str(size), "3 scoops")

    def test_machine_string_representation(self):
        size = Size(quantity=1, unit="cup", price="5")
        self.assertEqual(repr(size), "Size(quantity=1, unit='cup', price='5')")


class IceCreamTests(unittest.TestCase):

    """Tests for IceCream."""

    def test_initializer(self):
        one_quart = Size(quantity=1, unit="quart", price="$9")
        vanilla = Flavor("vanilla")
        quart_of_vanilla = IceCream(flavor=vanilla, size=one_quart)
        self.assertEqual(quart_of_vanilla.size, one_quart)
        self.assertEqual(quart_of_vanilla.flavor, vanilla)

    def test_string_representation(self):
        one_quart = Size(quantity=1, unit="quart", price="$9")
        vanilla = Flavor("vanilla")
        quart_of_vanilla = IceCream(flavor=vanilla, size=one_quart)
        self.assertEqual(str(quart_of_vanilla), '1 quart of vanilla')
        self.assertEqual(str(quart_of_vanilla), '1 quart of vanilla')
        two_scoops = IceCream(
            flavor=Flavor("chocolate"),
            size=Size(quantity=2, unit="scoop", price="$3"),
        )
        self.assertEqual(str(two_scoops), '2 scoops of chocolate')


class MonthTests(unittest.TestCase):

    """Tests for Month."""

    def test_initialization(self):
        month = Month(2019, 1)
        self.assertEqual(month.year, 2019)
        self.assertEqual(month.month, 1)

    def test_machine_readable_representation(self):
        month = Month(2019, 1)
        self.assertEqual(repr(month), 'Month(year=2019, month=1)')

    def test_human_readable_representation(self):
        month = Month(2019, 1)
        self.assertEqual(str(month), '2019-01')

    def test_string_representations(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(str(python2_eol), "2020-01")
        new_month = eval(repr(python2_eol))
        self.assertEqual(new_month.year, python2_eol.year)
        self.assertEqual(new_month.month, python2_eol.month)

    def test_first_method(self):
        python2_eol = Month(2020, 1)
        eol_date = python2_eol.first()
        self.assertEqual(eol_date.year, 2020)
        self.assertEqual(eol_date.month, 1)
        self.assertEqual(eol_date.day, 1)
        self.assertEqual(str(eol_date), '2020-01-01')
        self.assertEqual(str(eol_date - timedelta(days=1)), '2019-12-31')

    @unittest.skip("Comparable Month")
    def test_equality(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(python2_eol, Month(2020, 1))
        self.assertNotEqual(python2_eol, Month(2020, 2))
        self.assertNotEqual(python2_eol, Month(2019, 1))
        self.assertFalse(python2_eol != Month(2020, 1))
        self.assertFalse(python2_eol == Month(2020, 2))
        self.assertNotEqual(python2_eol, date(2020, 1, 1))
        self.assertNotEqual(python2_eol, (2020, 1))
        self.assertNotEqual((2020, 1), python2_eol)  # tuples aren't months

    @unittest.skip("Comparable Month")
    def test_ordering(self):
        python2_eol = Month(2020, 1)
        pycon_2019 = Month(2019, 5)
        self.assertLess(pycon_2019, python2_eol)
        self.assertGreater(python2_eol, pycon_2019)
        self.assertLessEqual(pycon_2019, python2_eol)
        self.assertGreaterEqual(python2_eol, pycon_2019)
        self.assertFalse(pycon_2019 > python2_eol)
        self.assertFalse(pycon_2019 >= python2_eol)
        self.assertFalse(python2_eol < pycon_2019)
        self.assertFalse(python2_eol <= pycon_2019)
        with self.assertRaises(TypeError):
            python2_eol < (2021, 12)  # tuples aren't months
        with self.assertRaises(TypeError):
            python2_eol >= (2021, 12)  # tuples aren't months
        with self.assertRaises(TypeError):
            (2021, 12) < python2_eol  # tuples aren't months

    @unittest.skip("Month Formatting")
    def test_formatting(self):
        python2_eol = Month(2020, 1)
        leap_month = Month(2000, 2)
        self.assertEqual("{:%Y-%m}".format(python2_eol), "2020-01")
        with set_locale('C'):
            self.assertEqual("{0:%b %Y}".format(leap_month), "Feb 2000")
            self.assertEqual("{:%b %Y}".format(python2_eol), "Jan 2020")

    @unittest.skip("Month from_date")
    def test_from_date(self):
        python2_eol = Month.from_date(date(2020, 1, 1))
        self.assertEqual(python2_eol, Month(2020, 1))
        leap_month = Month.from_date(date(2000, 2, 29))
        self.assertEqual(leap_month, Month(2000, 2))

    @unittest.skip("Memory-Efficient Month")
    def test_memory_efficient(self):
        python2_eol = Month(2020, 1)
        with self.assertRaises(Exception):
            python2_eol.__dict__


@contextmanager
def set_locale(name):
    saved = setlocale(LC_TIME)
    try:
        yield setlocale(LC_TIME, name)
    finally:
        setlocale(LC_TIME, saved)


class MonthDeltaTests(unittest.TestCase):

    """Tests for MonthDelta."""

    def test_initializer(self):
        four_months = MonthDelta(4)
        self.assertEqual(four_months.months, 4)

    def test_equality(self):
        self.assertEqual(MonthDelta(12), MonthDelta(12))
        self.assertNotEqual(MonthDelta(11), MonthDelta(12))
        self.assertIs(MonthDelta(12) != MonthDelta(12), False)
        self.assertIs(MonthDelta(11) == MonthDelta(12), False)
        self.assertIs(MonthDelta(0) == timedelta(0), False)
        self.assertIs(MonthDelta(0) == 0, False)
        self.assertIs(MonthDelta(6) == 6, False)

    def test_adding_month_delta_to_unknown_value(self):
        with self.assertRaises(TypeError):
            MonthDelta(4) + 8
        with self.assertRaises(TypeError):
            8 + MonthDelta(4)

    def test_adding_and_subtracting_with_monthdeltas(self):
        self.assertEqual(MonthDelta(4) + MonthDelta(2), MonthDelta(6))
        self.assertEqual(MonthDelta(4) - MonthDelta(2), MonthDelta(2))
        with self.assertRaises(TypeError):
            MonthDelta(4) - 8
        with self.assertRaises(TypeError):
            8 - MonthDelta(4)

    def test_month_arithmetic_with_month_deltas(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = MonthDelta(231)
        self.assertEqual(python2_eol + MonthDelta(4), Month(2020, 5))
        self.assertEqual(MonthDelta(13) + python2_eol, Month(2021, 2))
        self.assertEqual(python2_eol - MonthDelta(4), Month(2019, 9))
        self.assertEqual(python2_eol - MonthDelta(13), Month(2018, 12))
        self.assertEqual(python2_release + python2_lifetime, python2_eol)

    def test_month_subtracting_months(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = python2_eol - python2_release
        self.assertEqual(python2_lifetime, MonthDelta(20*12 - 9))

    def test_month_arithmetic_with_other_types(self):
        python2_eol = Month(2020, 1)
        python2_release = Month(2000, 10)
        python2_lifetime = python2_eol - python2_release
        with self.assertRaises(TypeError):
            python2_eol + python2_release
        with self.assertRaises(TypeError):
            python2_eol * python2_release
        with self.assertRaises(TypeError):
            python2_eol * python2_lifetime
        with self.assertRaises(TypeError):
            python2_lifetime - python2_eol
        with self.assertRaises(TypeError):
            python2_eol - date(1999, 12, 1)

    @unittest.skip("MonthDelta Arithmetic")
    def test_scaling_and_division(self):
        self.assertEqual(MonthDelta(4) * 2, MonthDelta(8))
        self.assertEqual(2 * MonthDelta(4), MonthDelta(8))
        self.assertEqual(MonthDelta(4) / MonthDelta(2), 2)
        self.assertEqual(MonthDelta(18) // 12, MonthDelta(1))
        self.assertEqual(MonthDelta(18) // MonthDelta(12), 1)
        self.assertEqual(MonthDelta(18) % MonthDelta(12), 6)
        self.assertEqual(MonthDelta(18) % 12, MonthDelta(6))
        self.assertEqual(-MonthDelta(18), MonthDelta(-18))
        with self.assertRaises(TypeError):
            MonthDelta(4) * "a"
        with self.assertRaises(TypeError):
            MonthDelta(4) * 2.0
        with self.assertRaises(TypeError):
            MonthDelta(4) / 2.0
        with self.assertRaises(TypeError):
            MonthDelta(4) * MonthDelta(2)
        with self.assertRaises(TypeError):
            MonthDelta(4) % 0.5


class RowTests(unittest.TestCase):

    """Tests for Row."""

    def test_no_arguments(self):
        row = Row()
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, set())

    def test_single_argument(self):
        row = Row(a=1)
        self.assertEqual(row.a, 1)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'a'})

    def test_two_arguments(self):
        row = Row(a=1, b=2)
        self.assertEqual(row.a, 1)
        self.assertEqual(row.b, 2)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'a', 'b'})

    def test_many_arguments(self):
        row = Row(thing='a', item=2, stuff=True)
        self.assertEqual(row.thing, 'a')
        self.assertEqual(row.item, 2)
        self.assertEqual(row.stuff, True)
        attributes = {x for x in dir(row) if not x.startswith('__')}
        self.assertEqual(attributes, {'thing', 'item', 'stuff'})

    def test_no_positional_arguments_accepted(self):
        with self.assertRaises(Exception):
            Row(1, 2)
        with self.assertRaises(Exception):
            Row(1)


class Timer:

    """Context manager to time a code block."""

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start


if __name__ == "__main__":
    from helpers import error_message
    error_message()
