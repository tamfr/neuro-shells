# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:47:46 2013

@author: Mott
"""
from mix import mix
import sqlite3
 
conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES) # Using :memory: to put "database" in RAM.
cursor = conn.cursor() # Setting cursor to augment database.
 
# Create a table in database
cursor.execute("""CREATE TABLE mixes
                  (mix_label text, time_stamp DATE, PPF_batch DATE, beaker_mass real, total_mass real,
                   PPF2DEF_antecedent real, PPF2DEF_consequent real, BAPO real, HMB real, TiO2 real, I784 real) 
               """)

mixes = {} # Initiates dictionary to store instances of mix globally.

cur = cursor.execute("SELECT * FROM mixes") # Select all data from table.
rows = cur.fetchall() # Fetches all rows from table.

# The following loops creates mix instances from mixes stored in database to be used in script.
for row in rows:
    if row != None:
        mixes[row[0]] = (mix())
        mixes[row[0]].defineFromDatabase(row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
        mixes[row[0]].label(row[0])
        mixes[row[0]].create()

def curingTests():
    run = 1 # Turns the follwoing loop on.
    while run > 0: # Keeps loop running until run = 0.   
        ask = raw_input('\n\nIs this a new mixture? [Y/N] ')   
        if ask == 'Y' or ask == 'y':       
            c = 1        
            while True and c == 1:
                try:
                    mixName = raw_input('\nMix name? (case sensitive) ')
                    if mixes[mixName] != 0: 
                        up = raw_input('This mix already exists! Would you like to update it? [Y/N] ')
                        if up == 'Y' or up == 'y':
                            mixes[mixName].update()
                        else:
                            break
                    break
                except KeyError:
                    mixes[mixName] = (mix())
                    mixes[mixName].define()
                    mixes[mixName].label(mixName)
                    mixes[mixName].create()
                    c = 0
        elif ask == 'N' or ask == 'n':
            while True:        
                try:
                    mixName = raw_input('\nMix name to update? (case sensitive) ')
                    if mixes[mixName] != 0:
                        mixes[mixName].update()
                    break
                except KeyError:
                    new = raw_input('This mix does not exist! Would you like to create it? [Y/N] ')
                    if new == 'Y' or new == 'y': 
                        mixes[mixName] = (mix())
                        mixes[mixName].define()
                        mixes[mixName].label(mixName)
                        mixes[mixName].create()
                    else:
                        break
        else:
            print 'Please enter either /"Y" or /"N"! '         
        c = 1
        while True and c == 1:
            try:
                ask = raw_input('\n\nKeep running? [Y/N] (WARNING: If you close interpreter, all data will be lost!) ')
                if ask == 'Y' or ask == 'y': 
                    c = 0
                elif ask == 'N' or ask == 'n':
                    run = 0
                    c = 0
                else:
                    print 'Please enter either /"Y" or /"N"! '
                    c = 1
            except ValueError:
                print 'Please enter either /"Y" or /"N"! '
    