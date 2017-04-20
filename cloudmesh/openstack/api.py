from __future__ import print_function
from ruamel import yaml
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import readfile
from collections import OrderedDict

from cloudmesh.common.default import Default
from cloudmesh.common.dotdict import dotdict

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import libcloud.security
import warnings
import libcloud

from pprint import pprint

warnings.simplefilter("ignore")
#warnings.warn(libcloud.security.VERIFY_SSL_DISABLED_MSG)

class OpenStack(object):

    def __init__(self, cloud=None):

        if cloud is None:
            default = Default()
            cloud = default["general"]["cloud"]
            default.close()

        filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
        content = readfile(filename)
        d = yaml.load(content, Loader=yaml.RoundTripLoader)
        self.info = d["cloudmesh"]["clouds"][cloud]

        print(yaml.dump(self.info, indent=4, Dumper=yaml.RoundTripDumper))

        self.driver = None
        self.authenticate()

    def authenticate(self):
        libcloud.security.VERIFY_SSL_CERT = False

        provider = get_driver(Provider.OPENSTACK)

        credentials = dotdict(self.info["credentials"])
        print (credentials)
        print ("U", credentials.OS_USERNAME)
        self.driver = provider(
            credentials.OS_USERNAME,
            credentials.OS_PASSWORD,
            ex_force_auth_url=credentials.OS_AUTH_URL,
            ex_force_auth_version="2.0_password")

    def images(self):

        images = self.driver.list_images()
        return images


    def flavors(self):
        return None

    def vms(self):
        return None
