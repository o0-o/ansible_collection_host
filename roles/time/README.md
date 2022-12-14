# Time

Sync time with `localhost` if it is outside of the configured tolerance.

On SSH hosts, the raw module is used because time sync may be necessary to successfully install Python (see `o0_o.host.python_interpreter`).

Time zone configuration is unaffected and may be different between remote and local hosts except in the case of RouterOS where only GMT is supported (by this collection, not by RouterOS itself). So, in the case of RouterOS, the `o0_o.host.time_zone` role is run before syncing times to ensure the remote host's timezone is set to GMT.

## Requirements

The time must be accurate on `localhost`.

## Role variables

### Defaults

```yaml
time_sync_tolerance: 5
```

The sync tolerance is an integer representing the number of minutes of drift to allow between remote and local hosts. 5 was chosen as the default because that drift beyond 5 minutes will begin to cause issues with ldap/kerberos directory services such as Active Directory or FreeIPA.

## Dependencies

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
