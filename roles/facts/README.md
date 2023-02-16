# Facts

This role wraps the typical `gather_facts`, `setup` module behavior, adding some additional functionality.

If a Python interpreter is not yet available, preliminary facts are set based on `uname` output, and on Linux systems, the contents of `/etc/os-release` are stored in the `linux_os_release` dictionary. These variables are used by other pre-Python-friendly roles including `o0_o.host.time` and `o0_o.host.software`.

When a Python interpreter is available, the `setup` module is run along with `service_facts`, and some values are manually set for Raspberry Pi and macOS hosts, where the `setup` module fails to collect some values.

On RouterOS hosts, the `routing`, `interfaces`, `hardware` and `default` subsets are gathered using the `community.routeros.facts` module.

An `update facts` handler is also provided which simply runs `tasks/main.yml`. As a result, this role cannot include or import other roles.

## Requirements

None.

## Role variables

### Defaults

#### `bad_serials`

This is a list of unacceptable values for `ansible_product_serial`. If a Python interpreter is available and `ansible_product_serial` is set to one of these values or is undefined at the end of this role, a warning is printed via the `debug` module. Default values are an empty string or `0`. Uniqueness is not tested for, but may be in a future version.

#### `ssh_pub_key_local_file`

The default ssh public key local file the most recently modified result of `~/.ssh/*.pub` on localhost. This mimics the behavior of `ssh-copy-id` when no `-i` value is provided. Override `ssh_pub_key_local_file` to affect the value of `ssh_pub_key` indirectly.

#### `ssh_pub_key`

By default, the ssh public key is set to the contents of `ssh_pub_key_local_file`. Overriding `ssh_pub_key` will circumvent the use of `ssh_pub_key_local_file`.

#### `root_grp`

See `root_grps` (plural) below for details. This is intended as a catchall and it is set to `wheel`.

### Vars

#### `root_grps`

The root groups variable is a dictionary of root group names on different systems. BSD's prefer `wheel` whereas Linux distributions prefer `root`. Once the system type is defined, the value of `root_grp` (singular) is set to the appropriate value. `root_grp` is used by many other `o0_o` roles and collections when setting group ownership of files on target hosts.

## Dependencies

- `o0_o.host.connection`
- `o0_o.host.privilege_escalation`
- `o0_o.host.python_interpreter`
- `community.routeros`*

\* These are required for RouterOS hosts.

## Example playbooks

```yaml
- name: Example playbook using the o0_o.host.facts role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.facts
```

```yaml
- name: Example playbook using the update facts handler
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  tasks:

    # Changes to network configuration may result in stale fact values
    - name: Run tasks to configure a network interface
      ansible.builtin.shell: sh configure_interface
      notify: update facts
```

## License

MIT

## Author information

Email: o@o0-o.ooo
