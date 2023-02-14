# Software management

Configure software management including package managers, repositories and any other software managers. While most of the configuration revolves around what are generally referred to as package managers and repositories, the broader `software management` is chosen because system utilities like `freebsd_update` and macOS's `softwareudpate` are also included. Whether or not these are considered package managers or something else is a semantic question that is hopefully avoided by using a more general name.

This role can run without a Python interpreter. This allows software management to be configured so that a Python interpreter can be installed. In most cases, this is not necessary since most operating systems are installed with functional package management. However, in certain situations that may not be the case. For instance, if deploying to a sandboxed or air-gapped environment with a local mirror, it will not be possible to install Python without first configuring a package manager and repositories. Additionally, in some cases, if the operating system was installed from the network, the host may look to the PXE server for packages which may not be appropriate for every environment.

While this role can run using only the `raw` module to interact with the remote host, it should be run again once a Python interpreter is available. This is handled automatically in conjunction with the `o0_o.host.python_interpreter` role so no action is required. Just note that the role running twice when Python is not initially available is expected behavior.

This role will not fail to run on hosts that have no software management to configure (network devices), it will simply have no effect.

# Requirements

None.

## Role variables

### Defaults

 The defaults here are built from a combination of operating system-provided defaults, some hardening and best practices. They are too numerous to list here, so please see `defaults/main/` for the full definitions.

#### Use software management

```yaml
use_sw_mgmt: false
```

Once software management is successfully configured, this is set to `true`. This is used to control the logical flow of role dependency.

#### Default architectures

```yaml
os_arch: x86_64/amd64
```

This is the default architecture for each operating system. The default values are `x86_64` or `amd64` depending on which is preferred by the OS, specifically which is used in mirror paths.

#### Default releases

```yaml
os_release: 1.2.3
```

This is the default release for each operating system. The naming here correlates to mirror paths. For instance, Ubuntu uses the release nickname instead off the version string.

#### Package manager configuration

Package manager configuration is built from a series of variables, all of which may be set manually to achieve various results. Package managers and/or operating systems may have slightly different approaches. DNF is used as an example below because it is the most complex.

```yaml
fedora_dnf_cfg: >-
  {{  [ dnf_yum_cfg_common_default,
        dnf_yum_cfg_common_add,
        dnf_cfg_default,
        dnf_cfg_add,
        fedora_dnf_cfg_default,
        fedora_dnf_cfg_add ]
      | combine }}
```

Dictionaries with the `default` suffix contain default configuration boilerplate. It is generally close to what comes with a default installation of the package manager and/or operating system. They can be overriden in their entirety when this role is invoked.

Dictionaries with the `add` (additional) suffix are all set to `{}` in `defaults/main/`. They provide a mechanism for adding configuration that will be _combined with the values in the `default` version of the dictionary_. This is useful when one parameter should be added or changed without wiping out the entire default configuration.

This paradigm is repeated for configuration shared between DNF and YUM, configuration for DNF across all distributions and finally for DNF on Fedora specifically. The resulting configuration is stored in `fedora_dnf_cfg` which can also be provided when the role is invoked to statically define the entire DNF configuration.

Note that while this approach is replicated across most operating systems and package managers, some cases are much simpler. For instance, in OpenBSD, the only configuration values are `openbsd_install_url` and `openbsd_fw_url`. Review the appropriate files in `defaults/main/` if defaults need to be changed.

#### Repository configuration

Repository configuration is similar to that of package managers but slightly more complex. In this case, we use `Debian` as an example.

**Shared repository configuration**

```yaml
debian_apt_repos_cfg: "{{ [ repos_cfg,
                            apt_repos_default,
                            apt_repos_add,
                            debian_apt_repos_cfg_default,
                            debian_apt_repos_cfg_add ]
                          | combine }}"
```

Configuration is combined from most general to most specific in a similar way as the package manager configuration. Note that in this case, there is also a `repos_cfg` dictionary that contains defaults for all repositories across all operating systems. The only value set there is `enabled: false`. Repositories must be explicitly enabled as a best practice.

**Individual repository configurations**

```yaml
debian_apt_repo_main:
  enabled: true
debian_apt_repo_non_free:
  enabled: true
debian_apt_repo_contrib: {}
```

Each default repository has its own dictionary. These can only be defined in their entirety. The `default` and `add` paradigm is not applied here to prevent the default variables files from becoming unwieldy.

**Consolidated repository configurations**

```yaml
debian_apt_repos_default:
  main: >-
    {{ [debian_apt_repos_cfg, debian_apt_repo_main] | combine }}
  contrib: >-
    {{ [debian_apt_repos_cfg, debian_apt_repo_contrib] | combine }}
  non-free: >-
    {{ [debian_apt_repos_cfg, debian_apt_repo_non_free] | combine }}
debian_apt_repos_add: {}
debian_apt_repos: >-
  {{ [debian_apt_repos_default, debian_apt_repos_add] | combine }}
```

The individual repository configurations are combined with the shared configuration and consolidated in the `debian_apt_repos_default` dictionary. If any additional repositories are provided via the `repos_add` dictionary, they are combined with `debian_apt_repos_default`, resulting in `debian_apt_repos` which will be used to configure `/etc/apt/sources.list` (unless a `repos` dictionary is provided, in which case none of this will have any effect).

### Vars

Most of the variables set in `vars/main.yml` provide structure to the values provided by `defauts/main.yml`. This allows the defaults to be adjusted granularly while avoiding messy variable manipulation and parsing in the role.

**Architectures by operating system**

```yaml
arches:
  archlinux: "{{ archlinux_arch }}"
  centos: "{{ centos_arch }}"
  debian: "{{ debian_arch }}"
  fedora: "{{ fedora_arch }}"
  freebsd: "{{ freebsd_arch }}"
  openbsd: "{{ openbsd_arch }}"
  rocky: "{{ rocky_arch }}"
  ubuntu: "{{ ubuntu_arch }}"
```

**Releases by operating system**

```yaml
releases:
  archlinux: "{{ archlinux_release }}"
  centos: "{{ centos_release }}"
  debian: "{{ debian_release }}"
  fedora: "{{ fedora_release }}"
  freebsd: "{{ freebsd_release }}"
  openbsd: "{{ openbsd_release }}"
  rocky: "{{ rocky_release }}"
  ubuntu: "{{ ubuntu_release }}"
```

**Package manager configurations by operating system**

```yaml
os_pkg_mgr_cfgs:
  archlinux:
    pacman: "{{ archlinux_pacman_cfg }}"
  centos:
    yum: "{{ centos_yum_cfg }}"
  darwin:
    homebrew: "{{ darwin_homebrew_cfg }}"
    macos_softwareupdate: "{{ macos_softwareupdate_cfg }}"
  debian:
    apt: "{{ debian_apt_cfg }}"
  fedora:
    dnf: "{{ fedora_dnf_cfg }}"
  freebsd:
    freebsd_pkg: "{{ freebsd_pkg_cfg }}"
    freebsd_update: "{{ freebsd_update_cfg }}"
  openbsd:
    openbsd_pkg: "{{ openbsd_pkg_cfg }}"
    openbsd_fw: "{{ openbsd_fw_cfg }}"
    openbsd_sys: "{{ openbsd_sys_cfg }}"
  rocky:
    dnf:  "{{ rocky_dnf_cfg }}"
  ubuntu:
    apt: "{{ ubuntu_apt_cfg }}"
```

**Repository configurations by operating system and package manager**

```yaml
os_pkg_mgr_repos:
  archlinux:
    pacman: "{{ archlinux_pacman_repos }}"
  centos:
    yum: "{{ centos_yum_repos }}"
  darwin:
    homebrew: "{{ darwin_homebrew_repos }}"
    macos_softwareupdate: {} #Not applicable
  debian:
    apt: "{{ debian_apt_repos }}"
  fedora:
    dnf: "{{ fedora_dnf_repos }}"
  freebsd:
    freebsd_pkg: "{{ freebsd_pkg_repos }}"
    freebsd_upate: {} #Not applicable
  openbsd:
    openbsd_pkg:
      openbsd_repo: "{{ openbsd_pkg_repo }}"
    openbsd_fw:
      openbsd_fw_repo: "{{ openbsd_fw_repo }}"
    openbsd_sys:
      openbsd_sys_repo: "{{ openbsd_sys_repo }}"
  rocky:
    dnf: "{{ rocky_dnf_repos }}"
  ubuntu:
    apt: "{{ ubuntu_apt_repos }}"
```

**Role dependencies for SSH hosts**

```yaml
cfg_sw_ssh_deps:
  - role: o0_o.host.privilege_escalation
  - role: o0_o.host.time
```

## Dependencies

- `o0_o.inventory`
- `o0_o.host.connection`
- `o0_o.host.privilege_escalation`
- `o0_o.host.facts`
- `o0_o.host.time`
- `community.general`*

\* Required for doas support.

Note that the `privilege_escalation`, `software_management` and `mandatory_access_control` roles are all dependent on each other. While these roles are designed around these circular dependencies (they do not infinitely recurse), the outcome of running any one of these roles will be identical.

## Example playbook

```yaml
- name: Example playbook using the o0_o.host.software_management role
  hosts: all
  gather_facts: false
  any_errors_fatal: true
  roles:
    - name: o0_o.host.software_management
      centos_yum_cfg_add:
        installonly_limit: 5
```

## License

MIT

## Author information

Email: o@o0-o.ooo
