import pandas as pd
import os

main_file = "data/cleaned/internships_cleaned.csv"
skills_file = "data/cleaned/skills_cleaned.csv"
education_file = "data/cleaned/education_cleaned.csv"

main_df = pd.read_csv(main_file)
skills_df = pd.read_csv(skills_file)
education_df = pd.read_csv(education_file)

print("Datasets loaded successfully.")

print("Main:", main_df.shape)
print("Skills:", skills_df.shape)
print("Education:", education_df.shape)


main_df["Stipend_Range"] = (
    main_df["Stipend_Max"] - main_df["Stipend_Min"]
)

main_df["Stipend_Midpoint"] = (
    main_df["Stipend_Min"] + main_df["Stipend_Max"]
) / 2

main_df["Has_Stipend"] = (
    main_df["Average_Stipend"].notna()
).astype(int)


main_df["Is_Remote"] = (
    main_df["Work_Mode"] == "Remote"
).astype(int)

main_df["Is_Hybrid"] = (
    main_df["Work_Mode"] == "Hybrid"
).astype(int)

main_df["Is_Onsite"] = (
    main_df["Work_Mode"] == "On-site"
).astype(int)


main_df["Is_Full_Time"] = (
    main_df["Internship_Type"] == "Full-time"
).astype(int)

main_df["Is_Part_Time"] = (
    main_df["Internship_Type"] == "Part-time"
).astype(int)


skill_count = (
    skills_df
    .groupby("Internship_id")["Skills"]
    .nunique()
    .reset_index(name="Skill_Count")
)

main_df = main_df.merge(
    skill_count,
    on="Internship_id",
    how="left"
)

main_df["Skill_Count"] = (
    main_df["Skill_Count"]
    .fillna(0)
    .astype(int)
)


technical_skills = (
    skills_df[
        skills_df["Attribute"] == "Technical Skills"
    ]
    .groupby("Internship_id")["Skills"]
    .nunique()
    .reset_index(name="Technical_Skill_Count")
)

soft_skills = (
    skills_df[
        skills_df["Attribute"] == "Soft Skills"
    ]
    .groupby("Internship_id")["Skills"]
    .nunique()
    .reset_index(name="Soft_Skill_Count")
)

hr_tools = (
    skills_df[
        skills_df["Attribute"] == "HR Tools"
    ]
    .groupby("Internship_id")["Skills"]
    .nunique()
    .reset_index(name="HR_Tool_Count")
)

main_df = main_df.merge(
    technical_skills,
    on="Internship_id",
    how="left"
)

main_df = main_df.merge(
    soft_skills,
    on="Internship_id",
    how="left"
)

main_df = main_df.merge(
    hr_tools,
    on="Internship_id",
    how="left"
)

main_df[
    [
        "Technical_Skill_Count",
        "Soft_Skill_Count",
        "HR_Tool_Count"
    ]
] = main_df[
    [
        "Technical_Skill_Count",
        "Soft_Skill_Count",
        "HR_Tool_Count"
    ]
].fillna(0).astype(int)


def classify_education(value):

    if pd.isna(value):
        return "Not Specified"

    value = str(value).strip().lower()

    # PhD
    if "phd" in value:
        return "PhD"

    # Postgraduate / MBA
    elif (
        "mba" in value
        or "pgdm" in value
        or "master" in value
        or "post graduate" in value
        or "postgraduate" in value
    ):
        return "Postgraduate"

    # Diploma
    elif "diploma" in value:
        return "Diploma"

    # 12th
    elif "12th" in value:
        return "12th"

    # Graduate / Bachelor's
    elif (
        "bachelor" in value
        or "bba" in value
        or "b.com" in value
        or "btech" in value
        or "b.tech" in value
        or "bms" in value
        or "graduate" in value
        or "graduation" in value
        or "degree" in value
        or "business administration" in value
    ):
        return "Graduate"

    else:
        return "Other"


education_level = education_df[
    ["Internship_id", "Education_Required"]
].copy()

education_level["Education_Level"] = (
    education_level["Education_Required"]
    .apply(classify_education)
)

education_level = education_level[
    ["Internship_id", "Education_Level"]
].drop_duplicates(
    subset=["Internship_id"]
)

main_df = main_df.merge(
    education_level,
    on="Internship_id",
    how="left"
)

main_df["Education_Level"] = (
    main_df["Education_Level"]
    .fillna("Not Specified")
)

print("\n FEATURE ENGINEERING COMPLETE ")

print("\nNew columns:")

print(main_df.columns.tolist())

print("\nStipend features:")
print(
    main_df[
        [
            "Stipend_Range",
            "Stipend_Midpoint",
            "Has_Stipend"
        ]
    ].head()
)

print("\nSkill features:")
print(
    main_df[
        [
            "Skill_Count",
            "Technical_Skill_Count",
            "Soft_Skill_Count",
            "HR_Tool_Count"
        ]
    ].head()
)

print("\nEducation levels:")
print(
    main_df["Education_Level"].value_counts()
)

output_folder = "data/feature_engineered"

os.makedirs(output_folder, exist_ok=True)

output_path = (
    f"{output_folder}/internships_feature_engineered.csv"
)

main_df.to_csv(
    output_path,
    index=False
)

print("\nSaved:")
print(output_path)