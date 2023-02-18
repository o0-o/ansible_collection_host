# Time

Configure the time zone and sync time with `localhost` if it is outside of the configured tolerance.

On SSH hosts, the raw module is used because time sync may be necessary to successfully use a package manager to install Python (see `o0_o.host.software_management` and `o0_o.host.python_interpreter`).

On RouterOS, only GMT is supported (by this collection, not by RouterOS itself). This may change in the future but is a low priority.

## Requirements

The time must be accurate on `localhost`.

## Role variables

### Defaults

#### Time zone

We use localhost's time zone by default. Not all systems support UTC as a time zone valuebecause UTC is not technically a time zone. It is a standard that dictates the use of GMT.

#### Time sync tolerance

```yaml
time_sync_tolerance: 5
```

The sync tolerance is an integer representing the number of minutes of drift to allow between remote and local hosts. 5 was chosen as the default because that drift beyond 5 minutes will begin to cause issues with ldap/kerberos directory services such as Active Directory or FreeIPA.

#### Dependencies

```yaml
time_deps:
  - role: o0_o.host.privilege_escalation
```

We need privilege escalation to set change the time zone and time.

## Dependencies

- `o0_o.host.connection`
- `community.routeros`

## Example playbook

```yaml
- name: Example playbook using the o0_o.host.time role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
     - {name: o0_o.host.time, time_sync_tolerance: 30}
```

## License

MIT

## Author information

Email: o@o0-o.ooo
