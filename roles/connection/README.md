# Connection

Configure Ansible's connection to the host.

## Requirements

While this role will make a modest attempt to guess the values of Ansible connection variables (especially if it is a Vagrant virtual machine), an ssh key must be deployed onto the target host. It does not make any attempt to brute force passowrds.

`ansible_pylibssh` is required for using the `network_cli` connection type with `libssh`. This role will proactively install/update `pip` and `ansible-pylibssh` on `localhost` if `use_libssh` is `true`, which it is by default.

## Role variables

### Ansible configuration

Ansible connection configuration variables such as `remote_user` are inherently considered while attempting to configure the host connection.

### Defaults

#### Use connection

```yaml
use_con: false
```

Once a connection is successfully established, this is set to `true`. This is used to control the logical flow of the role.

#### Use libssh

```yaml
use_libssh: true
```

When `true`, this role will install or update `pip` and `ansible-pylibssh` on `localhost`.

#### Connection retries

```yaml
con_retries: 2
```

This controls how many times to retry the connection. Note that this does not retry on unreachable, but will retry if the registered output is not what it should be. This was implemented to address a strange issue with a FreeBSD VM which would successfully connect but output nothing on the first attempt.

#### Connection timeout

```yaml
con_timeout: 12
```

This controls the timeout value for connection attempts (in seconds).

#### Default administrator user names

```yaml
default_adms:
  - root
  - pi
  - vagrant
  - admin
```

This is a list of common default administrator user names. This is useful when you have a mix of different systems that have your SSH key deployed to them but under various default users. If the connection is not initially successful, this role will retry with each of these users.

## Dependencies

- `o0_o.inventory`
- `community.routeros`

## Example playbook

There is nothing special about running the role. It is included as a dependency for all `o0_o` roles that do not explicitly taget `localhost`.

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
