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

        # print(yaml.dump(self.info, indent=4, Dumper=yaml.RoundTripDumper))

        self.driver = None
        self.authenticate()

    def authenticate(self):
        libcloud.security.VERIFY_SSL_CERT = False

        provider = get_driver(Provider.OPENSTACK)

        credentials = dotdict(self.info["credentials"])
        # print (credentials)
        # print ("U", credentials.OS_USERNAME)
        self.driver = provider(
            credentials.OS_USERNAME,
            credentials.OS_PASSWORD,
            ex_force_auth_url=credentials.OS_AUTH_URL,
            ex_force_auth_version="3.x_password",
            ex_tenant_name=credentials.OS_TENANT_NAME,
            # ex_domain_name=credentials.OS_PROJECT_DOMAIN_ID,
            ex_force_service_type='compute',
            ex_force_service_region=credentials.OS_REGION_NAME)



    def _list(self, data):
        d = {}

        for image in data:
            # print (image.__dict__)
            d[image.name] = image.__dict__
            del d[image.name]["_uuid"]
            del d[image.name]["driver"]

        return d

    def images(self):
        return (self._list(self.driver.list_images()))


    def flavors(self):
        return (self._list(self.driver.list_sizes()))

    def vms(self):
        return (self._list(self.driver.list_nodes()))
