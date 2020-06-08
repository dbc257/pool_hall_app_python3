import json
from pool_table import PoolTable
from config import Config
config = Config()

# class handles generation of json files for susbsequent billing and for data recovery
class TableData():
    def __init__(self, date):
        self.date = date
        self.entry_list = []
        self.recovery_list = []

    # cretes a session entry for later billing
    def create_entry(self, table, start, end, total_time):
        f_start = config.date_format(start)
        f_end = config.date_format(end)
        f_total_time = config.timer_format(end, start)
        cost = config.cost_calc(end, start)
        entry = {
            "Pool Table Number": table, "Start Time": f_start,
            "End Time": f_end, "Total Time Played": f_total_time, "Cost": cost
        }
        self.entry_list.append(entry)
        return self.entry_list

    # creates a data recocvery entry a checkout for possible app failure
    def create_recovery_entry(self, table, start, end):
        rec_entry = {"Pool Table Number": table,
                     "Start Time": str(start), "End Time": str(end)}
        self.recovery_list.append(rec_entry)
        return self.recovery_list

    # writes to json file for billing
    def log_entry(self, entry):
        with open(f'{self.date}.json', 'w') as file_object:
            json.dump(entry, file_object, indent=2)

    # writes to json recovery file
    def rec_entry(self, entry):
        with open(f'{self.date}-rec.json', 'w') as file_object:
            json.dump(entry, file_object, indent=2)

    # loads json recovery file -- json object conversion
    def recovery(self, date):
        with open(f'{self.date}-rec.json') as file_object:
            recovery_list = json.load(file_object)
        return recovery_list