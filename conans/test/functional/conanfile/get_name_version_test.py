import textwrap
import unittest

from conans.test.utils.tools import TestClient


class GetVersionNameTest(unittest.TestCase):

    def get_version_name_test(self):
        client = TestClient()
        conanfile = textwrap.dedent("""
            from conans import ConanFile
            class Lib(ConanFile):
                def get_name(self):
                    self.name = "pkg"
                def get_version(self):
                    self.version = "2.1"
            """)
        client.save({"conanfile.py": conanfile})
        client.run("export . user/testing")
        self.assertIn("pkg/2.1@user/testing: A new conanfile.py version was exported", client.out)
        client.run("install pkg/2.1@user/testing --build=missing")
        self.assertIn("pkg/2.1@user/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Build",
                      client.out)
        client.run("install pkg/2.1@user/testing")
        self.assertIn("pkg/2.1@user/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Cache",
                      client.out)

    def get_version_name_file_test(self):
        client = TestClient()
        conanfile = textwrap.dedent("""
            from conans import ConanFile, load
            class Lib(ConanFile):
                def get_name(self):
                    self.name = load("name.txt")
                def get_version(self):
                    self.version = load("version.txt")
            """)
        client.save({"conanfile.py": conanfile,
                     "name.txt": "pkg",
                     "version.txt": "2.1"})
        client.run("export . user/testing")
        self.assertIn("pkg/2.1@user/testing: A new conanfile.py version was exported", client.out)
        client.run("install pkg/2.1@user/testing --build=missing")
        self.assertIn("pkg/2.1@user/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Build",
                      client.out)
        client.run("install pkg/2.1@user/testing")
        self.assertIn("pkg/2.1@user/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Cache",
                      client.out)

    def get_version_name_errors_test(self):
        client = TestClient()
        conanfile = textwrap.dedent("""
            from conans import ConanFile
            class Lib(ConanFile):
                def get_name(self):
                    self.name = "pkg"
                def get_version(self):
                    self.version = "2.1"
            """)
        client.save({"conanfile.py": conanfile})
        client.run("export . other/1.1@user/testing", assert_error=True)
        self.assertIn("ERROR: Package recipe exported with name other!=pkg", client.out)
        client.run("export . 1.1@user/testing", assert_error=True)
        self.assertIn("ERROR: Package recipe exported with version 1.1!=2.1", client.out)
        # These are checked but match and don't conflict
        client.run("export . 2.1@user/testing")
        client.run("export . pkg/2.1@user/testing")
