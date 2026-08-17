SELECT COUNT(*) AS total_internships
FROM internships;

SELECT 
    Work_Mode,
    COUNT(*) AS internship_count
FROM internships
GROUP BY Work_Mode
ORDER BY internship_count DESC;

SELECT 
    Internship_Type,
    COUNT(*) AS internship_count
FROM internships
GROUP BY Internship_Type
ORDER BY internship_count DESC;


SELECT 
    State_Clean,
    COUNT(*) AS internship_count
FROM internships
GROUP BY State_Clean
ORDER BY internship_count DESC
LIMIT 10;


SELECT 
    s.Skills,
    COUNT(*) AS requirement_count
FROM skills s
JOIN internships i
    ON s.Internship_id = i.Internship_id
GROUP BY s.Skills
ORDER BY requirement_count DESC
LIMIT 10;

SELECT 
    Attribute,
    COUNT(*) AS skill_requirement_count
FROM skills
GROUP BY Attribute
ORDER BY skill_requirement_count DESC;

SELECT
    Internship_Title,
    Company_Name,
    City_Clean,
    Stipend_Midpoint
FROM internships
WHERE Work_Mode = 'Remote'
ORDER BY Stipend_Midpoint DESC
LIMIT 20;

SELECT
    Internship_Title,
    Company_Name,
    Work_Mode,
    Stipend_Midpoint
FROM internships
WHERE Stipend_Midpoint > 20000
ORDER BY Stipend_Midpoint DESC
LIMIT 20;

SELECT
    Work_Mode,
    COUNT(*) AS internship_count
FROM internships
WHERE Stipend_Midpoint > 20000
GROUP BY Work_Mode
ORDER BY internship_count DESC;

USE internship_market;

SELECT COUNT(*) AS internship_count
FROM internships;

SELECT
    COUNT(*) AS total_rows,
    COUNT(Stipend_Midpoint) AS stipend_midpoint_count,
    COUNT(Has_Stipend) AS has_stipend_count,
    COUNT(Skill_Count) AS skill_count_rows
FROM internships;

SELECT
    Internship_Title,
    Company_Name,
    Work_Mode,
    Stipend_Midpoint
FROM internships
WHERE Stipend_Midpoint > 20000
ORDER BY Stipend_Midpoint DESC
LIMIT 20;


USE internship_market;

SELECT
    COUNT(*) AS Total_Internships,
    COUNT(DISTINCT Company_Name) AS Total_Companies,
    COUNT(DISTINCT City_Clean) AS Total_Cities,
    COUNT(DISTINCT Source_Platform) AS Total_Platforms
FROM internships;

SELECT
    Work_Mode,
    COUNT(*) AS Internship_Count
FROM internships
GROUP BY Work_Mode
ORDER BY Internship_Count DESC;

SELECT
    Internship_Type,
    COUNT(*) AS Internship_Count
FROM internships
GROUP BY Internship_Type
ORDER BY Internship_Count DESC;


SELECT
    City_Clean,
    COUNT(*) AS Internship_Count
FROM internships
WHERE City_Clean IS NOT NULL
  AND City_Clean <> 'Not Specified'
GROUP BY City_Clean
ORDER BY Internship_Count DESC
LIMIT 10;

SELECT
    COUNT(Stipend_Midpoint) AS Paid_Internships,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend,
    MIN(Stipend_Midpoint) AS Minimum_Stipend,
    MAX(Stipend_Midpoint) AS Maximum_Stipend
FROM internships
WHERE Stipend_Midpoint IS NOT NULL;

WITH ranked AS (
    SELECT
        Stipend_Midpoint,
        ROW_NUMBER() OVER (ORDER BY Stipend_Midpoint) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM internships
    WHERE Stipend_Midpoint IS NOT NULL
)
SELECT
    AVG(Stipend_Midpoint) AS Median_Stipend
FROM ranked
WHERE rn IN (
    FLOOR((total_rows + 1) / 2),
    CEIL((total_rows + 1) / 2)
);


-- HIGH STIPEND BY WORK MODE

SELECT
    Work_Mode,
    COUNT(*) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend,
    ROUND(MAX(Stipend_Midpoint), 2) AS Highest_Stipend
FROM internships
WHERE Stipend_Midpoint >= 50000
GROUP BY Work_Mode
ORDER BY Average_Stipend DESC;


-- HIGH STIPEND BY CITY

SELECT
    City_Clean,
    COUNT(*) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend,
    ROUND(MAX(Stipend_Midpoint), 2) AS Highest_Stipend
FROM internships
WHERE Stipend_Midpoint >= 50000
GROUP BY City_Clean
ORDER BY Average_Stipend DESC;

SELECT
    State_Clean,
    COUNT(*) AS Internship_Count
FROM internships
WHERE State_Clean <> 'Not Specified'
GROUP BY State_Clean
ORDER BY Internship_Count DESC
LIMIT 10;


SELECT
    State_Clean,
    COUNT(*) AS Internship_Count
FROM internships
WHERE State_Clean <> 'Not Specified'
GROUP BY State_Clean
ORDER BY Internship_Count DESC
LIMIT 10;


SELECT
    City_Clean,
    COUNT(*) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend
FROM internships
WHERE City_Clean <> 'Not Specified'
GROUP BY City_Clean
HAVING COUNT(*) >= 50
   AND AVG(Stipend_Midpoint) > 20000
ORDER BY Average_Stipend DESC;

SELECT
    COUNT(Stipend_Midpoint) AS Paid_Internships,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend,
    MIN(Stipend_Midpoint) AS Minimum_Stipend,
    MAX(Stipend_Midpoint) AS Maximum_Stipend
FROM internships
WHERE Stipend_Midpoint IS NOT NULL;

WITH ranked AS (
    SELECT
        Stipend_Midpoint,
        ROW_NUMBER() OVER (ORDER BY Stipend_Midpoint) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM internships
    WHERE Stipend_Midpoint IS NOT NULL
)
SELECT
    AVG(Stipend_Midpoint) AS Median_Stipend
FROM ranked
WHERE rn IN (
    FLOOR((total_rows + 1) / 2),
    CEIL((total_rows + 1) / 2)
);


SELECT
    CASE
        WHEN Stipend_Midpoint IS NULL THEN 'Not Specified'
        WHEN Stipend_Midpoint = 0 THEN 'Unpaid'
        WHEN Stipend_Midpoint < 10000 THEN 'Low'
        WHEN Stipend_Midpoint < 20000 THEN 'Medium'
        WHEN Stipend_Midpoint < 50000 THEN 'High'
        ELSE 'Very High'
    END AS Stipend_Category,
    COUNT(*) AS Internship_Count
FROM internships
GROUP BY Stipend_Category
ORDER BY Internship_Count DESC;


SELECT
    Work_Mode,
    COUNT(Stipend_Midpoint) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend,
    ROUND(MIN(Stipend_Midpoint), 2) AS Minimum_Stipend,
    ROUND(MAX(Stipend_Midpoint), 2) AS Maximum_Stipend
FROM internships
WHERE Stipend_Midpoint IS NOT NULL
GROUP BY Work_Mode
ORDER BY Average_Stipend DESC;

SELECT
    City_Clean,
    Work_Mode,
    COUNT(*) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend
FROM internships
WHERE Stipend_Midpoint IS NOT NULL
  AND City_Clean <> 'Not Specified'
GROUP BY City_Clean, Work_Mode
HAVING COUNT(*) >= 20
ORDER BY Average_Stipend DESC;


SELECT
    City_Clean,
    Work_Mode,
    Internship_Type,
    COUNT(*) AS Internship_Count,
    ROUND(AVG(Stipend_Midpoint), 2) AS Average_Stipend
FROM internships
WHERE Stipend_Midpoint IS NOT NULL
  AND City_Clean <> 'Not Specified'
GROUP BY
    City_Clean,
    Work_Mode,
    Internship_Type
HAVING COUNT(*) >= 10
ORDER BY
    Average_Stipend DESC,
    Internship_Count DESC;