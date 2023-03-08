# Release notes

## `1.0.0-alpha.1`

* `o0_o.host` collection created.
* `first_found_by_host_attributes` lookup plugin added.
* `connection` role added.
* `privilege_escalation` role added.
* `time` role added.
* `software_management` role added.
* `facts` role added.
* `python_interpreter` role added.
* `mandatory_access_control` role added.
* `milestone_001` playbook added.

## `1.0.0-alpha.2`

* Minor aesthetic changes after initial Galaxy import


## `1.0.0-alpha.3`

* Use * for lists in README to be compatible with RST
* Fix condition on network connection facts so they aren't set when the connection fails
* Better handle cases where Ansible user is root
* Fix condition on running roles if the Python interpreter is changed
* Fix IP loop in connection role

## `1.0.0-alpha.4`

* `o0_o.host.users` role added.
* Various changes to other roles to support the `users` role.
