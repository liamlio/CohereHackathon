import streamlit as st
from process_text import return_most_relevant_passage, return_summary, return_patent
from bs4 import BeautifulSoup
import requests

st.set_page_config(layout="wide")
patent_number = None
url = "https://patents.google.com/patent/{patent_number}/en"
with st.sidebar:
    with st.form("patent_number"):
        st.header("Input Patent Number")
        patent_number_new = st.text_input("Patent Number").replace(" ", "").replace(",", "")
        patent_number_submit = st.form_submit_button('Submit')
    st.write("Or select a default patent number from the dropdown.")
    patent_number_selected = st.selectbox(
                "Patent Number",
                ("US7615532B2 - Insulin derivatives", "US8961763B2 - Dual-pore device", "US777194A - Variable-speed dynamo.", "US20210008212A1 - Solid Carriers for Improved Delivery of Active Ingredients in Pharmaceutical Compositions"),
                index=None,
                placeholder="Select a default Patent to view.",
                )
    if patent_number_selected:
        patent_number = patent_number_selected.split(" ")[0]
    elif patent_number_submit:
        patent_number = patent_number_new
        
    # st.write("Or a search for a patent using the search form below.")
    # with st.form("search_patent"):
    #     st.header("Search for a Patent")
    #     search_query = st.text_input("Search Query").replace(" ", "+")
    #     search_url = "https://patents.google.com/?q=({search_query}&oq={search_query})"
    #     search_submit = st.form_submit_button('Search')
    # if search_submit:
    #     response = requests.get(search_url.format(search_query=search_query))
    #     soup = BeautifulSoup(response.content, "html.parser")
    #     results = soup.find_all("a", {"id:": "link"})[:10]
    #     names = []
    #     search_patent_numbers = []
    #     for result in results:
    #         try:
    #             result.


if patent_number:
    response = requests.get(url.format(patent_number=patent_number))
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.head.title.string
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
    sections = []
    html = u"" + str(soup.find("h2"))
    for tag in soup.find("h2").next_siblings:
        if tag.name == "h2":
            sections.append(html)
            html = u"" + str(tag)
        else:
            html += str(tag)
    info = sections[0]
    try:
        links = sections[1]
    except:
        links = None
    sections = soup.find_all("section")
    for section in sections:
        if section.h2:
            for key in patent.keys():
                if key in str(section.h2):
                    patent[key] = section
        else:
            if "metadata" in str(section):
                patent["Metadata"] = section

    patent_col, tool_col = st.columns(spec=[2, 1], gap="small")

    with patent_col.container(height=1000):
        st.header(title.replace(" - Google Patents", ""))
        with st.expander("Patent Details"):
            st.markdown(info, unsafe_allow_html=True)
        with st.expander("Links"):
            st.markdown(links, unsafe_allow_html=True)
        if patent["Images"]:
            with st.expander("Images"):
                st.markdown(patent["Images"], unsafe_allow_html=True)
        if patent["Classifications"]:
            with st.expander("Classifications"):
                st.markdown(patent["Classifications"], unsafe_allow_html=True)
        with st.expander("Definitions"):
            st.markdown(patent["Definitions"], unsafe_allow_html=True)
        st.markdown(patent["Abstract"], unsafe_allow_html=True)
        st.markdown(patent["Description"], unsafe_allow_html=True)
        st.markdown(patent["Claims"], unsafe_allow_html=True)
        st.markdown(patent["Applications"], unsafe_allow_html=True)
        st.markdown(patent["Metadata"], unsafe_allow_html=True)
        st.markdown(patent["ID"], unsafe_allow_html=True)
        st.markdown(patent["Published as"], unsafe_allow_html=True)
        st.markdown(patent["Similar Documents"], unsafe_allow_html=True)
        st.markdown(patent["Legal Events"], unsafe_allow_html=True)
    with tool_col:
        st.header("AI Generated Patent Summary")
        patent_summary = return_summary(patent_number, prompt="Summarize this patent so it is human readable. Translate the patent like content to plain English.")
        st.write(patent_summary)
        with st.form("summarize_citation"):
            st.header("Summarize a Cited Patent in relation to this Patent")
            st.write("Generate an AI generated summary of summary of how a cited or related patent relates to this patent.")
            country = st.selectbox(
                "Patent Country",
                ("United States (US)", "Canada (CA)", "United Kingdom (UK)", "Europe (EP)", "China (CN)", "Japan (JP)", "Australia (AU)"),
                index=None,
                placeholder="Select Country of Origin for Patent Reference.",
                )
            patent_citation_to_summarize = st.text_input("Patent Number").replace(" ", "").replace(",", "")
            summary_citation_submit = st.form_submit_button('Generate Relevancy Summary')
        if summary_citation_submit:
            patent_df = return_patent(patent_number)
            patent_citation_to_summarize = patent_citation_to_summarize.replace("US", "").replace("CA", "").replace("UK", "").replace("CN", "").replace("JP", "").replace("AU", "")
            patent_citation_to_summarize = country[-3:-1] + patent_citation_to_summarize
            text = " ".join(patent_df.clean_text.to_list())
            st.write(return_summary(patent_citation_to_summarize, prompt=f"Summarize this patent so it is human readable. Translate the patent like content to plain English. Summarize the patent in relation to the following patent: {patent_summary}"))
        with st.form("in_context"):
            st.header("In-Context Citations")
            st.write("Find the most relevant content from a cited patent in relation to this patent.")
            country = st.selectbox(
                "Patent Country",
                ("United States (US)", "Canada (CA)", "United Kingdom (UK)", "Europe (EP)", "China (CN)", "Japan (JP)", "Australia (AU)"),
                index=None,
                placeholder="Select Country of Origin for Patent Reference.",
                )
            citation_patent_number = st.text_input("Patent Number").replace(" ", "").replace(",", "")
            relevant_text = st.text_area("Copy/Paste any relevant text from the patent reference.")
            in_context_submit = st.form_submit_button('Find most relevant content from cited patent.')
        if in_context_submit:
            citation_patent_number = citation_patent_number.replace("US", "").replace("CA", "").replace("UK", "").replace("CN", "").replace("JP", "").replace("AU", "")
            citation_patent_number = country[-3:-1] + citation_patent_number
            st.write(f"Cited Patent: {citation_patent_number}")
            relevant_desc = return_most_relevant_passage(relevant_text, citation_patent_number)
            relevant_claims = None
            if relevant_claims:
                st.subheader(f"Relevant Content from {citation_patent_number}:")
                st.write(relevant_desc)
                st.write(f"Relevant Claim from {citation_patent_number}:")
                st.write(relevant_claims)
            else:
                st.subheader(f"Relevant Content from {citation_patent_number}:")
                st.write(relevant_desc)
else:
    st.header("Please Input a Patent Number from the sidebar to the left! :)")
