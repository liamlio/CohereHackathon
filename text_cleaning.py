
import numpy as np
import re
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests


# def return_embeddings(
#     clean_text: list[str],
#     api_key: str,
#     input_type_embed="search_document",
#     model_name="embed-english-v3.0",
# ) -> np.array:
#     co = cohere.Client(api_key)
#     embeddings = co.embed(
#         texts=clean_text, model=model_name, input_type=input_type_embed
#     ).embeddings
#     return embeddings


def download_patent_text(patent_url: str):
    # Send a GET request to the patent URL
    response = requests.get(patent_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        description_paragraphs = soup.find_all(
            "div", {"class": "description-paragraph"}
        )
        claims = soup.find_all("div", {"class": "claim-text"})

        if description_paragraphs:
            patent_df = pd.DataFrame({"text": description_paragraphs + claims})

            patent_df["clean_text"] = patent_df.text.astype(str).apply(
                lambda x: remove_text_between_angle_brackets(clean_text(x))
            )

            patent_df = patent_df[patent_df["clean_text"] != ""]
            patent_df = patent_df[patent_df["clean_text"].str.len() > 100]
            return patent_df
        else:
            print("Could not find patent text on the page.")
    else:
        print(f"Failed to fetch the patent page. Status code: {response.status_code}")


def remove_text_between_angle_brackets(input_string: str) -> str:
    # Define a regular expression pattern to match text between < and >
    pattern = re.compile(r"<.*?>")
    # Use sub() function to replace the matched pattern with an empty string
    result_string = re.sub(pattern, "", input_string)
    return result_string


def clean_text(x: str) -> str:
    return x.replace("\n", " ")


# def return_most_relevant_passage(input_passage: str, patent_number: str) -> str:
#     cohere_api_key = os.environ.get("cohere_api_key")
#     patent_url = f"https://patents.google.com/patent/{patent_number}"
#     patent_df = download_patent_text(patent_url)
#     passage_embedding = return_embeddings([input_passage], cohere_api_key)
#     searched_patent_embeddings = return_embeddings(
#         patent_df["clean_paragraphs"].to_list(), cohere_api_key
#     )
#     similarities = cosine_similarity(passage_embedding, searched_patent_embeddings)
#     most_relevant_passage_index = np.argmax(similarities)
#     return patent_df.iloc[most_relevant_passage_index]["clean_paragraphs"]