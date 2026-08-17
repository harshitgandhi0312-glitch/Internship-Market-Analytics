USE internship_market;

LOAD DATA LOCAL INFILE 'D:/Internship-Market-Analytics/data/feature_engineered/internships_feature_engineered.csv'
INTO TABLE internships
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:/Internship-Market-Analytics/data/cleaned/skills_cleaned.csv'
INTO TABLE skills
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:/Internship-Market-Analytics/data/cleaned/education_cleaned.csv'
INTO TABLE education
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

USE internship_market;

SELECT COUNT(*) AS internship_count
FROM internships;

SELECT COUNT(*) AS skill_count
FROM skills;

SELECT COUNT(*) AS education_count
FROM education;


USE internship_market;

TRUNCATE TABLE internships;

USE internship_market;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE skills;
TRUNCATE TABLE education;
TRUNCATE TABLE internships;

SET FOREIGN_KEY_CHECKS = 1;

USE internship_market;

SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM skills;
DELETE FROM education;
DELETE FROM internships;

SET FOREIGN_KEY_CHECKS = 1;

SELECT
    (SELECT COUNT(*) FROM internships) AS internships_count,
    (SELECT COUNT(*) FROM skills) AS skills_count,
    (SELECT COUNT(*) FROM education) AS education_count;

DESCRIBE internships;