import os

import numpy as np
import pandas as pd
import yake
from rake_nltk import Rake
from tika import config, parser


def pdf_to_text(filename: str) -> str:
    """Extract text from pdf using Tika

    Args:
        filename (str): target filename

    Returns:
        str: body of the text
    """
    tika_parsed = parser.from_file(filename)
    return tika_parsed["content"]


def parse_keywords_rake(main_text: str) -> pd.DataFrame:
    """Parse keywords using Rake

    Args:
        main_text (str): input text, parsed from pdf

    Returns:
        pd.DataFrame: Dataframe with keyword/score pairs
    """
    rake_handler = Rake()
    rake_results = rake_handler.extract_keywords_from_text(main_text)
    # b = rake_handler.get_ranked_phrases()
    keywords = pd.DataFrame(rake_handler.get_ranked_phrases_with_scores())
    keywords.columns = ["score", "keywords"]
    keywords = keywords.loc[keywords["score"] >= np.percentile(keywords["score"], 95)]
    keywords["method"] = "rake"
    return keywords[["keywords", "score", "method"]]


def parse_keywords_yake(main_text: str) -> pd.DataFrame:
    """Parse keywords using Yake

    Args:
        main_text (str): input text, parsed from pdf

    Returns:
        pd.DataFrame: Dataframe with keyword/score pairs
    """
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(main_text)
    keywords = pd.DataFrame(keywords)
    keywords.columns = [
        "keywords",
        "score",
    ]
    keywords["method"] = "yake"
    return keywords


def keyword_extract(filename: str) -> pd.DataFrame:
    """Tie the whole process of keyword extraction together

    Args:
        filename (str): Target Filename

    Returns:
        str: [description]
    """
    text = pdf_to_text(filename)
    result = parse_keywords_rake(text)
    result = result.append(parse_keywords_yake(text))
    result["filename"] = os.path.basename(filename)
    return result


if __name__ == "__main__":
    input_folder = "../Report_samples/"
    input_files = [
        # "SanJose1",
        "SanJose14",
        "SanJose15",
        "SanJose16",
        "SanJose17",
        "SanJose18",
        "SanJose19",
    ]
    data = pd.DataFrame()
    for file in input_files:
        path = f"{input_folder}{file}.pdf"
        data = data.append(keyword_extract(path))
        print(f"Done: {path}")
    data.to_csv("rake_output.csv", index=False)
