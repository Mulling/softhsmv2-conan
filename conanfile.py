from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class Softhsmv2Conan(ConanFile):
    name = "softhsmv2"
    version = "2.6.1"
    license = "<Put the package license here>"
    author = "OpenDNSSEC"
    url = "https://github.com/opendnssec/SoftHSMv2"
    releases = "https://github.com/opendnssec/SoftHSMv2/archive/refs/tags/%s.tar.gz"
    description = """
A potential problem with the use of the PKCS#11 interface is that it might
limit the wide spread use of OpenDNSSEC, since a potential user might not be
willing to invest in a new hardware device. To counter this effect, OpenDNSSEC
is providing a software implementation of a generic cryptographic device with a
PKCS#11 interface, the SoftHSM. SoftHSM is designed to meet the requirements of
OpenDNSSEC, but can also work together with other cryptographic products
because of the PKCS#11 interface.
    """
    settings = "compiler"
    generators = "make"

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
