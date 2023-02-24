"""Tests for dunder exercises"""
from collections.abc import Generator, Iterable, Mapping
from io import StringIO
from textwrap import dedent
from time import sleep
from sys import getsizeof
import unittest


from dunder import (
    ReverseView,
    Comparator,
    RomanNumeral,
    Timer,
    FancyDict,
    reloopable,
)


class ReverseViewTests(unittest.TestCase):

    """Tests for ReverseView."""

    def test_can_iterate_at_least_once(self):
        numbers = [2, 1, 3, 4, 7, 11, 18]
        view = ReverseView(numbers)
        self.assertEqual(list(view), [18, 11, 7, 4, 3, 1, 2])

    def test_can_iterate_more_than_once(self):
        numbers = [2, 1, 3, 4, 7, 11, 18]
        view = ReverseView(numbers)
        self.assertEqual(list(view), [18, 11, 7, 4, 3, 1, 2])
        self.assertEqual(list(view), [18, 11, 7, 4, 3, 1, 2])
        self.assertEqual(list(view), list(view))

    def test_updating_sequence_updates_view(self):
        numbers = [2, 1, 3, 4, 7, 11, 18]
        view = ReverseView(numbers)
        self.assertEqual(list(view), [18, 11, 7, 4, 3, 1, 2])
        numbers.append(29)
        self.assertEqual(list(view), [29, 18, 11, 7, 4, 3, 1, 2])
        numbers.pop(0)
        self.assertEqual(list(view), [29, 18, 11, 7, 4, 3, 1])

    def test_no_memory_used(self):
        numbers = list(range(10000))
        view = ReverseView(numbers)
        next(iter(view))
        if isinstance(view, Generator):
            size = sum(
                get_size(obj)
                for obj in view.gi_frame.f_locals.values()
            )
        else:
            size = get_size(view)
        self.assertLess(size, 400000, 'Too much memory used')
        self.assertNotEqual(type(view), list)
        self.assertNotEqual(type(view), tuple)

    def test_does_not_slice_sequence(self):
        class UnsliceableList(list):
            def __getitem__(self, index):
                if not isinstance(index, int):
                    return NotImplemented("Only indexes accepted")
                return super().__getitem__(index)
        numbers = UnsliceableList([2, 1, 3, 4, 7, 11, 18])
        view = ReverseView(numbers)
        self.assertEqual(list(view), [18, 11, 7, 4, 3, 1, 2])

    def test_has_length_and_repr_and_is_indexable(self):
        numbers = [2, 1, 3, 4, 7, 11, 18]
        view = ReverseView(numbers)

        # Has length
        self.assertEqual(len(view), 7)
        self.assertEqual(len(view), 7)
        numbers.append(29)
        self.assertEqual(len(view), 8)
        numbers.pop()
        self.assertEqual(len(view), 7)

        # Is indexable
        self.assertEqual(view[0], 18)
        self.assertEqual(view[-1], 2)
        self.assertEqual(view[2], 7)
        self.assertEqual(view[-2], 1)
        numbers.append(29)
        self.assertEqual(view[0], 29)
        self.assertEqual(view[-1], 2)
        numbers.pop(0)
        self.assertEqual(view[0], 29)
        self.assertEqual(view[-1], 1)

        # Has a nice string representation
        self.assertEqual(list(view), [29, 18, 11, 7, 4, 3, 1])
        self.assertEqual(str(view), "[29, 18, 11, 7, 4, 3, 1]")


class ComparatorTests(unittest.TestCase):

    """Tests for Comparator."""

    def test_equality_with_delta(self):
        self.assertEqual(5.5, Comparator(6, delta=0.5))
        self.assertEqual(6.5, Comparator(6, delta=0.5))
        self.assertNotEqual(6.51, Comparator(6, delta=0.5))
        self.assertNotEqual(5.49, Comparator(6, delta=0.5))

    def test_equality_with_default_delta(self):
        self.assertEqual(Comparator(5), 4.99999999)
        self.assertEqual(Comparator(5), 5.00000001)
        self.assertEqual(5, Comparator(4.99999999))
        self.assertEqual(5, Comparator(5.00000001))
        self.assertNotEqual(Comparator(5), 4.99999)
        self.assertNotEqual(Comparator(5), 5.00001)

    def test_negative_numbers(self):
        self.assertNotEqual(-5.5, Comparator(-6, delta=0.25))
        self.assertEqual(-5.75, Comparator(-6, delta=0.25))
        self.assertEqual(-6.25, Comparator(-6, delta=0.25))
        self.assertNotEqual(-6.3, Comparator(-6, delta=0.25))

    def test_very_small_delta(self):
        self.assertEqual(-6.000000000000001, Comparator(-6, delta=1e-15))
        self.assertNotEqual(-6.000000000000002, Comparator(-6, delta=1e-15))

    def test_string_representation(self):
        self.assertEqual(
            repr(Comparator(5, delta=0.1)),
            "Comparator(5, delta=0.1)",
        )
        self.assertEqual(repr(Comparator(5)), "Comparator(5, delta=1e-07)")
        self.assertEqual(str(Comparator(5)), "Comparator(5, delta=1e-07)")

    def test_addition_and_subtraction(self):
        self.assertEqual(Comparator(5, delta=0.1) + 6, 11.1)
        self.assertEqual(6 + Comparator(5, delta=0.1), 10.9)
        self.assertNotEqual(Comparator(5, delta=0.1) + 6, 11.2)
        self.assertNotEqual(6 + Comparator(5, delta=0.1) + 6, 10.8)
        self.assertEqual(Comparator(7, delta=0.1) - 6, 1.05)
        self.assertNotEqual(Comparator(7, delta=0.1) - 6, 1.2)
        self.assertEqual(7 - Comparator(7, delta=0.1), 0.05)
        self.assertNotEqual(7 - Comparator(7, delta=0.1), 0.11)
        self.assertEqual(6 - Comparator(7, delta=0.1), -1.05)

    def test_arithmetic_and_comparisons_with_comparators(self):
        five = Comparator(5, delta=0.1)
        six = Comparator(6, delta=0.1)
        seven = Comparator(7, delta=0.5)
        self.assertEqual(five + six, 11.1)
        self.assertNotEqual(five + six, 11.2)
        self.assertEqual(five + seven, 12.1)
        self.assertEqual(five + seven, 12.5)
        self.assertEqual(seven + five, 12.5)
        self.assertNotEqual(five + seven, 12.6)


class RomanNumeralTests(unittest.TestCase):

    """Tests for RomanNumeral."""

    def verify(self, integer, numeral):
        self.assertEqual(int(RomanNumeral(numeral)), integer)
        self.assertNotEqual(int(RomanNumeral(numeral)), integer+1)
        self.assertNotEqual(int(RomanNumeral(numeral)), integer-1)

    def test_single_digit(self):
        self.verify(1, "I")
        self.verify(5, "V")
        self.verify(10, "X")
        self.verify(50, "L")
        self.verify(100, "C")
        self.verify(500, "D")
        self.verify(1000, "M")

    def test_two_digits_ascending(self):
        self.verify(2, "II")
        self.verify(6, "VI")
        self.verify(11, "XI")
        self.verify(15, "XV")
        self.verify(20, "XX")
        self.verify(60, "LX")
        self.verify(101, "CI")
        self.verify(105, "CV")
        self.verify(110, "CX")
        self.verify(150, "CL")
        self.verify(550, "DL")
        self.verify(600, "DC")
        self.verify(1100, "MC")
        self.verify(2000, "MM")

    def test_three_digits_ascending(self):
        self.verify(3, "III")
        self.verify(7, "VII")
        self.verify(12, "XII")
        self.verify(16, "XVI")
        self.verify(21, "XXI")
        self.verify(25, "XXV")
        self.verify(30, "XXX")

    def test_four_digits_ascending(self):
        self.verify(8, "VIII")
        self.verify(13, "XIII")
        self.verify(17, "XVII")
        self.verify(22, "XXII")
        self.verify(26, "XXVI")
        self.verify(31, "XXXI")
        self.verify(35, "XXXV")

    def test_many_digits(self):
        self.verify(1888, "MDCCCLXXXVIII")

    def test_subtractive(self):
        self.verify(4, "IV")
        self.verify(9, "IX")
        self.verify(14, "XIV")
        self.verify(19, "XIX")
        self.verify(24, "XXIV")
        self.verify(29, "XXIX")
        self.verify(40, "XL")
        self.verify(90, "XC")
        self.verify(44, "XLIV")
        self.verify(94, "XCIV")
        self.verify(49, "XLIX")
        self.verify(99, "XCIX")
        self.verify(1999, "MCMXCIX")
        self.verify(1948, "MCMXLVIII")

    def test_string_representation(self):
        self.assertEqual(str(RomanNumeral("I")), "I")
        self.assertEqual(repr(RomanNumeral("CD")), "RomanNumeral('CD')")
        # Some conversion happens for some numbers
        fourteen = RomanNumeral("XIIII")
        self.assertEqual(str(fourteen), "XIV")
        self.assertEqual(repr(fourteen), "RomanNumeral('XIV')")

    def test_adding(self):
        sixty_five = RomanNumeral("LXV")
        eighty_seven = RomanNumeral("LXXXVII")
        self.assertEqual(int(sixty_five + eighty_seven), 152)
        self.assertEqual(type(sixty_five + eighty_seven), RomanNumeral)
        self.assertEqual(int(sixty_five + 87), 152)
        self.assertEqual(type(sixty_five + 87), RomanNumeral)
        self.assertEqual(str(sixty_five + 87), str("CLII"))

    def test_equality_and_ordering(self):
        self.assertEqual(RomanNumeral("I"), 1)
        self.assertNotEqual(RomanNumeral("I"), 2)
        self.assertEqual(RomanNumeral("I"), "I")
        self.assertLess(RomanNumeral("MCMXLVIII"), RomanNumeral("MCMXCIX"))
        self.assertGreater(RomanNumeral("MCMXCIX"), RomanNumeral("MCMXLVIII"))
        self.assertGreaterEqual(RomanNumeral("IX"), RomanNumeral("III"))
        self.assertLessEqual(RomanNumeral("III"), RomanNumeral("IX"))
        self.assertGreaterEqual(RomanNumeral("X"), RomanNumeral("X"))
        self.assertLessEqual(RomanNumeral("IIII"), RomanNumeral("IV"))
        self.assertFalse(RomanNumeral("V") < RomanNumeral("IV"))
        self.assertFalse(RomanNumeral("V") > RomanNumeral("IX"))
        self.assertFalse(RomanNumeral("V") <= RomanNumeral("IV"))
        self.assertFalse(RomanNumeral("V") >= RomanNumeral("IX"))
        with self.assertRaises(TypeError):
            RomanNumeral("X") < "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") <= "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") > "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") >= "XX"
        self.assertFalse(RomanNumeral("V") < 4)
        self.assertFalse(RomanNumeral("V") > 9)
        self.assertFalse(RomanNumeral("V") <= 4)
        self.assertFalse(RomanNumeral("V") >= 9)
        with self.assertRaises(TypeError):
            RomanNumeral("X") < "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") <= "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") > "XX"
        with self.assertRaises(TypeError):
            RomanNumeral("X") >= "XX"

    @unittest.skip("RomanNumeral from_int")
    def test_from_int(self):
        numeral = RomanNumeral.from_int(1)
        self.assertEqual(numeral, "I")
        self.assertEqual(numeral, 1)
        self.assertEqual(type(numeral), RomanNumeral)
        self.assertEqual(str(RomanNumeral.from_int(10)), "X")
        self.assertEqual(str(RomanNumeral.from_int(21)), "XXI")
        self.assertEqual(str(RomanNumeral.from_int(600)), "DC")
        self.assertEqual(str(RomanNumeral.from_int(2000)), "MM")
        self.assertEqual(str(RomanNumeral.from_int(12)), "XII")
        self.assertEqual(str(RomanNumeral.from_int(25)), "XXV")
        self.assertEqual(str(RomanNumeral.from_int(6)), "VI")
        self.assertEqual(str(RomanNumeral.from_int(4)), "IV")
        self.assertEqual(str(RomanNumeral.from_int(9)), "IX")
        self.assertEqual(str(RomanNumeral.from_int(14)), "XIV")
        self.assertEqual(str(RomanNumeral.from_int(1888)), "MDCCCLXXXVIII")
        self.assertEqual(str(RomanNumeral.from_int(1999)), "MCMXCIX")
        self.assertEqual(str(RomanNumeral.from_int(1948)), "MCMXLVIII")


class TimerTests(unittest.TestCase):

    """Tests for Timer."""

    _baseline = None

    @staticmethod
    def get_baseline(count=5):
        times = 0
        for i in range(count):
            with Timer() as timer:
                sleep(0)
            times += timer.elapsed
        return times / count

    def assertTimeEqual(self, actual, expected):
        if self._baseline is None:
            self._baseline = self.get_baseline()
        self.assertAlmostEqual(actual, self._baseline+expected, delta=0.005)

    def test_short_time(self):
        with Timer() as timer:
            sleep(0.01)
        self.assertGreater(timer.elapsed, 0.01)
        self.assertLess(timer.elapsed, 1)

    def test_very_short_time(self):
        with Timer() as timer:
            pass
        self.assertTimeEqual(timer.elapsed, 0)

    def test_two_timers(self):
        with Timer() as timer1:
            sleep(0.005)
            with Timer() as timer2:
                sleep(0.005)
            sleep(0.005)
        self.assertLess(timer2.elapsed, timer1.elapsed)

    def test_reusing_same_timer(self):
        timer = Timer()
        with timer:
            sleep(0.0005)
        elapsed1 = timer.elapsed
        with timer:
            sleep(0.004)
        self.assertLess(elapsed1, timer.elapsed)


class FancyDictTests(unittest.TestCase):

    """Tests for FancyDict."""

    def test_constructor(self):
        FancyDict()
        FancyDict({'a': 2, 'b': 3})

    def test_key_access(self):
        d = FancyDict({'a': 2, 'b': 3})
        self.assertEqual(d['a'], 2)
        self.assertEqual(d['b'], 3)

    def test_attribute_access(self):
        d = FancyDict({'a': 2, 'b': 3})
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)

    def test_original_dictionary_unchanged(self):
        mapping = {'a': 2, 'b': 3}
        d = FancyDict(mapping)
        d.c = 4
        self.assertEqual(mapping, {'a': 2, 'b': 3})

    def test_allow_setting_keys_and_attributes(self):
        d = FancyDict({'a': 2, 'b': 3})
        d['a'] = 4
        self.assertEqual(d['a'], 4)
        self.assertEqual(d.a, 4)
        d.c = 9
        self.assertEqual(d['c'], 9)
        self.assertEqual(d.c, 9)
        self.assertEqual(d['b'], 3)
        x = FancyDict()
        y = FancyDict()
        x.a = 4
        y.a = 5
        self.assertEqual(x.a, 4)

    def test_keyword_arguments_equality_and_get_method(self):
        d = FancyDict(a=2, b=3, c=4, d=5)
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)
        self.assertEqual(d['c'], 4)
        self.assertEqual(d['d'], 5)
        x = FancyDict({'a': 2, 'b': 3})
        y = FancyDict({'a': 2, 'b': 4})
        self.assertNotEqual(x, y)
        y.b = 3
        self.assertEqual(x, y)
        x.c = 5
        self.assertNotEqual(x, y)
        y.c = 5
        self.assertEqual(x, y)
        self.assertIsNone(y.get('d'))
        self.assertEqual(y.get('c'), 5)
        self.assertEqual(y.get('d', 5), 5)

    def test_keys_values_items_containment_and_length(self):
        d = FancyDict(a=2, b=3, c=4, d=5)
        self.assertEqual(set(d.keys()), {'a', 'b', 'c', 'd'})
        self.assertEqual(set(d.values()), {2, 3, 4, 5})
        self.assertEqual(
            set(d.items()),
            {('a', 2), ('b', 3), ('c', 4), ('d', 5)},
        )
        self.assertEqual(len(d), 4)
        self.assertTrue('a' in d)
        self.assertFalse('a' not in d)
        self.assertFalse('e' in d)
        self.assertTrue('e' not in d)
        self.assertNotIn('get', d)
        with self.assertRaises(KeyError):
            d['get']
        with self.assertRaises(KeyError):
            d['keys']
        self.assertNotIn('values', d)
        self.assertNotIn('setdefault', d)
        self.assertEqual(d.pop('b', None), 3)
        self.assertNotIn('b', d)
        self.assertEqual(d.pop('b', None), None)
        self.assertNotIn('b', d)
        with self.assertRaises(KeyError):
            d.pop('b')

    def test_normalize_attribute(self):
        d = FancyDict({'greeting 1': 'hi'}, normalize=True)
        self.assertEqual(d['greeting 1'], 'hi')
        self.assertEqual(d.greeting_1, 'hi')
        d.greeting_2 = 'hello'
        self.assertEqual(d['greeting 2'], 'hello')
        self.assertEqual(d.greeting_2, 'hello')
        d['greeting 2'] = 'hey'
        self.assertEqual(d['greeting 2'], 'hey')
        self.assertEqual(d.get('greeting 2'), 'hey')
        self.assertEqual(d.greeting_2, 'hey')
        with self.assertRaises(AttributeError):
            d.greeting2
        d = FancyDict({'greeting 1': 'hi'})
        self.assertEqual(d['greeting 1'], 'hi')
        with self.assertRaises(AttributeError):
            d.greeting_1

    def test_dir(self):
        d = FancyDict(a=2, b=3, c=4, d=5)
        self.assertIn('a', dir(d))
        self.assertIn('b', dir(d))
        self.assertIn('c', dir(d))
        self.assertIn('d', dir(d))


class ReloopableTests(unittest.TestCase):

    """Tests for reloopable."""

    one_line = "hello\n"

    two_lines = "line 1\nline 2\n"

    no_final_newline = "line 1\nline 2\nline 3"

    simone = dedent("""
        Picket lines, school boycotts
        They try to say it's a communist plot
        All I want is equality
        For my sister, my brother, my people, and me
    """.lstrip("\n"))

    many_lines = "This is a file\n" * 1000

    empty = ""

    def test_empty_file(self):
        f = StringIO(self.empty)
        reloop = reloopable(f)
        self.assertEqual(list(reloop), [])
        self.assertEqual(list(reloop), [])
        self.assertEqual(list(reloop), [])

    def test_one_line(self):
        f = StringIO(self.one_line)
        reloop = reloopable(f)
        self.assertEqual(list(reloop), ["hello\n"])
        self.assertEqual(list(reloop), ["hello\n"])
        self.assertEqual(list(reloop), ["hello\n"])

    def test_two_lines(self):
        f = StringIO(self.two_lines)
        reloop = reloopable(f)
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n"])
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n"])
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n"])

    def test_no_final_newlines(self):
        f = StringIO(self.no_final_newline)
        reloop = reloopable(f)
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n", "line 3"])
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n", "line 3"])
        self.assertEqual(list(reloop), ["line 1\n", "line 2\n", "line 3"])

    def test_many_lines(self):
        f = StringIO(self.many_lines)
        reloop = reloopable(f)
        self.assertEqual(list(reloop), ["This is a file\n"] * 1000)
        self.assertEqual(list(reloop), ["This is a file\n"] * 1000)
        self.assertEqual(list(reloop), ["This is a file\n"] * 1000)

    def test_data_in_file_is_not_stored(self):
        f = StringIO(self.many_lines)
        reloop = reloopable(f)

        self.assertEqual(list(reloop), ["This is a file\n"] * 1000)

        # Put new contents in the file
        f.seek(0)
        f.write(self.two_lines)
        f.truncate()

        self.assertEqual(list(reloop), ["line 1\n", "line 2\n"])


def get_size(obj, seen=None):
    """Return size of any Python object."""
    if seen is None:
        seen = set()
    size = getsizeof(obj)
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    if hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    if hasattr(obj, '__slots__'):
        size += sum(
            get_size(getattr(obj, attr), seen)
            for attr in obj.__slots__
            if hasattr(obj, attr)
        )
    if isinstance(obj, Mapping):
        size += sum(
            get_size(k, seen) + get_size(v, seen)
            for k, v in obj.items()
        )
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        size += sum(get_size(item, seen) for item in obj)
    return size


if __name__ == "__main__":
    unittest.main(verbosity=2)

if __name__ == "__main__":
    from helpers import error_message
    error_message()
