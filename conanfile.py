from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class SoftHSMv2(ConanFile):
    name = "softhsmv2"
    version = "2.6.1"
    license = "BSD-2-Clause"
    author = "OpenDNSSEC"
    url = "https://github.com/opendnssec/SoftHSMv2"
    description = "Conan package for the SoftHSM version 2, part of the OpenDNSSEC project."
    settings = "compiler"
    generators = "make"

    releases = "https://github.com/opendnssec/SoftHSMv2/archive/refs/tags/%s.tar.gz"

    source_path = "SoftHSMv2-%s" % version

    def source(self):
        file = "%s.tar.gz" % self.version
        source = self.releases % self.version

        try:
            # TODO: Check if we have it already
            tools.download(source , file)
        except:
            # TODO:
            return
        finally:
            tools.untargz(file, ".")
            os.unlink(file)

    def requirements(self):
        self.source()

        self.requires("openssl/1.1.1v")

    def build(self):
        openssl_path = self.deps_cpp_info["openssl"].rootpath

        with tools.chdir(self.source_path):
            atools = AutoToolsBuildEnvironment(self)

            self.run("./autogen.sh") # TODO: Check if have configure.sh already

            atools.configure(args=["--with-openssl=%s" % openssl_path]) # TODO: Check if we have Makefile already
            atools.make()

    def package(self):
        self.copy("libsofthsm2.so", dst="lib", src=self.source_path + "/src/lib/.libs/", keep_path=False)
        self.copy("softhsm2-util", dst="bin", src=self.source_path + "/src/bin/util/", keep_path=False)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

        self.cpp_info.libs = ["softhsmv2"]
