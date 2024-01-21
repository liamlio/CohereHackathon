import requests
from bs4 import BeautifulSoup
import pandas as pd
from text_cleaning import remove_text_between_angle_brackets, clean_text


def download_patent_text(patent_url: str):
    # Send a GET request to the patent URL
    response = requests.get(patent_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        patent = {
            "Images": None,
            "Classifications": None,
            "Definitions": None,
            "Abstract": None,
            "Description": None,
            "Claims": None,
            "Applications": None,
            "Legal Events": None,
            "Metadata": None,
            "ID": None,
            "Published as": None,
            "Similar Documents": None,
            "Legal Events": None
        }
        sections = soup.find_all("section")
        for section in sections:
            if section.h2:
                for key in patent.keys():
                    if key in str(section.h2):
                        patent[key] = section
            else:
                if "metadata" in str(section):
                    patent["Metadata"] = section
        
        try:
            description = "".join(list(patent["Description"].find("div", {"itemprop": "content"}).strings)).replace("\n", "").split("  ")
            for i,des in enumerate(description):
                if len(des) < 50:
                    description[i-1] += des
                    description.pop(i)
            description = [d.encode("utf-8").decode("utf-8") for d in description if d != ""]
            if patent["Claims"]:
                claims = "".join(list(patent["Claims"].find("div", {"itemprop": "content"}).strings)).replace("\n", "").split("  ")
                for i, claim in enumerate(claims):
                    if len(claim) < 50:
                        claims[i-1] += claim
                        claims.pop(i)
                claims = [c.encode("utf-8").decode("utf-8") for c in claims if c != ""]
                return description, claims
            else:
                return description, None
        except:
            print("Could not find patent text on the page.")
        
    else:
        print(f"Failed to fetch the patent page. Status code: {response.status_code}")