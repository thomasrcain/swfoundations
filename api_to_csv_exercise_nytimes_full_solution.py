import requests
import csv
import pandas as pd

base_url = "https://api.nytimes.com/svc/archive/v1"
myapikey = "kEBQsEG9EGEfQNutEqFNXBSq6m7etGAk"

year = "1961"
# year = input("Enter a 4-digit year after 1851: ")
month = "9"
# month = input("Enter a digit indicating the month of the year (1-12): ")
month_url = month+".json"
url_parts = (base_url,year,month_url)
url = "/".join(url_parts)
print(url)

querystring = {"api-key": myapikey}
response = requests.request("GET", url, params=querystring)

# Use the json method in requests module to convert the json to a dict
api_dict = response.json()
response_dict = api_dict["response"]
print(f"There are {response_dict['meta']['hits']} articles in this month of {year}.")

# Grab all the articles.  A list of dictionaries.
articles = response_dict['docs']

dob = "1961-09-09"
dobArticles = []
for article in articles:
    (mmddyyyy, garbage) = article["pub_date"].split('T')
    if dob == mmddyyyy:
        dobArticles.append(article)

print(f'There are {len(dobArticles)} published on your bday.')
print(dobArticles[0])

articles_df = pd.DataFrame(dobArticles)

print(articles_df.shape)

###################################################################
#  Write the data to CSV
#
#  Create a meaningful filename
###################################################################

csv_filename = "nytimes_archives" + "-" + dob + ".csv"

# time to create a CSV
with open(csv_filename, 'w') as csvfile:
    fieldnames = dobArticles[1].keys()
    print(f"Here are the fields that we'll write to the CSV file: \n {fieldnames}")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for article in dobArticles:
        writer.writerow(article)
