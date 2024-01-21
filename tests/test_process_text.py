from .process_text import return_most_relevant_passage, return_summary


def test_return_most_relevant_passage():
    test_passage = " DNA translocation speed through a nanopore "
    patent_number = "US8961763"
    expected_answer = "Nanopore sensors are purely electrical, and can detect DNA in concentrations/volumes that are no greater than what is available from a blood or saliva sample. Additionally, nanopores promise to dramatically increase the read-length of sequenced DNA, from 450 bases to greater than 10,000 bases."
    most_relevant_passage = return_most_relevant_passage(test_passage, patent_number)
    assert most_relevant_passage == expected_answer


def test_return_summary():
    patent_number = "US8961763"
    prompt = f"Focusing on details related to the following: ' DNA translocation speed through a nanopore '. Summarize in easy to understand language"
    summary = return_summary(patent_number, prompt)
    assert summary