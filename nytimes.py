import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')


def article_search():
    query = input("Enter a broad query term: ").strip().lower()
    #filter_query_flag = input("Refine query? (y/n)")

    headers = {
        'API-Secret': API_SECRET
    }

    params = {
        'api-key': API_KEY
    }

    period = 30
    base_url = "https://api.nytimes.com/svc/search/v2"
    endpoint = f'/articlesearch.json?q={query}'

    r = requests.get(base_url + endpoint, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()

        with open('outfile.txt', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print(f"Something went wrong: {r.text}")
        print(r.url)


def main():
    print(r"""   _  ___  ________  ___                              __          
  / |/ | \/ /_  __/ / _ |___ ____ ________ ___ ____ _/ /____  ____
 /    / \  / / /   / __ / _ `/ _ `/ __/ -_) _ `/ _ `/ __/ _ \/ __/
/_/|_/  /_/ /_/   /_/ |_\_, /\_, /_/  \__/\_, /\_,_/\__/\___/_/   
                       /___//___/        /___/                    """)

    print('''
    Pick a function.
    1. Article Search

        ''')
    user_select_function = input().strip().lower()

    match user_select_function:
        case '1':
            article_search()


if __name__ == "__main__":
    main()

