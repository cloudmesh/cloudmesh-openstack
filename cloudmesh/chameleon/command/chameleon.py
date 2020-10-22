from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from glob import glob
from cloudmesh.common.util import readfile, banner
from cloudmesh.chameleon.Chameleon import Chameleon

class ChameleonCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_chameleon(self, args, arguments):
        """
        ::

          Usage:
                chameleon credential find [--file=FILE]
                chameleon credential create --file=FILE

          This command is used to locate the chameleon cloud credential.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """

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

        arguments.FILE = arguments['--file'] or None

        if arguments.find:
            if arguments.FILE is None:
                # look first in ~/.cloudmesh
                # look next in ~/Download

                path = path_expand("~")
                files = glob(f"{path}/.cloudmesh/CH-*.sh") + glob(f"{path}/Downloads/CH-*.sh")

                list_rc_files(files)
            else:
                files = [arguments.FILE]
                # look in file
                list_rc_files(files)
        elif arguments.create and arguments.FILE is not None:
            Chameleon.create_yaml_file(arguments.FILE)
        else:
            Console.error("Please check your arguments")

        return ""
