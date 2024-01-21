-- View data
SELECT *
FROM pre_auth_patients;

-- ***************************
-- DATA CLEANING -------------
-- ***************************

-- Remove duplicate rows
DROP TABLE IF EXISTS pre_auth_patients_cleaned;
CREATE TABLE pre_auth_patients_cleaned AS
SELECT DISTINCT *
FROM pre_auth_patients;

-- View data
SELECT * FROM pre_auth_patients_cleaned;


--Renaming columns is not necessary

--Determine % missing data for all columns
DROP TABLE IF EXISTS pre_auth_null_counts;
CREATE TABLE pre_auth_null_counts AS
SELECT 'pre_auth_id'as column_name, (COUNT(*)-COUNT(pre_auth_id))::float/ (COUNT(*))*100 AS null_percent 
FROM pre_auth_patients_cleaned
UNION ALL
SELECT 'patient_id' as column_name, (COUNT(*)-COUNT(patient_id))::float/ (COUNT(*))*100 AS null_percent 
FROM pre_auth_patients_cleaned
UNION ALL
SELECT 'gender' as column_name, (COUNT(*)-COUNT(gender))::float/ (COUNT(*))*100 AS null_percent 
FROM pre_auth_patients_cleaned
UNION ALL
SELECT 'created_at' as column_name, (COUNT(*)-COUNT(created_at))::float/ (COUNT(*))*100 AS null_percent 
FROM pre_auth_patients_cleaned
UNION ALL
SELECT 'dob'as column_name, (COUNT(*)-COUNT(dob))::float/ (COUNT(*))*100 AS null_percent 
FROM pre_auth_patients_cleaned
UNION ALL
SELECT 'coverage_start_date'as column_name, (COUNT(*)-COUNT(coverage_start_date))::float/ (COUNT(*))*100 AS null_percent FROM pre_auth_patients_cleaned;

--View null counts with more than 5% missing data
UPDATE pre_auth_null_counts
SET null_percent = ROUND(null_percent);

SELECT *
FROM pre_auth_null_counts
WHERE null_percent > 5
ORDER BY null_percent DESC;

--since no column with more than 60% missing data, no effect on statistical conclusion

--Change column types?
--Convert DOB to Date

--Patients with Appts 
-- View data
SELECT *
FROM patients_with_appts;

-- ***************************
-- DATA CLEANING -------------
-- ***************************

-- Remove duplicate rows
DROP TABLE IF EXISTS patients_with_appts_cleaned;
CREATE TABLE patients_with_appts_cleaned AS
SELECT DISTINCT *
FROM patients_with_appts;

-- View data
SELECT * FROM patients_with_appts_cleaned;

--Renaming columns is not necessary

--Determine % missing data for all columns
DROP TABLE IF EXISTS patients_with_appts_null_counts;
CREATE TABLE patients_with_appts_null_counts AS
SELECT 'patient_id' as column_name, (COUNT(*)-COUNT(patient_id))::float/ (COUNT(*))*100 AS null_percent 
FROM patients_with_appts_cleaned
UNION ALL
SELECT 'first_appt_time_start' as column_name, (COUNT(*)-COUNT(first_appt_time_start))::float/ (COUNT(*))*100 AS null_percent 
FROM patients_with_appts_cleaned
UNION ALL
SELECT 'first_noncancelled_appt_time_start' as column_name, (COUNT(*)-COUNT(first_noncancelled_appt_time_start))::float/ (COUNT(*))*100 AS null_percent FROM patients_with_appts_cleaned
UNION ALL
SELECT 'source'as column_name, (COUNT(*)-COUNT(source))::float/ (COUNT(*))*100 AS null_percent 
FROM patients_with_appts_cleaned;

--View null counts with more than 5% missing data
UPDATE patients_with_appts_null_counts
SET null_percent = ROUND(null_percent);

SELECT *
FROM patients_with_appts_null_counts
WHERE null_percent > 5
ORDER BY null_percent DESC;


--Exploratory Data Analysis

-- Distinct patient counts (pre_auth patients, direct booking patients, all patients)
-- define pre-auth patients as those in pre_auth_patients dataset and source as pre-auth in patients with appts dataset, no overlap
-- define direct booking patients as those with source = db in patients with appts dataset
-- total patient count

--SELECT (SELECT COUNT(DISTINCT(PRE_AUTH_ID))
--FROM pre_auth_patients_cleaned) +  ;




