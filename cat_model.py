#!/usr/bin/env python3
import copy
from datetime import datetime
from datetime import date
from pathlib import Path
from dateutil.relativedelta import relativedelta

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
    counter = 0

    def __init__(self, name, dob='', last_name='', sex='', breed=''):
        """Weight is expected to be a 2d list with entries set as weight-timestamp pairs"""
        Cat.counter += 1
        self.created = datetime.now()
        self.name = [name, self.created]
        self.last_name = [last_name, self.created] if last_name else []
        self.sex = [sex, self.created] if sex else []
        self.breed = [breed, self.created] if breed else []
        self.dob = [dob, self.created] if dob else []
        self.fixed = []
        self.weight = []
        self.notes = []
        self.identifiers = {}
        self.vet = {}
        self.insurance_details = {}
        self.medical_history = {}
        self.medicines = {}
        self._id = Cat.counter
        self._obese = False
        self._daily_calories = 0
        self._age = None
        self.deactivated = [False, self.created]

    @property
    def id(self):
        return self._id

    @property
    def age(self):
        if self.dob:
            today = date.today()
            current_age = relativedelta(today, self.dob[0])
            return current_age
        else:
            return None

    @property
    def obese(self):
        return self._obese

    @property
    def set_obese(self):
        self._obese = not self._obese

    @property
    def daily_calories(self):
        return self._daily_calories

    @property
    def set_daily_calories(self):
        if not self.weight or not self.age:
            return None
        rer = self.calculate_rer(self.weight[-1][0])
        if self.age.years >= 1:
            if self.obese == True:
                self._daily_calories = rer
            elif self.fixed == True:
                self._daily_calories = rer * 1.2
            else:
                self._daily_calories = rer * 1.4
        elif self.age.months >= 5:
            self._daily_calories = rer * 2
        else:
            self._daily_calories = rer * 2.5

    def __str__(self):
        return_string = f'{self.name[0]}'
        if self.last_name:
            return_string += ' ' + self.last_name[0]
        return return_string

    def add_weight(self, new_weight):
        """Add a new weight-timestamp pair to self.weight"""
        self.weight.append([new_weight, datetime.now()])
        self.set_daily_calories

    def update_value(self, attribute, new_value):
        """Update the value of the selected attribute"""
        if self.validate_attribute_exists(attribute):
            self.__dict__[attribute] = [new_value, datetime.now()]
        else:
            raise AttributeError(f'{attribute.title()} is not a supported attribute')

    def flip_bool_value(self, attribute):
        """Flip the value of the selected bool attribute"""
        if self.validate_attribute_exists(attribute):
            if type(self.__dict__[attribute][0]) is bool:
                self.__dict__[attribute] = [not self.__dict__[attribute][0], datetime.now()]

    def add_list_value(self, attribute, new_value):
        """Append new_value to the selected attribute"""
        if self.validate_is_list(attribute):
            self.__dict__[attribute].append([new_value, datetime.now()])
            print(self.__dict__[attribute][-1])

    def update_list_value(self, attribute, new_value, list_index=-1):
        """Update the value of the selected list attribute based on list_index"""
        if self.validate_is_list(attribute):
            self.__dict__[attribute][list_index] = [new_value, datetime.now()]

    def delete_list_value(self, attribute, del_index=-1):
        """Delete a list record at del_index for the selected attribute"""
        if self.validate_is_list(attribute):
            self.__dict__[attribute].pop(del_index)

    def update_dict_value(self, attribute, key, new_value):
        """Update the value of the selected dict attribute key"""
        if self.validate_is_dict(attribute):
            self.__dict__[attribute][key] = [new_value, datetime.now()]

    def calculate_rer(self, weight):
        try:
            rer = 30 * weight + 70
            return rer
        except TypeError:
            return None

    def validate_attribute_exists(self, validation_value):
        return validation_value in self.__dict__

    def validate_value_exists(self, validation_value):
        return bool(validation_value)

    def validate_is_positive_float(self, validation_value):
        try:
            if float(validation_value) > 0:
                return True
        except (ValueError, TypeError):
            return False

    def validate_is_list(self, validation_value):
        if self.validate_attribute_exists(validation_value):
            if self.__dict__[validation_value] == []:
                return True
            else:
                return type(self.__dict__[validation_value][0]) is list

    def validate_is_dict(self, validation_value):
        if self.validate_attribute_exists(validation_value):
            if self.__dict__[validation_value] == {}:
                return True
            else:
                return type(self.__dict__[validation_value][0]) is dict

    """def validate_is_date(self, validation_value):
        try:
            datetime.strptime(validation_value, %d %B %Y)
            return True
        except ValueError:
            return False"""

    def validate_is_nonfuture_date(self, validation_value):
        if datetime.now() >= validation_value:
            return True
        return False

class CatCollection:
    def __init__(self, **attributes):
        self.collection = {}
        self.attributes = attributes

    def add_new_cat(self, name, dob='', last_name='', sex='', breed=''):
        new_cat = Cat(name, dob, last_name, sex, breed)
        self.collection[new_cat.id] = new_cat
        return self.collection[new_cat.id]

    def select_by_id(self, menu, id):
        print(f'select_by_id menu = {menu}')
        print(f'select_by_id id = {id}')
        a = menu.get(id)
        print(f'select_by_id result = {a}')
        return menu.get(id)

    """def select_cat_by_name(self, cat_name):
        for cat in self.collection.values():
            print(f'select cat by name cat_name = {cat_name}')
            print(f'select cat by name cat = {cat}')
            print(f'select cat by name cat.name = {cat.name}')
            if cat_name == cat.name:
                return cat
        return False"""

    def list_cats(self):
        list_of_cats = []
        for cat in self.collection.values():
            list_of_cats.append(cat.__str__)
        return list_of_cats

    def cat_menu(self):
        menu = copy.deepcopy(self.collection)
        menu['A'] = 'Add a new cat'
        menu['E'] = 'Exit'
        return menu

    def validate_menu_selection(self, menu, user_selection):
        try:
            if user_selection.isdigit():
                user_selection = int(user_selection)
            menu_selection = menu.get(user_selection)
            if menu_selection:
                return menu_selection
            else:
                return 'Invalid Selection'
        except (TypeError, ValueError):
            return 'Invalid Selection'


if __name__ == "__main__":
    a = Cat('Piroshki', datetime(year=1975, month=11, day=5))
    print(a.id)
    print(a.age.years)
    print(a.age.months)
    print(a.age.days)
