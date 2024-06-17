import re
from collections import namedtuple
from pyisemail import is_email
from constants import *


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


ValidationErrors = namedtuple('ValidationErrors', CONTACT_VALIDATION_ERRORS)
ValidationErrors.__new__.__defaults__ = (False, False, False, False, None)  # Implicitní hodnoty


class ValidationResult:
    def __init__(self):
        self.valid = True
        self.errors = ValidationErrors()

    def add_error(self, field, error):
        self.valid = False
        errors_dict = self.errors._asdict()
        errors_dict[field] = error
        self.errors = ValidationErrors(**errors_dict)

    def is_valid(self):
        return self.valid

    def get_errors(self):
        return self.errors

    def __repr__(self):
        return f"ValidationResult(valid={self.valid}, errors={self.errors})"

    def __bool__(self):
        return self.valid

    def print_errors(self):
        """Print errors in human readable table on screen"""
        print("---------- ValidationResult errors ----------")
        parametr_column_width = len(max(CONTACT_VALIDATION_ERRORS, key=len))
        if not self.valid:
            for index, error in enumerate(CONTACT_VALIDATION_ERRORS):
                spaces_needed = parametr_column_width - len(error)
                print(f"| {error.upper()}{' ' * spaces_needed} | {self.errors[index] if self.errors[index] else '-'}")
        else:
            print("No errors found")
        print("---------------------------------------------")


def validate_contact_data(contact_data, minimal_data_fields=MINIMAL_DATA_FIELDS):
    validation_result = ValidationResult()

    # 1. Kontrola minimálních klíčů
    missing_fields = [field for field in minimal_data_fields if field not in contact_data]
    if missing_fields:
        validation_result.add_error('general', f"Chybí povinná pole: {', '.join(missing_fields)}")

    # 2. Kontrola zda alespoň jméno nebo příjmení je zadáno
    if not (contact_data.get('jmeno') or contact_data.get('prijmeni')):
        validation_result.add_error('general', "Musí být zadáno alespoň jméno nebo příjmení.")

    # 3. Validace emailu + telefonu -> alespon jeden musi byt zadan aby byl kontakt platny
    if not(contact_data.get('email') or contact_data.get('telefon')):
        validation_result.add_error('general', "Musí být zadáno alespoň email nebo telefon.")
    else:
        email = contact_data.get('email')
        if email:
            if not is_valid_email(email):
                validation_result.add_error('email', f"Neplatný email: {email}")

        # 4. Validace telefonního čísla
        telefon = contact_data.get('telefon')
        if telefon:
            if not re.match(r'^\+?\d{9,}$', telefon):
                validation_result.add_error('telefon', "Telefon musí obsahovat alespoň 9 číslic, ideálně s předvolbou státu (např. +420).")

    return validation_result


def normalize_contact_data(contact_data):
    """Normalize contact data like names tu capitalize and so on."""
    contact_data_to_string = {key: str(value) for key, value in contact_data.items() if key in CSV_FIELD_NAMES}
    normalized_data = {
        'jmeno':     contact_data_to_string['jmeno'].strip().capitalize() if contact_data_to_string.get('jmeno') else "",
        'prijmeni':  contact_data_to_string['prijmeni'].strip().capitalize() if contact_data_to_string.get('prijmeni') else "",
        'rozliseni': contact_data_to_string['rozliseni'].strip() if contact_data_to_string.get('rozliseni') else "",
        'email': contact_data_to_string['email'].strip() if contact_data_to_string.get('email') else "",
        'telefon':   contact_data_to_string['telefon'].strip() if contact_data_to_string.get('telefon') else "",
        }
    return normalized_data


if __name__ == '__main__':
    # Testování
    data = {
        'jmeno': 'Pavla',
        'prijmeni': 'Nováková',
        'rozliseni': '',
        'email': 'pavla@novakopvi.cz',
        'telefon': '987456321'
    }

    result = validate_contact_data(data)
    print(f"Data valid: {result.is_valid()}")
    print(result.errors)
    # Simple email validation
    print("VALIDATE EMAILS")
    print("simple: ", is_email('homera@klxxxsimpsons1.cz'))
    print("detail: ", is_email('homera@klxxxsimpsons1.cz', check_dns=True, diagnose=True))

