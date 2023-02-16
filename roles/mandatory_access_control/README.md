# Mandatory Access Control

Install, enable and configure a mandatory access control system if one is available on the target host.

## Requirements

None.

## Role Variables

The `mac` variable is set to the name of the mandatory access control system that is or will be configured on the target system. These values are set in the `vars/` files according to the system type. Currently, the only valid values are `selinux` and `apparmor`. The value is written to the host's hostvars inventory file at the end of the role so that other roles can determine the MAC system on the host without always running this role.

If a host has no MAC system, then `mac` is set to an empty string. This allows us to determine if there is legitimately no MAC on the target host or if this role has simply not been run yet.

The `ansible_mac_deps` list contains the names of packages that are required on the system for mandatory access control and in the case of SELinux, packages required for Ansible to be able to manipulate it. As in the case of `mac`, values are set by system type in `vars/`

## Dependencies

- `o0_o.inventory`
- `o0_o.host.connection`
- `o0_o.host.privilege_escalation`
- `o0_o.host.time`
- `o0_o.host.software_management`
- `o0_o.host.python_interpreter`
- `ansible.posix`

## Example Playbook


```yaml
- name: Example playbook using the o0_o.host.mandatory_access_control role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.mandatory_access_control
```

## License

MIT

## Author Information

Email: o@o0-o.ooo
