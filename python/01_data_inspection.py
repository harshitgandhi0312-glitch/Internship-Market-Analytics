import pandas as pd


main_file = "data/raw/HR_Internship_SampleData.csv"
skills_file = "data/raw/HR_Internship_SampleData_Skills.csv"
education_file = "data/raw/HR_Internship_SampleData_Education.csv"

main_df = pd.read_csv(main_file)
skills_df = pd.read_csv(skills_file)
education_df = pd.read_csv(education_file)

# # Display basic information
# print("MAIN DATASET")
# print("Shape:", main_df.shape)
# print(main_df.head())

# print("\nSKILLS DATASET")
# print("Shape:", skills_df.shape)
# print(skills_df.head())

# print("\nEDUCATION DATASET")
# print("Shape:", education_df.shape)
# print(education_df.head())

print("\nMAIN DATASET COLUMNS")

print(main_df.columns.tolist())


print("\nSKILLS DATASET COLUMNS ")

print(skills_df.columns.tolist())


print("\nEDUCATION DATASET COLUMNS ")

print(education_df.columns.tolist())




print("\nMAIN DATA TYPES ")

print(main_df.dtypes)


print("\n SKILLS DATA TYPES ")

print(skills_df.dtypes)


print("\nEDUCATION DATA TYPES ")

print(education_df.dtypes)



print("\nMAIN MISSING VALUES ")

print(main_df.isnull().sum())


print("\n SKILLS MISSING VALUES ")

print(skills_df.isnull().sum())


print("\n EDUCATION MISSING VALUES ")

print(education_df.isnull().sum())




print("\n DUPLICATES ")

print("Main duplicates:", main_df.duplicated().sum())
print("Skills duplicates:", skills_df.duplicated().sum())
print("Education duplicates:", education_df.duplicated().sum())

print("\nUNIQUE VALUES")

print("\nWork Mode:")
print(main_df["Work_Mode"].value_counts(dropna=False))

print("\nInternship Type:")
print(main_df["Internship_Type"].value_counts(dropna=False))

print("\nDuration:")
print(main_df["Duration"].value_counts(dropna=False))

print("\nStipend Min:")
print(main_df["Stipend_Min"].value_counts(dropna=False).head(30))

print("\nStipend Max:")
print(main_df["Stipend_Max"].value_counts(dropna=False).head(30))

print("\nCompany Type:")
print(main_df["Company_Type"].value_counts(dropna=False))

print("\nDepartment:")
print(main_df["Department"].value_counts(dropna=False).head(30))

print("\nDUPLICATE SKILL RECORDS")

skill_duplicates = skills_df[
    skills_df.duplicated(keep=False)
]

print(skill_duplicates)

print("\nSKILL ATTRIBUTES ")

print(skills_df["Attribute"].value_counts())

print("\n TOP SKILLS ")

print(skills_df["Skills"].value_counts().head(30))

print("\n EDUCATION REQUIREMENTS ")

print(
    education_df["Education_Required"]
    .value_counts(dropna=False)
    .head(30)
)

print("\nALL NON-NUMERIC STIPEND MIN VALUES ")

stipend_min_numeric = pd.to_numeric(
    main_df["Stipend_Min"].astype(str).str.replace(",", ""),
    errors="coerce"
)

print(
    main_df.loc[
        stipend_min_numeric.isna() & main_df["Stipend_Min"].notna(),
        "Stipend_Min"
    ].unique()
)

print("\nALL NON-NUMERIC STIPEND MAX VALUES ")

stipend_max_numeric = pd.to_numeric(
    main_df["Stipend_Max"].astype(str).str.replace(",", ""),
    errors="coerce"
)

print(
    main_df.loc[
        stipend_max_numeric.isna() & main_df["Stipend_Max"].notna(),
        "Stipend_Max"
    ].unique()
)