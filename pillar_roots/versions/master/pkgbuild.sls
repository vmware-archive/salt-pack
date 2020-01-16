# This file provides pillar data that will be used by Jinja macros to define #
# various SLS elements in templated SLS files. The formatting is flexible and
# allows for defaults to be overridden on a per-version basis.
#
# The top-level key must be named "pkgbuild_registry", which will contain
# sub-dictionaries for each platform. Each platform will contain its own
# sub-dictionary containing keys for each package. Here's an example:
#
# pkgbuild_registry:
#   rhel7:
#     foo:
#       version: 1.0.1-2
#       results:
#         - foo
#         - foo-devel
#     bar:
#       version: 2.1.0-1
#       build_deps:
#         - foo
#       additional_deps:
#         - baz
#     baz:
#       version: 4.5-3
#       4.2-1:
#         additional_deps:
#           - qux
#     qux:
#       version: 3.1-3
#     python-foo:
#       name: pyfoo
#       version: 6.1-1
#       additional_deps:
#         - foo
#
# The package keys ("foo", "bar", etc. in the example above) correspond to the
# directory names underneath the "pkg" dir which contains all the package
# sources and specs. If the actual package name to be built differs from this,
# then a sub-key called "name" must be used to specify the actual package name.
# This allows for differences between package naming in different distros to be
# managed flexibly. So, for instance, the sources and specs in
# pkg/python-foo/6_1/rhel7 would be for a package which will ultimately be
# named "pyfoo".
#
# The "results" key will contain a list of package names which will be built.
# If omitted, then it will be assumed that only a single package will be built,
# and its name will be the name of the parent dictionary key (or the value of #
# its "name" key, if present). For example, in the above example, "bar", "baz"
# and "qux" will build packages named "bar', "baz", and "qux", respectively.
# "foo" will build two packages, "foo" and "foo-devel", while "python-foo" will
# build a package named "pyfoo".
#
# The "version" key is required and should be defined in the format
# <version>-<release>. Note that the "release" portion of the version will not
# be included in the directory containing the sources and specs. For example,
# the files for the "baz" package above would be located in pkg/baz/4_5/rhel7/.
# The dots would be replaced with underscores to reduce confusion as dots
# signifiy directory boundaries when referenced as an SLS path (e.g.
# pkg.baz.4_5.rhel7).
#
# Two keys are used to detail dependency relationships, "build_deps" and
# "additional_deps".
#
# The "build_deps" key will contain a list of keys referring to the packages
# which are required as build-time dependencies. Note that individual package
# names should not be specified here, just the dictionary key for that package.
# For each build dep, the package(s) referred to by the "results" key (or its
# fallback) values will be added to the "deps" argument of the pkgbuild.built
# state, causing them to be installed in the build chroot before building.
#
# The "additional_deps" key will contain a list of keys referring to any
# runtime dependencies of the package, excluding any of those already defined
# in "build_deps". The build_deps and additional_deps will be defined as
# "require" requisites, ensuring that they are successfully built before
# attempting to build the current package. This is why runtime dependencies
# which are not also build dependencies do not need to be defined in the
# "additional_deps" key. Dependencies which are runtime-only and not needed at
# build time should be included here.
#
# NOTE: Only dependencies managed by this automated build system need to be
# defined in either "build_deps" or "additional_deps".
#
# A "noarch" key must be present and set to True to build
# architecture-independent packages, otherwise it will be assumed that the
# package is architecture-specific and the architecture will be inferred from
# the value of the pkgbuild.build_arch pillar key.
#
# Finally, keys for a specific <version>-<release> combo can contain
# "build_deps", "additional_deps", and "results" sub-keys, which can be used to
# define deviations from the values defined in higher-level keys. For example,
# if building "baz", and its "version" key is set to 4.2-1, then "qux" will be
# assumed to be a runtime dependency, whereas if the version is set to anything
# else then it will not.
#
# Keep in mind that setting these values will not automagically set build and
# runtime dependencies, versions, etc. in the spec files, the specs must be
# edited independently. The purpose of this pillar data is simply to make
# packages aware of their dependencies and pull in the right build deps, have
# the right requisites set, etc.

pkgbuild_registry:
  rhel7:
    libsodium:
      version: 1.0.16-1
      results:
        - libsodium
        - libsodium-devel
    libtomcrypt:
      version: 1.17-23
      results:
        - libtomcrypt
        - libtomcrypt-devel
    libtommath:
      version: 0.42.0-4
      results:
        - libtommath
        - libtommath-devel
    openpgm:
      version: 5.2.122-2
      results:
        - openpgm
        - openpgm-devel
    openssl:
      version: 1.0.2k-14
      results:
        - openssl
        - openssl-devel
        - openssl-libs
        - openssl-perl
        - openssl-static
    python-chardet:
      version: 2.2.1-1
      noarch: True
    python-cherrypy:
      version: 5.6.0-3
      noarch: True
      build_deps:
        - python-mock
    python-crypto:
      version: 2.6.1-2
    python-enum34:
      version: 1.0-4
      noarch: True
    python-futures:
      version: 3.0.3-1
      noarch: True
    python-ioflo:
      version: 1.3.8-1
      noarch: True
    python-libcloud:
      name: python2-libcloud
      version: 2.0.0-2
      noarch: True
    python-libnacl:
      version: 1.6.1-1
      noarch: True
      build_deps:
        - libsodium
      results:
        - python-libnacl
    python-m2crypto:
      version: 0.31.0-4
      results:
        - m2crypto
      build_deps:
        - openssl
        - python-typing
    python-msgpack:
      version: 0.5.6-7
      results:
        - python2-msgpack
    python-mock:
      version: 1.0.1-9
      noarch: True
      results:
        - python2-mock
    python-psutil:
      version: 2.2.1-1
    python-pycryptodome:
      version: 3.6.1-2
      results:
        - python2-pycryptodomex
      build_deps:
        - libtommath
        - libtomcrypt
        - libtomcrypt-devel
    python-pyzmq:
      name: python-zmq
      version: 15.3.0-3
      build_deps:
        - zeromq
    python-raet:
      version: 0.6.5-1
      noarch: True
      build_deps:
        - python-ioflo
        - python-libnacl
      additonal_deps:
        - python-simplejson
    python-simplejson:
      version: 3.3.3-1
    python-tornado:
      version: 4.2.1-1
    python-timelib:
      version: 0.2.4-1
      noarch: True
    python-typing:
      version: 3.5.2.2-4
      noarch: True
      results:
        - python2-typing
    python-urllib3:
      version: 1.10.2-1
      noarch: True
    python-yaml:
      name: PyYAML
      version: 3.11-1
    salt:
      version: master-tobereplaced_date-0
      noarch: True
      build_deps:
        - python-pycryptodome
        - python-msgpack
        - python-yaml
        - python-pyzmq
        - python-markupsafe
        - python-tornado
        - python-futures
        - python-libcloud
      results:
        - salt
        - salt-master
        - salt-minion
        - salt-syndic
        - salt-api
        - salt-cloud
        - salt-ssh
    zeromq:
      version: 4.1.4-7
      build_deps:
        - openpgm
      results:
        - zeromq
        - zeromq-devel

  rhel6:
    babel:
      name: python27-babel
      version: 0.9.4-5.3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-babel
    libgit2:
      version: 0.20.0-3
      build_deps:
        - python27
      results:
        - python27-libgit2
        - python27-libgit2-devel
    libsodium:
      version: 0.4.5-3
      results:
        - libsodium
        - libsodium-debuginfo
        - libsodium-devel
    libtomcrypt:
      version: 1.17-23
      results:
        - libtomcrypt
        - libtomcrypt-devel
    libtommath:
      version: 0.42.0-4
      results:
        - libtommath
        - libtommath-devel
    libyaml:
      version: 0.1.3-4
      results:
        - libyaml
        - libyaml-debuginfo
        - libyaml-devel
    pciutils:
      version: 3.1.10-4
      results:
        - pciutils
        - pciutils-debuginfo
        - pciutils-devel
        - pciutils-devel-static
        - pciutils-libs
    pytest:
      name: pytest27
      version: 2.7.0-2
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-py
      results:
        - pytest27
    python27:
      version: 2.7.13-3.ius
      results:
        - python27
        - python27-debuginfo
        - python27-devel
        - python27-libs
        - python27-test
        - python27-tools
        - tkinter27
    python-backports:
      name: python27-backports
      version: 1.0-7
      build_deps:
        - python27
    python-backports-ssl_match_hostname:
      name: python27-backports-ssl_match_hostname
      version: 3.4.0.2-4
      noarch: True
      build_deps:
        - python27
        - python-backports
        - python-setuptools
    python-chardet:
      name: python27-chardet
      version: 3.0.4-8
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-nose
      results:
        - python27-chardet
    python-cherrypy:
      name: python27-cherrypy
      version: 5.6.0-5
      noarch: True
      build_deps:
        - python27
        - python-mock
        - python-nose
      results:
        - python27-cherrypy
    python-crypto:
      name: python27-crypto
      version: 2.6.1-5
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-crypto
    python-pycryptodome:
      name: python27-pycryptodome
      version: 3.6.1-2
      build_deps:
        - python27
        - python-setuptools
        - libtommath
        - libtomcrypt
        - libtomcrypt-devel
      results:
        - python27-pycryptodomex
    python-enum34:
      name: python27-enum34
      version: 1.0-6
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-enum34
    python-futures:
      name: python27-futures
      version: 3.0.3-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-futures
    python-idna:
      name: python27-idna
      version: 2.7-4
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-idna
    python-ioflo:
      name: python27-ioflo
      version: 1.3.8-4
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-ioflo
    python-ipaddress:
      name: python27-ipaddress
      version: 1.0.18-6
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-ipaddress
    python-jinja2:
      name: python27-jinja2
      version: 2.8.1-3
      noarch: True
      build_deps:
        - python27
        - python-babel
        - python-markupsafe
      results:
        - python27-jinja2
    python-libcloud:
      name: python27-libcloud
      version: 2.0.0-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-libcloud
    python-libnacl:
      name: python27-libnacl
      version: 1.6.1-1
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - libsodium
      results:
        - python27-libnacl
    python-markupsafe:
      name: python27-markupsafe
      version: 0.11-12
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-markupsafe
    python-msgpack:
      name: python27-msgpack
      version: 0.4.6-3
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-msgpack
    python-mock:
      name: python27-mock
      version: 1.0.1-12
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-mock
    python-nose:
      name: python27-nose
      version: 1.3.7-2
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-mock
      results:
        - python27-nose
    python-pip:
      name: python27-pip
      version: 9.0.1-2.ius
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-pip
    python-psutil:
      name: python27-psutil
      version: 5.4.2-1.ius
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-psutil
    python-py:
      name: python27-py
      version: 1.4.27-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-py
    python-pygit2:
      name: python27-pygit2
      version: 0.20.3-5
      build_deps:
        - python27
        - python-setuptools
        - python-nose
        - libgit2
      results:
        - python27-pygit2
    python-pycurl:
      name: python27-pycurl
      version: 7.19.0-11
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-pycurl
    python-pysocks:
      name: python27-pysocks
      version: 1.6.8-7
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-pysocks
    python-pyzmq:
      name: python27-zmq
      version: 14.5.0-4
      build_deps:
        - python27
        - python-setuptools
        - zeromq
    python-raet:
      name: python27-raet
      version: 0.6.6-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-ioflo
        - python-six
      additional_deps:
        - python-libnacl
    python-requests:
      name: python27-requests
      version: 2.20.1-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-chardet
        - python-idna
        - python-pysocks
        - python-urllib3
      results:
        - python27-requests
    python-setuptools:
      name: python27-setuptools
      version: 36.6.0-1.ius
      noarch: True
      build_deps:
        - python27
      results:
        - python27-setuptools
    python-six:
      name: python27-six
      version: 1.9.0-4
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-six
    python-tornado:
      name: python27-tornado
      version: 4.2.1-4
      build_deps:
        - python27
        - python-backports-ssl_match_hostname
        - python-pycurl
        - python-setuptools
      results:
        - python27-tornado
    python-timelib:
      name: python27-timelib
      version: 0.2.4-3
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-timelib
    python-unittest2:
      name: python27-unittest2
      version: 1.1.0-6
      noarch: True
      build_deps:
        - python27
        - python-setuptools
        - python-six
      results:
        - python27-unittest2
    python-urllib3:
      name: python27-urllib3
      version: 1.23-6
      noarch: True
      build_deps:
        - python27
        - python-backports-ssl_match_hostname
        - python-ipaddress
        - python-pysocks
        - python-setuptools
        - python-six
      results:
        - python27-urllib3
    python-yaml:
      name: python27-PyYAML
      version: 3.11-3
      build_deps:
        - python27
        - python-setuptools
        - libyaml
      results:
        - PyYAML27
    salt:
      version: master-tobereplaced_date-0
      noarch: True
      build_deps:
        - python27
        - python-pycrypto
        - python-msgpack
        - python-yaml
        - python-requests
        - python-pyzmq
        - python-markupsafe
        - python-tornado
        - python-futures
        - python-libcloud
      results:
        - salt
        - salt-master
        - salt-minion
        - salt-syndic
        - salt-api
        - salt-cloud
        - salt-ssh
    yum-utils:
      version: 1.1.30-30
      noarch: True
      results:
        - yum-utils
        - yum-NetworkManager-dispatcher
        - yum-plugin-verify
        - yum-plugin-fastestmirror
        - yum-plugin-show-leaves
        - yum-plugin-filter-data
        - yum-plugin-versionlock
        - yum-plugin-ps
        - yum-plugin-tsflags
        - yum-plugin-changelog
        - yum-plugin-remove-with-leaves
        - yum-plugin-downloadonly
        - yum-plugin-tmprepo
        - yum-plugin-protectbase
        - yum-plugin-priorities
        - yum-plugin-post-transaction-actions
        - yum-plugin-fs-snapshot
        - yum-plugin-aliases
        - yum-plugin-local
        - yum-plugin-auto-update-debug-info
        - yum-plugin-security
        - yum-plugin-rpm-warm-cache
        - yum-plugin-list-data
        - yum-plugin-upgrade-helper
        - yum-plugin-merge-conf
        - yum-plugin-keys
        - yum-updateonboot
    zeromq:
      version: 4.0.5-4
      results:
        - zeromq
        - zeromq-devel


  amzn:
    libsodium:
      version: 0.4.5-3
      results:
        - libsodium
        - libsodium-debuginfo
        - libsodium-devel
    python-cherrypy:
      name: python27-cherrypy
      version: 3.2.2-6
      noarch: True
    python-enum34:
      name: python27-enum34
      version: 1.0-5
      noarch: True
    python-gnupg:
      name: python27-gnupg
      version: 0.3.8-4
      noarch: True
    python-impacket:
      name: python27-impacket
      version: 0.9.14-3
      noarch: True
    python-ioflo:
      name: python27-ioflo
      version: 1.3.8-2
      noarch: True
    python-libcloud:
      name: python27-libcloud
      version: 2.0.0-2
      noarch: True
      results:
        - python27-libcloud
    python-libnacl:
      name: python27-libnacl
      version: 1.6.1-2
      noarch: True
      build_deps:
        - libsodium
    python-msgpack:
      name: python27-msgpack
      version: 0.4.6-2
    python-psutil:
      name: python27-psutil
      version: 5.2.2-2.ius
      results:
        - python27-psutil
    python-pysocks:
      name: python27-pysocks
      version: 1.6.8-7
      noarch: True
      build_deps:
        - python27
        - python-setuptools
      results:
        - python27-pysocks
    python-pyzmq:
      name: python27-zmq
      version: 14.5.0-3
      build_deps:
        - zeromq
    python-raet:
      name: python27-raet
      version: 0.6.3-3
      noarch: True
      build_deps:
        - python-ioflo
      additional_deps:
        - python-libnacl
    python-tornado:
      name: python27-tornado
      version: 4.2.1-2
    python-timelib:
      name: python27-timelib
      version: 0.2.4-2
      noarch: True
    salt:
      version: master-tobereplaced_date-0
      noarch: True
      build_deps:
        - python-msgpack
        - python-pyzmq
        - python-tornado
        - python-libcloud
        - python-gnupg
        - python-futures
      results:
        - salt
        - salt-master
        - salt-minion
        - salt-syndic
        - salt-api
        - salt-cloud
        - salt-ssh
    winexe:
      version: 1.1-b787d2.1
      results:
        - winexe
        - winexe-debuginfo
      build_deps:
        - python-impacket
    zeromq:
      version: 4.0.5-4
      results:
        - zeromq
        - zeromq-devel

