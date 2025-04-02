#!/usr/bin/env python3
import uuid
from datetime import datetime
from datetime import date
from pathlib import Path

"""
Cat Tracker written by Uriah Efe McKinney
    The goal of this program is to ensure I'm on top of all of my cats' health needs.
    This includes:
        calculating how much food they should eat each meal based on the standard cat calorie calculation
        tracking their vet visits, medications/treatments, etc
    The data should be persistent and sharable
    The UX should be intuitive
    All model code should be unit tested
    See README for more details on core use cases
"""

class Cat:
    def __init__(self, name, dob, last_name='', breed='', fixed=False, **attributes):
        """Weight is expected to be a 2d list with entries set as weight-timestamp pairs"""
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.last_name = last_name
        self.dob = dob
        self.breed = breed
        self.fixed = fixed
        self.obese = False
        self.daily_calories = 0
        self.weight = []
        self.notes = ''
        self.created = Helpers().get_timestamp()
        self.deactivated = [False, self.created]
        self.attributes = attributes

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def add_weight(self, new_weight):
        """Add a new weight-timestamp pair to self.weight"""
        self.weight.append([new_weight, Helpers().get_timestamp()])
        self.daily_calories = self.calculate_calories(new_weight)

    def update_detail(self, attribute, new_value):
        """Update the value of the specified attribute"""
        if attribute == 'weight':
            self.add_weight(new_value)
            return True
        elif attribute == 'daily_calories':
            return False
        elif attribute in self.__dict__:
            self.__dict__[attribute] = new_value
            return True
        return False

    def calculate_calories(self, weight):
        rer = self.calculate_rer(weight)
        age = self.cat_age()
        if age['years'] >= 1:
            if self.obese == True:
                return rer
            elif self.fixed == True:
                return rer * 1.2
            else:
                return rer * 1.4
        elif age['months'] >= 5:
            return rer * 2
        else:
            return rer * 2.5

    def calculate_rer(self, weight):
        return 30 * weight + 70

    def cat_age(self):
        today = date.today()
        years = today.year - self.dob.year
        months = today.month - self.dob.month
        if months < 0:
            years -= 1
            months += 12
        return {
            'years':years,
            'months':months,
        }

    def activation_toggle(self):
        self.deactivated[0] = not self.deactivated[0]
        self.deactivated[1] = Helpers().get_timestamp()

class CatCollection:
    def __init__(self, **attributes):
        self.collection = {}
        self.attributes = attributes

    def add_new_cat(self, name, dob, **attributes):
        pass

    def select_cat(self, name):
        found_cats = []
        for cat in self.collection.values():
            if name in cat.name:
                found_cats.append(cat)
        if found_cats:
            return found_cats
        return False







class Validators:
    def __init__(self, *args):
        self.args = args

    def validate_value_exists(self, validation_value):
        return bool(validation_value)

    def validate_positive_float(self, validation_value):
        try:
            if float(validation_value) > 0:
                return True
        except (ValueError, TypeError):
            return False

class Helpers:
    def __init__(self, *args):
        self.args = args

    def get_timestamp(self):
        now = datetime.now()
        return datetime.timestamp(now)

    def get_date(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%d %B %Y')

if __name__ == "__main__":
    a = Cat('Piroshki', '2025-09-30')
    print(a.uuid)
