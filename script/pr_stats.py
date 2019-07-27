from github import Github
import click

class PR_Stats(object):
    def __init__(self, token):
        self.github = Github(token)

    def run(self):
        for repo in self.github.get_user().get_repos():
            click.echo(repo.name)


@click.command()
@click.option('--token', '-t', prompt='GitHub personal access token')
def main(token):
    p = PR_Stats(token)
    p.run()

if __name__ == "__main__":
    main()
