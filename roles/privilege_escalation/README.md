# Privilege escalation

Configure privilege escalation for the Ansible user and write the become method to the host's host_vars inventory file.

## Requirements

None

## Role variables

### Optional

#### `new_ansible_user_var`

Set this value to configure Ansible's become method for a different user than the current Ansible user. This is useful for setting up privilege escalation for a user before setting `ansible_user` to that user. Note that `ansible_user` is not updated by this role but should be set to the new value as soon as this role is finished running as it will update `ansible_become_method` which may break `become` on the current Ansible user.

See `o0_o.host.ansible_user` for how this is done in practice.

### Vars

See `vars/` for platform-specific overrides of the variables below which are set in `vars/main.yml`.

#### `doas`

```yaml
doas_cfg_path: /etc
doas_cfg_file: doas.conf
doas_cfg_mode: 0600
doas_bin: /usr/bin/doas
```

#### `sudo`

```yaml
sudo_cfg_path: /etc
sudo_cfg_file: sudoers
sudo_cfg_subdir: sudoers.d
sudo_cfg_subdir_mode: 0750
sudo_cfg_subdir_file_mode: 0440
sudo_bin: /usr/bin/sudo
visudo_bin: /usr/sbin/visudo
```

#### SELinux

```yaml
adm_seuser: staff_u
```

## Dependencies

- `o0_o.inventory`
- `community.general`*

\* Not technically required unless SELinux is in use.

## Example Playbook

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
