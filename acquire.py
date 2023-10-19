"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "nyukat/breast_cancer_classifier",
    "lishen/end2end-all-conv",
    "ImagingLab/ICIAR2018",
    "Jean-njoroge/Breast-cancer-risk-prediction",
    "abhinavsagar/breast-cancer-classification",
    "bupt-ai-cz/BCI",
    "nyukat/BIRADS_classifier",
    "nyukat/GMIC",
    "srimani-programmer/Breast-Cancer-Predictor",
    "ResearchKit/ShareTheJourney",
    "Swarbricklab-code/BrCa_cell_atlas",
    "ecobost/cnn4brca",
    "Adamouization/Breast-Cancer-Detection-Mammogram-Deep-Learning",
    "yala/Mirai",
    "akshaybahadur21/BreastCancer_Classification",
    "Dipeshtamboli/Image-Classification-and-Localization-using-Multiple-Instance-Learning",
    "viritaromero/Breast-Cancer-Detection",
    "AFAgarap/wisconsin-breast-cancer",
    "cheersyouran/cancer-detector",
    "bupt-ai-cz/BALNMP",
    "cystanford/breast_cancer_data",
    "mrdvince/breast_cancer_detection",
    "dangnh0611/kaggle_rsna_breast_cancer",
    "gscdit/Breast-Cancer-Detection",
    "microsoft/Machine-Learning-Patient-Risk-Analyzer-SA",
    "sayakpaul/Breast-Cancer-Detection-using-Deep-Learning",
    "ezgisubasi/breast-cancer-gene-expression",
    "Elhamkesh/Breast-Cancer-Scikitlearn",
    "Anki0909/BreakHist-Dataset-Image-Classification",
    "Piyush-Bhardwaj/Breast-cancer-diagnosis-using-Machine-Learning",
    "nyukat/GLAM",
    "mawady/bus-segmentation",
    "raviolli77/machineLearning_breastCancer_Python",
    "almaan/her2st",
    "akshaybahadur21/Breast-Cancer-Deep-Learning",
    "st186/Detection-of-Breast-Cancer-using-Neural-Networks",
    "CRYPTOcoderAS/Breast-Cancer-Detection-ML-Project",
    "rishiswethan/Cancer-detection-using-CNN",
    "mvab/mendelian-randomization-breast-cancer",
    "kanchitank/Medibuddy-Smart-Disease-Predictor",
    "advikmaniar/ML-Healthcare-Web-App",
    "javismiles/Deep-Learning-predicting-breast-cancer-tumor-malignancy",
    "yala/OncoServe_Public",
    "bora-pajo/breast-cancer-prediction",
    "aditisingh/Breast_cancer_detection",
    "bhklab/genefu",
    "IBM/MAX-Breast-Cancer-Mitosis-Detector",
    "vbookshelf/Breast-Cancer-Analyzer",
    "rezacsedu/Multimodal-autoencoder-for-breast-cancer",
    "Jonas1312/PFA-ScanNet",
    "hrsht-13/Breast-Cancer-Detection",
    "sirCamp/kaggle-breast-cancer-prediction",
    "theArjun/disease-predictor",
    "datasets/breast-cancer",
    "rajat1994/WebApp-for-breast-cancer-detection",
    "BodenmillerGroup/SCPathology_publication",
    "analokmaus/kaggle-rsna-breast-cancer",
    "NajiAboo/BPSO_BreastCancer",
    "sebastianbk/BreastCancerNeuralNetwork",
    "akshaybahadur21/Breast-Cancer-Neural-Networks",
    "NeuroSyd/breast-cancer-sub-types",
    "jbustospelegri/breast_cancer_diagnosis",
    "jordanvaneetveldt/breast_mass_detection",
    "AFAgarap/support-vector-machine",
    "AhmedEnnaime/Salamti",
    "vishabh123/vishabh",
    "gayathri1462/Breast-Cancer-Detection-Web-App",
    "antaloaalonso/Classification-Model-YT-Video",
    "Elysian01/Impulse-LifeSaviour",
    "aimlcommunity/Breast-Cancer-Detection-using-Machine-Learning",
    "jnarhan/Breast_Cancer",
    "mungujn/machine-learning-detect-cancer",
    "vasudev-sharma/Breast-Cancer-Detection-using-Artificial-Neural-Networks",
    "yuhaomo/HoVerTrans",
    "MainakRepositor/Breast-Cancer-Detector",
    "akashxg/Mammogram-Image-Classifier",
    "Zero-We/PMIL",
    "lucko515/breast-cancer-classification",
    "forderation/breast-cancer-retrieval",
    "DaemonFG/BreastCancerWisconsin",
    "mrtungleung/breast_cancer",
    "nalamidi/Breast-Cancer-Classification-with-Support-Vector-Machine",
    "gholste/breast_mri_fusion",
    "LailaMahmoudi/Breast-Cancer-Predictions-With-SVM",
    "yala/Tempo",
    "scottykwok/bach2018",
    "ab93/Detection-of-Breast-Cancer-from-mammogram-images",
    "cyc1am3n/HeLP2019_Breast_Cancer_1st_solution",
    "lishen/dream2016_dm",
    "zhenweishi/QMITH",
    "Ammar-Raneez/ONCO",
    "mistersharmaa/BreastCancerPrediction",
    "alejandro-ao/streamlit-cancer-predict",
    "ynd/cancer-bayes",
    "arpit512512/Mammogram-Classification-using-GLCM-Features",
    "HiYellowC/AggNet",
    "BishalDali/Breast_Cancer_Prediction",
    "AICAN-Research/H2G-Net",
    "IndianAIProduction-Channel/Breast-Cancer-Detection-App",
    "gmineo/Breast-Cancer-Prediction-Project"
]
 

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_contents = requests.get(get_readme_download_url(contents)).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data2.json", "w"), indent=1)
