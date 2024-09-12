from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class SoftHSMv2(ConanFile):
    name = "softhsmv2"
    version = "2.6.1"
    license = "BSD-2-Clause"
    author = "OpenDNSSEC"
    url = "https://github.com/opendnssec/SoftHSMv2"
    description = "Conan package for the SoftHSM version 2, part of the OpenDNSSEC project."
    settings = {"os", "arch", "compiler", "build_type"}
    generators = "make"

    options = {
        "openssl": [None, "ANY"],
        "botan": [None, "ANY"],
        "disable_non_paged_memory": [None, True, False],
        "enable_gost": [None, True, False],
        "enable_ecc": [None, True, False],
        "enable_eddsa": [None, True, False],
        "disable_visibility": [True, False],
    }

    default_options = {
        "openssl": None,
        "botan": None,
        "disable_non_paged_memory": None,
        "enable_gost": None,
        "enable_ecc": None,
        "enable_eddsa": None,
        "disable_visibility": True,
    }

    source_path = f"SoftHSMv2-{version}"

# --with-migrate		Build the migration tool. Used when migrating
# 			a SoftHSM v1 token database. Requires SQLite3
# --with-objectstore-backend-db
# 			Build with database object store (SQLite3)
# --with-sqlite3=PATH	Specify prefix of path of SQLite3
# --disable-p11-kit	Disable p11-kit integration (default enabled)
# --with-p11-kit=PATH	Specify install path of the p11-kit module, will
#			override path given by pkg-config

    def validate(self):
        if self.options.openssl and self.options.botan:
            raise ConanInvalidConfiguration("Cannot use both openssl and botan at the same time")


    def source(self):
        file = f"{self.version}.tar.gz"
        source = f"https://github.com/opendnssec/SoftHSMv2/archive/refs/tags/{self.version}.tar.gz"

        try:
            # TODO: Check if we have it already?!
            tools.download(source , file)
        except:
            # TODO:
            return
        finally:
            tools.untargz(file, ".")
            os.unlink(file)

    def requirements(self):
        if self.options.openssl:
            self.requires(self.options.openssl.__str__())

    def build(self):

        build_args = []

        if self.options.openssl:
            build_args.append(f"--with-openssl={self.deps_cpp_info[self.options.openssl.__str__().split("/")[0]].rootpath}")

        if self.options.botan:
            build_args.append(f"--with-botan={self.deps_cpp_info[self.options.botan.__str__().split("/")[0]].rootpath}")

        if self.options.disable_non_paged_memory:
            build_args.append(f"--disable-non-paged-memory")

        if self.options.enable_gost:
            build_args.append(f"--disable-ghost")

        if self.options.enable_ecc:
            build_args.append(f"--disable-ecc")

        if self.options.enable_eddsa:
            build_args.append(f"--disable-eddsa")

        if self.options.disable_visibility:
            build_args.append(f"--disable-visibility")


        with tools.chdir(self.source_path):
            atools = AutoToolsBuildEnvironment(self)

            self.run("./autogen.sh") # TODO: Check if have configure.sh already

            atools.configure(args=build_args) # TODO: Check if we have Makefile already
            atools.make()

    def package(self):
        self.copy("libsofthsm2.so", dst="lib", src=self.source_path + "/src/lib/.libs/", keep_path=False)
        self.copy("softhsm2-util", dst="bin", src=self.source_path + "/src/bin/util/", keep_path=False)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

        self.cpp_info.libs = ["softhsmv2"]
