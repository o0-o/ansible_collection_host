# oØ.o's Host Collection for Ansible

This collection includes Ansible roles and plugins for opinionated, portable configuration of hosts with an emphasis on complete automation. Manual intervention is limited as much as possible, including writes to the Ansible inventory. Storage, network and service configuration are intentionally not included here (they are handled or will be handled by other `o0_o` collections).

## Code of Conduct

Be excellent to each other.

## Communication

Releases and other important changes will be announced through [the Github repository](https://github.com/o0-o/ansible_collection_host).

## Contributing to this collection

Contributions are welcome, especially support for additional platforms! Contribute via the normal pull request process on Github.

## Collection maintenance

oØ.o is the sole maintainer of this collection.

## Governance

This project is solely run by me, oØ.o. I have final say in all aspects of it. If this is not to your liking, please fork.

## Tested with Ansible

Versions 2.11+

## External requirements

- `ansible-pylibssh`

### Supported connections

- `ssh`
- `ansible.netcommon.network_cli`

## Included content

### Plugins

#### Lookup

- `first_found_by_host_attributes`

### Roles

- `connection`

## Using this collection

### Examples

```yaml
- name: Example playbook using the o0_o.host collection
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
    - o0_o.host.connection
```

### Installing the Collection from Ansible Galaxy

```shell
pip install ansible-pylibssh
ansible-galaxy role install o0_o.inventory
ansible-galaxy collection install o0_o.host
```

You can also include Ansible dependencies in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
roles:
  - name: o0_o.inventory
collections:
  - name: o0_o.host
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```shell
ansible-galaxy collection install o0_o.host --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```shell
ansible-galaxy collection install o0_o.host:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

### `0.1.0-alpha.1`
- Initially created the collection.
- `first_found_by_host_attributes` lookup plugin added.
- `connection` role added.

## Roadmap

### Plugins

#### Lookup
- ~~First found tasks, vars or template file based on system attributes~~

### Roles
- ~~Connection~~
- Privilege escalation
- Time
- Python interpreter
- Facts
- Mandatory access control (MAC)
- Ansible user
- Time zone
- System-specific sane defaults and hardening
  - Arch Linux
  - Centos/RHEL 7
  - Rocky/RHEL 8
  - Fedora
  - Debian
  - Ubuntu
  - FreeBSD
  - OpenBSD
  - macOS
  - RouterOS
- Repository
- Updates
- Antivirus
- Auditing
- Intrusion detection

### Playbooks
- Host configuration baseline

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

This collection uses the MIT license.

See [LICENSE](https://spdx.org/licenses/MIT.html) to see the full text.

---

This file was written using boilerplate from the [Ansible collection template repository](https://github.com/ansible-collections/collection_template).
