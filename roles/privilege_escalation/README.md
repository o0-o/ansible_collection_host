# Privilege escalation

Configure privilege escalation for the Ansible user and write the become method to the host's host_vars inventory file.

## Requirements

None

## Role variables

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
