import json

from json import JSONEncoder


class Feat:
    def __init__(self):
        self.name = ""
        self.src = ""
        self.page = ""
        self.src_raw = ""
        self.src_category = ""
        self.pfs = ""
        self.prerequisite = ""
        self.rarity = ""
        self.level = ""
        self.summary = ""
        self.text = ""
        self.trait = []
        self.resistance = []
        self.speed = []
        self.weakness = []
        self.actions = []
        self.frequency = []
        self.trigger = []
        self.skill = []
        self.archetype = []
        self.requirement = []
        self.school = []
        self.cost = []
        self.spoilers = []
        self.access = []

class Encoder(json.JSONEncoder):
    def default(self, i):
        return i.__dict__
