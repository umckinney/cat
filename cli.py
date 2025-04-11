#!/usr/bin/env python3
import sys
import copy
from datetime import datetime
from cat_model import Cat
from cat_model import CatCollection
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
        print(f'Cat Manager - {self.view_name}')

    def print_content(self, content):
        """ Print the content to screen """
        print(content)

    def print_menu(self, content):
        """Prints menu values from a dict"""
        for key, value in content.items():
            print(f'{key} - {value.__str__()}')

    def print_list(self, content):
        """Expects a List"""
        for i in content:
            print(i)
            self.newline()

    def print_cat_details(self, content):
        """Expects a Cat object"""
        print(f'content = {content}')
        print(f'Name: {content.__str__()}')
        print(f'not content.age = {not content.age}')
        age = 'Age: -' if not content.age else f'Age: {content.age.years} years {content.age.months} months old'
        print(age)
        weight = 'Weight: -' if not content.weight else f'Weight: {content.weight[-1][0]}'
        print(weight)
        breed = 'Breed: -' if not content.breed else f'Breed: {content.breed[0]}'
        print(breed)
        sex = 'Sex: -' if not content.sex else f'Sex: {content.sex[0]}'
        print(sex)
        if len(content.sex) == 0:
            fix_label = 'Fixed'
        else:
            if content.sex[0] == 'male':
                fix_label = 'Neutered'
            elif content.sex[0] == 'female':
                fix_label = 'Spayed'
            else:
                fix_label = 'Fixed'
        fixed = f'{fix_label}: -' if not content.fixed else f'{fix_label}: {content.fixed[0]}'
        print(fixed)
        print('Notes:')
        if len(content.notes) == 0:
            print('-')
        else:
            print(content.notes[-1][0])

    def collect_user_input(self, collection_string):
        """ Collect user input """
        return input(collection_string + ' >>> ')

def main():
    """Start mailroom program flow"""
    cats = CatCollection()
    program_running = True
    while program_running:
        main_view = View('Main Menu')
        main_view.clear_screen()
        main_view.print_title()
        main_view.newline()
        cat_menu = cats.cat_menu()
        main_view.print_menu(cat_menu)
        main_view.newline()
        user_selection = main_view.collect_user_input('Enter your selection')
        validated_user_selection = cats.validate_menu_selection(cat_menu, user_selection)
        print(f'user_selection = {user_selection}')
        print(f'validated_user_selection = {validated_user_selection}')
        main_view.pause_screen()
        if validated_user_selection != 'Invalid Selection':
            if validated_user_selection == 'Add a new cat':
                add_cat_view(cats)
            elif validated_user_selection == 'Exit':
                exit_program()
            elif user_selection.isdigit():
                 cat_detail_view(cats.select_cat_by_name(validated_user_selection))

def cat_detail_view(cat):
    detail_view = View('Cat Details')
    detail_view.clear_screen()
    detail_view.print_title()
    detail_view.newline()
    detail_view.print_cat_details(cat)
    detail_view.pause_screen()

def add_cat_view(cat_collection):
    new_cat = {}
    add_a_cat_view = View('Add a Cat')
    add_a_cat_view.clear_screen()
    add_a_cat_view.print_title()
    add_a_cat_view.newline()
    name = ''
    while not name:
        name = add_a_cat_view.collect_user_input("Enter your cat's name")
    new_cat['name'] = name
    new_cat['last_name'] = add_a_cat_view.collect_user_input("Enter your cat's last name - optional")
    sex_options = ['male', 'female', '']
    sex = 'default'
    while sex not in sex_options:
        sex = add_a_cat_view.collect_user_input("Pick your cat's sex: male, female - optional")
    new_cat['sex'] = sex
    new_cat['breed'] = add_a_cat_view.collect_user_input("Enter your cat's breed (YYYY) - optional")
    year = add_a_cat_view.collect_user_input("Enter your cat's year of birth - optional")
    if year:
        month = add_a_cat_view.collect_user_input("Enter your cat's birth month (MM) - optional")
        month = 1 if not month else month
        day = add_a_cat_view.collect_user_input("Enter your cat's birthdate (D) - optional")
        day = 1 if not day else day
        print(f'year = {year}, month = {month}, day = {day}')
        new_cat['dob'] = datetime(int(year), int(month), int(day))
    else:
        new_cat['dob'] = ''
    cat = cat_collection.add_new_cat(new_cat['name'], new_cat['dob'], new_cat['last_name'], new_cat['sex'], new_cat['breed'])
    cat_detail_view(cat)

def exit_program():
    """End program"""
    print('Program Ended Successfully')
    sys.exit()

if __name__ == "__main__":
    main()



