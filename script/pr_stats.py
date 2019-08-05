#!/usr/local/bin/python

from datetime import datetime
from github import Github
import click
import sys

class PR_Stats(object):
    def __init__(self, token, per_page = 100):
        self.github = Github(token, per_page = per_page)


    def generate_search_query(self, created_since = None):
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        search_query = 'repo:{} is:pr is:merged'.format(self.repo.full_name)

        # Prevent race conditions with new PRs being merged while pulling the stats
        if self.prs_merged_since is None:
            search_query = ' merged:<{}'.format(self.prs_search_init_at.strftime(time_format))
        else:
            search_query += ' merged:{}..{}'.format(self.prs_merged_since.strftime(time_format), self.prs_search_init_at.strftime(time_format))

        if created_since is not None:
            search_query += ' created:>{}'.format(created_since.strftime(time_format))

        return search_query


    def search_pull_requests(self, created_since = None):
        search_query = self.generate_search_query(created_since)
        click.echo('==> Search query: {}'.format(search_query))

        search_response = self.github.search_issues(search_query, sort='created', order='asc')
        click.echo('==> Search response total count: {}'.format(search_response.totalCount))

        return search_response


    def format_pull_request(self, pr):
        return '{},{},{},{}'.format(pr.id, pr.user.login, pr.created_at, pr.closed_at)


    def dump_pull_requests(self, repo_name, merged_since, output):
        self.repo = self.github.get_repo(repo_name)
        self.prs_search_init_at = datetime.now()
        self.prs_merged_since = None
        if merged_since is not None:
            self.prs_merged_since = merged_since

        total_dumped = 0
        search_response = self.search_pull_requests()
        while search_response.totalCount > 0:
            last_dumped_pr = None
            for pr in search_response:
                output.write(self.format_pull_request(pr) + "\n")
                last_dumped_pr = pr
                total_dumped += 1
            click.echo('==> [PAGINATING]')
            search_response = self.search_pull_requests(last_dumped_pr.created_at)

        click.echo('==> [SUCCESS] Total pull requests dumped: {}'.format(total_dumped))


def cli_validate_merged_since(ctx, param, value):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise click.BadParameter('needs to be date with format YYYY-MM-DD')
    except TypeError:
        return None


@click.command()
@click.option('--token', '-t', prompt='GitHub personal access token', help='GitHub OAuth Token')
@click.option('--repo_name', '-r', prompt='GitHub repository name', help='Full name of GitHub repository (e.g. emberjs/ember.js)')
@click.option('--merged_since', '-s', type=str, callback=cli_validate_merged_since, help='OPTIONAL. Fetch pull requests merged after this date.')
def main(token, repo_name, merged_since):
    pr_stats = PR_Stats(token)
    pr_stats.dump_pull_requests(repo_name, merged_since, sys.stdout)

if __name__ == '__main__':
    main()
