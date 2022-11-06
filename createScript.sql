DROP TABLE IF EXISTS employees, examinationType, passedExaminations, users, ruletype, rules, rulesExaminations, employeesRules;


CREATE table IF NOT EXISTS employees (
	id SERIAL NOT NULL PRIMARY KEY,
	empployeeId VARCHAR(10) NOT NULL,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
	personalNumber VARCHAR(15) NOT NULL,
	userComment TEXT,
	expectionDate DATE 					/* datum skoncenia vynimky */
);

CREATE TABLE IF NOT EXISTS examinationType (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	periodicity INT NOT NULL
);


CREATE TABLE IF NOT EXISTS passedExaminations (
	id SERIAL NOT NULL PRIMARY KEY,
	employeeId INT NOT NULL REFERENCES employees,
	examinationTypeId INT NOT NULL REFERENCES examinationType,
	date DATE NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
	id SERIAL NOT NULL PRIMARY KEY,
	email VARCHAR(100) NOT NULL,
	hashedPwd VARCHAR(100) NOT NULL										/*upravit dlzku*/
);


CREATE TABLE IF NOT EXISTS ruleType (									/* co za typ pravidla (pozicia, zmennost, interne)*/
	id SERIAL NOT NULL PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rules (
	id SERIAL NOT NULL PRIMARY KEY,
	ruleTypeId INT NOT NULL REFERENCES ruletype,
	name TEXT NOT NULL,
	locality TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS rulesExaminations (
    id SERIAL NOT NULL PRIMARY KEY,
    ruleId INT NOT NULL REFERENCES rules,
    examinationTypeId INT NOT NULL REFERENCES examinationType
);

CREATE TABLE IF NOT EXISTS employeesRules (
    id SERIAL NOT NULL PRIMARY KEY,
    ruleId INT NOT NULL REFERENCES rules,
    employeeId INT NOT NULL REFERENCES employees
);



