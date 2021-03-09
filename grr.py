from datetime import datetime, timezone
import argparse
import requests
import sys

VERSION = 0.1


def setup_argparse():
    """Setup and parse arguments"""
    reddit_parser = argparse.ArgumentParser(
        prog="Gil's Reddit Reader",
        description="Pull post info from Reddit for reading from the comfort of your terminal.",
        usage="grr.py [options] subreddit",
    )
    reddit_parser.add_argument("-l",
                               metavar="Listing type",
                               dest="listing",
                               choices=["hot", "new", "best",
                                        "random", "rising", "top"],
                               help="The type of listing to sort by. Possible arguments: hot, new, best, random, rising, top", default="hot", required=False)
    reddit_parser.add_argument('-c',
                               metavar="Post count",
                               dest="count",
                               help="The number of posts to pull in a request.", default=10, required=False)
    reddit_parser.add_argument("-t",
                               metavar="Timeframe",
                               dest="timeframe",
                               choices=["hour", "day", "week",
                                        "month", "year", "all"],
                               help="How far back in time you want to check for posts. Possible arguments: hour, day, week, month, year, all", default="all", required=False)
    reddit_parser.add_argument("subreddit",
                               help="The subreddit from which posts will be pulled.",)
    args = reddit_parser.parse_args()

    return args


def pull_posts(sub, listing, count, timeframe):
    """Request JSON data from Reddit and return"""
    url = f"https://www.reddit.com/r/{sub}/{listing}.json?limit={count}&t={timeframe}&raw_json=1"
    headers = {
        'User-agent': f'GRAPI v{VERSION}'
    }
    try:
        r = requests.get(url, headers=headers)
    except:
        print("Could not fetch url")
        sys.exit()
    return r.json()


def print_feed(data):
    """Iterate through results and print formatted posts"""
    for item in data["data"]["children"]:
        post = item["data"]
        ratio = int(post["upvote_ratio"] * 100)
        created = to_local_time(post["created_utc"])
        if len(post["title"]) > 100:
            print(
                f"\033[93m{post['title'][:100]}...\033[0m ({post['score']} - {ratio}%)")
        else:
            print(
                f"\033[93m{post['title']}\033[0m ({post['score']} - {ratio}%)")
        print(
            f"\033[93mPosted:\033[0m {created} \033[93mby\033[0m {post['author']}")
        print(f"\033[93mComments:\033[0m {post['num_comments']}")
        print(f"\033[93mURL:\033[0m {post['url']}")
        if post["selftext"]:
            print(f"\033[93mBody:\033[0m {post['selftext'][:200]}...")

        print('~~~~~~~~~~~~~~~~~~~~~~')


def to_local_time(utc_time):
    """Convert Reddit's stored UTC time to local formatted time"""
    t = datetime.utcfromtimestamp(utc_time)
    new_time = t.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return new_time.strftime("%x - %X")


if __name__ == '__main__':
    args = setup_argparse()

    response = pull_posts(args.subreddit, args.listing,
                          args.count, args.timeframe)
    print_feed(response)
