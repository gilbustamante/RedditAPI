import requests

VERSION = 0.1


def pull_posts(sub, listing, limit, timeframe):
    url = f"https://www.reddit.com/r/{sub}/{listing}.json?limit={limit}&t={timeframe}&raw_json=1"
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
    limit = 10
    timeframe = "all"

    response = pull_posts(subreddit, listing, limit, timeframe)
    for data in response["data"]["children"]:
        post = data["data"]
        if len(post["title"]) > 100:
            print(f"{post['title'][:100]}... ({post['score']})")
        else:
            print(f"{post['title']} ({post['score']})")

        print(f"Author: {post['author']}")

        print(f"URL: {post['url']}")

        if post["selftext"]:
            print(f"{post['selftext'][:50]}...")

        print('----------------------')
