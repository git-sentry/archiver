import os

import click
from zen_core.configuration.config_reader import read_config
from zen_core.handlers.git_client import GitClient
from zen_core.logging.printer import write, focus_out
from zen_core.parsing.toml_parser import parse_repo_configuration


def apply_configuration(git_client, repo_configurations, dry_run):
    for repo_name, repo_configuration in repo_configurations.items():
        matching_repos = git_client.search_repos(f'git-sentry/{repo_name}')

        for repo in matching_repos:
            repo.archive()
        for repo in matching_repos:
            print(f'{repo.full_name()} - {repo.archived()}')
            # for org in matching_orgs:
            #     org_config = org_config.resolve(org)
            #     current_configuration = org.configuration()
            #
            #     difference = org_config.diff(current_configuration)
            #
            #     if difference.length() != 0:
            #         write(f'Configuration analysis for {focus_out(org.login())} is complete.')
            #         write(difference)
            #
            #     if not dry_run:
            #         for m in difference.members():
            #             org.grant_access(m)
            #
            #         for m in difference.admins():
            #             org.grant_access(m, role='admin')
            #
            #         for team_name, team_config in difference.teams().items():
            #             existing_team = org.team(team_name)
            #             if existing_team is None:
            #                 existing_team = org.create_team(team_name)
            #
            #             for repo, permission in team_config.repos().items():
            #                 existing_team.add_to_repo(repo, permission)
            #
            #             for member in team_config.members():
            #                 existing_team.grant_access(member)
            #             for admin in team_config.admins():
            #                 existing_team.grant_access(admin, role='maintainer')


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
