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

    def source(self):
        file = "%s.tar.gz" % self.version
        source = self.releases % self.version

        try:
            tools.download(source , file)
        except:
            # TODO:
            return
        finally:
            tools.untargz(file, ".")

    def requirements(self):
        self.source()

        self.requires("openssl/1.1.1v")

    def build(self):
        openssl_path = self.deps_cpp_info["openssl"].rootpath

        self.output.info(openssl_path)
        with tools.chdir("SoftHSMv2-%s" % self.version):
            atools = AutoToolsBuildEnvironment(self)

            self.run("./autogen.sh")

            atools.configure(args=["--with-openssl=%s" % openssl_path])
            atools.make()

    def package(self):
        path = "SoftHSMv2-%s" % self.version

        self.copy("libsofthsm2.so", dst="lib", src=path + "/src/lib/.libs/", keep_path=False)
        self.copy("softhsm2-util", dst="bin", src=path + "/src/bin/util/", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["softhsmv2"]
