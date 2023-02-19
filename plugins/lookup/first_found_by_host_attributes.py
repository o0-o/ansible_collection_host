from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: first_found_by_host_attributes
    author: o0-o
    short_description: return first found path to vars, tasks or template file
      based on attributes of the host
    description:
      - This lookup is an extension of the builtin C(first_found) plugin.
      - This lookup checks a list of files and paths based on the host
        operating system and other characteristics, and returns the full path
        to the first match in the current search path(s).
      - The lookup checks for matches from most to least specific, beginning
        with the distribution name, full version and network management
        service.
      - A type of C(vars), C(tasks) or C(template) is required for this plugin
        to operate.
      - In addition to gathered Ansible facts and Ansible special variables,
        a C(net_mgr) fact may be set to indicate the network management system
        in use on the host (typically to differentiate between NetworkManager,
        systemd-networkd, etc. on Linux).
      - In addition to gathered Ansible facts and Ansible special variables,
        a C(mac) fact may be set to indicate which mandatory access control
        system is in use (typically to differentiate between SELinux and
        AppArmor).
      - "The lookup checks for matches in the following order:

        C(ansible_distribution)-C(ansible_distribution_version)-C(net_mgr)

        C(ansible_distribution)-C(ansible_distribution_version)-C(mac)

        C(ansible_distribution)-C(ansible_distribution_version)

        C(ansible_distribution)-C(ansible_distribution_major_version)-\
        C(net_mgr)

        C(ansible_distribution)-C(ansible_distribution_major_version)-C(mac)

        C(ansible_distribution)-C(ansible_distribution_major_version)

        C(ansible_distribution)-C(net_mgr)

        C(ansible_distribution)-C(mac)

        C(ansible_distribution)

        C(ansible_system)-C(net_mgr)

        C(ansible_system)-C(mac)

        C(ansible_system)

        C(net_mgr)

        C(mac)

        C(ansible_network_os) (does not use FQCN)

        C(ansible_connection) (does not use FQCN)"
    notes:
      - Lookups that call for facts that are undefined are omitted.
      - When using the C(o0_o.host.mac) role, the possible values of C(mac)
        are C(selinux) or C(apparmor).
      - When using the C(o0_o.network) collection, the possible values of
        C(net_mgr) are C(nm) for NetworkManager and C(netd) for
        systemd-networkd.
    options:
      _terms:
        description: C(vars), C(tasks) or C(template)
        required: True
      files:
        description: This is an option for the C(first_found) plugin which this
          plugin extends. For this plugin to work, it needs to be included
          here, but the option has no effect.
        type: list
        elements: string
        required: False
      paths:
        description: This is an option for the C(first_found) plugin which this
          plugin extends. For this plugin to work, it needs to be included
          here, but the option has no effect.
        type: list
        elements: string
        required: False
      prefix:
        type: string
        default: ''
        description:
          - A prefix to use on all file names.
        required: False
      suffix:
        type: string
        default: ''
        description:
          - A suffix to use on all file names.
          - The suffix does not include the extension which is set with 'ext'.
        required: False
      delim:
        type: string
        default: '-'
        description:
          - This is the delimiter to be used between host attributes.
        required: False
      default:
        type: string
        description:
          - This is a default file name to search for.
          - The default file is matched last.
          - The default file name is subject to prefix, suffix and ext.
        required: False
      ext:
        type: string
        description:
          - This is the extension to use when searching for files.
          - The default value is 'j2' for templates and 'yml' for vars and
            tasks.
        required: False
      skip:
        type: boolean
        default: False
        description:
          - When C(true), return C(/dev/null/) when no files are matched.
          - This is useful when used with C(include_vars) or C(include_tasks)
            modules, as C(/dev/null) results in no action or error. It is
            not recommended to use C(skip=true) with the C(src) parameter of
            the C(template) module.
          - When C(false) and C(lookup) or C(query) specifies
            I(errors='ignore'), all errors (including no file found, but
            potentially others) return C('')
        required: False
"""

# TODO: add more examples
EXAMPLES = """
# A possible result here would be 'cfg_my_srv_debian-11.yml'
- name: Run tasks to configure a service based on the host platform
  ansible.builtin.include_tasks: >-
    {{ lookup(  'o0_o.utils.first_found_by_platform',
                'tasks',
                prefix='cfg_my_srv_ ) }}

# /dev/null is returned on if skip=true and no matches are found. This
# allows `include_tasks` to run successfully without actually doing
# anything if desired.
- name: Define variables based on the host platform and do nothing if no
    matches are found
  ansible.builtin.include_tasks: >-
    {{ lookup(  'o0_o.utils.first_found_by_platform',
                'tasks',
                skip=true ) }}
"""

RETURN = """
  _raw:
    description:
      - path to file found
    type: string
"""

import ansible.plugins.lookup.first_found as first_found

from ansible.errors import AnsibleLookupError


class LookupModule(first_found.LookupModule):

    def _process_plat_terms(self, terms, variables, kwargs):

        # Audit terms
        if len(terms) != 1:
            raise AnsibleLookupError(
                "Invalid number of terms supplied, can handle 'vars', 'tasks' "
                + "or 'template' but got: %s"
                % terms
            )

        if terms[0] not in ['vars', 'tasks', 'template']:
            raise AnsibleLookupError(
                "Invalid term supplied, can handle 'vars', 'tasks' or "
                + "'template' but got: %s"
                % terms
            )

        # Define the sequence of variables to be used by first_found in
        # order of highest to lowest precedence
        ff_plat_keys_seq = [
            [
                'ansible_distribution',
                'ansible_distribution_version',
                'net_mgr'
            ],
            ['ansible_distribution', 'ansible_distribution_version', 'mac'],
            ['ansible_distribution', 'ansible_distribution_version'],
            [
                'ansible_distribution',
                'ansible_distribution_major_version',
                'net_mgr'
            ],
            [
                'ansible_distribution',
                'ansible_distribution_major_version',
                'mac'
            ],
            ['ansible_distribution', 'ansible_distribution_major_version'],
            ['ansible_distribution', 'net_mgr'],
            ['ansible_distribution', 'mac'],
            ['ansible_distribution'],
            ['ansible_os_family', 'net_mgr'],
            ['ansible_os_family', 'mac'],
            ['ansible_os_family'],
            ['ansible_system', 'net_mgr'],
            ['ansible_system', 'mac'],
            ['ansible_system'],
            ['net_mgr'],
            ['mac'],
            ['ansible_network_os'],
            ['ansible_connection']
        ]

        # Define term and default extension
        term = terms[0]

        if term == 'template':
            term = 'templates'
            default_ext = 'j2'
        else:
            default_ext = 'yml'

        # Get options
        self.set_options(var_options=variables, direct=kwargs)

        # Define plugin parameters
        ext = self.get_option('ext') or default_ext
        prefix = self.get_option('prefix')
        suffix = self.get_option('suffix')
        delim = self.get_option('delim')
        default = self.get_option('default')
        var_keys = list(variables.keys())
        files = []

        # Loop through the sequence of variables to be used by
        # first_found
        for plat_keys in ff_plat_keys_seq:
            plat_attrs = []

            # Only proceed if all variables are defined
            if len(set(plat_keys).intersection(var_keys)) == len(plat_keys):
                # Put each variable value in a list
                for k in plat_keys:
                    if k in ['ansible_network_os', 'ansible_connection']:
                        # Strip FQCN
                        plat_var = variables[k].split('.')[-1]
                    else:
                        plat_var = variables[k]
                    plat_attrs = plat_attrs + [str(plat_var)]

                # Define the full file name to be passed to first_found
                file = prefix + delim.join(plat_attrs) + suffix + '.' + ext
                files.append(file)

        # Handle default file name if it was defined in the plugin
        # parameters
        if default:
            default_file = prefix + default + suffix + '.' + ext
            files.append(default_file)

        # Define the path to be passed to first_found
        p_suffix = '/' + term + '/'
        paths = [
            s_path + p_suffix for s_path in variables['ansible_search_path']
        ]

        plat_terms = [{'files': files, 'paths': paths}]

        # Use /dev/null to handle skip if it was enabled in the plugin
        # parameters
        if self.get_option('skip'):
            plat_terms.append({'files': ['null'], 'paths': ['/dev/']})

        # Return the terms to be used by first_found
        return plat_terms

    def run(self, terms, variables, **kwargs):

        # Define the terms to be used by ansible.builtin.first_found
        plat_terms = self._process_plat_terms(terms, variables, kwargs)

        # Run the first_found module with the terms defined by this
        # plugin
        return super(LookupModule, self).run(plat_terms, variables)
