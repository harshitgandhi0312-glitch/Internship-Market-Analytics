import pandas as pd
import matplotlib.pyplot as plt

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


print("\nINTERNSHIP TYPES")

print(
    main_df["Internship_Type"]
    .value_counts()
)


print("\nWORK MODE ")

print(
    main_df["Work_Mode"]
    .value_counts()
)


print("\n COMPANY TYPES ")

print(
    main_df["Company_Type"]
    .value_counts()
)


print("\nTOP INTERNSHIP TITLES")

print(
    main_df["Internship_Title"]
    .value_counts()
    .head(20)
)

print("\nTOP STATES ")

print(
    main_df["State_Clean"]
    .value_counts()
    .head(20)
)

print("\n TOP CITIES ")

print(
    main_df["City_Clean"]
    .value_counts()
    .head(20)
)

print("\nSTIPEND OVERVIEW ")

print("Average Minimum Stipend:",
      main_df["Stipend_Min"].mean())

print("Median Minimum Stipend:",
      main_df["Stipend_Min"].median())

print("Average Maximum Stipend:",
      main_df["Stipend_Max"].mean())

print("Median Maximum Stipend:",
      main_df["Stipend_Max"].median())

print("Average Stipend:",
      main_df["Average_Stipend"].mean())

print("Median Stipend:",
      main_df["Average_Stipend"].median())


print("\nSTIPEND BY WORK MODE")

stipend_workmode = (
    main_df[
        main_df["Stipend_Status"] == "Paid"
    ]
    .groupby("Work_Mode")["Average_Stipend"]
    .agg(["count", "mean", "median"])
    .sort_values("median", ascending=False)
)

print(stipend_workmode)



print("\n STIPEND BY INTERNSHIP TYPE ")

stipend_type = (
    main_df[
        main_df["Stipend_Status"] == "Paid"
    ]
    .groupby("Internship_Type")["Average_Stipend"]
    .agg(["count", "mean", "median"])
    .sort_values("median", ascending=False)
)

print(stipend_type)

print("\n STIPEND BY DURATION ")

stipend_duration = (
    main_df[
        (main_df["Stipend_Status"] == "Paid") &
        (main_df["Duration_Months"].notna())
    ]
    .groupby("Duration_Months")["Average_Stipend"]
    .agg(["count", "mean", "median"])
    .sort_index()
)

print(stipend_duration)


print("\n STIPEND DATA COMPLETENESS ")

both = (
    main_df["Stipend_Min"].notna() &
    main_df["Stipend_Max"].notna()
).sum()

only_min = (
    main_df["Stipend_Min"].notna() &
    main_df["Stipend_Max"].isna()
).sum()

only_max = (
    main_df["Stipend_Min"].isna() &
    main_df["Stipend_Max"].notna()
).sum()

neither = (
    main_df["Stipend_Min"].isna() &
    main_df["Stipend_Max"].isna()
).sum()

print("Both Min & Max:", both)
print("Only Min:", only_min)
print("Only Max:", only_max)
print("Neither:", neither)

main_df["Average_Stipend"] = (
    main_df["Stipend_Min"] + main_df["Stipend_Max"]
) / 2

# If only minimum stipend is available,
# use minimum as the available stipend value
main_df["Average_Stipend"] = main_df["Average_Stipend"].fillna(
    main_df["Stipend_Min"]
)


workmode_stipend = (
    main_df[
        (main_df["Stipend_Status"] == "Paid") &
        (main_df["Work_Mode"] != "Not Specified")
    ]
    .groupby("Work_Mode")["Average_Stipend"]
    .median()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

workmode_stipend.plot(kind="bar")

plt.title("Median Internship Stipend by Work Mode")
plt.xlabel("Work Mode")
plt.ylabel("Median Stipend (₹)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "reports/figures/stipend_by_work_mode.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n TOP 20 SKILLS ")

top_skills = (
    skills_df["Skills"]
    .value_counts()
    .head(20)
)

print(top_skills)


print("\n SKILL CATEGORIES ")

skill_categories = (
    skills_df["Attribute"]
    .value_counts()
)

print(skill_categories)


top_10_skills = (
    skills_df["Skills"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

top_10_skills.plot(kind="barh")

plt.title("Top 10 Skills Required for HR Internships")
plt.xlabel("Number of Internship Listings")
plt.ylabel("Skill")

plt.tight_layout()

plt.savefig(
    "reports/figures/top_10_skills.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


skill_categories = (
    skills_df["Attribute"]
    .value_counts()
)

plt.figure(figsize=(8, 5))

skill_categories.plot(kind="bar")

plt.title("Skill Categories in HR Internship Listings")
plt.xlabel("Skill Category")
plt.ylabel("Number of Skill Requirements")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "reports/figures/skill_categories.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


major_titles = [
    "HR Operations Intern",
    "HR Intern",
    "Talent Acquisition Intern",
    "Learning & Development Intern",
    "Recruitment Intern"
]

for title in major_titles:

    print(f"\n {title.upper()} ")

    title_skills = (
        skills_df[
            skills_df["Internship_Title"] == title
        ]["Skills"]
        .value_counts()
        .head(10)
    )

    print(title_skills)


    print("\n SKILLS VS STIPEND ")

# Keep only internships with a paid stipend
paid_internships = main_df[
    (main_df["Stipend_Status"] == "Paid") &
    (main_df["Average_Stipend"].notna())
][
    ["Internship_id", "Average_Stipend"]
]

# Join skills with stipend information
skills_stipend = skills_df.merge(
    paid_internships,
    on="Internship_id",
    how="inner"
)

# Calculate skill demand and stipend
skill_stipend_analysis = (
    skills_stipend
    .groupby("Skills")
    .agg(
        Internship_Count=("Internship_id", "nunique"),
        Median_Stipend=("Average_Stipend", "median"),
        Average_Stipend=("Average_Stipend", "mean")
    )
    .sort_values("Internship_Count", ascending=False)
)

# Only consider skills appearing in at least 20 internships
skill_stipend_analysis = skill_stipend_analysis[
    skill_stipend_analysis["Internship_Count"] >= 20
]

print(
    skill_stipend_analysis
    .sort_values("Median_Stipend", ascending=False)
    .head(20)
)

print("\n POPULAR SKILLS WITH STIPEND ")

popular_skills = skill_stipend_analysis[
    skill_stipend_analysis["Internship_Count"] >= 100
].sort_values(
    "Median_Stipend",
    ascending=False
)

print(popular_skills.head(20))


print("\n HIGH STIPEND INVESTIGATION ")

high_stipend = main_df[
    main_df["Average_Stipend"] >= 50000
].copy()

print("Number of internships with stipend >= ₹50,000:",
      len(high_stipend))

print("\nStipend distribution:")

print(
    high_stipend["Average_Stipend"]
    .describe()
)

print("\nTop high-stipend records:")

print(
    high_stipend[
        [
            "Internship_id",
            "Internship_Title",
            "Company_Name",
            "City_Clean",
            "Work_Mode",
            "Internship_Type",
            "Stipend_Min",
            "Stipend_Max",
            "Average_Stipend"
        ]
    ]
    .sort_values(
        "Average_Stipend",
        ascending=False
    )
    .head(30)
    .to_string(index=False)
)

high_stipend_skills = skills_stipend[
    skills_stipend["Average_Stipend"] >= 50000
]

print("\n SKILLS IN HIGH-STIPEND INTERNSHIPS ")

print(
    high_stipend_skills["Skills"]
    .value_counts()
    .head(20)
)


print("\n========== HIGH STIPEND BY SOURCE ==========")

print(
    high_stipend["Source_Platform"]
    .value_counts()
)

print("\n========== HIGH STIPEND BY INTERNSHIP TYPE ==========")

print(
    high_stipend["Internship_Type"]
    .value_counts()
)

print("\n========== HIGH STIPEND BY WORK MODE ==========")

print(
    high_stipend["Work_Mode"]
    .value_counts()
)

print("\n========== HIGH STIPEND BY CITY ==========")

print(
    high_stipend["City_Clean"]
    .value_counts()
    .head(20)
)


print("\n========== STIPEND PERCENTILES ==========")

print(
    main_df["Average_Stipend"]
    .describe(
        percentiles=[
            0.25,
            0.50,
            0.75,
            0.90,
            0.95,
            0.99
        ]
    )
)

print("\n========== HIGH STIPEND IDS ==========")

print(
    high_stipend[
        [
            "Internship_id",
            "Company_Name",
            "Stipend_Min",
            "Stipend_Max",
            "Average_Stipend",
            "Source_Platform"
        ]
    ]
    .sort_values(
        "Average_Stipend",
        ascending=False
    )
    .to_string(index=False)
)