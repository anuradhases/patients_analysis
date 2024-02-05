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
SELECT TO_VARCHAR(TO_DATE(dob,'MM/DD/YY'), 'YYYY-MM-DD')
FROM pre_auth_patients_cleaned;

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

-- ***************************
-- EXPLORATORY DATA ANALYSIS -------------
-- ***************************

-- Distinct patient counts (pre_auth patients, direct booking patients, all patients)

-- define pre-auth patients as those in pre_auth_patients dataset and source as pre-auth in patients with appts dataset, no overlap

--Will need to merge pre-auth dataset with patients with appts dataset on Patient ID
--Assumed all pre-auth patients come from pre-auth dataset and no additional pre-auth patients added to patients with appts dataset

SELECT COUNT(DISTINCT(pre_auth_id))AS pre_auth_count
FROM pre_auth_patients_cleaned;
-- 33238

-- define direct booking patients as patients not in pre_auth dataset 
-- all other sources assumed to be direct booking since there are only two sources where patients can book appointments
WITH db_patients AS (SELECT patient_id FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id))
SELECT COUNT(DISTINCT(patient_id))
FROM db_patients;
--627

-- total patient count
SELECT
(SELECT COUNT(DISTINCT (pre_auth_id)) FROM pre_auth_patients_cleaned)+
(WITH db_patients AS (SELECT patient_id FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id))
SELECT COUNT(DISTINCT(patient_id))
FROM db_patients) AS total_count;
-- AS total_count;
--33865

--(for each pre-auth and direct booking)
-- What is the % of patients that have their first_appt_time_start within 1 week (<= 7 days) of their coverage_start_date?
--denominator includes all pre_auth patients (including those that didn't book appointments)

-- for pre-auth patients, join on patient id from pre-auth table and patients with appts table
-- assume first_appt_time_start after coverage_start_date (logically)

SELECT
(SELECT COUNT(DISTINCT(pre_auth.patient_id))
FROM pre_auth_patients_cleaned pre_auth
JOIN patients_with_appts_cleaned p_appts
ON pre_auth.patient_id = p_appts.patient_id
WHERE (DATEDIFF (day, pre_auth.coverage_start_date, p_appts.first_appt_time_start)) <= 7) * 100
/ (SELECT COUNT(DISTINCT(pre_auth_id)) FROM pre_auth_patients_cleaned) AS pre_auth_percent;


-- direct booking are patients with no patient id in pre_auth table
-- not possible to answer this question for direct booking patients since coverage_start_date not provided
-- coverage_start_date only in pre_auth table

-- What percent of patients end up rescheduling their first appointment?
-- Rescheduled patients defined as first_non_cancelled_appt_time_start after first_appt_time_start
-- Denominator are patients that have scheduled an appt (value for first_appt_time_start)

-- pre-auth
SELECT
(SELECT COUNT (DISTINCT(pre_auth.patient_id))
FROM pre_auth_patients_cleaned pre_auth
JOIN patients_with_appts_cleaned p_appts
ON pre_auth.patient_id = p_appts.patient_id
WHERE p_appts.first_noncancelled_appt_time_start > p_appts.first_appt_time_start)/
(SELECT COUNT(DISTINCT(pre_auth.patient_id))
FROM pre_auth_patients_cleaned pre_auth
JOIN patients_with_appts_cleaned p_appts
ON pre_auth.patient_id = p_appts.patient_id
WHERE p_appts.first_appt_time_start IS NOT NULL)* 100 AS pre_auth_rescheduled;

-- 13.45% 

-- What is the average number of days for rescheduling their first appointment?

SELECT ROUND(AVG(DATEDIFF(day, p_appts.first_appt_time_start, p_appts.first_noncancelled_appt_time_start)))
AS average_days_reschedule_pre_auth
FROM patients_with_appts_cleaned p_appts
JOIN pre_auth_patients_cleaned pre_auth
ON p_appts.patient_id = pre_auth.patient_id
WHERE p_appts.first_noncancelled_appt_time_start > p_appts.first_appt_time_start
AND p_appts.first_appt_time_start IS NOT NULL;
--17 days


-- direct booking
WITH direct_booking_patients AS
(SELECT patient_id, first_noncancelled_appt_time_start, first_appt_time_start
FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS (SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id))
SELECT (SELECT COUNT(DISTINCT(patient_id))
FROM direct_booking_patients WHERE first_noncancelled_appt_time_start > first_appt_time_start)/
(SELECT COUNT(DISTINCT(patient_id)) FROM direct_booking_patients WHERE first_appt_time_start IS NOT NULL) * 100 AS db_rescheduled;

--9.57%

--Average # of days for rescheduling

SELECT ROUND(AVG(DATEDIFF(day, first_appt_time_start, first_noncancelled_appt_time_start)))
FROM patients_with_appts_cleaned p_appts
WHERE NOT EXISTS(SELECT patient_id FROM pre_auth_patients_cleaned pre_auth
WHERE pre_auth.patient_id = p_appts.patient_id)
AND first_noncancelled_appt_time_start > first_appt_time_start;

--13 days


-- What is the gender distribution (%female and % male) of pre_auth patients

-- check out distinct values for gender
SELECT DISTINCT(gender)
FROM pre_auth_patients_cleaned;
-- no null values
-- value of 0 will be included but not imputed, since not enough data to impute 

SELECT gender, ROUND(COUNT(DISTINCT(pre_auth_id))/(SELECT COUNT(DISTINCT(pre_auth_id))
FROM pre_auth_patients_cleaned) *100 ,2) AS pre_auth_gender_counts
FROM pre_auth_patients_cleaned
GROUP BY gender;
-- 66.15% female
-- 30.59% male
-- 3.26% unknown

-- What is the % of pre-auth females and % of pre-auth males who book appointments?
-- booking appointments defined as patient id in patients with appts dataset

SELECT gender, ROUND((COUNT(DISTINCT pre_auth_id, CASE WHEN EXISTS (SELECT patient_id FROM patients_with_appts_cleaned p_appts WHERE p_appts.patient_id = pre_auth_patients_cleaned.patient_id) THEN patient_id END)/ COUNT(DISTINCT pre_auth_id) * 100),2) AS percent_gender_booked
FROM pre_auth_patients_cleaned 
GROUP BY gender;

-- 70.46% females book
-- 64.56% males book
-- 40.68% unknown book




