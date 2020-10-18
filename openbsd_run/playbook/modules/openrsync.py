#!/usr/bin/env python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict


class Openrsync:
    def __init__(self, module: AnsibleModule) -> None:
        """"""
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/bin/openrsync"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""


def main() -> None:
    module: AnsibleModule = AnsibleModule(argument_spec={})

    openrsync: Openrsync = Openrsync(module)

    result: Dict[str, Any] = {
        "changed": openrsync.changed,
        "command": openrsync.command,
        "msg": openrsync.msg,
        "reboot": openrsync.reboot,
        "rc": openrsync.rc,
        "stdout": openrsync.stdout,
        "stderr": openrsync.stderr,
    }

    if openrsync.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
