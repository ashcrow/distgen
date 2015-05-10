from __future__ import print_function
import os, sys


class PathManager(object):
    envvar = None

    def __init__(self, path, envvar=None):
        self.path = path
        self.envvar = envvar


    def get_file(self, relative, prefered_path=None, fail=False,
                 file_desc="file"):
        path = self.get_path()
        if prefered_path:
            path = prefered_path + path

        for i in path:
            config_file = i + "/" + relative
            if os.path.isfile(config_file):
                return config_file

        if fail:
            print("can't find {0} '{1}'".format(file_desc, relative))
            sys.exit(1)

        return None


    def open_file(self, relative, prefered_path=None,
                  fail=False, file_desc="file"):

        filename = self.get_file(relative, prefered_path, fail=fail,
                                 file_desc=file_desc)
        if not filename:
            return None

        try:
            fd = open(filename)
        except IOError as err:
            if fail:
                print("can't open file {0}".format(relative))
                sys.exit(1)
            return None

        return fd


    def get_path(self):
        path = self.path
        if self.envvar and self.envvar in os.environ:
            env_path = os.environ[self.envvar].split(':')
            path = env_path + path

        return [os.getcwd()] + path
