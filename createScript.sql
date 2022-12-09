DROP TABLE IF EXISTS rule, city, department, positionRule, shiftRule, hiddenRule, employee, examinationType, passedExamination, users, rulesExamination;

CREATE TABLE IF NOT EXISTS rule (
	id SERIAL NOT NULL PRIMARY KEY
);

CREATE table IF NOT EXISTS city (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL
);

CREATE table IF NOT EXISTS department (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT null,
	cityId INT NOT NULL REFERENCES city
);

CREATE table IF NOT EXISTS positionRule (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT null,
	departmentId INT NOT NULL REFERENCES department,
	ruleId INT NOT NULL REFERENCES rule
);

CREATE table IF NOT EXISTS shiftRule (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT null,
	ruleId INT NOT NULL REFERENCES rule
);

CREATE table IF NOT EXISTS hiddenRule (
	id SERIAL NOT NULL PRIMARY KEY,
	ruleId INT NOT NULL REFERENCES rule
);

CREATE table IF NOT EXISTS employee (
	id SERIAL NOT NULL PRIMARY KEY,
	empployeeId VARCHAR(10) NOT NULL,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
	personalNumber VARCHAR(15) NOT NULL,
	userComment TEXT,
	exceptionDate DATE, 					/* datum skoncenia vynimky */
	positionRuleId INT NOT NULL REFERENCES positionRule,
	shiftRuleId INT NOT NULL REFERENCES shiftRule,
	hiddenRuleId INT NOT NULL REFERENCES hiddenRule
);

CREATE TABLE IF NOT EXISTS examinationType (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	periodicity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS passedExamination (
	id SERIAL NOT NULL PRIMARY KEY,
	employeeId INT NOT NULL REFERENCES employee,
	examinationTypeId INT NOT NULL REFERENCES examinationType,
	date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
	id SERIAL NOT NULL PRIMARY KEY,
	email VARCHAR(100) NOT NULL,
	hashedPwd VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS rulesExamination (
    id SERIAL NOT NULL PRIMARY KEY,
    ruleId INT NOT NULL REFERENCES rule,
    examinationTypeId INT NOT NULL REFERENCES examinationType
);
