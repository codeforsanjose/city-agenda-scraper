import pickle
from os import listdir
from os.path import isfile, join

import regex as re
from tika import parser

sample_file = "../Agenda_samples/SanJose_Legistar_01-05-2021.pdf"

parsed = parser.from_file(sample_file)
content = parsed["content"]


# Initial target: SanJose_Legistar
def dirPDF2pkl(filedir: str, filename: str, xhtml_output: bool = False) -> dict:
    """Load a folder of PDF, extract each file's content, and dump everything into a dict
    Saves the dict as a pickle file

    Args:
        filedir (str): path to folder with PDFs
        filename (str): filename of the output pickle file

    Returns:
        dict: Dictionary containing filename: content pairs.
    """
    minsFiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]
    contentDICT = {
        f: parser.from_file(
            join(filedir, f),
            xmlContent=xhtml_output,
            config_path="./src/tika_config.xml",
        )["content"]
        for f in minsFiles
    }
    with open(filename, "wb") as handle:
        pickle.dump(contentDICT, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return contentDICT


sample_path = "../Agenda_samples/"
raw = dirPDF2pkl(sample_path, "meeting_minutes.pkl")
raw2 = dirPDF2pkl(sample_path, "meeting_minutes_html.pkl", xhtml_output=True)

# TODO: Get google drive access
