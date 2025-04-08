#!/usr/bin/env python3
import sys
from cat_model import Cat
from cat_model import CatCollection
from cat_model import Helpers
from cat_model import Validators
from docutils.writers.odf_odt import fix_ns


##########################################################
# UI CLASSES                                             #
##########################################################
class View:
    """Base View class"""
    def __init__(self, view_name):
        self.view_name = view_name

    def newline(self):
        print('\n')

    def pause_screen(self):
        """ Pause the screen """
        return input('Press ENTER to continue')

    def clear_screen(self):
        """ Clear the screen """
        print("\033c", end='')

    def print_title(self):
        """ Print the title to screen """
        print(f'Donation Manager - {self.view_name}')

    def print_content(self, content):
        """ Print the content to screen """
        print(content)

    def collect_user_input(self, collection_string):
        """ Collect user input """
        return input(collection_string + ' >>> ')

class Menu(View):
    def print_content(self, content):
        """Prints menu values based on the selected menu type"""
        for key, value in content.items():
            print(f'{key} - {value.__name__.replace('_', ' ').title()}')

class List(View):
    def print_content(self, content):
        """Expects a List"""
        for i in content:
            print(i)

class Detail(View):
    """Expects a Cat object"""
    def print_content(self, content):
        print(f'Name: {content.__str__}')
        self.newline()
        print('Age: -') if not content.dob else print(f'Age: {content.cat_age["years"]} years {contentn.cat_age["months"] months old}')
        self.newline()
        print('Weight: -') if not content.weight else print(f'Weight: {content.weight[-1]}')
        self.newline()
        print('Breed: -') if not content.breed else print(f'Breed: {content.breed}')
        self.newline()
        print('Sex: -') if not content.sex else print(f'Sex: {content.sex}')
        self.newline()
        if content.gender = 'male':
            fix_label = 'Neutered'
        elif content.gender = 'female':
            fix_label = 'Spayed'
        else: fix_label = 'Fixed'
        print(f'{fix_label}: -') if not content.fixed else print(f'{fix_label}: {content.fixed}')
        self.newline()
        print('Notes:')
        self.newline()
        print(content.Notes)

