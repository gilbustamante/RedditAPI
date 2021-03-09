import requests

VERSION = 0.1


def pull_posts(sub, listing, limit, timeframe):
    url = f"https://www.reddit.com/r/{sub}/{listing}.json?limit={limit}&t={timeframe}"
    headers = {
        'User-agent': f'GRAPI v{VERSION}'
    }
    try:
        r = requests.get(url, headers=headers)
    except:
        print("Could not fetch url")
    return r.json()


if __name__ == '__main__':
    subreddit = "games"
    listing = "hot"
    limit = 3
    timeframe = "all"

    response = pull_posts(subreddit, listing, limit, timeframe)
    for post in response["data"]["children"]:
        print(post["data"]["title"])
