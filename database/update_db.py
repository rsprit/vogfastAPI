# Import Section----------------------------------------------------------------

import requests
import pandas as pd
from time import sleep


# import generate_db

# Main--------------------------------------------------------------------------

class Monitor:

    def __init__(self):
        self.url = "http://fileshare.csb.univie.ac.at/vog/"
        self.last_data = None
        self.pause_between_requests = 10  # Minutes

    def update(self):
        """Get the modification dates from fileshare and call generate_db function if the dates changed
        Raises: TypeError if no previous data exist"""
        result = requests.get(self.url).text
        data = pd.read_html(result)[0]["Last modified"].dropna()
        try:
            if not self.check_equality(self.last_data, data):  # Inefficient but more native way of checking
                print("Generating DB")  # TODO: Replace by generate_db function
            else:
                print("Database already up to date.")
        except TypeError:
            print("Generating DB for the first time")  # TODO: Replace by generate_db function
        self.last_data = data

    @staticmethod  # Maybe not necessary, call self in the function instead
    def check_equality(date_old, date_new):
        """Check if all items in the lists dateA and dateB are identical
            Returns: bool
            Raises: IndexError"""
        date_old = list(date_old)  # Type safety - putting an error if not type == list probably better practice
        date_new = list(date_new)
        for i, item in enumerate(date_old):
            try:
                if item != date_new[i]:
                    return False
            except IndexError:
                return False
        return True

    def run(self):
        """Call indefinitely the updateDB function and suspend execution for the given number of seconds"""
        while True:
            self.update()
            sleep(self.pause_between_requests * 60)


# Run it------------------------------------------------------------------------

if __name__ == "__main__":
    Monitor().run()
