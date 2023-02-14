# Privilege escalation

Configure privilege escalation for a specified user (the Ansible user by default). If `sudo` is used in combination with a system running `SELinux`, appropriate user contexts are configured.

## Requirements

None

## Role variables

### Defaults

#### Privileged user

```yaml
priv_user: "{{ ansible_user }}
```

Set this value to configure privilege escalation for a different user than the current Ansible user. This is useful for setting up privilege escalation for a user before setting `ansible_user` to that user. Note that `ansible_user` is not updated by this role.

#### Privilege escalation methods

```yaml
priv_methods:
  - doas
  - sudo
fallback_priv_method: sudo
```

If `doas` is available, it is preferred over `sudo`. If neither is functional, fallback to `sudo`. In the case that `ansible_user` is root and `priv_user` is not, an attempt will be made to install `sudo`.

### Vars

See `vars/` for variables specific to `doas`, `sudo` and role dependencies. Knowing their values is not crucial for using or understanding this role.

## Dependencies

- `o0_o.host.connection`
- `o0_o.host.facts`
- `o0_o.host.software_management`
- `o0_o.host.python_interpreter`
- `o0_o.host.mandatory_access_control`
- `community.general`*
- `ansible.posix`*

\* Required for `doas` and/or SELinux support.

## Example Playbook

There is nothing special about running the role. It is included as a dependency for almost all `o0_o` roles.

```yaml
- name: Example playbook using the o0_o.host.connection role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.privilege_escalation
```

## License

MIT

## Author information

Email: o@o0-o.ooo
