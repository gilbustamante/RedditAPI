#!/usr/bin/python
"""
Fetches Reddit posts from given subreddit based on supplied options, formats
them and prints them to stdout
"""
from datetime import datetime, timezone
import sys
import argparse
from colorama import Fore, Style, init
import requests

VERSION = 0.2

# Initialize colorama (for Windows)
init()


def setup_argparse():
    """Setup and parse arguments"""
    reddit_parser = argparse.ArgumentParser(
        prog="Gil's Reddit Reader",
        description="Pull post info from Reddit for reading from the comfort \
        of your terminal.",
        usage="grr.py [options] subreddit",
    )
    reddit_parser.add_argument("-l",
                               metavar="Listing type",
                               dest="listing",
                               choices=["hot", "new", "best",
                                        "random", "rising", "top"],
                               help="The type of listing to sort by. \
                               Possible arguments: hot, new, best, random, \
                               rising, top.", default="hot", required=False)
    reddit_parser.add_argument('-c',
                               metavar="Post count",
                               dest="count",
                               help="The number of posts to pull in a \
                               request.", default=10, required=False)
    reddit_parser.add_argument("-t",
                               metavar="Timeframe",
                               dest="timeframe",
                               choices=["hour", "day", "week",
                                        "month", "year", "all"],
                               help="How far back in time you want to check \
                               for posts. Possible arguments: hour, day, \
                               week, month, year, all.", default="all",
                               required=False)
    reddit_parser.add_argument("subreddit",
                               help="The subreddit from which posts will be \
                               pulled.",)
    cli_args = reddit_parser.parse_args()

    return cli_args


def pull_posts(sub, listing, count, timeframe):
    """Request JSON data from Reddit and return"""
    url = f"https://www.reddit.com/r/{sub}/{listing}.json?limit={count}"\
        f"&t={timeframe}&raw_json=1"
    headers = {
        'User-agent': f'GRAPI v{VERSION}'
    }
    try:
        res = requests.get(url, headers=headers)
    except requests.ConnectionError as ex:
        print("There was a connection error:")
        print(ex)
        sys.exit()
    return res.json()


def yel(input_text):
    """Helper function to print yellow text"""
    return Fore.YELLOW + input_text + Style.RESET_ALL


def red(input_text):
    """Helper function to print red text"""
    return Fore.RED + input_text + Style.RESET_ALL


def green(input_text):
    """Helper function to print red text"""
    return Fore.GREEN + input_text + Style.RESET_ALL


def print_feed(data):
    """Iterate through results and print formatted posts"""
    for item in data["data"]["children"]:
        post = item["data"]
        ratio = int(post["upvote_ratio"] * 100)
        created = to_local_time(post["created_utc"])
        if len(post["title"]) > 100:
            title = yel(f"{post['title'][:100]}... ")
            if ratio > 50:
                score = green(f"({post['score']} - {ratio}%)")
            else:
                score = red(f"({post['score']} - {ratio}%)")
            print(title + score)
        else:
            title = yel(f"{post['title']} ")
            if ratio > 50:
                score = green(f"({post['score']} - {ratio}%)")
            else:
                score = red(f"({post['score']} - {ratio}%)")
            print(title + score)

        print(f"{yel('Posted:')} {created} {yel('by')} {post['author']}")
        print(f"{yel('Comments:')} {post['num_comments']}")
        print(f"{yel('URL:')} {post['url']}")
        if post["selftext"]:
            print(f"{yel('Body:')} {post['selftext'][:200]}...")

        print('~~~~~~~~~~~~~~~~~~~~~~')


def to_local_time(utc_time):
    """Convert Reddit's stored UTC time to local formatted time"""
    current = datetime.utcfromtimestamp(utc_time)
    new_time = current.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return new_time.strftime("%x - %X")


if __name__ == '__main__':
    args = setup_argparse()

    response = pull_posts(args.subreddit, args.listing,
                          args.count, args.timeframe)
    try:
        print_feed(response)
    except KeyError:
        print('That subreddit either does not exist or is set to private.')
