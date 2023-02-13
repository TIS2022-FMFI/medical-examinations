# medical-examinations
Maintains information about workers medical examinations and notifies about upcoming examinations

# Import zamestnancov a ich prejdenych prehliadok z excelu
- excel sa musi nachadzat v priecinku excel s nazvom zamestnanci_prehliadky.xlsx
- spustime python script excelParserEmployee.py nachadzajuci sa v priecinku excel (script zmaze aktualnych zamestnancov a ich prejdene prehliadky)


# Nastavenie databazy
pripojenie na databazu sa nastavuje v subore prehliadky/settings.py
Tam upravime DATABASES na vlastne NAME, USER, PASSWORD, HOST a PORT