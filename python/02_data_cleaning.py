import pandas as pd
import os


main_file = "data/raw/HR_Internship_SampleData.csv"
skills_file = "data/raw/HR_Internship_SampleData_Skills.csv"
education_file = "data/raw/HR_Internship_SampleData_Education.csv"

output_folder = "data/cleaned"



main_df = pd.read_csv(main_file)
skills_df = pd.read_csv(skills_file)
education_df = pd.read_csv(education_file)

print("Main:", main_df.shape)
print("Skills:", skills_df.shape)
print("Education:", education_df.shape)

main_df.rename(
    columns={
        "Intrnship_Title": "Internship_Title"
    },
    inplace=True
)

skills_df.rename(
    columns={
        "Intrnship_Title": "Internship_Title"
    },
    inplace=True
)

education_df.rename(
    columns={
        "Intrnship_Title": "Internship_Title"
    },
    inplace=True
)

for df in [main_df, skills_df, education_df]:

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].str.strip()


work_mode_mapping = {
    "Work from Office": "On-site",
    "On-site": "On-site",
    "Onsite": "On-site",
    "Remote": "Remote",
    "Hybrid": "Hybrid",
    "Hybrid (mostly remote)": "Hybrid"
}

main_df["Work_Mode"] = main_df["Work_Mode"].replace(work_mode_mapping)

main_df["Work_Mode"] = main_df["Work_Mode"].fillna("Not Specified")


internship_type_mapping = {
    "Full-time Internship": "Full-time",
    "Full-time": "Full-time",
    "Full Time": "Full-time",
    "Part-time Internship": "Part-time",
    "Part-time": "Part-time",
    "Part Time": "Part-time"
}

main_df["Internship_Type"] = (
    main_df["Internship_Type"]
    .replace(internship_type_mapping)
    .fillna("Not Specified")
)


company_type_mapping = {
    "Startup (Early Stage)": "Startup",
    "Startup (Early Stage, 11-50 employees)": "Startup",
    "Startup (Early Stage, 51-200 employees)": "Startup",
    "Startup (1-10 employees)": "Startup",
    "Startup (201-500 employees)": "Startup",
    "Private Limited (201-500 employees)": "Private Limited"
}

main_df["Company_Type"] = (
    main_df["Company_Type"]
    .replace(company_type_mapping)
    .fillna("Not Specified")
)


def clean_duration(value):
    if pd.isna(value):
        return pd.NA

    value = str(value).strip().lower()

    # Handle clear numeric values
    if value.isdigit():
        return int(value)

    # Handle values like "3 months", "1 month"
    if "month" in value:
        number = value.split()[0]

        if number.isdigit():
            return int(number)

    # Handle ambiguous values
    return pd.NA


main_df["Duration_Months"] = main_df["Duration"].apply(clean_duration)

main_df["Duration_Months"] = pd.to_numeric(
    main_df["Duration_Months"],
    errors="coerce"
)

def duration_category(months):

    if pd.isna(months):
        return "Not Specified"

    if months <= 2:
        return "Short-term"

    elif months <= 4:
        return "Medium-term"

    elif months <= 6:
        return "Long-term"

    else:
        return "Extended"


main_df["Duration_Category"] = main_df["Duration_Months"].apply(
    duration_category
)

def get_stipend_status(row):
    min_value = row["Stipend_Min"]
    max_value = row["Stipend_Max"]

    # Explicitly unpaid
    if isinstance(min_value, str) and min_value.strip().lower() == "unpaid":
        return "Unpaid"

    # No stipend information
    if pd.isna(min_value) and pd.isna(max_value):
        return "Not Specified"

    return "Paid"


main_df["Stipend_Status"] = main_df.apply(
    get_stipend_status,
    axis=1
)


def clean_stipend(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    if value.lower() == "unpaid":
        return 0

    value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return pd.NA


main_df["Stipend_Min"] = main_df["Stipend_Min"].apply(clean_stipend)

main_df["Stipend_Max"] = main_df["Stipend_Max"].apply(clean_stipend)

main_df["Stipend_Min"] = pd.to_numeric(
    main_df["Stipend_Min"],
    errors="coerce"
)

main_df["Stipend_Max"] = pd.to_numeric(
    main_df["Stipend_Max"],
    errors="coerce"
)


main_df["Average_Stipend"] = (
    main_df["Stipend_Min"] + main_df["Stipend_Max"]
) / 2

# Standardize Attribute values
attribute_mapping = {
    "Technical Skill": "Technical Skills",
    "Technical Skills": "Technical Skills",
    "Soft Skill": "Soft Skills",
    "Soft Skills": "Soft Skills",
    "HR Tools": "HR Tools"
}

skills_df["Attribute"] = skills_df["Attribute"].replace(
    attribute_mapping
)

# Remove exact duplicate records
skills_df = skills_df.drop_duplicates()

print("\nSkills duplicates removed.")
print("New Skills shape:", skills_df.shape)


education_df["Education_Required_Raw"] = (
    education_df["Education_Required"]
)

education_df["Education_Required"] = (
    education_df["Education_Required"]
    .fillna("Not Specified")
)

city_mapping = {
    "Bangalore": "Bengaluru",
    "Bengaluru (Bangalore)": "Bengaluru",
    "Gurgaon": "Gurugram",
    "India": "Not Specified"
}

main_df["City_Clean"] = (
    main_df["City"]
    .replace(city_mapping)
    .fillna("Not Specified")
)


state_mapping = {
    "India": "Not Specified"
}

main_df["State_Clean"] = (
    main_df["State"]
    .replace(state_mapping)
    .fillna("Not Specified")
)

def stipend_flag(stipend):

    if pd.isna(stipend):
        return "Not Specified"

    elif stipend >= 50000:
        return "High Stipend"

    else:
        return "Normal"


main_df["Stipend_Flag"] = main_df["Average_Stipend"].apply(
    stipend_flag
)


os.makedirs(output_folder, exist_ok=True)

main_output = f"{output_folder}/internships_cleaned.csv"
skills_output = f"{output_folder}/skills_cleaned.csv"
education_output = f"{output_folder}/education_cleaned.csv"

main_df.to_csv(main_output, index=False)
skills_df.to_csv(skills_output, index=False)
education_df.to_csv(education_output, index=False)

print("\n CLEANING COMPLETE ")

print("Saved:", main_output)
print("Saved:", skills_output)
print("Saved:", education_output)


print("\n VALIDATION ")

print("\nMain Dataset:")
print(main_df.shape)

print("\nWork Mode:")
print(main_df["Work_Mode"].value_counts(dropna=False))

print("\nInternship Type:")
print(main_df["Internship_Type"].value_counts(dropna=False))

print("\nCompany Type:")
print(main_df["Company_Type"].value_counts(dropna=False))

print("\nStipend Status:")
print(main_df["Stipend_Status"].value_counts(dropna=False))

print("\nDuration:")
print(main_df["Duration_Months"].value_counts(dropna=False).sort_index())

print("\nDuration Category:")
print(main_df["Duration_Category"].value_counts())

print("\nSkills Dataset:")
print(skills_df.shape)

print("\nEducation Dataset:")
print(education_df.shape)