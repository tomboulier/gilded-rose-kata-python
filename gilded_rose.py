# -*- coding: utf-8 -*-

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
    
def decrease_sell_in(item: Item, amount: int = 1) -> None:
    item.sell_in -= amount

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if is_normal(item):
                decrease_quality(item)
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                if is_backstage_pass(item):
                    if item.sell_in < 11:
                        increase_quality(item)
                    if item.sell_in < 6:
                        increase_quality(item)
            if not is_sulfuras(item):
                decrease_sell_in(item)
            if item.sell_in < 0:
                if not is_aged_brie(item):
                    if not is_backstage_pass(item):
                        if item.quality > 0:
                            if not is_sulfuras(item):
                                item.quality = item.quality - 1
                    if is_backstage_pass(item):
                        item.quality = 0
                else:
                    increase_quality(item)
