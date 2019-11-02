import csv
import os
import fireo

from db.ghost_record import GhostRecord

class GhostNameLoader():
    """ Do a init load of all ghost_name """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_reader = None
        self.ghost_record = GhostRecord()

    def run(self):
        # init Firestore connection
        firebase_auth = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
        fireo.connection(from_file=firebase_auth)

        try:
            with open('tests/ghost_names.csv', mode='r') as self.csv_file:
                self.csv_reader = csv.reader(self.csv_file, delimiter=',')
                header = next(self.csv_reader, None)  # skip header
                for name, description in self.csv_reader:
                    print(name, "-->", description)
                    self.ghost_record.id = name
                    self.ghost_record.name = name
                    self.ghost_record.description = description
                    self.ghost_record.save()
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    GhostNameLoader().run()