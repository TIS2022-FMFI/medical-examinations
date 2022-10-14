DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
	id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	empployeeId VARCHAR(10) NOT NULL,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
	personalNumber VARCHAR(15) NOT NULL,
	comment TEXT(1000)
);

DROP TABLE IF EXISTS examinationType;
CREATE TABLE examinationType (
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS passedExaminations;
CREATE TABLE passedExaminations (
	id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	employeeId MEDIUMINT UNSIGNED NOT NULL,
	examinationTypeId SMALLINT UNSIGNED NOT NULL,
	FOREIGN KEY passedExaminationsFKemployeeId (employeeId)
		REFERENCES employees(id),
	FOREIGN KEY passedExaminationsFKexaminationTypeId (examinationTypeId)
		REFERENCES examinationType(id)
);