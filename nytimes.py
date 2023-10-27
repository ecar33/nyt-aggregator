import requests
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')


def article_search():
    filter = ''
    query = input("Enter a broad query term: ").strip().lower()

    filter_query_flag = input("Refine query? (y/n) ").strip().lower()
    while (filter_query_flag != 'y' and filter_query_flag != 'n'):
        print("Please input y/n ")
        filter_query_flag = input().strip().lower()

    if filter_query_flag == 'y':
        filter = filter_queries()

    headers = {
        'API-Secret': API_SECRET
    }

    params = {
        'api-key': API_KEY
    }

    period = 30
    base_url = "https://api.nytimes.com/svc/search/v2"
    endpoint = f'/articlesearch.json?q={query}&fq={filter}'

    r = requests.get(base_url + endpoint, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()
        parsed_json = parse_article_search(data)

        print(parsed_json)
        user_select_function()

    else:
        print(f"Something went wrong: {r.text}")
        print(r.url)


def top_stories_viewer():
    headers = {
        'API-Secret': API_SECRET
    }

    params = {
        'api-key': API_KEY
    }

    section = input('''Selection a section: 
    The possible section values are:
    arts, automobiles, books / review, business, fashion,
    food, health, home, insider, magazine, movies, nyregion, obituaries, opinion, politics,
    realestate, science, sports, sundayreview,
    technology, theater, t - magazine, travel, upshot, us, and world: ''').strip().lower()

    base_url = "https://api.nytimes.com/svc/topstories/v2/"
    endpoint = f'/{section}.json'

    r = requests.get(base_url + endpoint, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()

        parsed_articles = parse_top_stories(data)
        print(parsed_articles)
        user_select_function()

        # with open("outfile.json", "w") as outfile:
        #     outfile.write(json.dumps(data, indent=4))

    else:
        print(f"Something went wrong: {r.text}")
        print(r.url)


def filter_queries():
    def get_query_terms(prompt):
        query_terms = input(f"Enter query terms for {prompt} (separated by commas): ").split(",")

        normalized_query = []
        for term in query_terms:
            normalized_query.append(re.sub(r'\s+', ' ', term))
        concatenated_input = " OR ".join([term.strip() for term in normalized_query])
        return encase_multiword_tokens(concatenated_input)

    queries = {
        "body": (),
        "headline": (),
        "glocations": (),
        "news_desk": (),
        "organizations": (),
        "person": ()
    }
    choice_map = {
        "1": ("body search", "body"),
        "2": ("headline search", "headline"),
        "3": ("glocation search", "glocations"),
        "4": ("news desk search", "news_desk"),
        "5": ("organization search", "organizations"),
        "6": ("person search", "person")
    }

    while True:
        print('''
        Choose a filter query from the list, press q to stop
        1. Body Search
        2. Headline
        3. Geographic Location
        4. News Desk
        5. Organization
        6. Person
        ''')

        filter_query_choice = input().strip().lower()

        if filter_query_choice == "q":
            break
        elif filter_query_choice in choice_map:
            prompt, key = choice_map[filter_query_choice]

            if queries[key]:
                print(f'Current query is {queries[key]}')
                choice = input("Would you like to change? (press c to change)")
                if choice == "c":
                    queries[key] = get_query_terms(prompt)
            else:
                queries[key] = get_query_terms(prompt)

        else:
            print("Choose from the list, or q to quit.")

    lucene_query = " AND ".join(f"{key}:({value})" for key, value in queries.items() if value)
    print(lucene_query)
    return lucene_query


def encase_multiword_tokens(query):
    tokens = query.split(' OR ')
    processed_tokens = []
    for token in tokens:
        if " " in token:
            processed_tokens.append(f'"{token}"')
        else:
            processed_tokens.append(token)

    processed_query_string = " OR ".join(processed_tokens)

    return processed_query_string


def parse_article_search(data):
    parsed_json = []
    if "response" in data and "docs" in data["response"]:
        for index, article in enumerate(data["response"]["docs"]):
            abstract = article.get("abstract", None)
            web_url = article.get("web_url", None)
            snippet = article.get("snippet", None)
            headline = article["headline"].get("main", None) if "headline" in article else None

            parsed_article = {"abstract": abstract,
                              "web_url": web_url,
                              "snippet": snippet,
                              "headline": headline,
                              "article_number": index + 1}

            parsed_json.append(parsed_article)

    return parsed_json


def parse_top_stories(data):
    parsed_json = []
    if "results" in data:
        for index, article in enumerate(data["results"]):
            title = article.get("title", None)
            abstract = article.get("abstract", None)
            url = article.get("url", None)
            byline = article.get("byline")

            parsed_article = {"abstract": abstract,
                              "title": title,
                              "abstract": abstract,
                              "url": url,
                              "byline": byline,
                              "article_number": index + 1}

            parsed_json.append(parsed_article)

    return parsed_json

def user_select_function():
    print('''
    Pick a function.
    1. Article Search
    2. Top Stories
    ''')
    user_select_function = input().strip().lower()

    match user_select_function:
        case '1':
            article_search()
        case '2':
            top_stories_viewer()

    return user_select_function

def main():
    print(r"""   _  ___  ________  ___                              __          
  / |/ | \/ /_  __/ / _ |___ ____ ________ ___ ____ _/ /____  ____
 /    / \  / / /   / __ / _ `/ _ `/ __/ -_) _ `/ _ `/ __/ _ \/ __/
/_/|_/  /_/ /_/   /_/ |_\_, /\_, /_/  \__/\_, /\_,_/\__/\___/_/   
                       /___//___/        /___/                    """)

    user_select_function()




if __name__ == "__main__":
    main()
