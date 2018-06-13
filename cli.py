import time 
import sqlite3
import subprocess
import sys

data = {}

def welcome():
    print('Would you like to enter Mike Will Made Inc as an admin or customer?')
    print('------------------------------------')
    print("1. Administrator")
    print("2. Customer")
    print('3. Exit')

    reply = input("> ") 

    while True:
        if reply == '1' or reply == 'Administrator':
            print('Please enter 4 digit access code to enter')

            for i in range(3):
                
                reply = input('> ')

                if reply == '4508':
                    admin()
                    break
        
                else:
                    print("Sorry this input is invalid. . .")
                    
        elif reply == '2' or reply == 'Customer':
            welcome_client()
            
        elif reply == '3' or reply == 'Exit':
            quit_func()
            break

def welcome_client():
    print("Welcome to Mike Will Made Inc.")
    print("1. Account holder")
    print('2. Exit')

    reply = input("> ") 

    if reply == '1' or reply == 'Account holder':
        client_info()
    
    if reply == '2' or reply == 'Exit':
        welcome()
        
# Admin function 
def admin():
    print('------------------------------------')
    while True:
        print('------------------------------------')
        print("Where would you like to navigate?")
        print('1. Open SQLite')
        print('2. Add / modify customer')
        print('3. Exit')

        reply = input("> ") 

        if reply == '1' or reply == 'Open SQLite':
            subprocess.call(
            ["/usr/bin/open", "-a", "/Applications/DB Browser for SQLite.app", "cli.db"])
            '''data_get_table()'''

        if reply == '2' or reply == 'Add / modify customer':
            print('------------------------------------')
            time.sleep(0.5)
            mod_client_info()
            '''data_get_table()'''
            
        if reply == '3' or reply == 'Exit': 
            welcome()
            
# This function is for admins to modify or add a customers information
def mod_client_info():
    print('1. Add new customer')
    print('2. Edit customer')
    print('3. print list')
    print('4. Exit ')

    reply = input('> ')

    if reply == '1' or reply == 'Add new customer':
        print("Please enter the customers current information and a 4 digit pin.")

        while True:
            
            pin = int(input('Pin:' ))
            if pin > 9999:
                print('Please enter in a 4 digit pin number. . .')   
                continue             
            name = input('Name: ')
            name = name.title()
            email = input('Email: ')
            points = int(input('points: '))

            print('Is the displayed info correct:', pin, name, email, '&', points)
            print('(y/n)')

            reply = input('> ')

            if reply == 'y':
                print("Adding new customer. . .")
                
                data.update( { pin: {
                'name': name,
                'points': points,
                'email': email,
                'trigger': True
                }})
                data_entries(pin, name, email, points)
                break
                  
            elif reply == 'n':
                print('Please re enter the customers information. . . ')
                continue
 
            else:
                print("This input is invalid.")
                continue
        
    if reply == '2' or reply == 'Edit customer':
        print("Please enter a customers name to search. . .")

        search = int(input('Pin: '))

        if search in data:
            print("Pin: " + str(data[search]) + "\n")
            print("Is this the desired customer? (y/n) ")
            
            reply = input('> ')

        if search not in data:
            print('Sorry this customer does not exist. . . ')
            mod_client_info()

        if reply == 'y':

            print('1. Delete customer')
            print('2. Edit info')

            reply = input('> ')

            if reply == '1' or reply == 'delete customer':
                print('deleting customer. . . ')
                data.pop(search)
                data_delete(search)
                mod_client_info()

            if reply == '2' or reply == 'Edit info':
                print("Please enter the customers valid information. . .")

                pin = search

                name = input('Name: ')
                email = input('Email: ')
                points = int(input('points: '))

                print('Updating new log. . . ')

                user = data[search]

                data.update( { pin: {
                'name': name,
                'points': points,
                'email': email,
                }})
                data_update(pin, name, email, points, search)
                data.update({pin: user})
                mod_client_info()


    if reply == '3' or reply == 'print list':
        print(data)
        mod_client_info()

    if  reply == '4' or reply == 'Exit':
        welcome()

def database_table():
    conn = sqlite3.connect('cli.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS dictionaryInfo(Name TEXT, Email TEXT, Pin INTERGER, Points INTERGER)')
    c.close()
    conn.close()

def data_entries(pin, name, email, points):
    # c.execute("INSERT INTO dictionaryInfo VALUES('Name', 'mike@gmail.com', 'Python', 500)")
    conn = sqlite3.connect('cli.db')
    c = conn.cursor()
    c.execute("INSERT INTO dictionaryInfo(name, email, pin, points) VALUES(?, ?, ?, ?)", (name, email, pin, points))
    conn.commit()
    c.close()
    conn.close()
    mod_client_info()

def data_update(name, email, pin, points, search): 
    conn = sqlite3.connect('cli.db')
    c = conn.cursor()
    c.execute('UPDATE dictionaryInfo SET name = ?, email = ?, pin = ?, points = ? WHERE name = ?', (name, email, pin, points, search))
    conn.commit()
    c.close()
    conn.close()
    mod_client_info()

def data_delete(name):
    conn = sqlite3.connect('cli.db')
    c = conn.cursor()
    c.execute('DELETE FROM dictionaryInfo WHERE name = ?', (name,))
    conn.commit()
    c.close()
    conn.close()


def data_get_table(name, email, pin, points):
    conn = sqlite3.connect('cli.db')
    c = conn.cursor()
    c.execute('select * from Updates')

# extract column names
    column_names = [d[0] for d in c.description]
    for row in c:
        info = data(zip(name, email, pin, points, row))

#dump it to a json string
    reply = json.dumps(info)
    conn.commit()
    c.close()
    conn.close()
# This function is for customers who are checking in on their personal information
def client_info():
    print("Please enter your pin number to access your account.")
    
    while True:
        pin = int(input("Pin: "))

        if pin in data:
            print ("Pin: " + str(pin))
            print ("Pin: " + str(data[pin]) + "\n")
            print("Is this the desired customer? (y/n) ")

            reply = input('> ')
            
            if reply == 'y':
                # If the customer has already grabbed their free points for the day this code will execute
                if data[pin]['trigger'] == False:
                    print('Sorry you have already accessed your free points for the day.')
                    break
                # After the customer has collected their free points trigger gets set to false. Disabling them of getting more points.
                print("Welcome back! Here is 50 points for checking into your account")
                data[pin]['points']+=50
                data[pin]['trigger'] = False
                print("Thanks for checking in today come back tomorrow to claim more points...")
                break

            if reply == 'n':
                print("Erm strange...Please try to re enter your information.")

            else:
                print('Sorry your input is invalid')

def quit_func():
    print('see ya again. . . ')
    sys.exit()
    
database_table()
welcome()

## Try and finally for closing out sqlite...prevents it rom locking.