# What's this?

This is a conan package for DreamWorks' [OpenVDB](http://www.openvdb.org/)
library.

# How to use it?

If you are familiar with conan, the only useful information for you in this
section is that you can obtain pre-built binaries from the
`https://api.bintray.com/conan/zogi/conan-packages`
conan remote.
Otherwise you can find a bit more detailed description on how to use this
package.

Install [python 2.7+](https://www.python.org/download/releases/2.7/) and
[conan](http://conanio.readthedocs.io/en/latest/installation.html).
Add this conan package to your local package recipes either by cloning the repo
and calling conan export manually, or by adding my conan bintray repository to
your conan remotes. The latter has the advantage that you can download pre-built
binaries from bintray.

### Obtain the package from bintray.

To add my conan bintray repo to your conan remotes, run:

```
$ conan remote add zogi-bintray https://api.bintray.com/conan/zogi/conan-packages
```

### Add the recipe manually.

Clone this repository. From the directory where you cloned the repo run:

```
$ conan export zogi/testing
```

### Using the package in your project.

Write a
[conanfile](http://conanio.readthedocs.io/en/latest/reference/conanfile_txt.html)
including `OpenVDB/4.0.2@zogi/testing` in the `[requires]` section.
If you use CMake, add `${CONAN_LIBS}` to the list of libs to link against.
From your build directory run

```bash
$ conan install --build=missing path_to_your_conanfile
```

Now just run cmake as usual to build.

# Testing

This conan package has been tested using the following configurations:
- Windows 10 and MSVC 15.0.
- CentOS 6 and gcc 4.8 conforming to
[vfxplatform 2017](http://www.vfxplatform.com/)
using this [docker image](https://github.com/zogi/docker-mayadev).

If you use this on any other platform/configuration mentioned above, please
inform me of any problems you encounter.
