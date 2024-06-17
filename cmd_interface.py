"""
Classes to operate CSV database through command line interface
"""
from pathlib import Path
from database_lib import *


class CsvContacts:
    """"""
    database = []

    _csv_file_path = None
    delimiter = ','
    quotechar = '"'

    def __init__(self, csv_file_path='databanka.csv', **kwargs):
        self.set_csv_file_path(csv_file_path)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_csv_file_path(self, csv_file_path='databanka.csv'):
        csv_file = Path(csv_file_path)
        if csv_file.exists() and csv_file.is_file():
            self._csv_file_path = csv_file_path
        else:
            print(f"Zadany CSV sobor {csv_file.resolve()} neexistuje, enbo k nemu nemate prava...")

    def nacist_kontakty_csv(self):
        """"""
        if self._csv_file_path is not None:
            self.database = nacist_kontakty_csv(self._csv_file_path,
                                                delimiter=self.delimiter,
                                                quotechar=self.quotechar)
        else:
            print("Neni zadana cesta k CSV souboru s daty...")

    def ulozit_kontakty_csv(self):
        """"""
        if self.database is not []:
            ulozit_kontakty_csv(self.database,
                                file_path=self._csv_file_path,
                                delimiter=self.delimiter,
                                quotechar=self)
        else:
            print("Databaze neobsahuje zadna data neni co ukladat...")

    def setridit_kontakty(self):
        """"""
        if self.database is not []:
            self.database = setridit_kontakty(self.database)
        else:
            print("Databaze neobsahuje zadna data neni co tridit...")

    def vytvorit_kontakt(self, **kwargs):
        """"""
        vytvorit_kontakt(self.database, **kwargs)

    def smazat_kontakt(self, database_id):
        """"""
        smazat_kontakt(self.database, database_id)

    def najit_kontakt(self, **kwargs):
        """"""
        nalezene_kontakty = najit_kontakt(self.database, **kwargs)
        if nalezene_kontakty:
            for index, kontakt in nalezene_kontakty:
                self.detail_kontaktu(index)
        print(f"Nalezeno kontaktu: {len(nalezene_kontakty)}")

    def detail_kontaktu(self, database_id):
        """"""
        detail_kontaktu(self.database[database_id], database_id)

    def upravit_kontakt(self, database_id, **kwargs):
        """"""
        upravit_kontakt(self.database, database_id, **kwargs)

    def vypsat_kontakty(self):
        """"""
        if self.database is not []:
            vypsat_kontakty(self.database)
        else:
            print("Databaze neobsahuje zadna data neni co vypsat...")


if __name__ == "__main__":
    x = CsvContacts()
    x.nacist_kontakty_csv()
    x.setridit_kontakty()
    print("======== VYPIS KONTAKTU ========")
    x.vypsat_kontakty()
    print("======== VYHLEDAVAM ========")
    x.najit_kontakt(prijmeni='Novák')
