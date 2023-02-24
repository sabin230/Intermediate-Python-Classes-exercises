"""Inheritance exercises"""


class CyclicList:
    """Class with list-like structure that loops cyclicly."""


class EasyDict:
    """Class which allows both attribute and get/set item syntax."""


class MinimumBalanceAccount:
    """Bank account which does not allow balance to drop below zero."""


class Node:

    """Nodes for use in making hierarchies or trees."""

    def __init__(self, name, *, ancestors=[]):
        self.ancestors = list(ancestors)
        self.name = name

    def ancestors_and_self(self):
        """Return iterable with our ordered ancestors and our own node."""
        return [*self.ancestors, self]

    def make_child(self, *args, **kwargs):
        """Create and return a child node of the current node."""
        return type(self)(*args, ancestors=self.ancestors_and_self(), **kwargs)

    def __str__(self):
        """Return a slash-delimited ancestors hierarchy for this node."""
        return " / ".join([
            node.name
            for node in [*self.ancestors, self]
        ])

    def __repr__(self):
        return self.name


class DoublyLinkedNode:
    """Class with Nodes that are doubly-linked"""


class Tree:

    """Tree-like object"""


class FieldTrackerMixin:

    """Mixin for tracking specific attribute changes."""


class LastUpdatedDictionary:

    """Dictionary that maintains last-updated order of items."""


class OrderedCounter:

    """Counter that maintains last-updated item order."""


class MaxCounter:
    """Counter-like class that allows retrieving all maximums."""
