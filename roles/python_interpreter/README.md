# Python Interpreter

Define and, if necessary, install a functional Python interpreter on the remote host.

The remote host's default minor version of Python 3 is preferred except in the case of RHEL/CentOS 7, where Python 2 is preferred because of missing Python 3 SELinux libraries.

The remote host's package manager may fail to install Python if repositories are misconfigured or time is out of sync. This role will attempt to correct each of these potential issues by running the `o0_o.host.package_manager` and/or `o0_o.host.time` roles, retrying Python installation after each role has executed. The `raw` Ansible module is used exclusively to interact with the remote host until a functional Python interpreter is defined. The resulting path to the Python interpreter is written to the remote hosts' `host_vars` file. If that Python interpreter becomes unavailable (become of a snapshot rollback for instance), re-running this role will correct for this, either by detected another functional Python interpreter, or installing one (`ansible_python_interpreter` is always tested and never inherently trusted).

While most Ansible collections will take for granted the availability of a Python interpreter, this leaves the task of deploying Python on systems like BSDs, macOS and some minimal Linux distributions, up to the administrator. The `o0_o` collections reject this assumption and will proactively install a Python interpreter with this role.

## Requirements

None.

## Role Variables

### Defaults

```yaml
python_pkg: python3
```

## Dependencies

- `o0_o.inventory`
- `o0_o.host.connection`
- `o0_o.host.privilege_escalation`
- `o0_o.host.facts`
- `o0_o.host.software_management`

## Example Playbook

```yaml
- name: Example playbook using the o0_o.host.python_interpreter role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.python_interpreter
```

## License

MIT

## Author Information

Email: o@o0-o.ooo
