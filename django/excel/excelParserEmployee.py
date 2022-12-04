from openpyxl import load_workbook

# toto bolo treba lebo mi import "from employee.models import Employee"
# hadzal error "django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS,
#               but settings are not configured. You must either define the environment variable
#               DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings."
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prehliadky.settings")
django.setup()

from employee.models import Employee


class ExcelParserEmployee:
    def __init__(self, file_name='zamestnanci_prehliadky.xlsx'):
        workbook = load_workbook(file_name, data_only=True)     # data_only=True ignores loading formulas and loads only values
        self.sheet = workbook[workbook.sheetnames[0]]
        self.header_row_cells = self.sheet[1]

        self.column_numbers = {
            'employeeid': self._get_column_number_of_header('OC'),
            'surname': self._get_column_number_of_header('Priezvisko'),
            'name': self._get_column_number_of_header('Meno'),
            'personalNumber': self._get_column_number_of_header('Rodné číslo'),
            'zmennost': self._get_column_number_of_header('Zmennosť'),
            'pozicia': self._get_column_number_of_header('Pozícia'),
            'oddelenie': self._get_column_number_of_header('Oddelenie'),
            'pracovisko': self._get_column_number_of_header('Pracovisko'),
            'userComment': self._get_column_number_of_header('POZNÁMKA')
        }

        column_of_first_exam_type = self._get_column_number_of_header('Dátum poslednej prehliadky') + 1

    def insert_employees_to_db(self):
        # skip first line in sheet (header)
        itersheet = iter(self.sheet)
        next(itersheet)
        for row in itersheet:
            e = Employee()

            e.name = next(filter(lambda x: x.column == self.column_numbers['name'], row)).value
            e.surname = next(filter(lambda x: x.column == self.column_numbers['surname'], row)).value
            e.personalNumber = next(filter(lambda x: x.column == self.column_numbers['personalNumber'], row)).value
            e.userComment = next(filter(lambda x: x.column == self.column_numbers['userComment'], row)).value
            # e.exceptionExpirationDate

            if any(elem is None for elem in [e.name, e.surname, e.personalNumber]):
                print('zle meno')
                continue
            e.save()


    def _get_column_number_of_header(self, value):
        for cell in self.header_row_cells:
            if cell.value == value:
                return cell.column


a = ExcelParserEmployee()
a.get_employees()
