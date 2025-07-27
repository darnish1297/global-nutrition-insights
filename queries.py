queries = {
    # --- Obesity Queries ---
    "Top 5 Regions with Highest Obesity (2022)": """
        SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        WHERE Year = 2022
        GROUP BY Region
        ORDER BY Avg_Obesity DESC
        LIMIT 5;
    """,

    "Top 5 Countries with Highest Obesity": """
        SELECT Country, MAX(Mean_Estimate) AS High_Est
        FROM obesity
        GROUP BY Country
        ORDER BY High_Est DESC
        LIMIT 5;
    """,

    "Obesity Trend in India": """
        SELECT Year, Mean_Estimate
        FROM obesity
        WHERE Country = 'India'
        ORDER BY Year;
    """,

    "Average Obesity by Gender": """
        SELECT Gender, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Gender;
    """,

    "Country Count by Obesity Level and Age Group": """
    SELECT 
         age_group,
         CASE 
          WHEN Mean_Estimate < 10 THEN 'Low'
          WHEN Mean_Estimate BETWEEN 10 AND 20 THEN 'Medium'
          ELSE 'High'
        END AS Obesity_Level,
        COUNT(DISTINCT Country) AS Country_Count
       FROM obesity
    GROUP BY age_group, Obesity_Level
    ORDER BY age_group, Obesity_Level;
    """,

    "Top 5 Most/Least Reliable Countries by CI_Width": """
        SELECT Country, AVG(CI_Width) AS Avg_CI
        FROM obesity
        GROUP BY Country
        ORDER BY Avg_CI DESC
        LIMIT 5;

        SELECT Country, AVG(CI_Width) AS Avg_CI
        FROM obesity
        GROUP BY Country
        ORDER BY Avg_CI ASC
        LIMIT 5;
    """,

    "Average Obesity by Age Group": """
        SELECT age_group, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY age_group;
    """,

    "Top 10 Consistent Low-Obesity Countries": """
        SELECT Country, AVG(Mean_Estimate) AS Avg_Obesity, AVG(UpperBound - LowerBound) AS Avg_CI
        FROM obesity
        GROUP BY Country
        HAVING Avg_Obesity < 10 AND Avg_CI < 5
        ORDER BY Avg_Obesity ASC
        LIMIT 10;
    """,

    "Countries Where Female Obesity > Male by 5+": """
        SELECT f.Country, f.Year, (f.Mean_Estimate - m.Mean_Estimate) AS Gender_Gap
        FROM obesity f
        JOIN obesity m ON f.Country = m.Country AND f.Year = m.Year
        WHERE f.Gender = 'FEMALE' AND m.Gender = 'MALE'
          AND (f.Mean_Estimate - m.Mean_Estimate) > 5
        ORDER BY Gender_Gap DESC;
    """,

    "Global Average Obesity Per Year": """
        SELECT Year, AVG(Mean_Estimate) AS Global_Avg_Obesity
        FROM obesity
        GROUP BY Year
        ORDER BY Year;
    """,

    # --- Malnutrition Queries ---
    "Average Malnutrition by Age Group": """
        SELECT age_group, AVG(Mean_Estimate)
        FROM malnutrition
        GROUP BY age_group
        ORDER BY AVG(Mean_Estimate) DESC;
    """,

    "Top 5 Countries with Highest Malnutrition": """
        SELECT Country, ROUND(MAX(Mean_Estimate), 2) AS Max_Malnutrition
        FROM malnutrition
        GROUP BY Country
        ORDER BY Max_Malnutrition DESC
        LIMIT 5;
    """,

    "Malnutrition Trend in African Region Over the Years": """
        SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
        FROM malnutrition
        WHERE Region = 'Africa'
        GROUP BY Year
        ORDER BY Year;
    """,

    "Average Malnutrition by Gender": """
        SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Gender;
    """,

    "Malnutrition Level-Wise CI Width by Age Group": """
        SELECT age_group, ROUND(AVG(UpperBound - LowerBound), 2) AS Avg_CI_Width
        FROM malnutrition
        GROUP BY age_group
        ORDER BY Avg_CI_Width DESC;
    """,

    "Yearly Malnutrition Change in India, Nigeria, Brazil": """
        SELECT Country, Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
        FROM malnutrition
        WHERE Country IN ('India', 'Nigeria', 'Brazil')
        GROUP BY Country, Year
        ORDER BY Country, Year;
    """,

    "Regions with Lowest Malnutrition Averages": """
        SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Region
        ORDER BY Avg_Malnutrition ASC
        LIMIT 5;
    """,

    "Countries with Increasing Malnutrition Levels": """
        SELECT Country, MAX(Mean_Estimate), MIN(Mean_Estimate)
        FROM malnutrition
        GROUP BY Country
        HAVING (MAX(Mean_Estimate)-MIN(Mean_Estimate))>0
        ORDER BY (MAX(Mean_Estimate)-MIN(Mean_Estimate)) DESC
        LIMIT 10;
    """,

    "Year-wise Min/Max Malnutrition Comparison": """
        SELECT Year,
               MIN(Mean_Estimate) AS Min_Malnutrition,
               MAX(Mean_Estimate) AS Max_Malnutrition
        FROM malnutrition
        GROUP BY Year
        ORDER BY Year;
    """,

    "High CI Width Malnutrition Records (>5)": """
        SELECT Country, Year, age_group, ROUND(UpperBound - LowerBound, 2) AS CI_Width
        FROM malnutrition
        WHERE (UpperBound - LowerBound) > 5
        ORDER BY CI_Width DESC;
    """,

    # --- Combined Queries ---
    "Obesity vs Malnutrition Comparison by Country": """
        SELECT o.Country,AVG(o.Mean_Estimate),AVG(m.Mean_Estimate)
        FROM obesity o
        JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
        WHERE o.Country IN ('India', 'USA', 'Nigeria', 'Brazil', 'China')
        GROUP BY o.Country;
    """,

    "Gender-Based Obesity and Malnutrition Comparison": """
        SELECT o.Gender, o.Country, AVG(o.Mean_Estimate), AVG(m.Mean_Estimate)
        FROM obesity o
        JOIN malnutrition m ON o.Gender = m.Gender AND o.Country = m.Country AND o.Year = m.Year
        GROUP BY o.Gender, o.Country
        ORDER BY o.Country;
    """,

    "Region-Wise Obesity vs Malnutrition (Africa & Americas)": """
        SELECT o.Region,
               AVG(o.Mean_Estimate) AS Avg_Obesity,
               AVG(m.Mean_Estimate) AS Avg_Malnutrition
        FROM obesity o
        JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
        WHERE o.Region IN ('Africa', 'Americas')
        GROUP BY o.Region;
    """,

    "Countries with Obesity Up & Malnutrition Down": """
        SELECT o.Country,
               MAX(o.Mean_Estimate) - MIN(o.Mean_Estimate) AS Obesity_Change,
               MIN(m.Mean_Estimate) - MAX(m.Mean_Estimate) AS Malnutrition_Change
        FROM obesity o
        JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
        GROUP BY o.Country
        HAVING Obesity_Change > 0 AND Malnutrition_Change > 0;
    """,

    "Age-Wise Obesity vs Malnutrition Trends": """
        SELECT o.age_group, o.Country, o.Year,
               AVG(o.Mean_Estimate) AS Avg_Obesity,
               AVG(m.Mean_Estimate) AS Avg_Malnutrition
        FROM obesity o
        JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year AND o.age_group = m.age_group
        GROUP BY o.age_group;
    """
}
