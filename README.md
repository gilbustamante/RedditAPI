# RedditAPI
Script that pulls in posts from a given subreddit.

## Requirements
The following modules are needed:
  * `requests`
  * `colorama`

Install with this command:
```
pip install requests colorama
```

## Usage
```
python grr.py [options] <subreddit>
```
Options:
| Option           | Description                                                                | Default |
|------------------|----------------------------------------------------------------------------|---------|
| `-l <listing>`   | Listing type. The type of listing to sort by, e.g. `hot`, `rising`, etc.   | `hot`
| `-c <number>`    | Post count. The number of posts to pull in a request.                      | `10`
| `-t <timeframe>` | How far back in time you want to check for posts, e.g. `day`, `week`, etc. | `all`

## TODO
* Handle calling non-existent subreddits
* Handle `count` number not including pinned posts
* Set min/max amount of posts to pull
