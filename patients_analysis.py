#Part 1: Understand the Data
#included in the Document

#Part 2: Data Acquisition
#Determine the structure of the data
#csv

#Import relevant modules
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
from datetime import date
from matplotlib import pyplot as plt

#Read data into script
pre_auth_file = input("Enter pre_auth file path:")
pre_auth = pd.read_csv(pre_auth_file)
#clean trailing space in column name
pre_auth.rename(columns = lambda x: x.strip(), inplace = True)

patients_with_appts_file = input("Enter patients_with_appts file path:")
patients_with_appts = pd.read_csv(patients_with_appts_file)
#clean trailing space in column name
patients_with_appts.rename(columns=lambda x: x.strip(), inplace= True)



#Part 3: Inspect Data

#Pre-Auth

#print first 5 rows
#print(pre_auth.head())
#print stats on columns (# of non null values)
#print(pre_auth.info())
#print # of rows and # of columns
#print(pre_auth.shape)

# 6 relevant columns: (PRE_AUTH_ID, PATIENT_ID, GENDER,
# CREATED_AT, DOB, COVERAGE_START_DATE)

#33238 rows(observations)


#Patients With Appts

#print first 5 rows
#print(patients_with_appts.head())
#print stats on columns (# of non null values)
#print(patients_with_appts.info())
#print # of rows and # of columns
#print(patients_with_appts.shape)

#4 relevant columns: (PATIENT_ID, FIRST_APPT_TIME_START,
# FIRST_NONCANCELLED_APPT_TIME_START, Source)
# Source column is not capitalized in title

# 23111 rows(observations)


#Part 4: Data Cleaning

#Pre Auth

#Remove duplicates
pre_auth = pre_auth.drop_duplicates()

#Reshape Data as necessary
#for now, determined it is not needed

#Remove unecessary columns
#print(pre_auth.columns)
pre_auth.drop("Unnamed: 6" ,axis =1, inplace = True)

#Check
#print(pre_auth.info())


#Clean up Data Types (if necessary)

#PRE_AUTH_ID should be stored as a categorical variable but stored as integer
pre_auth['PRE_AUTH_ID'] = pre_auth['PRE_AUTH_ID'].astype('string')
pre_auth['PRE_AUTH_ID'] = pre_auth['PRE_AUTH_ID'].replace(' ','')
#PATIENT_ID should be stored as a categorical variable but stored as float
#since has null values will change data type after split into two tables (pre-auth who booked
# and pre-auth who didn't book)
#Change data type of time variables
pre_auth['GENDER'] = pre_auth['GENDER'].astype('string')
pre_auth['CREATED_AT'] = pd.to_datetime(pre_auth['CREATED_AT'])
pre_auth['DOB'] = pd.to_datetime(pre_auth['DOB'])
pre_auth['COVERAGE_START_DATE'] = pd.to_datetime(pre_auth['COVERAGE_START_DATE'])

#Check datatypes changed
#print(pre_auth.info())


#how many rows and columns in dataset after -removing duplicates,
#unecessary columns, and changing data types?
#print("The pre-authorized dataset shape is " + str(pre_auth.shape))
#33238 rows and 6 columns


#Missing Data?
#non-null count doesn't match total # of observations for PATIENT_ID

#What type of missing data is it?
#It is structurally missing data, there is no PATIENT_ID if pre-authorized
#patient didn't book an appts

#Remove any trailing space in columns

#Separate into two tables

#First Table are pre-auth patients that booked an appt
pre_auth_book_appt = pre_auth[pre_auth['PATIENT_ID'].notna()]
pre_auth_book_appt['PATIENT_ID'] = pre_auth_book_appt['PATIENT_ID'].apply(np.int64)
pre_auth_book_appt['PATIENT_ID'] = pre_auth_book_appt['PATIENT_ID'].astype('string')
#Remove trailing space
pre_auth_book_appt['PATIENT_ID'] = pre_auth_book_appt['PATIENT_ID'].replace(' ','')
#Check if duplicates in PRE_AUTH_ID(unique identifier)
#print(pre_auth_book_appt[pre_auth_book_appt.duplicated(['PRE_AUTH_ID'])].count())
#Describe datatable
#print("The pre-authorized patients who booked appts dataset shape is " +str(pre_auth_book_appt.shape))
#23319 rows and 6 columns

#Check
#print(pre_auth_book_appt.info())

#Second Table are pre-auth patients that did not book an appt
pre_auth_didnt_book_appt = pre_auth[pre_auth['PATIENT_ID'].isna()]
pre_auth_didnt_book_appt['PATIENT_ID'] = pre_auth_didnt_book_appt['PATIENT_ID'].astype('string')
#Check if duplicates in PRE_AUTH_ID(unique identifier)
#print(pre_auth_didnt_book_appt[pre_auth_didnt_book_appt.duplicated(['PRE_AUTH_ID'])].count())
#Describe datatable
#print("The pre-authorized patients who didn't book appts dataset shape is " +str(pre_auth_didnt_book_appt.shape))
#9919 rows and 6 columns
#all PATIENT_ID values are NA, and cannot be stripped of trailing space

#Check
#print(pre_auth_didnt_book_appt.info())

#Does entries in both tables add up to entries in cleaned dataset?
#Check accounted for all data in pre_auth dataset
# pre_auth_tables_sum = pre_auth_book_appt.shape[0] + pre_auth_didnt_book_appt.shape[0]
# print(pre_auth_tables_sum == pre_auth.shape[0])
#printed True; good to move forward

#Check no overlap in pre-auth ID in two tables
#print( pre_auth['PRE_AUTH_ID'].nunique() == pre_auth_book_appt['PRE_AUTH_ID'].nunique()+ pre_auth_didnt_book_appt['PRE_AUTH_ID'].nunique())
#no overlap meaning no pre-auth patients repeated in book and didn't book
#print("The distinct PRE_AUTH_ID count for pre-auth patients that didn't book appointments is "+str(pre_auth_didnt_book_appt['PRE_AUTH_ID'].nunique()))


#Patients with Appts

#Remove duplicates
patients_with_appts = patients_with_appts.drop_duplicates()

#Reshape Data as necessary
#for now not determined it is needed

#print(patients_with_appts.columns)
#Remove unecessary columns
patients_with_appts.drop("Unnamed: 4" ,axis =1, inplace = True)

#Check
#print(patients_with_appts.info())
#Clean up Data Types

#PATIENT_ID incorrectly stored as a numerical variable, when shoould be stored as categorical
patients_with_appts['PATIENT_ID'] = patients_with_appts['PATIENT_ID'].astype('string')
#clean trailing space from PATIENT_ID:
patients_with_appts['PATIENT_ID'] = patients_with_appts['PATIENT_ID'].replace(' ','')
#Change Data Type for Time Variables
#remove Z at the end of the time columns
patients_with_appts['FIRST_APPT_TIME_START'] = patients_with_appts['FIRST_APPT_TIME_START'].replace('Z','')
patients_with_appts['FIRST_NONCANCELLED_APPT_TIME_START'] = patients_with_appts['FIRST_NONCANCELLED_APPT_TIME_START'].replace('Z','')
patients_with_appts['FIRST_APPT_TIME_START'] = pd.to_datetime(patients_with_appts['FIRST_APPT_TIME_START'])
# due to error ValueError: day is out of range for month; used error ='coerce' changing those dates to NaT
patients_with_appts['FIRST_NONCANCELLED_APPT_TIME_START'] = pd.to_datetime(patients_with_appts['FIRST_NONCANCELLED_APPT_TIME_START'], errors = 'coerce')
#print(patients_with_appts['FIRST_APPT_TIME_START'])
#print(patients_with_appts['FIRST_NONCANCELLED_APPT_TIME_START'])

#Check
#print(patients_with_appts.info())

#how many rows and columns in dataset after -removing duplicates,
#unecessary columns, and changing column type?
#print(patients_with_appts.shape)

#Missing Data?
#Value counts equal total number of observations (23111) except for Source

#Separate into table with Source and table without Source

#Check categories available
#print (patients_with_appts['Source'].value_counts())

# one row with Source as 'B'; assumed as 'db', will replace
patients_with_appts['Source'] = patients_with_appts['Source'].replace('B','db')

#Checked that there is no double source listed for one patient
#and that the distinct PATIENT_ID counts equal to the distinct 
# PATIENT_ID count of the dataset

#three tables to split into
# #Patients with Appts: Source is pre-auth
# patients_with_appts_Source_pre_auth = patients_with_appts[patients_with_appts['Source'] == 'pre-auth']
# #Patients with Appts: Source is direct booking
# patients_with_appts_Source_db = patients_with_appts[patients_with_appts['Source'] == 'db']
# #Patients with Appts with no Source:
# patients_with_appts_no_source = patients_with_appts[patients_with_appts['Source'].isna()]

#Check no overlap in PATIENT ID between Sources
# print(patients_with_appts['PATIENT_ID'].nunique() == 
#       patients_with_appts_Source_pre_auth['PATIENT_ID'].nunique() +
#       patients_with_appts_Source_db['PATIENT_ID'].nunique() +
#       patients_with_appts_no_source['PATIENT_ID'].nunique())
#printed True, no overlap in PATIENT ID between Sources


#distinct PATIENT_ID count in patients_with_appts
num_patients_with_appts = patients_with_appts['PATIENT_ID'].nunique()

#Part 5: Exploratory Data Analysis/Data Visualization

#Question 1: Distinct Count

#is there an overlap in PATIENT_ID in the pre_auth dataset and patients with appts dataset?

#are there duplicate PATIENT_IDs in pre_auth_book_appts?
#print(pre_auth_book_appt[pre_auth_book_appt.duplicated(['PATIENT_ID'])].count())
#12 duplicates of PATIENT_ID
#print(pre_auth_book_appt[pre_auth_book_appt.duplicated(['PRE_AUTH_ID'])].count())
#no duplicates of PRE_AUTH_ID
#further investigation
#print duplicated rows
##print(pre_auth_book_appt[pre_auth_book_appt['PATIENT_ID'].isin(
#pre_auth_book_appt['PATIENT_ID'][pre_auth_book_appt['PATIENT_ID'].duplicated()])].sort_values('PATIENT_ID'))
# different PRE_AUTH patients have the same PATIENT_ID (that is an issue)
#Since don't have enough information and no clear other identifer to
# distinguish duplicates besides PRE_AUTH_ID which is not in patients_with_appts
#continue accordingly

#are there duplicate PATIENT_IDs in patients_with_appts?
#print(patients_with_appts[patients_with_appts.duplicated(['PATIENT_ID'])].count())
# no PATIENT_ID duplicates! Yay!

patient_id_overlap = pre_auth_book_appt.merge(patients_with_appts, on = 'PATIENT_ID', how ='inner')
#print(patient_id_overlap.shape)
#print(patient_id_overlap.info())
#contains null values for Source, non null value count is 22458 which is less than
# total row count of 22496
#print(patient_id_overlap.head())
#print(patient_id_overlap['Source'].value_counts())
#found out that Source is mislabeled as 'db' for pre-auth patients
# will relabel Source values as 'db' to 'pre-auth' in patients_with_appts
patient_id_overlap['Source'] = patient_id_overlap['Source'].str.replace('db','pre-auth')
#print(patient_id_overlap['Source'].value_counts())
#update patients_with_appts
patients_with_appts['Source'].update(patient_id_overlap['Source'])
#check updated
#print(patients_with_appts['Source'].value_counts())
#print(patient_id_overlap.info())
#print(patient_id_overlap[patient_id_overlap.duplicated(['PATIENT_ID'])].count())
#print(patient_id_overlap['PATIENT_ID'].nunique())
#print(patient_id_overlap['PRE_AUTH_ID'].nunique())

# TABLES FOR ANALYSIS 

# TABLE 1: PRE-AUTH PTS with no APPTS

# TABLE 2: PATIENT_ID_OVERLAP: PRE-AUTH PTS with APPTS overlap with
# patients_with_appts dataset on PATIENT_ID


# TABLE 3: PRE_AUTH PTS with APPTS no overlap
# pre_auth_book_appt updated with no overlap in PATIENT_ID with
# patients_with_appts dataset
# subtract merged dataset (patient_id_overlap) from pre_auth_book_appts
cond = pre_auth_book_appt['PATIENT_ID'].isin(patient_id_overlap['PATIENT_ID'])
pre_auth_book_appt.drop(pre_auth_book_appt[cond].index, inplace = True)
#print(pre_auth_book_appt.head())
#print(pre_auth_book_appt['PRE_AUTH_ID'].nunique())

# TABLE 4: PATIENTS WITH APPTS no overlap & Source == 'pre-auth'
# patients_with_appts updated with no overlap in PATIENT_ID with
# pre_auth dataset
# subtract merged dataset (patient_id_overlap) from patients_with_appts, and source as pre-auth
cond = patients_with_appts['PATIENT_ID'].isin(patient_id_overlap['PATIENT_ID'])
patients_with_appts.drop(patients_with_appts[cond].index, inplace = True)
pre_auth_patients_with_appts = patients_with_appts[patients_with_appts['Source']== 'pre-auth']
#print(pre_auth_patients_with_appts['PATIENT_ID'].nunique())

# TABLE 5: PATIENTS WITH APPTS no overlap & Source == 'db'
db_appts = patients_with_appts[patients_with_appts['Source'] == 'db']
#print(db_appts['PATIENT_ID'].nunique())

# TABLE 6: PATIENTS WITH APPTS no overlap & Source == null
unknown_appts = patients_with_appts[patients_with_appts['Source'].isna()]
#print(unknown_appts['PATIENT_ID'].nunique())

#Check if data in pre_auth was missed
#print(pre_auth['PRE_AUTH_ID'].nunique() == patient_id_overlap['PRE_AUTH_ID'].nunique()+
#pre_auth_book_appt['PRE_AUTH_ID'].nunique() +
#pre_auth_didnt_book_appt['PRE_AUTH_ID'].nunique())
# printed True, good to proceed


#Check if data in patients_with_appts was missed
#print( num_patients_with_appts == patient_id_overlap['PATIENT_ID'].nunique()+
#pre_auth_patients_with_appts['PATIENT_ID'].nunique()
#+ db_appts['PATIENT_ID'].nunique() + unknown_appts['PATIENT_ID'].nunique())
# printed True, good to proceed


#Pre-Auth Patients: Distinct Count
#This includes all pre-authorized patients (ones that booked an appt, and ones that didnt book an appt)
pre_auth_pts_distinct = (patient_id_overlap['PRE_AUTH_ID'].nunique() + pre_auth_book_appt['PRE_AUTH_ID'].nunique()
+ pre_auth_didnt_book_appt['PRE_AUTH_ID'].nunique() + pre_auth_patients_with_appts['PATIENT_ID'].nunique())
#patients_with_appts_pre_auth_nomerge = 
print(" The pre-authorized patients distinct count is: " + str(pre_auth_pts_distinct))
#Direct Booking Patients: Distinct Count
#This sheet includes all patients (pre-auth and direct booking) that have booked an appt
#Separate pre-auth from direct booking

#21830 pre-auth patients booked appts according to patients_with_appts dataset
#Note: one row with value of 'B' not sure if this is typo or not
#other two categories are pre-auth and db(direct booking)
directbooking_pts_distinct = db_appts['PATIENT_ID'].nunique()
print(" The direct booking patients distinct count is: " + str(directbooking_pts_distinct))

#Total Number of Patients (including those that didnt book)
total_pts = (pre_auth_pts_distinct + directbooking_pts_distinct + unknown_appts['PATIENT_ID'].nunique())
print(" The total patients distinct count is: " + str(total_pts))


#Question 2:
 
#Pre-AUTH patients
# a) What is the % of patients that have their first_appt_time_start within 1 week (<= 7 days)
# of their coverage_start_date?
# Provide numerator and denominator, and % 
print('PRE_AUTHORIZED PATIENTS')
#check for missing data
#print(len(patient_id_overlap[patient_id_overlap['COVERAGE_START_DATE'].isna()])/len(patient_id_overlap))
#print(len(patient_id_overlap[patient_id_overlap['FIRST_APPT_TIME_START'].isna()])/len(patient_id_overlap))
# both printed 0
#no missing data, good to move forward

#print(patient_id_overlap.columns)
patient_id_overlap['time_to_book_appts'] = (patient_id_overlap['FIRST_APPT_TIME_START']
                                - patient_id_overlap['COVERAGE_START_DATE'])
#
patient_id_overlap['time_to_book_appts'] = patient_id_overlap['time_to_book_appts'].astype('string')
patient_id_overlap['time_to_book_appts'] = patient_id_overlap['time_to_book_appts'].replace(' ','')
patient_id_overlap[['time_to_book_days','time_to_book_time']] = patient_id_overlap['time_to_book_appts'].str.split('days', expand = True)
#print(patient_id_overlap.head())
patient_id_overlap['time_to_book_days'] = patient_id_overlap['time_to_book_days'].astype(int)

book_appts_numerator = len(patient_id_overlap[(patient_id_overlap['time_to_book_days'] <= 7) & (patient_id_overlap['time_to_book_days'] >= 0)])
book_appts_denominator = len(patient_id_overlap[patient_id_overlap['time_to_book_days']>=0])

percent_book_appts = round(book_appts_numerator / book_appts_denominator * 100)
#print(percent_book_appts)
print(str(percent_book_appts) +"% of pre-authorized patients book their appointment within the first week.")



#b) What percent of patients end up rescheduling their first appointment?

#create table with all pre-auth patients

pre_auth_appts = pd.concat([patient_id_overlap, pre_auth_patients_with_appts])
#print(pre_auth_appts.head())
#print(pre_auth_appts.columns)

# check for missing data
#print(round(len(pre_auth_appts[pre_auth_appts['FIRST_NONCANCELLED_APPT_TIME_START'].isna()])/len(pre_auth_appts)*100))
#since 10% missing there is less confidence in the accuracy of this conclusion
# Ideally,this data should be obtained if possible.
# Since not enough information is known about the data to impute, these data points will be dropped, but a note
# will be made in the conclusion.

pre_auth_appts = pre_auth_appts.dropna(axis=0, subset=['FIRST_NONCANCELLED_APPT_TIME_START'])

pre_auth_rescheduled = pre_auth_appts.query('FIRST_APPT_TIME_START < FIRST_NONCANCELLED_APPT_TIME_START')


pre_auth_resched_numerator = len(pre_auth_rescheduled)
pre_auth_resched_denominator = len(pre_auth_appts)

percent_pre_auth_rescheduled = round(pre_auth_resched_numerator/pre_auth_resched_denominator *100)
print(str(percent_pre_auth_rescheduled) +"% of pre-authorized patients reschedule their appointment.")
pre_auth_rescheduled['time_to_resched'] = pre_auth_rescheduled['FIRST_NONCANCELLED_APPT_TIME_START'] - pre_auth_rescheduled['FIRST_APPT_TIME_START']
pre_auth_rescheduled['time_to_resched'] = pre_auth_rescheduled['time_to_resched'].astype(str).str.replace(' ','')
pre_auth_rescheduled[['time_to_resched_days','time_to_resched_time']] = pre_auth_rescheduled['time_to_resched'].str.split('days', expand = True)
pre_auth_rescheduled['time_to_resched_days'] = pre_auth_rescheduled['time_to_resched_days'].astype(int)
avg_days_resched_pre_auth = pre_auth_rescheduled['time_to_resched_days'].mean()
#print(pre_auth_rescheduled['FIRST_NONCANCELLED_APPT_TIME_START'])
#print(pre_auth_rescheduled.head())
print("The average days for rescheduling for pre-authorized patients are " + str(round(avg_days_resched_pre_auth)) +" day(s).")

# total_pre_auth_patients_with_appts = pd.concat([patient_id_overlap[['PATIENT_ID',
#                                             'FIRST_APPT_TIME_START', 'FIRST_NONCANCELLED_APPT_TIME_START',
#                                             'Source']], pre_auth_patients_with_appts])
# print(total_pre_auth_patients_with_appts.head())

#Direct Booking patients
# a) What is the % of patients that have their first_appt_time_start within 1 week (<= 7 days)
# of their coverage_start_date?
print('DIRECT BOOKING PATIENTS')
print('Not possible to answer this question since coverage start date is not given for direct booking patients.')

#b) What percent of patients end up rescheduling their first appointment?
# rescheduling means they have a first_noncancelled_time_start different from first_appt_time_start
# check for missing data
#print(round(len(db_appts[db_appts['FIRST_NONCANCELLED_APPT_TIME_START'].isna()])/len(db_appts)*100))
#since 4% missing, can drop these values based on principle: if there is less than 5% missing data, there is confidence in the
# statistical conclusion.
db_appts.dropna(axis= 0, subset=['FIRST_NONCANCELLED_APPT_TIME_START'])
db_rescheduled = db_appts.query('FIRST_APPT_TIME_START < FIRST_NONCANCELLED_APPT_TIME_START')

db_resched_numerator = len(db_rescheduled)
db_resched_denominator = len(db_appts)
percent_db_rescheduled = round(db_resched_numerator/db_resched_denominator * 100)
print(str(percent_db_rescheduled) +"% of direct booking patients reschedule their appointment.")
db_rescheduled['time_to_resched'] = db_rescheduled['FIRST_NONCANCELLED_APPT_TIME_START'] - db_rescheduled['FIRST_APPT_TIME_START']
db_rescheduled['time_to_resched'] = db_rescheduled['time_to_resched'].astype(str).str.replace(' ','')
db_rescheduled[['time_to_resched_days','time_to_resched_time']] = db_rescheduled['time_to_resched'].str.split('days', expand = True)
db_rescheduled['time_to_resched_days'] = db_rescheduled['time_to_resched_days'].astype(int)
avg_days_resched_db = db_rescheduled['time_to_resched_days'].mean()
#print(pre_auth_rescheduled['FIRST_NONCANCELLED_APPT_TIME_START'])
#print(pre_auth_rescheduled.head())
print("The average days for rescheduling for direct booking patients are " + str(round(avg_days_resched_db)) +" day(s).")



#Question 3:
# Gender is another dimension I focused on, in pre-authorized patients, since 
# gender information is not given for direct booking patients.

#Statistics to answer:

# What is the gender % of pre-authorized patients?

#check values in columns
#print(pre_auth['GENDER'].value_counts())
#if Gender = '0' ignore value
#print(round(1084/len(pre_auth['GENDER'])*100))
#3 %; '0' values will be dropped from dataset

pre_auth_female = pre_auth[pre_auth['GENDER']== 'Female']
pre_auth_male = pre_auth[pre_auth['GENDER']== 'Male']
percent_pre_auth_f = round(len(pre_auth_female)/(len(pre_auth_female)+len(pre_auth_male)) * 100)
percent_pre_auth_m = round(len(pre_auth_male)/(len(pre_auth_female)+len(pre_auth_male)) * 100)
print(str(percent_pre_auth_f)+ " % of pre-authorized patients are female.")
print(str(percent_pre_auth_m)+ " % of pre-authorized patients are male.")

# What % of pre-auth females and pre-auth males who book appts?
# a pre-auth patient who books an appt has a PATIENT_ID
percent_pre_auth_f_book = round(len(pre_auth_female[pre_auth_female['PATIENT_ID'].notna()])
                                /len(pre_auth_female)*100)      
percent_pre_auth_m_book = round(len(pre_auth_male[pre_auth_male['PATIENT_ID'].notna()])
                                /len(pre_auth_male)*100)
print(str(percent_pre_auth_f_book)+ " % of pre-authorized female patients book appointments.")
print(str(percent_pre_auth_m_book)+ " % of pre-authorized male patients book appointments.")

#Pie Chart for Pre-Auth Gender Distribution
plt.pie([percent_pre_auth_f, percent_pre_auth_m],labels =['Female', 'Male'], autopct = '%0.1f%%')
plt.title('Pre-Authorized Patients Gender Distribution')
plt.savefig('Pre_Auth_gender_dist.jpg')
plt.close()
#plt.show()

#What is the age distribution of pre-authorized female and pre-authorized male patients?

# Pre-Auth Females
#inspect DOB column
#print(pre_auth_female['DOB'])
today = pd.to_datetime('today').date()
today = pd.to_datetime(today)
pre_auth_female['Age'] = ((today - (pre_auth_female['DOB'][pre_auth_female['DOB'].notna()]))/365)
pre_auth_female['Age'] = pre_auth_female['Age'].astype(str)
pre_auth_female['Age'] = pre_auth_female['Age'].str.replace('days' ,'')
#print(pre_auth_female['Age'])
pre_auth_female[['Age (yrs)','time(ignore)']] = pre_auth_female['Age'].str.split('  ', expand = True)
#print(pre_auth_female['Age (yrs)'])
pre_auth_female['Age (yrs)'] = pre_auth_female['Age (yrs)'].astype(int)
# found negative age values, which is not possible unless data is entered wrong,
# so only including positive ages in dataset (above age 3, when cognisant)
pre_auth_female = pre_auth_female[pre_auth_female['Age (yrs)'] >= 3]
#permanent change to pre_auth_female dataset, keep in mind for future statistics

#print(pre_auth_female['Age (yrs)'])
#pre_auth_female['Age (yrs)'] = [x[0] for x in pre_auth_female['Age (yrs)']]
pre_auth_female_age_dist = round((pd.cut(pre_auth_female['Age (yrs)'],[3,14,21,30,40,50]).value_counts())/ len(pre_auth_female) * 100)
#% of pre-auth female patients are sorted based on most frequent age to least frequent age
print (pre_auth_female_age_dist)
ax = pre_auth_female_age_dist.plot.bar()
plt.title('Pre-Authorized Female Patients Age Distribution')
plt.xlabel('Age Range')
plt.xticks(rotation = 30)
plt.ylabel('%')
fig=ax.get_figure()
fig.savefig('Pre_Auth_Female_Age_Dist.jpg')
#plt.show()
plt.close()
# Pre-Auth Males
#inspect DOB column
#print(pre_auth_male['DOB'])
today = pd.to_datetime('today').date()
today = pd.to_datetime(today)
pre_auth_male['Age'] = ((today - pre_auth_male['DOB'])/365)
pre_auth_male['Age'] = pre_auth_male['Age'].astype(str)
pre_auth_male['Age'] = pre_auth_male['Age'].str.replace('days' ,'')
#print(pre_auth_male['Age'])
pre_auth_male[['Age (yrs)','time(ignore)']] = pre_auth_male['Age'].str.split('  ', expand = True)
#print(pre_auth_male['Age (yrs)'])
pre_auth_male['Age (yrs)'] = pre_auth_male['Age (yrs)'].astype(int)
# found negative age values, which is not possible unless data is entered wrong,
# so only including positive ages in dataset (above age 3, when cognisant)
pre_auth_male = pre_auth_male[pre_auth_male['Age (yrs)'] >= 3]
#permanent change to pre_auth_male dataset, keep in mind for future statistics

#print(pre_auth_male['Age (yrs)'])
#pre_auth_female['Age (yrs)'] = [x[0] for x in pre_auth_female['Age (yrs)']]
pre_auth_male_age_dist = round((pd.cut(pre_auth_male['Age (yrs)'],[3,14,21,30,40,50]).value_counts())/ len(pre_auth_male) * 100)
print(pre_auth_male_age_dist)
ax = pre_auth_male_age_dist.plot.bar(color ='orange')
plt.title('Pre-Authorized Male Patients Age Distribution')
plt.xlabel('Age Range')
plt.xticks(rotation = 30)
plt.ylabel('%')
fig=ax.get_figure()
fig.savefig('Pre_Auth_Male_Age_Dist.jpg')
#plt.show()
#% of pre-auth male patients are sorted based on most frequent age to least frequent age

