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
from rule.models import City, Department, Rule, PositionRule, ShiftRule


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
            'shift': self._get_column_number_of_header('Zmennosť'),
            'position': self._get_column_number_of_header('Pozícia'),
            'department': self._get_column_number_of_header('Oddelenie'),
            'city': self._get_column_number_of_header('Mesto'),
            'userComment': self._get_column_number_of_header('POZNÁMKA')
        }
        self.column_of_first_exam_type = self._get_column_number_of_header('Dátum poslednej prehliadky') + 1

        for cell in self.header_row_cells[self.column_of_first_exam_type-1:]:
            self.column_numbers[cell.value] = cell.column

        self.examination_type_objects_by_column_number = dict()

    def start(self):
        PassedExaminations.objects.all().delete()
        Employee.objects.all().delete()
        ExaminationType.objects.all().delete()

        self.insert_examination_types_to_db()
        self.insert_employees_to_db()

    def _get_or_create_position_rule(self, position_name, department_name, city_name):
        try:
            return PositionRule.objects.get(name=position_name)
        except PositionRule.DoesNotExist:
            department = self._get_or_create_department(department_name, city_name)
            rule = Rule()
            rule.save()
            pr = PositionRule()
            pr.name = position_name
            pr.departmentId = department
            pr.ruleId = rule
            pr.save()
            return pr

    def _get_or_create_department(self, department_name, city_name):
        try:
            return Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            city = self._get_or_create_city(city_name)
            d = Department()
            d.name = department_name
            d.cityId = city
            d.save()
            return d

    def _get_or_create_city(self, city_name):
        try:
            return City.objects.get(name=city_name)
        except City.DoesNotExist:
            city = City()
            city.name = city_name
            city.save()
            return city

    def _get_or_create_shift_rule(self, shift_rule_name):
        try:
            return ShiftRule.objects.get(name=shift_rule_name)
        except ShiftRule.DoesNotExist:
            rule = Rule()
            rule.save()
            sr = ShiftRule()
            sr.name = shift_rule_name
            sr.ruleId = rule
            sr.save()
            return sr


    def insert_employees_to_db(self):




        # skip first line in sheet (header)
        itersheet = iter(self.sheet)
        next(itersheet)
        for row in itersheet:
            position_name = next(filter(lambda x: x.column == self.column_numbers['position'], row)).value
            department_name = next(filter(lambda x: x.column == self.column_numbers['department'], row)).value
            city_name = next(filter(lambda x: x.column == self.column_numbers['city'], row)).value
            position_rule = self._get_or_create_position_rule(position_name, department_name, city_name)
            shift_rule_name = next(filter(lambda x: x.column == self.column_numbers['shift'], row)).value
            shift_rule = self._get_or_create_shift_rule(shift_rule_name)
            e = Employee()
            e.name = next(filter(lambda x: x.column == self.column_numbers['name'], row)).value
            e.surname = next(filter(lambda x: x.column == self.column_numbers['surname'], row)).value
            e.personalNumber = next(filter(lambda x: x.column == self.column_numbers['personalNumber'], row)).value
            e.userComment = next(filter(lambda x: x.column == self.column_numbers['userComment'], row)).value
            e.positionRuleId = position_rule
            e.shiftRuleId = shift_rule

            if any(elem is None for elem in [e.name, e.surname, e.personalNumber]):
                print('zle meno')
                continue
            e.save()

            for cell in row[self.column_of_first_exam_type-1:]:
                if cell.value is None:
                    continue

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
a.start()

