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

--30% missing data for patient_id

--since no column with more than 60% missing data, no effect on statistical conclusion

--Change column types?
--Convert DOB to Date


--view distinct values in Gender

SELECT DISTINCT(GENDER)
FROM pre_auth_patients_cleaned;
-- value as 0, this data will be ignored, since there is not enough information to impute


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

--View distinct values in source
SELECT DISTINCT(source)
FROM patients_with_appts_cleaned;
 --one value as B - do not know source of this patient without more information

 
--Exploratory Data Analysis

-- Distinct patient counts (pre_auth patients, direct booking patients, all patients)

-- define pre-auth patients as those in pre_auth_patients dataset and source as pre-auth in patients with appts dataset, no overlap

--Will need to merge pre-auth dataset with patients with appts dataset on Patient ID


SELECT
-- pre_auth_patients
(SELECT COUNT(DISTINCT(pre_auth_id)) FROM pre_auth_patients_cleaned)+
-- pre_auth patients with source as pre-auth
(SELECT COUNT(DISTINCT(patient_id)) FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id)
AND source ='pre-auth')
AS pre_auth_count;

-- 33238

-- define direct booking patients as patients not in pre_auth dataset and source not as 'pre-auth' 
-- all other sources assumed to be direct booking since there are only two sources where patients can book appointments

SELECT COUNT(DISTINCT(patient_id)) AS direct_booking_count FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id)
AND NOT source = 'pre-auth';

-- 625

-- total patient count
SELECT
(SELECT COUNT(DISTINCT (pre_auth_id)) FROM pre_auth_patients_cleaned)+
(SELECT COUNT(DISTINCT(patient_id)) AS direct_booking_count FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id))
AS total_count;

--33865












