"""Tests for inheritance exercises"""
import unittest

from inheritance import (
    CyclicList,
    EasyDict,
    MinimumBalanceAccount,
    Node,
    DoublyLinkedNode,
    Tree,
    FieldTrackerMixin,
    LastUpdatedDictionary,
    OrderedCounter,
    MaxCounter,
)


class CyclicListTests(unittest.TestCase):

    """Tests for CyclicList."""

    def test_constructor(self):
        CyclicList([1, 2, 3, 4])

    def test_accepts_non_lists(self):
        numbers = CyclicList({1, 2, 3})
        self.assertEqual(next(iter(numbers)), 1)
        letters = CyclicList('hello')
        self.assertEqual(next(iter(letters)), 'h')

    def test_iterate_to_length(self):
        numbers = CyclicList([1, 2, 3])
        i = iter(numbers)
        self.assertEqual([next(i), next(i), next(i)], [1, 2, 3])

    def test_iterate_past_length(self):
        numbers = CyclicList([1, 2, 3])
        new_list = [x for x, _ in zip(numbers, range(10))]
        self.assertEqual(new_list, [1, 2, 3, 1, 2, 3, 1, 2, 3, 1])

    def test_iterators_are_independent(self):
        numbers = CyclicList([1, 2, 3, 4])
        i1 = iter(numbers)
        i2 = iter(numbers)
        self.assertEqual(next(i1), 1)
        self.assertEqual(next(i1), 2)
        self.assertEqual(next(i2), 1)
        self.assertEqual(next(i2), 2)

    def test_length_append_and_pop(self):
        numbers = CyclicList([1, 2, 3])
        self.assertEqual(len(numbers), 3)
        numbers.append(4)
        self.assertEqual(numbers.pop(), 4)
        self.assertEqual(numbers.pop(0), 1)

    def test_supports_indexing(self):
        numbers = CyclicList([1, 2, 3, 4])
        self.assertEqual(numbers[2], 3)
        numbers = CyclicList([1, 2, 3, 4])
        self.assertEqual(numbers[4], 1)
        self.assertEqual(numbers[-1], 4)
        numbers[5] = 0
        self.assertEqual(numbers[1], 0)


class EasyDictTests(unittest.TestCase):

    """Tests for EasyDict."""

    def test_constructor(self):
        EasyDict()
        EasyDict({'a': 2, 'b': 3})

    def test_key_access(self):
        d = EasyDict({'a': 2, 'b': 3})
        self.assertEqual(d['a'], 2)
        self.assertEqual(d['b'], 3)

    def test_attribute_access(self):
        d = EasyDict({'a': 2, 'b': 3})
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)

    def test_keyword_arguments(self):
        d = EasyDict(a=2, b=3, c=4, d=5)
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)
        self.assertEqual(d['c'], 4)
        self.assertEqual(d['d'], 5)

    def test_equality(self):
        x = EasyDict({'a': 2, 'b': 3})
        y = EasyDict({'a': 2, 'b': 4})
        self.assertNotEqual(x, y)
        self.assertNotEqual(x, {'a': 2, 'b': 4})
        self.assertEqual(y, {'a': 2, 'b': 4})
        y = EasyDict({'a': 2, 'b': 3})
        self.assertEqual(x, y)
        x = EasyDict({'a': 2, 'b': 3, 'c': 5})
        self.assertNotEqual(x, y)
        y = EasyDict({'a': 2, 'b': 3, 'c': 5})
        self.assertEqual(x, y)
        self.assertNotEqual(x, (1, 2))

    def test_get_method(self):
        x = EasyDict({'a': 2, 'b': 4})
        self.assertIsNone(x.get('d'))
        self.assertEqual(x.get('b'), 4)
        self.assertEqual(x.get('c', 5), 5)

    def test_original_dictionary_unchanged(self):
        mapping = {'a': 2, 'b': 3}
        d = EasyDict(mapping)
        mapping['c'] = 4
        self.assertEqual(d, {'a': 2, 'b': 3})


class MinimumBalanceAccountTests(unittest.TestCase):

    """Tests for MinimumBalanceAccount."""

    def test_withdraw_from_new_account(self):
        account = MinimumBalanceAccount()
        with self.assertRaises(ValueError):
            account.withdraw(1)

    def test_exception_message(self):
        account = MinimumBalanceAccount()
        with self.assertRaises(ValueError) as cm:
            account.withdraw(1000)
        self.assertEqual(str(cm.exception), "Balance cannot be less than $0")

    def test_withdraw_above_zero(self):
        account = MinimumBalanceAccount()
        account.deposit(100)
        account.withdraw(99)
        self.assertEqual(account.balance, 1)

    def test_withdraw_to_exactly_zero(self):
        account = MinimumBalanceAccount()
        account.deposit(100)
        account.withdraw(100)
        self.assertEqual(account.balance, 0)

    def test_withdraw_to_below_zero(self):
        account = MinimumBalanceAccount()
        account.deposit(100)
        with self.assertRaises(ValueError):
            account.withdraw(101)

    def test_repr(self):
        account = MinimumBalanceAccount()
        self.assertEqual(repr(account), 'MinimumBalanceAccount(balance=0)')


class NodeTests(unittest.TestCase):

    """Tests for Node."""

    def test_single_node(self):
        self.assertEqual(str(Node('A')), 'A')

    def test_multiple_nodes(self):
        expected = ('Animalia / Chordata / Mammalia / Carnivora / Ailuridae '
                    '/ Ailurus / A. fulgens')
        red_panda = (
         Node("Animalia")
         .make_child("Chordata")
         .make_child("Mammalia")
         .make_child("Carnivora")
         .make_child("Ailuridae")
         .make_child("Ailurus")
         .make_child("A. fulgens")
         )
        self.assertEqual(str(red_panda), expected)


class DoublyLinkedNodeTests(unittest.TestCase):

    """Tests for DoublyLinkedNode."""

    def test_single_node(self):
        t = DoublyLinkedNode('A')
        leaves = [node.name for node in t.leaves()]
        self.assertEqual(leaves, ['A'])
        self.assertIs(t.is_leaf(), True)

    def test_multiple_nodes(self):
        root = DoublyLinkedNode('A')
        child1 = root.make_child('1')
        grandchild1 = child1.make_child('a')
        grandchild2 = child1.make_child('b')
        child2 = root.make_child('2')
        leaves0 = [node.name for node in root.leaves()]
        leaves1 = [node.name for node in child1.leaves()]
        leaves2 = [node.name for node in child2.leaves()]
        self.assertEqual(leaves0, ['a', 'b', '2'])
        self.assertEqual(leaves1, ['a', 'b'])
        self.assertEqual(leaves2, ['2'])
        self.assertIs(grandchild1.is_leaf(), True)
        self.assertIs(grandchild2.is_leaf(), True)
        self.assertIs(child1.is_leaf(), False)
        self.assertIs(child2.is_leaf(), True)


class DBModel:
    def __init__(self, **kwargs):
        self.id = None
        for name, value in kwargs.items():
            setattr(self, name, value)
    def save(self):
        self.id = 4  # This would be auto-generated normally
        self.stored = True  # Pretending to put stuff in a database


class TreeTests(unittest.TestCase):

    """Tests for Tree."""

    def test_set_and_delete_item(self):
        felidae = Tree()
        felidae['panthera'] = ['lion']
        felidae['felis'] = ['cat']
        self.assertEqual(felidae['panthera'], ['lion'])
        self.assertEqual(felidae['felis'], ['cat'])
        del felidae['felis']
        self.assertNotEqual(felidae['felis'], ['cat'])

    def test_get_missing_item(self):
        artiodactyla = Tree()
        cetacea = artiodactyla['cetacea']
        self.assertEqual(artiodactyla['cetacea'], cetacea)
        self.assertIsNot(artiodactyla['camelids'], cetacea)

    def test_modifying_deeply_nested_items(self):
        mammals = Tree()
        mammals['carnivora']['canidae']['canis'] = ['coyote']
        mammals['carnivora']['canidae']['canis'].append('wolf')
        self.assertEqual(
            mammals['carnivora']['canidae']['canis'],
            ['coyote', 'wolf'],
        )

    def test_repr(self):
        mammals = Tree()
        mammals['artiodactyla']['camelidae']['lama'] = ['Guanaco', 'llama']
        dictionary = {
            'artiodactyla': {
                'camelidae': {
                    'lama': ['Guanaco', 'llama'],
                },
            },
        }
        self.assertIn('artiodactyla', repr(mammals))
        self.assertIn('camelidae', repr(mammals))
        self.assertIn('lama', repr(mammals))
        self.assertIn("['Guanaco', 'llama']", repr(mammals))

    def test_getting_and_setting_and_deleting_attributes(self):
        mammals = Tree()

        # Accessing as attributes
        mammals['artiodactyla']['camelidae']['lama'] = ['Guanaco', 'llama']
        self.assertEqual(
            mammals.artiodactyla.camelidae.lama,
            ['Guanaco', 'llama'],
        )

        # Assigning as attributes
        mammals.carnivora.canidae.canis = ['coyote']
        mammals['carnivora']['canidae']['canis'].append('wolf')
        self.assertEqual(
            mammals['carnivora']['canidae']['canis'],
            ['coyote', 'wolf'],
        )
        self.assertEqual(
            mammals.carnivora.canidae.canis,
            ['coyote', 'wolf'],
        )

    def test_initialize_and_update_should_copy(self):
        # Initializing tree-of-trees with dict-of-dicts
        mammals = Tree({
            'artiodactyla': {
                'camelidae': {
                    'lama': ['Guanaco', 'llama'],
                },
            },
        })
        self.assertEqual(
            mammals.artiodactyla.camelidae.lama,
            ['Guanaco', 'llama'],
        )
        mammals.carnivora.canidae.canis = ['coyote', 'wolf']
        self.assertEqual(
            mammals['carnivora']['canidae']['canis'],
            ['coyote', 'wolf'],
        )
        self.assertEqual(
            mammals.carnivora.canidae.canis,
            ['coyote', 'wolf'],
        )

        # Updating with dict-of-dicts
        mammals.update({
            'carnivora': {
                'prionodontidae': {'prionodon': ['pardicolor', 'linsang']},
                'canidae': {
                    'otocyon': ['megalotis'],
                },
            },
        })
        self.assertEqual(
            mammals.carnivora.prionodontidae.prionodon,
            ['pardicolor', 'linsang'],
        )
        self.assertEqual(mammals.carnivora.canidae.otocyon, ['megalotis'])

        # Still has the previous values also
        self.assertEqual(
            mammals.carnivora.canidae.canis,
            ['coyote', 'wolf'],
        )


class FieldTrackerMixinTests(unittest.TestCase):

    """Tests for FieldTrackerMixin."""

    def test_initializer(self):
        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@trey.com")
        self.assertIsNone(trey.id)

    def test_previous_pre_and_post_save(self):
        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        trey.email = "trey@gmail.com"
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        trey.save()
        self.assertEqual(trey.previous('email'), "trey@gmail.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@gmail.com")
        self.assertEqual(trey.id, 4)

    def test_has_changed_pre_and_post_save(self):
        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertFalse(trey.has_changed('email'))
        trey.email = "trey@gmail.com"
        self.assertTrue(trey.has_changed('email'))
        trey.save()
        self.assertFalse(trey.has_changed('email'))
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@gmail.com")
        self.assertEqual(trey.id, 4)

    def test_changed_pre_and_post_save(self):
        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertEqual(trey.changed(), {})
        trey.email = "trey@gmail.com"
        self.assertEqual(trey.changed(), {'email': "trey@trey.com"})
        trey.save()
        self.assertEqual(trey.changed(), {})
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@gmail.com")
        self.assertEqual(trey.id, 4)


class LastUpdatedDictionaryTests(unittest.TestCase):

    """Tests for LastUpdatedDictionary."""

    def test_initial_order(self):
        d = LastUpdatedDictionary([('a', 1), ('c', 3), ('b', 2), ('d', 4)])
        self.assertEqual(list(d.keys()), ['a', 'c', 'b', 'd'])
        self.assertEqual(list(d.values()), [1, 3, 2, 4])

    def test_order_after_insertion(self):
        d = LastUpdatedDictionary([('a', 1), ('c', 3), ('b', 2), ('d', 4)])
        d['e'] = 5
        self.assertEqual(list(d.keys()), ['a', 'c', 'b', 'd', 'e'])
        self.assertEqual(list(d.values()), [1, 3, 2, 4, 5])

    def test_order_after_update(self):
        d = LastUpdatedDictionary([('a', 1), ('c', 3), ('b', 2), ('d', 4)])
        d['c'] = 0
        self.assertEqual(list(d.keys()), ['a', 'b', 'd', 'c'])
        self.assertEqual(list(d.values()), [1, 2, 4, 0])


class OrderedCounterTests(unittest.TestCase):

    """Tests for OrderedCounter."""

    def test_initial_order(self):
        c = OrderedCounter('hello world')
        self.assertEqual(
            list(c.keys()),
            ['h', 'e', ' ', 'w', 'o', 'r', 'l', 'd'],
        )
        self.assertEqual(list(c.values()), [1, 1, 1, 1, 2, 1, 3, 1])

    def test_order_after_insertion(self):
        c = OrderedCounter('hello world')
        c.update('cat')
        self.assertEqual(
            list(c.keys()),
            ['h', 'e', ' ', 'w', 'o', 'r', 'l', 'd', 'c', 'a', 't'],
        )
        self.assertEqual(list(c.values()), [1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1])

    def test_order_after_update(self):
        c = OrderedCounter('hello world')
        c.update('hey')
        self.assertEqual(
            list(c.keys()),
            [' ', 'w', 'o', 'r', 'l', 'd', 'h', 'e', 'y'],
        )
        self.assertEqual(list(c.values()), [1, 1, 2, 1, 3, 1, 2, 2, 1])


class MaxCounterTests(unittest.TestCase):

    """Tests for MaxCounter."""

    def test_works_like_counter(self):
        counts = MaxCounter("hello")
        self.assertEqual(counts, {'h': 1, 'e': 1, 'l': 2, 'o': 1})
        self.assertEqual(counts['h'], 1)
        self.assertEqual(counts['!'], 0)

    def test_single_maximum(self):
        counts = MaxCounter("hello")
        self.assertEqual(set(counts.max_keys()), {'l'})

    def test_multiple_maximums(self):
        counts = MaxCounter("no banana")
        self.assertEqual(set(counts.max_keys()), {'a', 'n'})

    def test_all_maximums(self):
        counts = MaxCounter("abcd")
        self.assertEqual(set(counts.max_keys()), set('abcd'))

    def test_empty(self):
        counts = MaxCounter("")
        self.assertEqual(set(counts.max_keys()), set())


if __name__ == "__main__":
    from helpers import error_message
    error_message()
