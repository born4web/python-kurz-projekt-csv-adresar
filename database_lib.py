"""
Library for CSVContacts application with CSV storred data
and list of items as database simulation...
"""
import csv
from functools import partial
from validation import validate_contact_data, normalize_contact_data
from constants import *


def nacist_kontakty_csv(file_path="databanka.csv", delimiter=',', quotechar='"'):
    """Read database from CSV file and return it as list"""
    print_errors_header = True
    print("------------ Nacitam data do databaze kontaktu -------------")
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar)
        database = []
        for item in reader:
            normalized_data = normalize_contact_data(item)
            if validate_contact_data(normalized_data):
                database.append(normalize_contact_data(item))
            else:
                if print_errors_header:
                    print("-------------- Tato data jsou chybna --------------")
                    print_errors_header = False
                detail_kontaktu(item)
    print("----------------------- Data nactena -----------------------")
    return database


def ulozit_kontakty_csv(database, file_path="databanka1.csv", delimiter=',', quotechar='"'):
    """Ulozi obsah databanky do CSV souboru. Pozor dojde k prepsani puvodniho obsahu"""
    print("------------ Ukladam data do databaze kontaktu -------------")
    with open(file_path, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,
                                delimiter=delimiter,
                                quotechar=quotechar,
                                fieldnames=CSV_FIELD_NAMES)
        writer.writeheader()
        writer.writerows(database)
    print("----------------------- Data ulozena -----------------------")


def _print_contact_table_row(label: str, value: str):
    # Delka hodnoty
    len_value = len(value) if value else 0
    # Zarovnej label na fixní délku
    formatted_label = f"{label:<{CONTACT_LABEL_CHARACTER_LENGTH}}"
    # Vypočítej počet chybějících znaků pro vyplnění řádku
    spaces_needed = CONTACT_TABLE_CHARACTER_LENGTH - CONTACT_LABEL_CHARACTER_LENGTH - len_value - 5  # 5: '|' + ' ' + '|' + ' ' + '|'
    # Vytiskni řádek s vyplněnými mezerami
    print(f"| {formatted_label}| {value}{' ' * spaces_needed}|")


def detail_kontaktu(contact_data, database_id: int = None):
    """Formated print contact data as table on screen"""
    if contact_data:
        print("-"*CONTACT_TABLE_CHARACTER_LENGTH)
        if database_id is not None:
            _print_contact_table_row("ID", str(database_id))
            print("-" * CONTACT_TABLE_CHARACTER_LENGTH)
        _print_contact_table_row("Jmeno", contact_data['jmeno'])
        _print_contact_table_row("Prijmeni", contact_data['prijmeni'])
        _print_contact_table_row("Rozliseni", contact_data['rozliseni'])
        _print_contact_table_row("Email", contact_data['email'])
        _print_contact_table_row("Telefon", contact_data['telefon'])
        print("-"*CONTACT_TABLE_CHARACTER_LENGTH)


def vypsat_kontakty(database: []):
    """List all database contacts"""
    for index, contact in enumerate(database):
        # print(f"{index}. {contact}")
        detail_kontaktu(contact, index)


def smazat_kontakt(database: [], database_id: int):
    """Delete contact at index position"""
    if database:
        try:
            return database.pop(database_id)
        except IndexError:
            print(f"Neexistujici kontakt s ID: {database_id}")


def setridit_kontakty(database: []):
    """"""
    sorted_data = sorted(database, key=lambda x: (x['prijmeni'], x['jmeno']))
    return sorted_data


def porovnej_shodu_vsech_parametru(database_item, **kwargs):
    """Funkce porovna shodu kwargs predanych parametru s parametry daneho prvku databaze

    Vraci True/False podle toho zda vsechny predane kwargs parametry jsou obsazeny v prvku
    a to jak klice tak opdpovidajici hodnoty.

    Funkce je vhodna pro detekci duplicit nebo vyhledavani podle parametru
    """
    for key, value in kwargs.items():
        if key not in database_item:
            return False
        else:
            if database_item[key] != str(value):
                return False
    return True


def najit_kontakt(database, **kwargs):
    """Vyhleda podle predanych kriterii vsechny kontakty ktere jim vyhovuji

    :return: [] - neni [item1, item2,...] - pokud nalezne shody
    """
    result = [(index, contact) for index, contact in enumerate(database) if porovnej_shodu_vsech_parametru(contact, **kwargs)]

    # Vysledek
    return result


def _otestuj_duplicitni_kontakt(database, **kwargs):
    """Prohleda databazi a detekuje zda existuje duplicitni kontakt.
    Duplicita se testuje jako jedinecna kombinace: jmeno, prijmeni, rozliseni.

    :return: [] - neni duplicita [item, item,...] seznam duplicit
    """
    testovane_parametry = ['jmeno', 'prijmeni', 'rozliseni']
    redukovany_kontakt = {key: kwargs[key] for key in testovane_parametry if key in kwargs}

    # POUZITI PARTIAL KONCEPTU
    # testuj_duplicitu = partial(porovnej_shodu_vsech_parametru, **redukovany_kontakt)
    # result = list(filter(testuj_duplicitu, database))

    # Vysledek - PRI DEFAKTO POUZITI COMPREHENSION
    return najit_kontakt(database, **redukovany_kontakt)


def vytvorit_kontakt(database, **kwargs):
    """Vytvori komntakt z predanych parametru.
    Zaroven jsou otestovany minimalni parametry pro vytvoreni kontaktu."""
    normalized_data = normalize_contact_data(kwargs)
    validated_data = validate_contact_data(normalized_data)
    if not validated_data.valid:
        validated_data.print_errors()
    else:
        existuje_duplicita = _otestuj_duplicitni_kontakt(database, **normalized_data)
        if not existuje_duplicita:
            database.append(normalized_data)
        else:
            print(f"Zadany kontakt jiz v databazi existuje: {existuje_duplicita}")


def upravit_kontakt(database: [], database_id: int, **kwargs):
    """Delete contact at index position"""
    normalized_data = normalize_contact_data(kwargs)
    validated_data = validate_contact_data(normalized_data)
    if not validated_data.valid:
        validated_data.print_errors()
    else:
        try:
            database[database_id].update(normalized_data)
        except IndexError:
            print(f"Neexistujici kontakt s ID: {database_id}")


if __name__ == "__main__":
    # nacti kontakty
    databanka = nacist_kontakty_csv()

    # vytvorit kontakt
    test_data = {
        'jmeno': 'Lenka',
        'telefon': 753951654,
    }
    vytvorit_kontakt(databanka, **test_data)

    # setridit a vypsat kontakty
    serazene = setridit_kontakty(databanka)
    vypsat_kontakty(serazene)

    # uprava datoveho zaznamu
    test_data = {
        'jmeno': 'Lenka',
        'telefon': 753951654,
        'prijmeni': 'Novotná',
    }
    upravit_kontakt(serazene, 0, **test_data)
    vypsat_kontakty(serazene)
    print("KONEC")
