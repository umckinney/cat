import pytest
from datetime import datetime
from cat_model import Cat
from cat_model import CatCollection

################################
# Cat class tests
################################
def test_cat_init():
    a = Cat('test1')
    assert a.name[0] == 'test1'
    assert a.name[1] < datetime.now()
    assert a.uuid

    b = Cat('test2', datetime(2024, 11, 5), 'mctest', 'male', 'siberian')
    assert b.name[0] == 'test2'
    assert b.last_name[0] == 'mctest'
    assert b.dob[0].strftime('%Y-%m-%d') == '2024-11-05'
    assert b.sex[0] == 'male'
    assert b.breed[0] == 'siberian'
    assert b.name[1] == b.last_name[1] == b.dob[1] == b.sex[1] == b.breed[1]

def test_str():
    a = Cat('test1')
    assert a.__str__() == 'test1'

    b = Cat('test2', last_name = 'mctest')
    assert b.__str__() == 'test2 mctest'

def test_add_weight():
    a = Cat('test1')
    a.add_weight(10)
    assert a.weight[-1][0] == 10
    assert a.daily_calories == 0

    b = Cat('test2', dob = datetime(2014, 11, 5))
    b.add_weight(8)
    assert b.weight[-1][0] == 8
    assert b.daily_calories == 434.0

def test_update_value():
    a = Cat('test1')
    a.update_value('last_name', 'mctest')
    assert a.last_name[0] == 'mctest'
    assert a.__str__() == 'test1 mctest'
    a.update_value('name', 'test2')
    assert a.name[0] == 'test2'
    assert a.__str__() == 'test2 mctest'
    with pytest.raises(AttributeError) as validation_error:
        a.update_value('blue', 'green')
    assert str(validation_error.value) == 'Blue is not a supported attribute'

def test_flip_bool_value():
    a = Cat('test1')
    assert a.deactivated[0] == False
    a.flip_bool_value('deactivated')
    assert a.deactivated[0] == True
    a.flip_bool_value('deactivated')
    assert a.deactivated[0] == False

def test_add_list_value():
    a = Cat('test1', datetime(2014, 11, 5))
    assert a.notes == []
    a.add_list_value('notes', 'note1')
    assert a.notes[0][0] == 'note1'
    a.add_list_value('notes', 'note2')
    assert a.notes[1][0] == 'note2'

def test_update_list_value():
    a = Cat('test1', datetime(2014, 11, 5))
    a.add_list_value('notes', 'note1')
    assert a.notes[0][0] == 'note1'
    a.add_list_value('notes', 'note2')
    assert a.notes[1][0] == 'note2'
    a.update_list_value('notes', 'new note 1', 0)
    assert a.notes[0][0] == 'new note 1'
    a.update_list_value('notes', 'new note 2')
    assert a.notes[1][0] == 'new note 2'

def test_delete_list_value():
    a = Cat('test1', datetime(2014, 11, 5))
    a.add_list_value('notes', 'note1')
    assert a.notes[0][0] == 'note1'
    a.add_list_value('notes', 'note2')
    assert a.notes[1][0] == 'note2'
    a.add_list_value('notes', 'note3')
    assert a.notes[2][0] == 'note3'
    assert len(a.notes) == 3
    a.delete_list_value('notes', 0)
    assert a.notes[0][0] == 'note2'
    assert len(a.notes) == 2
    a.delete_list_value('notes')
    assert a.notes[-1][0] == 'note2'
    assert len(a.notes) == 1

def test_update_dict_value():
    a = Cat('test1', datetime(2014, 11, 5))
    assert a.identifiers == {}
    a.update_dict_value('identifiers', 'chip id', '1234')
    assert a.identifiers['chip id'][0] == '1234'

def test_calculate_rer():
    a = Cat('test')
    assert a.calculate_rer(10) == 370
    assert a.calculate_rer('10') == None

################################
# CatCollection class tests
################################
def test_cat_collection_init():
    c_col = CatCollection()
    assert c_col.collection == {}

def test_add_new_cat():
    c_col = CatCollection()
    assert c_col.collection == {}
    c_col.add_new_cat('test1')
    assert c_col.collection != {}
    found_cat = ''
    for cat in c_col.collection.values():
        if 'test1' in cat.name:
            found_cat = cat
    assert found_cat

def test_select_cat():
    c_col = CatCollection()
    c_col.add_new_cat('test1')
    c_col.add_new_cat('test2')
    c_col.add_new_cat('test3')
    c_col.add_new_cat('test4')
    found_cat = c_col.select_cat('test2')
    assert found_cat.name[0] == 'test2'
    found_cat = c_col.select_cat('test1')
    assert found_cat.name[0] == 'test1'
    found_cat = c_col.select_cat('test5')
    assert found_cat == False

