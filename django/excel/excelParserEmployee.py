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
from examinationType.models import ExaminationType
from passedExamination.models import PassedExaminations


class ExcelParserEmployee:
    def __init__(self, file_name='zamestnanci_prehliadky.xlsx'):
        self.workbook = load_workbook(file_name, data_only=True)     # data_only=True ignores loading formulas and loads only values
        self.sheet = self.workbook['zamestnanci']
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
        self.column_of_first_exam_type = self._get_column_number_of_header('Dátum poslednej prehliadky') + 1

        for cell in self.header_row_cells[self.column_of_first_exam_type-1:]:
            self.column_numbers[cell.value] = cell.column

        self.examination_type_objects_by_column_number = dict()

    def insert_employees_to_db(self):
        PassedExaminations.objects.all().delete()
        Employee.objects.all().delete()
        ExaminationType.objects.all().delete()


        self.insert_examination_types_to_db()

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


            for cell in row[self.column_of_first_exam_type-1:]:
                if cell.value is None:
                    continue

                print(cell.value)
                pe = PassedExaminations()

                pe.employeeId = e
                pe.examinationTypeId = self.examination_type_objects_by_column_number[cell.column]
                pe.date = cell.value

                pe.save()




    def insert_examination_types_to_db(self):
        periodicities = self._get_periodicities_of_examination_types()
        for cell in self.header_row_cells[self.column_of_first_exam_type-1:]:
            et = ExaminationType()
            name = cell.value
            et.name = name
            et.periodicity = periodicities[name]
            et.save()

            self.examination_type_objects_by_column_number[cell.column] = et

    def _get_periodicities_of_examination_types(self):
        periodicities = dict()
        for row in self.workbook['periodicity']:            # sheet with periodicities
            examination_type, periodicity = [_.value for _ in row]
            periodicities[examination_type] = periodicity
        return periodicities

    def _get_column_number_of_header(self, value):
        for cell in self.header_row_cells:
            if cell.value == value:
                return cell.column


a = ExcelParserEmployee()
a.insert_employees_to_db()

