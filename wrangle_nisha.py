
import requests
import json
from env import github_token, github_username

def get_repository_details(repo_full_name):
    repo_url = f"https://api.github.com/repos/{repo_full_name}"
    readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
    repo_response = requests.get(repo_url, headers=headers)
    readme_response = requests.get(readme_url, headers=headers)
    if repo_response.status_code == 200 and readme_response.status_code == 200:
        repo_data = repo_response.json()
        readme_data = readme_response.json()
        language = repo_data["language"]
        readme_contents = requests.get(readme_data["download_url"]).text
        return {
            "repo": "/" + repo_full_name,
            "language": language,
            "readme_contents": readme_contents
        }
    else:
        return None

def get_repositories(query, sort="stars", order="desc", page=1, max_pages=10):
    base_url = "https://api.github.com/search/repositories"
    all_repos = []

    while page <= max_pages:
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": 10,  # You can get up to 100 results per page.
            "page": page  # Specify the page number
        }
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch page {page} of repositories.")
            break

        response_json = response.json()
        all_repos.extend(response_json["items"])
        
        page += 1

        if "Link" in response.headers:
            next_link = response.headers["Link"]
            if 'rel="next"' not in next_link:
                break

    return all_repos

def scrape_breast_cancer_repositories():
    # Search for breast cancer related repositories and handle pagination
    query = "breast cancer"
    page = 1
    max_pages = 10

    breast_cancer_repos = get_repositories(query, page=page, max_pages=max_pages)

    with open("breast_cancer_repositories.json", "w") as json_file:
        json.dump(breast_cancer_repos, json_file, indent=4)

    return breast_cancer_repos

# Example usage:
if __name__ == "__main__":
    scraped_repositories = scrape_breast_cancer_repositories()
    print(f"Scraped {len(scraped_repositories)} breast cancer repositories.")
=======
# wrangle the data
import pandas as pd
import numpy as np

# see the data
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# play with words
import unicodedata
from nltk.corpus import stopwords
import nltk
import re
from pprint import pprint

# split and model
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# import of stats testing
from scipy import stats
from scipy.stats import chi2_contingency

# import warning
import warnings
warnings.filterwarnings('ignore')


### functions to get the data###
### functions to prep the data ###

def basic_clean(original):
    '''
    Input: original text or .apply(basic_clean) to entire data frame
    Actions: 
    lowercase everything,
    normalizes everything,
    removes anything that's not a letter, number, whitespace, or single quote
    Output: Cleaned text
    '''
    # lowercase everything
    basic_cleaned = original.lower()
    # normalize unicode characters
    basic_cleaned = unicodedata.normalize('NFKD', basic_cleaned)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    # Replace anything that is not a letter, number, whitespace or a single quote.
    basic_cleaned = re.sub(r'[^a-z0-9\'\s]', '', basic_cleaned)
    
    return basic_cleaned


def tokenize(basic_cleaned):
    '''
    Input: basic_cleaned text string or .apply(tokenize) to entire data frame
    Actions:
    creates the tokenizer
    uses the tokenizer
    Output: clean_tokenize text string
    '''
    #create the tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use the tokenizer
    clean_tokenize = tokenize.tokenize(basic_cleaned, return_str=True)
    
    return clean_tokenize


def remove_stopwords(lemma_or_stem, extra_words=[], exclude_words=[]):
    '''
    Input:text string or .apply(remove_stopwords) to entire data frame
    Action: removes standard stop words
    Output: parsed_article
    '''
    # save stopwords
    stopwords_ls = stopwords.words('english')
    # removing any stopwords in exclude list
    stopwords_ls = set(stopwords_ls) - set(exclude_words)
    # adding any stopwords in extra list
    stopwords_ls = stopwords_ls.union(set(extra_words))
    
    # split words in article
    words = lemma_or_stem.split()
    # remove stopwords from list of words
    filtered = [word for word in words if word not in stopwords_ls]
    # join words back together
    parsed_article = ' '.join(filtered)
    
    return parsed_article
    
def lemmatize(clean_tokenize):
    '''
    Inputs: clean_tokenize
    Actions: creates lemmatizer and applies to each word
    Outputs: clean_tokenize_lemma
    '''
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    #use lemmatize - apply to each word in our string
    lemmas = [wnl.lemmatize(word) for word in clean_tokenize.split()]
    #join words back together
    clean_tokenize_lemma = ' '.join(lemmas)
    
    return clean_tokenize_lemma

def clean(text):
    '''
    A simple function to cleanup text data.
    
    Args:
        text (str): The text to be cleaned.
        
    Returns:
        list: A list of lemmatized words after cleaning.
    '''
    
    # basic_clean() function from last lesson:
    # Normalize text by removing diacritics, encoding to ASCII, decoding to UTF-8, and converting to lowercase
    text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    
    # Remove punctuation, split text into words
    words = re.sub(r'[^\w\s]', '', text).split()
    
    
    # lemmatize() function from last lesson:
    # Initialize WordNet lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Combine standard English stopwords with additional stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    
    # Lemmatize words and remove stopwords
    cleaned_words = [wnl.lemmatize(word) for word in words if word not in stopwords]
    
    return cleaned_words

def cleaned(df):
    '''
    This function will clean the df
    drop nulls, replace special characters
    '''
    # drop nulls
    df = df.dropna()
    # replace special characters with space
    df.readme_contents = df.readme_contents.str.replace('[/,_,-,:,"]', ' ', regex=True)
    # replace heavy, check, and mark with nothing
    df.readme_contents = df.readme_contents.str.replace('heavy', '').str.replace('check', '').str.replace('mark', '')
    # create column with clean text. Tokenized, normalized, lemmatized, stop words removed
    df['clean_norm_token'] = df.readme_contents.apply(tokenize).apply(basic_clean).apply(remove_stopwords).apply(lemmatize)
    # replace 124 with nothing. 124 was created by the program removing '|'
    df.clean_norm_token = df.clean_norm_token.str.replace('124', '')
    #in language column replace language with other if it is not in the top 5 languages
    top_5 = df.language.value_counts().head(5).index.tolist()
    df.language = df.language.apply(lambda x: x if x in top_5 else 'other')
    
    return df

### functions to split the data##

def split_function_cat_target(df_name, target_varible_column_name):
    train, test = train_test_split(df_name,
                                   random_state=123, #can be whatever you want
                                   test_size=.20,
                                   stratify= df_name[target_varible_column_name])
    
    train, validate = train_test_split(train,
                                   random_state=123,
                                   test_size=.25,
                                   stratify= train[target_varible_column_name])
    return train, validate, test

# the test will contain 20% of the data,
# the validation contain 25%('test_size') of previous train which is 20% of original dataset the same as the test set


