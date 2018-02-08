# Author: Colin O. Quinn
# Date Modified: 1/30/2018
# Email:
import os
import csv
import time
import string
import datetime
import sys
import serial
from random import randint

from struct import unpack
from binascii import unhexlify

#default vairables
SOCK_OWNER_NAME_1 = 'no_name_entered'
SOCK_OWNER_COUNTRY_1 = 'no_country_entered'
SOCK_OWNER_NAME_2 = 'no_name_entered'
SOCK_OWNER_COUNTRY_2 = 'no_country_entered'
CURRENT_DATE_TIME = 'system_date_error'
CSV_FILE_NAME = 'no_time_stamp_assigned'
EXPERIMENT_PREP_TIME = 5
EXPERIMENT_RUN_TIME = 30
DATA_COLLECTED = []

welcome = '''
===================================================================================================
   _____                _ _          _____            _          _____           _           _
  / ____|              | | |        / ____|          | |        |  __ \         (_)         | |
 | (___  _ __ ___   ___| | |_   _  | (___   ___   ___| | _____  | |__) | __ ___  _  ___  ___| |_
  \___ \| '_ ` _ \ / _ \ | | | | |  \___ \ / _ \ / __| |/ / __| |  ___/ '__/ _ \| |/ _ \/ __| __|
  ____) | | | | | |  __/ | | |_| |  ____) | (_) | (__|   <\__ \ | |   | | | (_) | |  __/ (__| |_
 |_____/|_| |_| |_|\___|_|_|\__, | |_____/ \___/ \___|_|\_\___/ |_|   |_|  \___/| |\___|\___|\__|
                             __/ |                                             _/ |
                            |___/                                             |__/
===================================================================================================\n
Welcome, please wait for system tests to finish...\n
'''
sys_options = '''\
Please select one of the following:\n
1) Run Experiment
2) View CSV Library
3) Ping FTP
4) Conduct System Tests
5) Quit (or ctrl+c at anytime)\n
Your selection:
'''
#2) Push CSV library to server
experiment_interface = '''
Selection (1):\n
Smelly Socks Experiment Interface - Fill in Following Information
===================================================================================================
'''
experiment_Details = '''
Test Chamber Location\t\tSock Owner Name\t\t\tSock Owner Country\t\tCSV name\t\t\t
-----------------------\t\t-----------------------\t\t-----------------------\t\t-----------------------
'''
experiment_header = '''\
===================================================================================================
    !!! EXPERIMENT IN PROGRESS  !!!
===================================================================================================
'''
experiment_footer = '''\n
===================================================================================================
    !!! EXPERIMENT CONCLUDED, CLOSE GATES  !!!
===================================================================================================
    '''
experiment_summary_and_re_prompt = '''
Experiment summary:
===================================================================================================\n
- Experiment CSV has been written to ".\csv_library\ ''' + CSV_FILE_NAME + '''"
- To push the CVS(s) in csv_library, select option #2\n
===================================================================================================\n
'''

def run_experiment():
    global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, SOCK_OWNER_NAME_2, SOCK_OWNER_COUNTRY_2, CSV_FILE_NAME,CURRENT_DATE_TIME
    clear()
    print(experiment_interface)
    print('Sock Owner Name (Test Chamber 1):\n')
    SOCK_OWNER_NAME_1 = retrieve_name_from_user()
    print('\nSock Owner Country (Test Chamber 1):\n')
    SOCK_OWNER_COUNTRY_1 = retrieve_country_from_user()
    print('\nSock Owner Name (Test Chamber 2):\n')
    SOCK_OWNER_NAME_2 = retrieve_name_from_user()
    print('\nSock Owner Country (Test Chamber 2):\n')
    SOCK_OWNER_COUNTRY_2 = retrieve_country_from_user()

    CURRENT_DATE_TIME = str(datetime.datetime.utcnow().strftime("%d-%m-%Y_%H:%M"))

    CSV_FILE_NAME = SOCK_OWNER_NAME_1.replace(' ','_').lower() + '_VS_' + SOCK_OWNER_NAME_2.replace(' ','_').lower() + '.csv'
    CSV_FILE_NAME2 = CURRENT_DATE_TIME + '.csv'
    clear()
    print('Experiment Details:')
    print(experiment_Details)
    print('Test Chamber 1'.ljust(32, ' ') + SOCK_OWNER_NAME_1.ljust(32, ' ') + SOCK_OWNER_COUNTRY_1.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007826'.ljust(32, ' ') + '\n')
    print('Test Chamber 2'.ljust(32, ' ') + SOCK_OWNER_NAME_2.ljust(32, ' ') + SOCK_OWNER_COUNTRY_2.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' '))# + '000000007827'.ljust(32, ' ') + '\n')
    raw_input('\nConfirm information and prep Gates. Press <enter> to begin. (You will have 5 seconds to get into place)\n ')

    print(experiment_header)
    count_down('Open gates in', EXPERIMENT_PREP_TIME, '', False)
    start_sensor_reader()
    print(experiment_footer)

    print('CSV saved to ' + CSV_FILE_NAME + '\n\n')
    myData = []
    if yes_or_no('Rerun experiment? <y/n + enter>') == False:
        write_to_csv()
    else:
        run_experiment()

def write_to_csv():
    global SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CSV_FILE_NAME, CURRENT_DATE_TIME
    DATA_COLLECTED = [[SOCK_OWNER_NAME_1, SOCK_OWNER_COUNTRY_1, CURRENT_DATE_TIME] , [randint(0,1) for p in range(0,30)]] #Delete when real data is here
    csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
    new_csv_file = open('.\csv_library\\' + CSV_FILE_NAME, 'w')
    with new_csv_file:
        writer = csv.writer(new_csv_file, dialect = 'myDialect')
        writer.writerows(DATA_COLLECTED)
    clear()
    print(experiment_summary_and_re_prompt)
    print(sys_options)
    choose_path()

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Please enter either y or n")

def start_sensor_reader():
    clear()
    counter = 0 #will count how many mosquitos have broken the plane
    voltage = 5 # voltage is assigned the maximun amount of voltage to begin
    average_voltage = 0
    voltage_population_size = 1000
    ArduinoSerial = serial.Serial('com4',9600) #Create Serial port object called arduinoSerialData
    print("Port opend <COM4>, at <9600> bits per second\n")
    time.sleep(2) #wait for 2 secounds for the communication to get established
    print("Calibrating sensors...\n")
    for x in range(0, voltage_population_size):
        try:
            serialOutput = ArduinoSerial.readline().strip().replace('\r','')
            average_voltage += float(serialOutput)
        except Exception:
            pass

    average_voltage = average_voltage/voltage_population_size
    print("Average voltage reading: ")
    print(average_voltage)
    print('\n')

    count_down('Open gates in', 0, '', False) #delete after demo EXPERIMENT_PREP_TIME

    t_end = time.time() + 60 * .1
    print("TEST HAS BEGUN")

    while time.time() < t_end:

        try:
            serialOutput = ArduinoSerial.readline().strip().replace('\r','')
            voltage = float(serialOutput)
        except Exception:
            print("start_sensor_reader() ==> Error Converting to float")
            sys.exc_clear()

        print(voltage)
        if(voltage < (average_voltage - .1)):
            print("!!!!!DETECTED!!!!! Total Mosquitos: ")
            counter += 1
            print(counter)

            while(voltage < (average_voltage - .1)):
                print("-not counted-")
                print(voltage)
                voltage = float(ArduinoSerial.readline().strip())

    print("!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!\n")
    print("A total of ")
    print(counter)
    print("mosqutios were detected")

def count_down(front_message, sleep_time, back_message, blank_sleep):
    if blank_sleep is False:
        for remaining in range(sleep_time, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(front_message + "{:2d} ".format(remaining) + back_message)
            sys.stdout.flush()
            time.sleep(1)
        print('\n')
    else:
            time.sleep(sleep_time)

def print_csv_library():
    with open('./csv_library/test_csv.csv') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            print(row)

def retrieve_name_from_user():
    name = None
    while not name:
        try:
            name = str(raw_input())
        except ValueError:
            print 'Invalid Name'
    return name

def retrieve_country_from_user():
    country = None
    while not country:
        try:
            country = str(raw_input()) #Use pyCountry in the future
        except ValueError:
            print 'Invalid Country'
    return country

def choose_path():
    action = None
    while not action:
        try:
            action = int(raw_input())
        except ValueError:
            print('Invalid Number')

    if action == 1:
        run_experiment()
        #write_to_csv() use for testing only
    else:
         if action == 2:
             print_csv_library()
         else:
            if action ==3:
                print('3')
            else:
                if action == 4:
                    print('4')
def clear():
     os.system('cls' if os.name=='nt' else 'clear')
clear()

start_sensor_reader()
# print(welcome.center(30));
# # time.sleep(4)
# print(sys_options)
# choose_path()
#
# mosquito = '''
#            _         _
#           /x\       /x\
#          /v\x\     /v\/\
#          \><\x\   /></x/
#           \><\x\ /></x/
#   __ __  __\><\x/></x/___
#  /##_##\/       \</x/    \__________
# |###|###|  \         \    __________\
#  \##|##/ \__\____\____\__/          \\
#    |_|   |  |  | |  | |              \|
#    \*/   \  |  | |  | /              /
#            /    /
#
# '''
