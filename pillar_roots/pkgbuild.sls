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

# set version to build
{% set build_version = '2017_7_0' %}

{% if build_version != '' %}
include:
    - .versions.{{build_version}}.pkgbuild

{% else %}

pkgbuild_registry:
  rhel7:
    libsodium:
      version: 1.0.5-1
      results:
        - libsodium
        - libsodium-devel
    openpgm:
      version: 5.2.122-2
      results:
        - openpgm
        - openpgm-devel
    python-chardet:
      version: 2.2.1-1
      noarch: True
    python-cherrypy:
      version: 3.2.2-4
      noarch: True
    python-crypto:
      version: 2.6.1-1
    python-enum34:
      version: 1.0-4
      noarch: True
    python-futures:
      version: 3.0.3-1
      noarch: True
    python-impacket:
      version: 0.9.14-1
      noarch: True
    python-ioflo:
      version: 1.3.8-1
      noarch: True
    python-libcloud:
      version: 0.20.0-1
      noarch: True
    python-libnacl:
      version: 1.4.3-1
      noarch: True
      build_deps:
        - libsodium
    python-msgpack:
      version: 0.4.6-1
    python-pyzmq:
      name: python-zmq
      version: 15.3.0-2
      build_deps:
        - zeromq
    python-raet:
      version: 0.6.3-2
      noarch: True
      build_deps:
        - python-ioflo
      additonal_deps:
        - python-libnacl
        - python-simplejson
    python-requests:
      version: 2.6.0-1
      noarch: True
      build_deps:
        - python-chardet
        - python-ordereddict
        - python-urllib3
    python-simplejson:
      version: 3.3.3-1
    python-tornado:
      version: 4.2.1-1
    python-tornado-salt:
      version: 4.2.1-1
    python-timelib:
      version: 0.2.4-1
      noarch: True
    python-urllib3:
      version: 1.10.2-1
      noarch: True
    python-yaml:
      name: PyYAML
      version: 3.11-1
    salt:
      version: 2016.3.2-1
      noarch: True
      build_deps:
        - python-crypto
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
    winexe:
      version: 1.1-b787d2
      results:
        - winexe
        - winexe-debuginfo
      build_deps:
        - python-impacket
    zeromq:
      version: 4.1.4-5
      build_deps:
        - openpgm
      results:
        - zeromq
        - zeromq-devel

  rhel6:
    babel:
      version: 0.9.4-5.1
      noarch: True
    libsodium:
      version: 0.4.5-3
      results:
        - libsodium
        - libsodium-debuginfo
        - libsodium-devel
    libyaml:
      version: 0.1.3-4
      results:
        - libyaml
        - libyaml-debuginfo
        - libyaml-devel
    openpgm:
      version: 5.2.122-2
      results:
        - openpgm
        - openpgm-devel
    pciutils:
      version: 3.1.10-4
      results:
        - pciutils
        - pciutils-debuginfo
        - pciutils-devel
        - pciutils-devel-static
        - pciutils-libs
    python-backports:
      version: 1.0-5
    python-backports-ssl_match_hostname:
      version: 3.4.0.2-2
      noarch: True
      build_deps:
        - python-backports
    python-chardet:
      version: 2.2.1-1
      noarch: True
    python-cherrypy:
      version: 3.2.2-4
      noarch: True
    python-crypto:
      version: 2.6.1-2
    python-crypto-salt:
      version: 2.6.1-4
    python-enum34:
      version: 1.0-4
      noarch: True
    python-futures:
      version: 3.0.3-1
      noarch: True
    python-impacket:
      version: 0.9.14-1
      noarch: True
    python-importlib:
      version: 1.0.2-2
      noarch: True
    python-ioflo:
      version: 1.3.8-1
      noarch: True
    python-jinja2:
      version: 2.7.3-1
      noarch: True
      build_deps:
        - python-babel
        - python-markupsafe
    python-libcloud:
      version: 0.20.0-1
      noarch: True
    python-libnacl:
      version: 1.4.3-1
      noarch: True
      build_deps:
        - libsodium
    python-markupsafe:
      version: 0.11-10
    python-msgpack:
      version: 0.4.6-1
    python-ordereddict:
      version: 1.1-2
      noarch: True
    python-pyzmq:
      name: python-zmq
      version: 14.5.0-2
      build_deps:
        - zeromq
    python-raet:
      version: 0.6.3-2
      noarch: True
      build_deps:
        - python-ioflo
      additional_deps:
        - python-libnacl
    python-requests:
      version: 2.6.0-3
      noarch: True
      build_deps:
        - python-chardet
        - python-ordereddict
        - python-urllib3
    python-six:
      version: 1.9.0-2
      noarch: True
    python-tornado:
      version: 4.2.1-1
      build_deps:
        - python-backports-ssl_match_hostname
    python-tornado-salt:
      version: 4.2.1-1
      build_deps:
        - python-backports-ssl_match_hostname
    python-timelib:
      version: 0.2.4-1
      noarch: True
    python-urllib3:
      version: 1.10.2-1
      noarch: True
    python-yaml:
      name: PyYAML
      version: 3.11-1
      build_deps:
        - libyaml
    salt:
      version: 2016.3.2-1
      noarch: True
      build_deps:
        - python-crypto
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
      build_deps:
        - openpgm
      results:
        - zeromq
        - zeromq-devel

  rhel5:
    babel:
      version: 0.9.5-2
      noarch: True
      build_deps:
        - python-distribute
    libffi:
      version: 3.0.5-1
      results:
        - libffi
        - libffi-debuginfo
        - libffi-devel
    libsodium:
      version: 0.4.5-3
      results:
        - libsodium
        - libsodium-debuginfo
        - libsodium-devel
    libyaml:
      version: 0.1.2-8
      results:
        - libyaml
        - libyaml-debuginfo
        - libyaml-devel
    openpgm:
      version: 5.2.122-2
      results:
        - openpgm
        - openpgm-devel
    pciutils:
      version: 3.1.10-4
      results:
        - pciutils
        - pciutils-debuginfo
        - pciutils-devel
        - pciutils-devel-static
        - pciutils-libs
    python26:
      version: 2.6.8-3
      results:
        - python26
        - python26-debuginfo
        - python26-devel
        - python26-libs
        - python26-test
        - python26-tools
    python-backports:
      name: python26-backports
      version: 1.0-4
    python-backports-ssl_match_hostname:
      name: python26-backports-ssl_match_hostname
      version: 3.4.0.2-2
      noarch: True
      build_deps:
        - python-backports
        - python-distribute
    python-chardet:
      name: python26-chardet
      version: 2.0.1-2
      noarch: True
      build_deps:
        - python-distribute
    python-cherrypy:
      name: python26-cherrypy
      version: 3.5.0-2
      noarch: True
      build_deps:
        - python-distribute
    python-crypto:
      name: python26-crypto
      version: 2.6.1-2
    python-crypto-salt:
      name: python26-crypto-salt
      version: 2.6.1-4
    python-distribute:
      name: python26-distribute
      version: 0.6.10-4
      noarch: True
    python-enum34:
      version: 1.0-4
      noarch: True
    python-importlib:
      version: 1.0.2-1
      noarch: True
    python-ioflo:
      name: python26-ioflo
      version: 1.3.8-1
      noarch: True
      build_deps:
        - python-distribute
    python-jinja2:
      name: python26-jinja2
      version: 2.5.5-6
      noarch: True
      build_deps:
        - python-babel
        - python-crypto
        - python-markupsafe
        - python-distribute
    python-libcloud:
      name: python26-libcloud
      version: 0.20.0-1
      noarch: True
      build_deps:
        - python-distribute
    python-libnacl:
      name: python26-libnacl
      version: 1.4.3-1
      noarch: True
      build_deps:
        - python-distribute
    python-nose:
      name: python26-nose
      version: 0.11.1-4
      noarch: True
      build_deps:
        - python-distribute
    python-markupsafe:
      name: python26-markupsafe
      version: 0.11-3
      build_deps:
        - python-distribute
    python-msgpack:
      name: python26-msgpack
      version: 0.4.5-1
      build_deps:
        - python-distribute
    python-ordereddict:
      version: 1.1-3
      noarch: True
      build_deps:
        - python-distribute
    python-pip:
      name: python26-pip
      version: 1.5.6-1
      noarch: True
      build_deps:
        - python-distribute
    python-pycurl:
      name: python26-pycurl
      version: 7.15.5.1-9
    python-pyzmq:
      name: python26-zmq
      version: 14.5.0-2
      build_deps:
        - zeromq
        - python-distribute
    python-requests:
      name: python26-requests
      version: 1.1.0-5
      noarch: True
      build_deps:
        - python-chardet
        - python-distribute
        - python-ordereddict
        - python-urllib3
    python-six:
      name: python26-six
      version: 1.6.1-2
      noarch: True
      build_deps:
        - python-distribute
    python-tornado:
      name: python26-tornado
      version: 4.2.1-1
      build_deps:
        - python-backports-ssl_match_hostname
        - python-distribute
      additonal_deps:
        - python-pycurl
    python-tornado-salt:
      name: python26-tornado-salt
      version: 4.2.1-1
      build_deps:
        - python-backports-ssl_match_hostname
        - python-distribute
      additonal_deps:
        - python-pycurl
    python-timelib:
      name: python26-timelib
      version: 0.2.4-1
      noarch: True
    python-urllib3:
      name: python26-urllib3
      version: 1.5-8
      noarch: True
      build_deps:
        - python-distribute
    python-yaml:
      name: python26-PyYAML
      version: 3.08-4
      build_deps:
        - libyaml
        - python-distribute
    rpmdevtools:
      version: 6.8-1
      noarch: True
    salt:
      version: 2016.3.2-1
      noarch: True
      build_deps:
        - python-crypto
        - python-msgpack
        - python-yaml
        - python-requests
        - python-pyzmq
        - python-markupsafe
        - python-tornado
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

{% endif %}
