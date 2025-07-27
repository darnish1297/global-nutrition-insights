import pandas as pd
import requests
api_urls = {
    "adult_obesity" : "https://ghoapi.azureedge.net/api/NCD_BMI_30C",
    "child_obesity":  "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C",
    "adult_malnutrition": "https://ghoapi.azureedge.net/api/NCD_BMI_18C",
    "child_malnutrition": "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"
}
def fetch_data(api_url):
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()["value"]
    return data
  else:
    print("Invalid url")


adult_obesity_data = pd.DataFrame(fetch_data(api_urls["adult_obesity"]))
adult_malnutrition_data = pd.DataFrame(fetch_data(api_urls["adult_malnutrition"]))
child_obesity_data = pd.DataFrame(fetch_data(api_urls["child_obesity"]))
child_malnutrition_data = pd.DataFrame(fetch_data(api_urls["child_malnutrition"]))

adult_obesity_data["age_group"] = "adult"
adult_malnutrition_data["age_group"] = "adult"
child_malnutrition_data["age_group"] = "child"
child_obesity_data["age_group"] = "child"

df_malnutrition = pd.concat([adult_malnutrition_data,child_malnutrition_data], ignore_index=True)
df_obesity = pd.concat([adult_obesity_data,child_obesity_data], ignore_index=True)

df_malnutrition = df_malnutrition[df_malnutrition["TimeDim"].between(2012,2022)]
df_obesity = df_obesity[df_obesity["TimeDim"].between(2012,2022)]

keep_cls = ["ParentLocation",
"Dim1",
"TimeDim",
"Low",
"High",
"NumericValue",
"SpatialDim",
"age_group"
]

df_malnutrition = df_malnutrition[keep_cls]
df_obesity = df_obesity[keep_cls]

new_cls = {
    "TimeDim" : "Year",
"Dim1" : "Gender",
"NumericValue" : "Mean_Estimate",
"Low" : "LowerBound",
"High" : "UpperBound",
"ParentLocation" : "Region",
"SpatialDim" : "Country"
}
df_malnutrition.rename(columns=new_cls, inplace = True)
df_obesity.rename(columns=new_cls, inplace = True)

# Step 1: Define the correct mapping
gender_map = {
    "SEX_MLE": "Male",
    "SEX_FMLE": "Female",
    "SEX_BTSX": "Both"
}

# Step 2: Apply it directly to the already-renamed column
df_obesity["Gender"] = df_obesity["Gender"].map(gender_map)
df_malnutrition["Gender"] = df_malnutrition["Gender"].map(gender_map)

import pycountry

def convert_country(code):
    try:
        return pycountry.countries.get(alpha_3=code).name
    except:
        return code  # fallback

special_cases = {
    'GLOBAL': 'Global',
    'WB_LMI': 'Low & Middle Income',
    'WB_HI': 'High Income',
    'WB_LI': 'Low Income',
    'EMR': 'Eastern Mediterranean Region',
    'EUR': 'Europe',
    'AFR': 'Africa',
    'SEAR': 'South-East Asia Region',
    'WPR': 'Western Pacific Region',
    'AMR': 'Americas Region',
    'WB_UMI': 'Upper Middle Income'
}

def handle_special_cases(code):
    return special_cases.get(code, convert_country(code))
df_malnutrition['Country'] = df_malnutrition['Country'].apply(handle_special_cases)
df_obesity['Country'] = df_obesity['Country'].apply(handle_special_cases)

df_malnutrition["CI_Width"] = df_malnutrition['UpperBound']-df_malnutrition['LowerBound']
df_obesity["CI_Width"] = df_obesity['UpperBound']-df_obesity['LowerBound']

def categorise_obesity(x):
  if x<25:
    return "LOW"
  elif 25<=x<=29.9:
    return "MODERATE"
  else:
    return "HIGH"

def categorise_malnutrition(x):
  if x<10:
    return "LOW"
  elif 10<=x<=19.9:
    return "MODERATE"
  else:
    return "HIGH"

df_obesity["obesity_level"] = df_obesity["Mean_Estimate"].apply(categorise_obesity)
df_malnutrition["malnutrition_level"] = df_malnutrition["Mean_Estimate"].apply(categorise_malnutrition)
print(df_malnutrition.head(

))

import sqlite3

# Step 1: Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect('nutrition_paradox.db')

# Step 2: Insert df_obesity and df_malnutrition directly into tables
df_obesity.to_sql('obesity', conn, if_exists='replace', index=False)
df_malnutrition.to_sql('malnutrition', conn, if_exists='replace', index=False)

# Step 3: Close connection


print("✅ Data inserted successfully using df.to_sql()")


cursor = conn.cursor()

conn.close()
