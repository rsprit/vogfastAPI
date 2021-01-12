import requests
import pandas as pd
from datetime import datetime
dateTimeObj = datetime.now()
import os
import generate_db as gen

# Main--------------------------------------------------------------------------

class Monitor:

    def __init__(self):
        self.url = "http://fileshare.csb.univie.ac.at/vog/"
        self.last_data = None
        self.last_data_fname = "last_data"

    def exists(self):
        result = os.path.exists(self.last_data_fname)
        if not result:
            print(f"{self.last_data_fname} does not exist")
        return result

    def initiate(self):
        print(f"create new database from fileshare.csb.univie.ac.at/vog/, at {dateTimeObj}")

        result = requests.get(self.url)
        if result.status_code != 200:
            raise ValueError('Service failed to respond')
        else:
            result = result.text

        data = pd.read_html(result)[0]["Last modified"].dropna()

        data.to_csv(self.last_data_fname, sep=";", index=False)
        gen.generate_db()

    def get_last(self):
        return pd.read_csv(self.last_data_fname, sep=";")

    def update(self, debug=False):
        """Get the modification dates from fileshare and call generate_db function if the dates changed"""
        self.last_data = self.get_last()

        result = requests.get(self.url)
        if result.status_code != 200:
            raise ValueError('Service failed to respond')
        else:
            result = result.text

        data = pd.DataFrame(pd.read_html(result)[0]["Last modified"].dropna())

        if not self.check_equality(self.numpy1DArrayToList(self.last_data.values),
                                   self.numpy1DArrayToList(data.values)):
            gen.generate_db()
            print(f"Updating DB at {dateTimeObj}")
        else:
            print(f"checked for modified data at {dateTimeObj}")
        if debug:
            return self.last_data.values, data.values

    @staticmethod
    def check_equality(date_old, date_new):
        """Check if all items in the lists date_old and date_new are identical
            Returns: bool"""
        date_old = list(date_old)
        date_new = list(date_new)
        for i, item in enumerate(date_old):
            try:
                if item != date_new[i]:
                    return False
            except IndexError:
                return False
        return True

    @staticmethod
    def numpy1DArrayToList(npArray):
        return npArray.reshape(len(npArray)).tolist()

    def run(self):
        if not self.exists():
            self.initiate()
        else:
            self.update()


# Run it------------------------------------------------------------------------

if __name__ == "__main__":
    Monitor().run()