# Users

Configure users including group membership and SSH credentials.

A `users` dictionary is written to the host variables file that reflects the current state of the system. That dictionary can be edited manually or written from scratch and those changes will be applied to the host. Deletions or omissions in `groups` or `ssh` values of a user will be applied to the host.

System accounts are omitted from the `users` dictionary except for the following exceptions:

* `root` which is configurable but cannot be deleted.
* If a system account is defined in the inventory it will persist there. To delete a system account, define it in the `users` dictionary with the key `del` set to `true` (omitting it will not delete it since system accounts are omitted by default).

Additional features include:

* Set dynamic user names (`?`s are replaced with random lowercase alphanumeric characters).
* Configure a new `ansible_user` by setting the `ansible` key to `true`.
* Grant administrator privileges by setting the `adm` key to `true`.
* Safeguard against deleting `ansible_user`.

## Requirements

None.

## Role variables

### Defaults

#### System user identification

```yaml
ignore_user_shells:
  - /bin/nologin
  - /sbin/nologin
  - /usr/bin/nologin
  - /usr/sbin/nologin
  - /bin/false
  - ''
sys_id_thresh: 1000
pwd_lock: '*'
```

These pertain to identifying system users and password locking. On macOS, the system ID threshold is 500, and on OpenBSD, the password lock is `*************` (see `vars/user_vars_darwin.yml` and `vars/user_vars_openbsd.yml`).

#### Administrator groups

```yaml
adm_grps: []
```

Administrator groups vary by operating system. None are set by default. See platform-specific files in `vars/` for Linux and macOS administrator group lists.

#### Users

```yaml
users:
  root:
    gecos: root
    group: root
    groups:
    - root
    home: /root
    shell: /bin/bash
    ssh:
      auth: []
      id: []
    uid: '0'
  _agent_????:
    adm: true
    ansible: true
    ssh:
      auth:
      - pub: AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ==
        type: rsa
      id: []
    sys: true
```

This dictionary can be provided by the inventory or if it is undefined, the current state of the host will be written to the host's `host_vars` file. The key for each user is its user name. Note that users with names that are also built-in dictionary methods (such as `pop` or `copy`) cannot be managed by this role.

*Randomized user names*

Instances of `?` in a user name will be replaced with random lower case alphanumeric characters. The `users` dictionary will be updated in the `host_vars` file with the randomized name after the role is run.

Valid keys for each user are:

*Self explanatory*

* `gecos`*
* `group` (primary)
* `groups`*
* `home`*
* `lock`* ** (password lock)
* `shell`*
* `uid`*

*SSH*

 `ssh.auth` is a list of dictionaries describing the authorized SSH keys for the user. The public key and type should be specified in each item.

`ssh.id`* is a list of dictionaries describing the SSH key pairs for the user. In addition to the `pub` `type`, `file` may also be set for each item to specify the file name. Setting `pub` here will have no effect (It is populated automatically).

*Administrator*

Setting `adm` to `true` will add the user to groups defined in `adm_grps` and will run the `o0_o.host.privilege_escalation` role for that user. `adm` will only be written to the inventory if it is set to `true`. `false` is implied and so it is omitted to reduce the footprint on the `host_vars` file.

*Ansible user*

Setting `ansible` to `true` will imply `adm` is also `true`, and redefine `ansible_user` after running the `o0_o.host.privilege_escalation` role. If the previous `ansible_user` does not exist in the `users` dictionary, it will be deleted. The `ansible` key is _not_ written back to the `users` dictionary once the user is configured to avoid tracking the same information in 2 places (`ansible_user` and `users`).

*Deletion*

Setting `del` to `true` or omitting the user from the `users` dictionary will delete the user unless it is `root` or the current `ansible_user`.

*System user*

Setting `sys`* to `true` will create a system user which has a UID below the value of `sys_id_thresh`. Additionally, any groups that are created while configuring the user will be system groups (groups that already exist will not be changed). `sys` is only intended for the creation of new users and does not persist in the `users` dictionary since the user's status is evident from the `uid` once it is created.


\* Not valid for RouterOS users
\** Not supported on macOS or for the root user on OpenBSD

## Dependencies

* `o0_o.inventory`
* `o0_o.host.connection`
* `o0_o.host.privilege_escalation`
* `o0_o.host.time`
* `o0_o.host.software_management`
* `o0_o.host.python_interpreter`
* `o0_o.host.mandatory_access_control`
* `community.routeros`

## Example playbook

```yaml
- name: Example playbook using the o0_o.host.users role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - o0_o.host.users
```

## License

MIT

## Author Information

Email: o@o0-o.ooo
