import json
import datetime as dt
import os

notes_empty = {'notes': []}
data_we_need = ['title', 'content', 'date']

def start():
    print('Choose your action:')
    choice = input('1 - add new note;\n2 - show all notes;\n3 - delete note;\n'
                   '4 - change note;\n5 - delete all notes;\n0 - exit;\n')
    while choice != '0':
        match [choice]:
            case ['1']:
                add_note()
            case ['2']:
                print_notes()
            case ['3']:
                title = input('Enter note\'s title you want to delete: ')
                if delete_note(title) is None:
                    print('Note with this title does\'t exist')
                elif delete_note(title) is -1:
                    print("You have no notes, please add note and try again")
                else:
                    print('Note successfully deleted')
            case ['4']:
                title = input('Enter note\'s title you want to change: ')
                if find_note(title) is None:
                    print('Note with this title does\'t found')
                else:
                    what_change = input('If you want change the title press 1 or 2 to change content: ')
                    if what_change is '1':
                        new_title = input('Enter new  title: ')
                        edit(title, new_title, None)
                    elif what_change is '2':
                        new_content = input('Enter new content: ')
                        edit(title, None, new_content)
                    else:
                        print('You enter incorrect data.')
            case ['5']:
                with open('test.json', 'w') as test:
                    json.dump(notes_empty, test)
            case ['0']:
                break
            case _:
                print('Your choice does\'t match with proposed, please choose again.')
        choice = input('1 - add new note;\n2 - show all notes;\n3 - delete note;\n4 - change note;\n0 - exit;\n')

def get_data():
    note = dict()
    for el in data_we_need:
        if el == 'date':
            note[el] = f'{dt.datetime.now()}'
            return note
        note[el] = input(f'Enter note {el}: ').strip()

def add_note():
    try:
        if os.stat('test.json').st_size == 0:
            with open('test.json', 'w') as test:
                notes0 = {'notes': []}
                notes0['notes'].append(get_data())
                json.dump(notes0, test, indent=4)
        else:
            with open('test.json') as test:
                notes1 = json.load(test)
                new_note = get_data()
                flag = True
                for d in notes1['notes']:
                    if new_note.get('title') == d.get('title'):
                        print(f'Note with this title exist\n {d}')
                        flag = False
                if flag:
                    notes1['notes'].append(new_note)
                    with open('test.json', 'w') as test1:
                        json.dump(notes1, test1, indent=4)
    except FileNotFoundError:
        with open('test.json', 'w') as test:
            notes0 = {'notes': []}
            notes0['notes'].append(get_data())
            json.dump(notes0, test)
    except TypeError:
        with open('test.json', 'w') as test:
            notes0 = {'notes': []}
            notes0['notes'].append(get_data())
            json.dump(notes0, test)


def delete_note(title):
    if read_notes() is None:
        return -1
    if find_note(title) is None:
        return None
    current_notes = read_notes()
    del current_notes.get('notes')[find_note(title)]
    with open('test.json', 'w') as notes:
        json.dump(current_notes, notes, indent=4)
        return 1


def edit(title, new_title, new_content):
    if find_note(title) is None:
        return None
    current_notes = read_notes()
    if new_title is None:
        current_notes.get('notes')[find_note(title)]['content'] = new_content
        current_notes.get('notes')[find_note(title)]['date'] = f'{dt.datetime.now()}'
    else:
        current_notes.get('notes')[find_note(title)]['title'] = new_title
        current_notes.get('notes')[find_note(title)]['date'] = f'{dt.datetime.now()}'
    with open('test.json', 'w') as notes:
        json.dump(current_notes, notes, indent=4)
    return 1


def find_note(title):
    if read_notes() is None:
        return None
    for i in range(len(read_notes()['notes'])):
        if read_notes()['notes'][i]['title'] == title:
            return i
    # for d in read_notes()['notes']:
    #     if d.get('title') == title:
    #         return d
    return None


def read_notes():
    try:
        with open('test.json') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        return None
    except FileNotFoundError:
        return None


def print_notes():
    if read_notes() is None:
        print("You have no notes, please add note and try again")
    else:
        for d in read_notes()['notes']:
            print(f'Title: {d["title"]}; Content: {d["content"]}; Change or creation date: {d["date"]}')
