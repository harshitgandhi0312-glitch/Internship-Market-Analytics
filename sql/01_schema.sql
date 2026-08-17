CREATE DATABASE IF NOT EXISTS internship_market;

USE internship_market;

SELECT DATABASE();

SHOW DATABASES;

SHOW TABLES;

SHOW TABLES FROM internship_market;

CREATE TABLE internships (
    Internship_id VARCHAR(20) PRIMARY KEY,
    Internship_Title VARCHAR(255),
    Company_Name VARCHAR(255),
    Industry VARCHAR(255),
    Company_Type VARCHAR(100),
    Internship_Type VARCHAR(100),
    City VARCHAR(255),
    State VARCHAR(100),
    Work_Mode VARCHAR(100),
    Department VARCHAR(255),
    Duration VARCHAR(100),

    Stipend_Min DECIMAL(12,2),
    Stipend_Max DECIMAL(12,2),

    Source_Platform VARCHAR(100),
    Post_Link TEXT,

    Duration_Months DECIMAL(5,2),
    Duration_Category VARCHAR(50),

    Stipend_Status VARCHAR(50),
    Average_Stipend DECIMAL(12,2),

    City_Clean VARCHAR(255),
    State_Clean VARCHAR(100),
    Stipend_Flag VARCHAR(50),

    Stipend_Range DECIMAL(12,2),
    Stipend_Midpoint DECIMAL(12,2),

    Has_Stipend TINYINT,

    Is_Remote TINYINT,
    Is_Hybrid TINYINT,
    Is_Onsite TINYINT,

    Is_Full_Time TINYINT,
    Is_Part_Time TINYINT,

    Skill_Count INT,
    Technical_Skill_Count INT,
    Soft_Skill_Count INT,
    HR_Tool_Count INT,

    Education_Level VARCHAR(50)
);


CREATE TABLE skills (
    Internship_id VARCHAR(20),
    Internship_Title VARCHAR(255),
    Attribute VARCHAR(100),
    Skills VARCHAR(255),

    FOREIGN KEY (Internship_id)
        REFERENCES internships(Internship_id)
);


CREATE TABLE education (
    Internship_id VARCHAR(20),
    Internship_Title VARCHAR(255),
    Education_Required VARCHAR(255),

    FOREIGN KEY (Internship_id)
        REFERENCES internships(Internship_id)
);


SHOW VARIABLES LIKE 'local_infile';

SET GLOBAL local_infile = 1;

SHOW VARIABLES LIKE 'local_infile';

SELECT @@local_infile AS local_infile;