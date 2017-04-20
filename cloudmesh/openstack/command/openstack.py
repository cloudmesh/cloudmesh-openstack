from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from ruamel import yaml
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import readfile
from cloudmesh.common.Printer import Printer
from collections import OrderedDict
from cloudmesh.common.default import Default

class OpenstackCommand(PluginCommand):
    @command
    def do_openstack(self, args, arguments):
        """
        ::

          Usage:
                openstack yaml 
                openstack yaml list [CLOUD]

          This command does some useful things.

          Arguments:
              FILE   a file name
            
          Options:
              -f      specify the file

        """
        # print(arguments)


        if arguments.yaml and arguments.list:


            filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
            content = readfile(filename)
            d = yaml.load(content, Loader=yaml.RoundTripLoader)
            if arguments.CLOUD is None:
                default = Default()
                default_cloud = default["general"]["cloud"]


                # print (yaml.dump(d, indent=4, Dumper=yaml.RoundTripDumper))
                info = OrderedDict()
                clouds = d["cloudmesh"]["clouds"]
                for cloud in clouds:
                    info[cloud] = {
                        "default": "",
                        "name": cloud,
                        "type": clouds[cloud]["cm_type"],
                        "label": clouds[cloud]["cm_label"],
                        "flavor": clouds[cloud]["default"]["flavor"],
                        "image": clouds[cloud]["default"]["image"]
                    }
                    if default_cloud == cloud:
                        info[cloud]["default"] = "*"

                print (Printer.dict(info,
                                    order=["default", "name", "type", "label", "flavor", "image"]))
                default.close()

            else:
                cloud = arguments.CLOUD
                clouds = d["cloudmesh"]["clouds"]
                print(yaml.dump(clouds[cloud], indent=4, Dumper=yaml.RoundTripDumper))


        elif arguments.yaml:


            filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
            content = readfile(filename)
            d = yaml.load(content, Loader=yaml.RoundTripLoader)
            print(yaml.dump(d, indent=4, Dumper=yaml.RoundTripDumper))