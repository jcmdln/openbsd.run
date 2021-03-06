from __future__ import annotations

from logging import Logger
from sys import exit

import ansible_runner as ansible
import click

from ansible_runner import Runner

from openbsd_run.playbook import path as playbook_path
from openbsd_run.utils.log import Log


@click.command(name="pkg_delete", short_help="Remove packages")
@click.option(
    "-a",
    default=False,
    help="Delete unused dependencies",
    is_flag=True,
    type=bool,
)
@click.option(
    "-D",
    default="",
    help="Force package removal, waiving the specified failsafe",
    type=str,
)
@click.argument("packages", nargs=-1)
@click.pass_context
def pkg_delete(context, a: bool, d: str, packages: list[str]) -> None:
    log: Logger = Log("openbsd-run: pkg")

    host_pattern = context.obj["host_pattern"]
    inventory_contents: dict = context.obj["inventory_contents"]
    quiet: bool = context.obj["quiet"]
    verbose: bool = context.obj["verbose"]

    extra_vars: dict = {}

    if a:
        extra_vars["pkg_delete_unused"] = a

    if d and d not in [
        "baddepend",
        "checksum",
        "dependencies",
        "nonroot",
        "scripts",
    ]:
        log.error("'%s' is not a valid failsafe to waive")
        exit(1)

    if d:
        extra_vars["pkg_force"] = d

    if "*" in packages:
        log.error("'%s' is not a valid list of package names" % packages)
        exit(1)
    else:
        extra_vars["pkg_packages"] = packages
        extra_vars["pkg_state"] = "absent"
        extra_vars["pkg_title"] = "delete"

    result: Runner = ansible.run(
        extravars=extra_vars,
        inventory=inventory_contents,
        limit=host_pattern,
        playbook="%s/site-pkg.yml" % playbook_path,
        project_dir=playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        verbosity=3 if verbose else None,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        exit(1)

    exit(0)
