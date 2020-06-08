from config import Config
from pool_table import PoolTable
from datetime import datetime
from time import time
from pool_table_data import TableData
day = datetime.now()

# table manager control center for all pool hall/app functions
class TableAdmin():
    def __init__(self, day):
        self.day = day
        self.date = config.date_only(day)

    def print_lines(self):
        print("-----------------------------------")

    # Main app menu
    def show_menu(self):
        print("-----------------------------------")    
        print(f"POOL TABLE MANAGER APP - Date: {self.date}")
        print("")
        print("Press 'c' to CHECKOUT a pool table")
        print("Press 'x' to CLOSE a pool table") 
        print("Press 'v' to VIEW all pool tables") 
        print("Press 'r' to RECOVER pool table activity") 
        print("Press 'q' to QUIT the app")
        self.print_lines()

    # function shows a list of all tables with current status
    def show_tables(self):
        current_time = datetime.now()
        print("")
        print("POOL TABLE LIST")
        self.print_lines()
        for table in tables:
            if table.occupied == True:
                status = "Occupied"
            else:
                status = "Available"
            if table.start_time != "":
                pretty_clock = config.clock_format(table.start_time,)
                elapsed_time = config.timer_format(
                    current_time, table.start_time)
                print(
                    f"Pool Table - {table.number} - {status} -  Start time: {pretty_clock} - Play time: {elapsed_time}")
            else:
                print(
                    f"Pool Table - {table.number} - {status}")
        self.print_lines()

    # function handles main menu choice and returns table choice to chooser() function
    def choose_table(self, user_input):
        while True:
            try:
                if user_input == "c":
                    choice = int(input("Enter which pool table number that you want to CHECKOUT: ")) - 1

                else:
                    choice = int(input("Enter which pool table number that you want to CLOSE: ")) - 1

                table = tables[choice]
                return table
            except ValueError:
                print("\n")
                print(
                    "*** Please enter a valid pool table number between 1 and 12. ***:")
                print("\n")
            except:
                print("\n")
                print(
                    "*** Please enter a valid pool table number between 1 and 12. ***:")
                print("\n")

    # function to re-assign attributes to table object from a json data recovery file
    def repopulate_data(self, json_data):
        recovery_time = datetime.now()
        for i in range(len(json_data)):
            temp_table = json_data[i]
            temp_table_no = int(temp_table["Pool Table Number"])
            print(temp_table_no)
            for table in tables:
                if table.number == temp_table_no:
                    table.occupied = True
                    table.start_time = datetime.strptime(
                        temp_table["Start Time"], "%Y-%m-%d %H:%M:%S.%f")
                    table.end_time = recovery_time

    # method handles all choices from main menu
    def chooser(self, user_input):
        if user_input == "c":
            print("")
            confirmation = input(
                "Are you sure that you want to checkout a pool table?\nPress 'y' for YES or 'n' for NO: ").lower()
            if confirmation == "n":
                print("")
            elif confirmation == "y":
                self.show_tables()
                table = self.choose_table(user_input)
                table.checkout()
                recovery_list = pool_table_data.create_recovery_entry(
                    table.number, table.start_time, table.end_time)
                pool_table_data.rec_entry(recovery_list)
                self.show_tables()
                print(
                    f"Pool table {table.number} has been checked out at: {config.clock_format(table.start_time)}")
            else:
                print("")
                print("*** You did not enter a valid response. Please try again. ***")

        elif user_input == "x":
            print("")
            confirmation = input(
                "Are you sure that you want to close out a pool table?\nPress 'y' for YES or 'n' for NO: ").lower()
            if confirmation == "n":
                print("")
            elif confirmation == "y":
                self.show_tables()
                all_available = True
                for table in tables:
                    if table.occupied == True:
                        all_available = False
                if all_available == True:
                    print("")
                    input(
                        "*** All pool tables are available. Choose another menu option. ***\n\n\nPress RETURN to go back to the MENU: ")
                else:
                    table = self.choose_table(user_input)
                    status = table.checkin()
                    if status == True:
                        entry = pool_table_data.create_entry(
                            table.number, table.start_time, table.end_time, table.time_played)
                        pool_table_data.log_entry(entry)
                        table.start_time = ""
                        self.show_tables()
                        print(
                            f"Pool table {table.number} has been closed out at: {config.clock_format(table.end_time)}")
            else:
                print("")
                print("*** You did not enter a valid response. Please try again. ***")
        
        elif user_input == "v":
            self.show_tables()
        
        elif user_input == "r":
            print("")
            confirmation = input(
                "Are you sure that you want to recover pool table activity?\nPress 'y' for YES or 'n' for NO: ").lower()
            if confirmation == "n":
                print("")
            elif confirmation == "y":
                recovery_list = pool_table_data.recovery(self.date)
                self.repopulate_data(recovery_list)
                self.show_tables()
            else:
                print("")
                print("*** You did not enter a valid response. Please try again. ***")

################ running of the app below ##################

# creating instances of classes to run app
config = Config()
manager = TableAdmin(day)
pool_table_data = TableData(manager.date)

# creating list and filling it with table objects
tables = []
for i in range(1, 13):
    table = PoolTable(i)
    tables.append(table)

# while loop that keeps app in a running state until user quits with 'q'
user_input = ""
while user_input != "q":
    manager.show_menu()
    user_input = input("Please enter a choice from the menu: ")
    manager.chooser(user_input)