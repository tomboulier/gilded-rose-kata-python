# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
    
def is_aged_brie(item: Item) -> bool:
    return item.name == "Aged Brie"

def is_backstage_pass(item: Item) -> bool:
    return item.name == "Backstage passes to a TAFKAL80ETC concert"

def is_sulfuras(item: Item) -> bool:
    return item.name == "Sulfuras, Hand of Ragnaros"
    
def is_normal(item: Item) -> bool:
    return not (
        is_aged_brie(item) or is_backstage_pass(item) or is_sulfuras(item)
    )
    
def increase_quality(item: Item, amount: int = 1) -> None:
    if is_sulfuras(item):
        # Sulfuras quality does not change
        return
    # for other items, increase quality up to a max of 50
    item.quality = min(50, item.quality + amount)
    
def decrease_quality(item: Item, amount: int = 1) -> None:
    if is_sulfuras(item):
        # Sulfuras quality does not change
        return
    # for other items, decrease quality down to a min of 0
    item.quality = max(0, item.quality - amount)
    
def drop_quality_to_zero(item: Item) -> None:
    if is_sulfuras(item):
        # Sulfuras quality does not change
        return
    item.quality = 0
    
def decrease_sell_in(item: Item) -> None:
    if is_sulfuras(item):
        # Sulfuras does not have an end date
        return
    item.sell_in -= 1
    
class UpdateStrategy(ABC):
    """Strategy interface for updating an item's quality and sell_in."""

    @abstractmethod
    def update(self, item: Item) -> None:
        """Update the given item."""
        raise NotImplementedError

class NormalUpdateStrategy(UpdateStrategy):
    def update(self, item: Item) -> None:
        decrease_quality(item)
        decrease_sell_in(item)
        if item.sell_in < 0:
            decrease_quality(item)

class AgedBrieUpdateStrategy(UpdateStrategy):
    def update(self, item: Item) -> None:
        increase_quality(item)
        decrease_sell_in(item)
        if item.sell_in < 0:
            increase_quality(item)

class BackstagePassUpdateStrategy(UpdateStrategy):
    def update(self, item: Item) -> None:
        increase_quality(item)
        if item.sell_in < 11:
            increase_quality(item)
        if item.sell_in < 6:
            increase_quality(item)
        decrease_sell_in(item)
        if item.sell_in < 0:
            drop_quality_to_zero(item)

class SulfurasUpdateStrategy(UpdateStrategy):
    def update(self, item: Item) -> None:
        # Sulfuras quality does not change
        pass
    
class StrategyFactory:
    @staticmethod
    def get(item):
        if is_aged_brie(item):
            return AgedBrieUpdateStrategy()
        if is_backstage_pass(item):
            return BackstagePassUpdateStrategy()
        if is_sulfuras(item):
            return SulfurasUpdateStrategy()
        return NormalUpdateStrategy()

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            strategy = StrategyFactory.get(item)
            strategy.update(item)
