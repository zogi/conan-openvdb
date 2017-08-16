# What's this?

This is a conan package for DreamWorks' [OpenVDB](http://www.openvdb.org/)
library.

# How to use it?

Install [python 2.7+](https://www.python.org/download/releases/2.7/) and
[conan](http://conanio.readthedocs.io/en/latest/installation.html).

Clone this repository. From the directory where you cloned the repo run:

```
$ conan export zogi/testing
```

Write a
[conanfile](http://conanio.readthedocs.io/en/latest/reference/conanfile_txt.html)
including `OpenVDB/4.0.2@zogi/testing` in the `[requires]` section.
If you use CMake, add `${CONAN_LIBS}` to the list of libs to link against.
From your build directory run

```bash
$ conan install --build=missing path_to_your_conanfile
```

Now just run cmake as usual to build.

### TBB and Boost

TBB and Boost are dependencies of OpenVDB, but being a bit bulky, are not
included in the conanfile as dependencies. This has the benefit of e.g. being
able to link against Maya's TBB if OpenVDB is used in a Maya plugin without
mentioning Maya in this conan package.
This also has the consequence that TBB and Boost have to be installed to
somewhere CMake can find in order to build and use this package.

On Windows the `BOOST_ROOT` and `TBB_ROOT` envvars should point to the Boost
and TBB root directories respectively so as to help CMake find them.

# Testing

This conan package has been tested using the following configurations:
- Windows 10 and MSVC 15.0.
- CentOS 6 and gcc 4.8 conforming to
[vfxplatform 2017](http://www.vfxplatform.com/)
using this [docker image](https://github.com/zogi/docker-mayadev).

If you use this on any other platform/configuration mentioned above, please
inform me of any problems you encounter.
