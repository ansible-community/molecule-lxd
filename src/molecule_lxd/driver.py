#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
import os
from typing import Dict
from molecule import logger
from molecule.api import Driver


LOG = logger.get_logger(__name__)


class LXD(Driver):
    """
    The class responsible for managing `LXD`_ containers.  `LXD`_ is `not` the
    default driver used in Molecule.

    Molecule leverages Ansible's `lxd_container`_ module, by mapping variables
    from ``molecule.yml`` into ``create.yml`` and ``destroy.yml``.
    The `lxd_container`_ module leverages the LXD API. Useful information
    about, for example the source variable can be found in the `LXD API documentation`.

    .. _`lxd_container`: https://docs.ansible.com/ansible/latest/lxd_container_module.html
    .. _`LXD API documentation`: https://github.com/lxc/lxd/blob/master/doc/rest-api.md#post-1

    .. code-block:: yaml

        driver:
          name: lxd
        platforms:
          - name: instance
            url: https://127.0.0.1:8443
            cert_file: /root/.config/lxc/client.crt
            key_file: /root/.config/lxc/client.key
            trust_password: password
            source:
              type: image
              mode: pull
              server: https://images.linuxcontainers.org
              protocol: lxd|simplestreams
              alias: ubuntu/xenial/amd64
            architecture: x86_64|i686
            config:
              limits.cpu: 2
            devices:
              kvm:
                path: /dev/kvm
                type: unix-char
            profiles:
              - default
            force_stop: True|False
            ignore_volatile_options: false
            target: node_name
            type: virtual-machine

    Provide a list of files Molecule will preserve, relative to the scenario
    ephemeral directory, after any ``destroy`` subcommand execution.

    .. code-block:: yaml

        driver:
          name: lxd
          safe_files:
            - foo

    .. _`LXD`: https://linuxcontainers.org/lxd/introduction/
    """  # noqa

    def __init__(self, config=None):
        super(LXD, self).__init__(config)
        self._name = "lxd"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def login_cmd_template(self):
        return "lxc exec {instance} bash"

    @property
    def default_safe_files(self):
        return []

    @property
    def default_ssh_connection_options(self):
        return []

    def login_options(self, instance_name):
        return {"instance": instance_name}

    def ansible_connection_options(self, instance_name):
        return {
            "ansible_connection": "community.general.lxd",
            "ansible_lxd_remote": os.getenv("LXC_REMOTE", "local"),
        }

    def sanity_checks(self):
        # FIXME(decentral1se): Implement sanity checks
        pass

    def template_dir(self):
        """Return path to its own cookiecutterm templates. It is used by init
        command in order to figure out where to load the templates from.
        """
        return os.path.join(os.path.dirname(__file__), "cookiecutter")

    def modules_dir(self):
        return os.path.join(os.path.dirname(__file__), "modules")

    @property
    def required_collections(self) -> Dict[str, str]:
        """Return collections dict containing names and versions required."""
        return {"community.general": "4.1.0"}
