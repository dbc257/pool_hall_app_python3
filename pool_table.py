from datetime import datetime
time = datetime.now()

# pool table class
class PoolTable:
    def __init__(self, number):
        self.number = number
        self.occupied = False
        self.start_time = ""
        self.end_time = ""
        self.time_played = ""
        self.current_time = ""

    # function changes attributes for checkout status
    def checkout(self):
        if self.occupied == True:
            print("")
            input(
                f"*** Pool table {self.number} is currently 'Occupied'. Please choose another pool table number. Press RETURN to go back to the MENU. ***")
        else:
            self.occupied = True
            self.start_time = datetime.now()
            self.end_time = datetime.now()
            self.time_played = self.end_time - self.start_time

    # changes pool table attributes to a closed and calculates delta time
    def checkin(self):
        if self.occupied == False:
            print("")
            input(
                "*** This pool table cannot be closed because its current status is 'Available'. Press RETURN to go back to the MENU. ***")
            return False
        else:
            self.occupied = False
            self.end_time = datetime.now()
            self.time_played = self.end_time - self.start_time
            return True