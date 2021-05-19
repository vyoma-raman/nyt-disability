import requests
import pandas as pd
import time
key = #insert your API key here

def scraper(month, year):
	"""
	Scrapes metadata for all NYT articles in a given month.
	param month: int 1-12 describing which month to scrape
	param year: int 1851-2021 describing which year to scrape
	param return: list of metadata for each article
	"""
    url = "https://api.nytimes.com/svc/archive/v1/{0}/{1}.json?api-key={2}".format(str(year), str(month), key)
    return requests.get(url).json()["response"]["docs"]

def parse(articles):
	"""
	Parses a list of article metadata into a dataframe with relevant information.
	param articles: list of metadata for each article
	param return: dataframe containing relevant information, one row for each article
	"""
	# Information to collect, organized into a dictionary
    data = {
        "date": [],
        "headline": [],
        "abstract": [],
        "document_type": [],
        "type_of_material": [],
        "news_desk": [],
        "section_name": [],
        "subjects": []
    }
    # Extract relevant metadata for each article
    for a in articles:
        data["date"].append(a["pub_date"])
        data["headline"].append(a["headline"]["main"])
        data["abstract"].append(a["abstract"])
        data["document_type"].append(a["document_type"])
        data["type_of_material"].append(a["type_of_material"])
        data["news_desk"].append(a["news_desk"])
        data["section_name"].append(a["section_name"])
        data["subjects"].append([sub["value"] for sub in a["keywords"]])
    # Convert metadata dictionary into dataframe
    return pd.DataFrame(data)

# Create empty dataframe
df = pd.DataFrame(columns = ["date", "headline", "abstract", "document_type", "type_of_material", "news_desk", "section_name"])
# Operate on each month + year pair
for year in range(1851, 2021):
    for month in range(1, 13):
    	# Create dataframe for metadata of month/year
        new_df = parse(scraper(month, year))
        # Combine new dataframe with total dataframe
        df = pd.concat([df, new_df]).reset_index(drop=True)
        print("Finished {0}/{1}".format(str(month), str(year)))
        # Sleep to avoid exceeding API request limit of 10 requests/minute
        time.sleep(6)
    # Save dataframe every 10 years
    if year % 10 == 0:
        df.to_csv("all_data.csv", index=False)
        print("Saved after {0}".format(str(year)))
# Tail case: Get metadata for 2021
for month in range(1, 5):
    new_df = parse(scraper(month, year))
    df = pd.concat([df, new_df]).reset_index(drop=True)
    print("Finished {0}/2021".format(str(month)))
    time.sleep(6)
df.to_csv("all_data.csv", index=False)
print("Saved after 2021")
