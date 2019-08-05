# dev-cycles (work in progress)

Analyzing PR data correlating it to the development cycles of an open-source project

#### Installing
```
[GITLAB_DOWNLOADS_DIR]/dev-cycles $ docker build -t dev-cycles .
```

#### Running
```
$ docker run -v --rm -it dev-cycles /app/script/pr_stats.py --token [GITHUB_OAUTH_TOKEN] --repo_name [FULL_REPO_NAME] {--merged_since [YYYY-MM-DD]}
```

#### Example
```
$ docker run -v --rm -it dev-cycles /app/script/pr_stats.py --token SECRET --repo_name emberjs/ember.js --merged_since 2019-08-01

==> Search query: repo:emberjs/ember.js is:pr is:merged merged:2019-08-01T00:00:00Z..2019-08-05T21:16:37Z
==> Search response total count: 2
467561172,rwjblue,2019-07-12 19:12:31,2019-08-01 00:24:47
476319285,Exelord,2019-08-02 19:12:40,2019-08-04 14:44:54

==> [PAGINATING]

==> Search query: repo:emberjs/ember.js is:pr is:merged merged:2019-08-01T00:00:00Z..2019-08-05T21:16:37Z created:>2019-08-02T19:12:40Z
==> Search response total count: 0

==> [SUCCESS] Total pull requests dumped: 2
```

#### `script/pr_stats.py`

```
Usage: pr_stats.py [OPTIONS]

Options:
  -t, --token TEXT         GitHub OAuth Token
  -r, --repo_name TEXT     Full name of GitHub repository (e.g.
                           emberjs/ember.js)
  -s, --merged_since TEXT  OPTIONAL. Fetch pull requests merged after this
                           date.
  --help                   Show this message and exit.
```

This script dumps GitHub Pull Request data from the requested repository.