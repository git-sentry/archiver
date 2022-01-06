import os

import click
from zen_core.handlers.git_client import GitClient
from zen_core.logging.printer import write, focus_out
from zen_core.parsing.toml_parser import parse_repo_configuration


def apply_configuration(git_client, repo_configurations, dry_run):
    for repo_name, repo_configuration in repo_configurations.items():
        repo = git_client.get_repo(repo_name)
        if repo:
            if dry_run:
                if not repo.archived():
                    print(f'{repo.full_name()}: {repo.archived()} -> True')
            else:
                repo.archive()
                print(f'{repo.full_name()} - {repo.archived()}')
        else:
            print(f'No repository matching {repo_name} found')


@click.group()
def cli():
    pass


@cli.command(help='Apply Git config from path')
@click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--dry-run', is_flag=True, default=False)
def apply(toml_path, dry_run):
    toml_path = os.path.expanduser(toml_path)
    git_client = GitClient()
    write(f'Welcome back, {focus_out(git_client.me().login())}!\n')

    repos = parse_repo_configuration(toml_path)
    apply_configuration(git_client, repos, dry_run)

    write('Nothing left to do, see you soon!')


def main():
    cli()
