# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Callable, Dict, ClassVar


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# Type alias for update functions
UpdateFn = Callable[[Item], None]


class UpdateStrategy:
    """Registry of update functions for Gilded Rose items.

    A single class manages:
    - a `registry` mapping item names → update function
    - helpers as static methods
    - the default update behavior for normal items
    """

    # --------------------------
    # Registry
    # --------------------------
    registry: ClassVar[Dict[str, UpdateFn]] = {}

    @classmethod
    def register(cls, item_name: str) -> Callable[[UpdateFn], UpdateFn]:
        """Decorator to register an update function for a given item name."""
        def decorator(func: UpdateFn) -> UpdateFn:
            cls.registry[item_name] = func
            return func
        return decorator

    @classmethod
    def get(cls, item: Item) -> UpdateFn:
        """Return the update function for this item, or fallback to normal behavior."""
        return cls.registry.get(item.name, cls.update_normal)

    # --------------------------
    # Helpers (static methods)
    # --------------------------

    @staticmethod
    def increase_quality(item: Item, amount: int = 1) -> None:
        """Increase quality up to a maximum of 50."""
        item.quality = min(50, item.quality + amount)

    @staticmethod
    def decrease_quality(item: Item, amount: int = 1) -> None:
        """Decrease quality down to a minimum of 0."""
        item.quality = max(0, item.quality - amount)

    @staticmethod
    def drop_quality_to_zero(item: Item) -> None:
        """Set quality to zero."""
        item.quality = 0

    @staticmethod
    def decrease_sell_in(item: Item) -> None:
        """Decrease sell_in by 1."""
        item.sell_in -= 1

    # --------------------------
    # Default strategy
    # --------------------------

    @staticmethod
    def update_normal(item: Item) -> None:
        """Default update logic for normal items."""
        UpdateStrategy.decrease_quality(item)
        UpdateStrategy.decrease_sell_in(item)
        if item.sell_in < 0:
            UpdateStrategy.decrease_quality(item)


# --------------------------
# Registered strategies
# --------------------------

@UpdateStrategy.register("Aged Brie")
def update_aged_brie(item: Item) -> None:
    UpdateStrategy.increase_quality(item)
    UpdateStrategy.decrease_sell_in(item)
    if item.sell_in < 0:
        UpdateStrategy.increase_quality(item)


@UpdateStrategy.register("Backstage passes to a TAFKAL80ETC concert")
def update_backstage(item: Item) -> None:
    UpdateStrategy.increase_quality(item)
    if item.sell_in < 11:
        UpdateStrategy.increase_quality(item)
    if item.sell_in < 6:
        UpdateStrategy.increase_quality(item)

    UpdateStrategy.decrease_sell_in(item)

    if item.sell_in < 0:
        UpdateStrategy.drop_quality_to_zero(item)


@UpdateStrategy.register("Sulfuras, Hand of Ragnaros")
def update_sulfuras(item: Item) -> None:
    # Legendary item: no change.
    pass


# --------------------------
# Main class
# --------------------------

class GildedRose:
    """Core class applying update strategies to items."""

    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            UpdateStrategy.get(item)(item)
