Google Classroom
Classroom
Somerville
Data Science
Stream
Classwork
People
All topics
Question
Explain a couple pros and cons of word clouds.
No due date
Completed Question
What are the main steps we take to clean text data? Do you have the steps in the correct order?
No due date
Completed Question
What is a capture group in Regex? How is it useful to us?
No due date
Completed Question
Question
No due date
Question
What were a couple types of plots we made in the exploration lesson? What did they help us learn about our data?
No due date
Question
What are the three ways we can split time series data into train/validate/test?
No due date
Question
Why is it important to convert a date to a DateTime object? What sort of operations can we perform as a result?
No due date
Question
How is JSON data structured?
No due date
Material
Stock portfolio excel file
Posted Aug 7
Handouts
Handouts
Material
Welcome Day - Syllabus
Posted Jun 13
Material
Welcome Day - How to Succeed
Posted Jun 14
Data
Data
Material
Data for Tableau Lesson
Posted Jul 24
Material
Movie Data
Posted Aug 7
Fundamentals
Fundamentals
Material
Pipeline Demo
Posted Jun 15
Completed Assignment
Hyperdoc Follow-up
3
3 comments
No due date
Material
Hyperdoc
Posted Jun 14
Completed Assignment
Data Science: Skills in Demand
Assessments/Projects
Due Jun 26, 9:30 AM
Completed Assignment
Fundamentals Quiz
Quizzes
No due date
SQL
SQL
Assignment
Review - Quizziz
No due date
Completed Assignment
Exercises - SQL
Exercises
No due date
Completed Assignment
SQL Quiz
Quizzes
Due Jul 6, 3:15 PM
Python
Python
Completed Assignment
Checkbook application
Assessments/Projects
No due date
Completed Assignment
Pandas Quiz
Quizzes
No due date
Completed Assignment
DS Libraries Exercises
Exercises
Due Jul 24, 5:00 PM
Completed Assignment
101 Exercises Prework Grade
Exercises
Due Jul 24, 5:00 PM
Completed Assignment
Exercises - Python
Exercises
No due date
Storytelling
Storytelling
Assignment
Storytelling project retrospective
No due date
Completed Assignment
Tableau Exercises
Exercises
No due date
Completed Assignment
Mini-Project - Storytelling
Assessments/Projects
No due date
Stats
Stats
Completed Assignment
Stats Quiz
Quizzes
No due date
Assignment
Review - Quizziz
No due date
Completed Assignment
Exercises - Stats
Exercises
No due date
Classification
Classification
Completed Assignment
Exercises - Classification
Exercises
No due date
Completed Assignment
Quiz - Classification
Quizzes
Due Aug 22, 10:45 AM
Completed Assignment
Project - Classification
2
2 comments
Assessments/Projects
Due Aug 21, 9:00 AM
Completed Assignment
Project - Retrospective
No due date
Regression
Regression
Material
Diamonds dataset
Posted Aug 31
Completed Assignment
Project - Regression
Assessments/Projects
Due Sep 12, 9:00 AM
Assignment
Exercises - Regression
Exercises
No due date
Assignment
Regression Project Reflection
No due date
Completed Assignment
Quiz - Regression & Review Topics
Quizzes
Due Sep 15, 12:25 PM
Clustering
Clustering
Completed Assignment
Exercises - Clustering
Exercises
Due Sep 25, 9:00 AM
Completed Assignment
Project - Clustering
Assessments/Projects
Due Sep 22, 10:00 AM
Time Series Analysis
Time Series Analysis
Assignment
Exercises - Time Series
Exercises
No due date
Individual Project
Individual Project
Completed Assignment
Individual Project
4
4 comments
Due Oct 5, 9:00 AM
Anomaly Detection
Anomaly Detection
Completed Assignment
Project - Anomaly Detection
Due Oct 11, 6:00 PM
NLP
NLP
Assignment
NLP Project
Assessments/Projects
Due Oct 24, 9:15 AM
Posted 9:21 AM
Assigned

acquire.py
Text
Progress Reports
Progress Reports
Completed Assignment
Progress Report 1 - Through SQL
No due date
Completed Assignment
Progress Report 2 - Through Tableau
No due date
Capstones
Capstones
Assignment
Capstone Proposals
No due date
Git Tracker
Git Tracker
Completed Assignment
Weekly Github activity (Week of September 11th)
No due date
Completed Assignment
Weekly Github activity (Week of September 4th)
No due date
Completed Assignment
Weekly Github activity (Week of August 28th)
No due date
Completed Assignment
Weekly Github activity (Week of August 14th)
No due date
Completed Assignment
Weekly Github activity (Week of August 7th)
No due date
Completed Assignment
Weekly Github activity (Week of July 31st)
Exercises
No due date
Completed Assignment
Weekly Github activity (Week of July 24th)
Exercises
No due date
Completed Assignment
Weekly Github activity (Week of July 17th)
Exercises
No due date
Completed Assignment
Weekly Github Activity (Week of July 10th)
Exercises
No due date
Completed Assignment
Weekly GitHub activity (Week of July 3rd)
Exercises
No due date
Attendance
Attendance
Completed Assignment
Attendance grade
Attendance
No due date
Expanded NLP Project
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

REPOS = []
 

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
acquire.py
Displaying acquire.py.