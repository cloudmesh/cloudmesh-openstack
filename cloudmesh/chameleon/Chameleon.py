from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from glob import glob
from cloudmesh.common.util import readfile, banner, writefile
import textwrap

class Chameleon(object):

    env = {
        'name': 'chameleon',
        'network_id': 'TBD',
        'OS_ACCESS_TOKEN_TYPE': "access_token",
        'OS_AUTH_TYPE': "v3oidcpassword",
        'OS_AUTH_URL': 'https://kvm.tacc.chameleoncloud.org:5000/v3',
        'OS_CLIENT_ID': "keystone-kvm-prod",
        'OS_CLIENT_SECRET': "none",
        'OS_DISCOVERY_ENDPOINT': "https://auth.chameleoncloud.org/auth/realms/chameleon/.well-known/openid-configuration",
        'OS_IDENTITY_API_VERSION': '3',
        'OS_IDENTITY_PROVIDER': "chameleon",
        'OS_INTERFACE': 'public',
        'OS_PASSWORD': 'TBD',
        'OS_PROJECT_ID': "0c738024330e4e368bae5d2043ac6657",
        'OS_PROTOCOL': "openid",
        'OS_REGION_NAME': "KVM@TACC",
        'OS_USERNAME': 'TBD'}

    sample = textwrap.dedent("""
        cloudmesh:
          cloud:
            {name}:
              cm:
                active: true
                heading: {name}
                host: chameleon
                label: {name}
                kind: openstack
                version: 2020
                service: compute
              credentials:
                auth:
                  auth_url: "https://kvm.tacc.chameleoncloud.org:5000/v3"
                  username: TBD
                  project_id: {OS_PROJECT_ID}
                  project_name: TBD
                  user_domain_name: "Default"
                  password: {OS_PASSWORD}
                region_name: {OS_REGION_NAME}
                interface: "{OS_INTERFACE}"
                identity_api_version: "{OS_IDENTITY_API_VERSION}"
                key_path: ~/.ssh/id_rsa.pub
              default:
                size: m1.medium
                image: CC-Ubuntu18.04
                network: {network_id}
            """).format(**env).strip()

    @staticmethod
    def list_rc_files(files):
        for file in files:
            banner(file)
            content = readfile(file)
            if "OS_IDENTITY_PROVIDER" not in content:
                Console.error(
                    f"{file} found. This is no longer a valid chameleon cloud credential. Switch to the new authentication.")
            else:
                Console.ok(f"{file} found. It contains a credential in new format")

                print(content)

    @staticmethod
    def read_rc_file(filename):
        variables = {}
        content = readfile(filename)
        for line in content.splitlines():
            if "export" in line:
                line = line.replace("export ", "")
                variable, value = line.split("=", 1)
                variables[variable] = value
        # for now overwrite password to set it by hand
        variables["OS_PASSWORD"] = "TBD"
        return variables

    @staticmethod
    def create_yaml_file(filename):
        variables = Chameleon.read_rc_file(filename)
        VERBOSE(variables)
        writefile("~/.cloudmesh/chameleon-tmp.yaml", Chameleon.sample)
        print (readfile("~/.cloudmesh/chameleon-tmp.yaml"))



