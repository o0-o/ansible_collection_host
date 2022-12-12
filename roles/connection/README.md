# Connection

Configure Ansible's connection to the host.

## Requirements

`ansible_pylibssh` is required for using the `network_cli` connection type with `libssh`.

```shell
pip install ansible-pylibssh
```

## Role Variables

### Ansible configuration

Ansible connection configuration variables such as `remote_user` are inherently considered while attempting to configure the host connection.

### Vars

#### Default administrator user names

```yaml
default_adms:
  - root
  - pi
  - vagrant
  - admin
```

This is a list of common default administrator user names. This is useful when you have a mix of different systems that have your SSH key deployed to them but under various default users. This role will find the right value for `ansible_user` and write it to the `host_vars` inventory file.

## Dependencies

- `o0_o.inventory`

## Example playbook

```yaml
- name: Example playbook using the o0_o.host.connection role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.connection
```

## License

MIT

## Author information

Email: o@o0-o.ooo
