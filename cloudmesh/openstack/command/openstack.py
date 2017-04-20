from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand


class OpenstackCommand(PluginCommand):

    @command
    def do_openstack(self, args, arguments):
        """
        ::

          Usage:
                openstack -f FILE
                openstack FILE
                openstack list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        print(arguments)



