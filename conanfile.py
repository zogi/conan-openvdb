import os
import shutil
from conans import ConanFile, CMake, tools


class OpenVDBConan(ConanFile):
    name = "OpenVDB"
    version = "4.0.2"
    license = "MPL-2.0"
    description = "OpenVDB is an open source C++ library comprising a novel hierarchical data structure and a large suite of tools for the efficient storage and manipulation of sparse volumetric data discretized on three-dimensional grids."
    url = "https://github.com/zogi/conan-openvdb"
    requires = ( "Boost/1.60.0@lasote/stable"
               , "TBB/4.4.4@memsharded/testing"
               , "blosc/1.11.2@zogi/stable"
               , "zlib/1.2.8@lasote/stable"
               , "IlmBase/2.2.0@Mikayex/stable"
               , "OpenEXR/2.2.0@Mikayex/stable"
               )
    boost_components_needed = "iostreams", "system", "thread"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = { "shared": [True, False]
              , "fPIC": [True, False]
              }
    default_options = "shared=False", "fPIC=False"
    exports = ["CMakeLists.txt", "fix-FindTBB-module.patch"]

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.options.shared and "fPIC" in self.options.fields:
            self.options.fPIC = True

        # Exclude Boost components which are not needed.
        boost_options = self.options["Boost"]
        for boost_option in boost_options.fields:
            if not boost_option.startswith("without_"):
                continue
            component = boost_option[8:]
            if component not in self.boost_components_needed:
                boost_options.add_option(boost_option, True)

    def source(self):
        self.run("git clone https://github.com/dreamworksanimation/openvdb src")
        self.run("cd src && git checkout v%s" % self.version)
        tools.replace_in_file("src/CMakeLists.txt", "PROJECT ( OpenVDB )",
                              "PROJECT ( OpenVDB )\n" +
                              "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n" +
                              "conan_basic_setup()\n"+
                              "ADD_DEFINITIONS(-std=c++11)")
        shutil.copy("CMakeLists.txt", "src/openvdb/CMakeLists.txt")
        tools.patch(base_path="src", patch_file="fix-FindTBB-module.patch")

    def build(self):
        os.environ.update(
            { "BOOST_ROOT": self.deps_cpp_info["Boost"].rootpath
            , "TBB_ROOT": self.deps_cpp_info["TBB"].rootpath
            , "BLOSC_ROOT": self.deps_cpp_info["blosc"].rootpath
            , "ILMBASE_ROOT": self.deps_cpp_info["IlmBase"].rootpath
            , "OPENEXR_ROOT": self.deps_cpp_info["OpenEXR"].rootpath
            })

        cmake = CMake(self)

        cmake.definitions.update(
            { "BUILD_SHARED": self.options.shared
            , "BUILD_TOOLS": False
            , "OPENVDB_BUILD_CORE": True
            , "OPENVDB_BUILD_UNITTESTS": False
            , "OPENVDB_BUILD_PYTHON_MODULE": False
            , "OPENVDB_ENABLE_3_ABI_COMPATIBLE": True
            , "CMAKE_INSTALL_PREFIX": self.package_folder
            })

        if "fPIC" in self.options.fields:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        cmake.configure(source_dir="src")
        cmake.build(target="install")

    def package(self):
        self.copy("LICENSE", src="src/openvdb", dst="licenses")

    def package_info(self):
        self.cpp_info.cppflags.append("-std=c++11")

        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs = ["libopenvdb"]
        else:
            self.cpp_info.libs = ["openvdb"]

        self.cpp_info.defines = [ "OPENVDB_3_ABI_COMPATIBLE"
                                , "OPENVDB_USE_BLOSC"
                                ]

        if self.options.shared:
            self.cpp_info.defines.append("OPENVDB_DLL")
        else:
            self.cpp_info.defines.append("OPENVDB_STATICLIB")

        if not self.options["OpenEXR"].shared:
            self.cpp_info.defines.append("OPENVDB_OPENEXR_STATICLIB")
