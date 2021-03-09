# RedditAPI
Script that pulls in posts from a given subreddit.

## Usage
```
python grr.py [options] <subreddit>
```
Options:
| Option      | Description |
| ----------- | ----------- |
| `-l <listing>` | Listing type. The type of listing to sort by, e.g. `hot`, `rising`, etc.       |
| `-c <number>`  | Post count. The number of posts to pull in a request        | 
| `-t <timeframe>`  | How far back in time you want to check for posts, e.g. `day`, `week`, etc.        | 

## TODO
* Handle calling non-existent subreddits
* Handle `count` number not including pinned posts
* Set min/max amount of posts to pull
* Better format how results are displayed
* Add cleaner color formatting
