# Salt Package Builder (salt-pack)

Salt-pack is an open-source package builder for most commonly used Linux platforms, for example: Redhat/CentOS and Debian/Ubuntu families, utilizing SaltStack states and execution modules to build Salt and a specified set of dependencies, from which a platform specific repository can be built.

Salt-pack relies on SaltStack’s Master-Minion functionality to build the desired packages and repository, and can install the required tools to build the packages and repository for that platform.

The Salt state file which drives the building process is found in salt/states/pkgbuild.py, which provides a typical salt virtual interface to perform the build process.  The virtual interface is satisfied by execution modules for the appropriate supported platform, for example :

Redhat / CentOS
: salt/modules/rpmbuild.py

Debian / Ubuntu
: salt/modules/debbuild.py

The Redhat/CentOS and Debian/Ubuntu platform families build process are internally specified differently, however the external build commands are the same, with keyword arguments for platform specification, for example: rhel6, ubuntu1204.  

The salt-pack project is maintained in GitHub at https://github.com/saltstack/salt-pack.git

# Overview

The building of packages is controlled by SLS state files for the various platforms, which in turn are at the leaf node of a directory tree describing the package name and version. For example:


```
file_roots / pkg / <pkg name> / <version> / OS /
                                                 init.sls
                                                 spec
                                                 sources
                                                 
```
where:

| File / Directory | Description                                                                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| init.sls         | Initialisation SSL file describing what is to be built. Note that this can include files obtained over the Internet.                                            |
| spec             | Directory containing file[s] describing the building of the package for this platform OS, e.g. rpm spec file for Redhat, dsc file or tarball for Debian/Ubuntu. |
| source           | various source files to be used in building the package, for example:  salt-2015.8.5.tar.gz.                                                                    |

| Operating System(OS) | Description       |
|----------------------|-------------------|
| rhel7                | Redhat 7          |
| rhel6                | Redhat 6          |
| rhel5                | Redhat            |
| debian8              | Debian 8 (jessie) |
| ubuntu1404           | Ubuntu 14.04 LTS  |
| ubuntu1204           | Ubuntu 12.04 LTS  |


For example:

`file_roots/pkg/salt/2015_8_7/rhel7/spec/salt.spec`

`file_roots/pkg/salt/2015_8_7/debian8/spec/salt_debian.tar.xz`

Currently the Redhat/CentOS and Debian/Ubuntu platforms are internally built differently.  The Redhat/CentOS builds are pillar data driven state files (pkgbuild.sls contained in pillar_roots) and makes heavy use of Jinja macro’s to define the package to be built, the location of sources and the output that should be produced when the build succeeds.  The Debian/Ubuntu builds are driven only driven by the state files and their contents.  The Debian/Ubuntu builds shall eventually also be driven by pillar data, similar to Redhat/CentOS, but to date there has been insufficient time to achieve this goal.

Packages can be built individually or make use of Salt’s state.highstate to build the salt package and all of its dependencies.

There are currently three highstate SLS files for the three main platforms. These files are as follows:

> `redhat_pkg.sls`
  `debian_pkg.sls`
  `ubuntu_pkg.sls`

Specific versions of these files for salt builds can be found in directory `file_roots/versions/<salt version/` , e.g. `file_roots/2015_8_7/redhat_pkg.sls` and can be specified on the command line, as shown in examples below.

The current families of operating systems, Redhat/CentOS, Debian and Ubuntu have default assumptions as to the most current for those platforms, with older versions being specified by use of command line pillar data. The default values can be overridden by using build_release keyword.

| Platform        | Default  | Overrides    |
|-----------------|----------|--------------|
| Redhat / CentOS | Redhat 7 | rhel6, rhel5 |
| Debian          | 8        | -            |
| Ubuntu          | 14.04    | ubuntu1204   |

The pillar data to drive the build process for Redhat can be found in the following locations:

> `pillar_roots / pkgbuild.sls`
  `pillar_roots / versions / <version> / pkgbuild.sls`

If the file pillar_roots/pkgbuild.sls has the field build_version set, then the file pillar_roots/versions/build_version/pkgbuild.sls is utilized in the building of Redhat packages.

# Setup

The tools required to build salt and it’s dependencies for the various minions and their operating system/platform is handled by state files and macros which can be found in the setup directory and it’s respective operating system/platform sub-directories.  

For example to install the required tools for Redhat 6, Debian 8 and Ubuntu 12 based minions, respectively :

> `salt rh6_minion state.sls setup.redhat.rhel6`
  `salt jessie_minion state.sls setup.debian.debian8`
  `salt ubuntu12_minion state.sls setup.ubuntu.ubuntu12`

The files used to install the tools for each platform are as follows:

### setup/base_map.jinja

Jinja macro file describing build destination, build user, and platform packages to use for highstate.

### macros.jinja

Helper macro definitions utilized in building Salt and it’s dependencies from pillar data (provided by pkgbuild.sls). Currently utilized by Redhat/CentOS build state files.

## Redhat

### setup/redhat/map.jinja

Helper macro definitions for building Redhat 5, 6 and 7 releases

### setup/redhat/init.sls

Common Redhat initialization state files that install the relevant platform tools on the minion to build salt and it’s dependencies, for example: mock, rpmdevtools, createrepo, etc.

### setup/redhat/rhel7/init.sls

### setup/redhat/rhel6/init.sls

### setup/redhat/rhel5/init.sls

Initialization state files install the relevant platform tools on the minion to build salt and it’s dependencies.

## Debian

### setup/debian/map.jinja

Helper macro definitions for building Debian 8 release. Eventually it is hoped to support other Debian releases, for example Debian 7 - Wheezy.

### setup/debian/init.sls

Common Debian initialization state files that install the relevant platform tools on the minion to build salt and it’s dependencies, for example: build-essential, dh-make, pbuilder, debhelper, devscripts, etc.

### setup/debian/debian8/init.sls

### setup/debian/debian7/init.sls

Initialization state files install the relevant platform tools on the minion to build salt and it’s dependencies, install apt-preferences, pbuilder hooks, other repositories to access, etc.

## Ubuntu

### setup/ubuntu/map.jinja

Helper macro definitions for building Ubuntu releases.

### setup/ubuntu/init.sls

Common ubuntu initialization state files that install the relevant platform tools on the minion to build salt and it’s dependencies, for example: build-essential, dh-make, pbuilder, debhelper, devscripts, etc.

### setup/ubuntu/ubuntu14/init.sls

### setup/ubuntu/ubuntu12/init.sls

Initialization state files install the relevant platform tools on the minion to build salt and it’s dependencies, install apt-preferences, pbuilder hooks, other repositories to access, etc.

# Command line Pillar overrides

The build and it’s build product can be controlled by various pillar data on the command line.

The following are command line pillar data overrides available for controlling build releases, destinations, architectures, versions, etc. These keys and values are typically defined in base_map.jinja, and platform’s macro.jinja files.  Note: the default for a platform is typically the newest for that platform, for example: the current default for the Ubuntu platform is ubuntu1404, however once Ubuntu 16.04 LTS is released, then the default shall become ubuntu1604.

| Key           | Values                        | Default                   | Description                                                                                                                                                  |
|---------------|-------------------------------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| build_dest    | Any absolute path             | /srv/pkgs                 | Path describing location to place the product of the build.                                                                                                  |
| build_runas   | Any user                      | Redhat / CentOS - builder | User to use when building - non-root on Redhat and CentOS platforms.                                                                                         |
|               |                               | Debian / Ubuntu - root    | Currently root on Debian and Ubuntu platforms (eventually shall allow for non-root building)                                                                 |
| build_version | Any format not containing ‘.’ | none                      | Typically version of package with dot ( ‘.’ ) replaced by underscore ( ‘_’ ) to accommodate Sal parsing, for example: 2015_8_7 for 2015.8.7, 1_0_3 for 1.0.3 |
| build_release | rhel7, rhel6, rhel5           | rhel7                     | Redhat / CentOS platforms                                                                                                                                    |
|               | debian8, debian7              | debian8                   | Debian platforms                                                                                                                                             |
|               | ubuntu1404, ubuntu1204        | ubuntu1404                | Ubuntu platforms                                                                                                                                             |
| build_arch    | i386, x86_64                  | x86_64                    | Redhat / CentOS platforms                                                                                                                                    |
|               | amd64                         | amd64                     | Debian platforms                                                                                                                                             |
|               | amd64                         | amd64                     | Ubuntu platforms                                                                                                                                             |
# Repo

The tools required to create repositories for salt and it’s dependencies for the various platforms are handled by state files and macros which can be found in the repo directory.



For example to create a repository for Redhat 6, Debian 8 and Ubuntu 12 based minions, respectively :

> `salt rh6_minion state.sls repo.redhat.rhel6 pillar='{ "keyid" : "ABCDEF12", "build_release" : "rhel6" }'`
  `salt jessie_minion state.sls repo.debian.debian8 pillar='{ "keyid" : "ABCDEF12" }'`
  `salt wheezy_minion state.sls repo.debian.debian7  pillar='{ "keyid" : "ABCDEF12" , "build_release" : "debian7"  }'`
  `salt ubuntu12_minion state.sls setup.ubuntu.ubuntu12 pillar='{ "build_release" : "ubuntu1204" }'`

Where the keyid to sign the repository built is an example value `ABCDEF12`, and where the platform is other than the default, the build release is specified.

Currently signing of packages and repositories is performed by hand before the repository is created, that is, the signing key and pass-phase are input by hand. in the case of Debian / Ubuntu this is achieved by the use of gpg-agent to cache the key and pass-phase, and then the repository is created.



## Redhat Signing Process

1.  Ensure .rpmmacros file in your home directory contains %signature and %_gpg_name

    ```bash
    echo "%signature gpg" >>$HOME/.rpmmacros
    echo "%_gpg_name email_address_packager" >>$HOME/.rpmmacros
    ```

1.  Import the appropriate package signing keys into your gpg keyring.

    ```bash
    gpg --import pubkey_filename
    gpg --import --allow-secret-key-import privkey_filename
    sudo rpm --import pubkey_filename
    ```

    That last command is to import your public key into the rpm database  so that it can be used to verify signatures using "rpm --checksig", that is, the rpm key-ring has to have the signing key to correctly sign the packages.

1.  Sign the packages.

    ```bash
    rpm --addsign pkgname.rpm
    ```

    Note: you must sign EL5 packages on a RHEL/CentOS 5 box, or else they won't install properly on RHEL/CentOS 5 host. This is due to Redhat / CentOS 5 using an older encryption/signing technology. Redhat 6 and 7 utilise a V4 signature but Redhat / CentOS 5 is unable to verify V4 signatures.

1.  Checking signatures are done correctly by running:

    ```bash
    rpm --checksig -v pkgname.rpm
    ```

1.  Once all rpm’s which require signing are signed, then you can proceed with creating the repository.

## Debian / Ubuntu Signing Process

1.  In order to sign packages and repositories on Debian / Ubuntu with a pass-phase, the use of gpg-agent to cache the key and pass-phase is currently required.

1.  Once all of the packages are built, excute the following steps:

    ```bash
    service salt-minion stop | systemctl stop salt-minion
    rm -f *.changes
    su - <username>
    killall gpg-agent
    chown -R username:username /var/log/salt* /var/run/salt* /var/cache/salt* /etc/salt* /srv
    ```

1.  Make sure $HOME/.gnupg/gpg.conf , ensure use-agent is uncommented, add it if it is missing, and gnu-agent.conf is configured, for example :

    `$HOME/.gnupg/gpg-agent.conf`:

    ```conf
    # ignore-cache-for-signing
    enable-ssh-support
    write-env-file $HOME/.gnupg/gpg-agent-info
    default-cache-ttl 31536000
    default-cache-ttl-ssh 31536000
    max-cache-ttl 31536000
    max-cache-ttl-ssh 31536000
    ## debug-all

    # PIN entry program
    # pinentry-program /usr/bin/pinentry-qt4
    # pinentry-program /usr/bin/pinentry-kwallet
    # pinentry-program /usr/bin/pinentry-gtk-2
    pinentry-program /usr/bin/pinentry-curses
    ```

    Note: that to use pinentry-curses in the example above, it needs to be installed

    ```bash
    apt-get install pinentry-curses
    ```

1.  Kill any active gpg-agent processes and run the following command:

    ```bash
    gpg-agent --daemon --enable-ssh-support --write-env-file $HOME/.gnupg/gpg-agent.env
    ```

1.  This outputs the following text, cut & paste to command line, such that is executed:

    ```bash
    GPG_AGENT_INFO=/tmp/gpg-m8N7GR/S.gpg-agent:25391:1; export GPG_AGENT_INFO;
    SSH_AUTH_SOCK=/tmp/gpg-aWsul8/S.gpg-agent.ssh; export SSH_AUTH_SOCK;
    SSH_AGENT_PID=25391; export SSH_AGENT_PID;
    ```

1.  Import the appropriate package signing keys into your gpg keyring.

    ```bash
    gpg --import public_key_filename
    gpg --import --allow-secret-key-import private_key_filename
    ```

1.  Sign the packages. The first time you attempt to sign something, it should pop-up a dialog box requesting a passphrase, enter it. You can confirm caching is working, since when you add a second item, it should just do it, with no passphrase requested. Note the sample key ‘ABCDEF12’.

    ```bash
    debsign -k ABCDEF12 *.dsc
    ```

    If the pop-up window does not occur, that is, value it already cached and you are unsure of when it will timeout, you can refresh the cache by the command:

    ```bash
    debsign --re-sign -k ABCDEF12 *.dsc
    ```

1.  Check that the package is signed correctly.

    ```bash
    gpg --verify <test version of dependency>.dsc
    ```

1.  Once all dsc’s which require signing are signed, then you can proceed with creating the repository. Edit the file /etc/salt/minion and set the following:

    ```yaml
    user: <username>
    ```

1.  Now in the same terminal, start up the salt-minion in the foreground,

    ```bash
    /usr/bin/salt-minion -l debug
    ```

1.  This should keep the cached passphrase since in the same session. After this you can issue the create repo command from the salt master:

    ```bash
    salt debian8_minion state.sls repo.debian.debian8 pillar=’{ “keyid” : “ABCDEF12” }’
    ```

# Packages

The packages directory contains all of the various dependencies and salt, listed initially by name, version and platforms for that version.  For example:

Each platform directory consists of an init.sls state file, a spec directory and an optional sources directory, as follows :

| State file / directory | Description                                                                                                                                                                                                                                                                                                                                                                             |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| init.sls               | describes the package and version being build for that platform, its dependencies and expected results.                                                                                                                                                                                                                                                                                 |
| spec                   | appropriate information for defining the building of package that is being  performed on the specific platform, for example: spec file for rpm, dsc for Debian/Ubuntu, tarball containing control files, etc. describing what is being build for Debian/Ubuntu (used for Salt)                                                                                                          |
| sources                | optional directory containing sources and dependencies for the package being built. Not required if all sources are obtained over the network. For example: pkg/python-timelib/0_2_4/rhel7 requires no sources since in init.sls, the macro expands to obtain the sources from https://pypi.python.org/packages/source/t/timelib/timelib-0.2.4.zip#md5=400e316f81001ec0842fa9b2cef5ade9 |
For example: package python-timelib, version 0.2.4

```txt
pkg/python-timelib/

└── 0_2_4

    ├── debian7

    │   ├── init.sls

    │   ├── sources

    │   │   ├── timelib_0.2.4-1.debian.tar.xz

    │   │   └── timelib_0.2.4.orig.tar.gz

    │   └── spec

    │       └── timelib_0.2.4-1.dsc

    ├── debian8

    │   ├── init.sls

    │   ├── sources

    │   │   ├── timelib_0.2.4-1.debian.tar.xz

    │   │   └── timelib_0.2.4.orig.tar.gz

    │   └── spec

    │       └── timelib_0.2.4-1.dsc

    ├── rhel5

    │   ├── init.sls

    │   ├── sources

    │   │   └── timelib-0.2.4.zip

    │   └── spec

    │       └── python-timelib.spec

    ├── rhel6

    │   ├── init.sls

    │   ├── sources

    │   │   └── timelib-0.2.4.zip

    │   └── spec

    │       └── python-timelib.spec

    ├── rhel7

    │   ├── init.sls

    │   └── spec

    │       └── python-timelib.spec

    ├── ubuntu1204

    │   ├── init.sls

    │   ├── sources

    │   │   ├── timelib_0.2.4-1.debian.tar.xz

    │   │   └── timelib_0.2.4.orig.tar.gz

    │   └── spec

    │       └── timelib_0.2.4-1.dsc

    └── ubuntu1404

        ├── init.sls

        ├── sources

        │   ├── timelib_0.2.4-1.debian.tar.xz

        │   └── timelib_0.2.4.orig.tar.gz

        └── spec

            └── timelib_0.2.4-1.dsc
```

## Layout of Init.sls

The init.sls file satifies the requirements of the pkgbuild.py state file, which is defined by  a Yaml file, as follow:

`<pkgname>_<version>`:

`pkgbuild.built`:

-   runas: <username>
-   force: <True | False - indication if build, regardless of existing build product>
-   results: <expected product of the build process>
-   dest_dir: <directory to place the product of the build process>
-   spec: < path to the package's spec file >
-   template: jinja
-   tgt: <target for the build process>
-   sources: <sources need to build package>

### Redhat - init.sls and pkgbuild.sls

On Redhat the build process is driven by pillar data present in pkgbuild.sls (or the versioned pkgbuild.sls if build_version is active), and macro expansions of that pillar data in init.sls.  The pkgbuild.sls file contains pillar data for rhel7, rhel6 and rhel5 platforms, defining salt and it’s dependencies and their dependencies for that platform.

For example, the section of pillar data information to build salt on rhel7 in pkgbuild.sls is as follows:

```yaml
    salt:
      version: 2015.8.7-1
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
```

This section details the following fields:

version                
: version of salt to build

noarch                
: architecture independent

build_deps        
: dependencies required by salt, these are build if not already built before attempting to build salt

results
: expected product of building salt

The salt init.sls file for Redhat 7 is as follows, and is primarily driven by using jinja templating and macros to fill the contents of the various fields required by the init.sls :

```yaml
{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "salt" %}
{% set pypi_name = sls_name %}

{% set pkg_info = pkg_data.get(sls_name, {}) %}
{% if "version" in pkg_info %}
  {% set pkg_name = pkg_info.get("name", sls_name) %}
  {% set version, release = pkg_info["version"].split("-", 1) %}
  {% if pkg_info.get("noarch", False) %}
    {% set arch = "noarch" %}
  {% else %}
    {% set arch = buildcfg.build_arch %}
  {% endif %}

{{ macros.includes(sls_name, pkg_data) }}

{{sls_name}}-{{version}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - force: {{force}}
{{ macros.results(sls_name, pkg_data) }}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pkg_name}}.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}
{{ macros.build_deps(sls_name, pkg_data) }}
{{ macros.requires(sls_name, pkg_data) }}

    - sources:
      ## - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}.tar.gz
      - {{ macros.pypi_source(pypi_name, version) }}
      - {{ macros.pypi_source("SaltTesting", "2015.7.10") }}
      - salt://{{slspath}}/sources/{{pkg_name}}-common.logrotate
      - salt://{{slspath}}/sources/README.fedora
      - salt://{{slspath}}/sources/{{pkg_name}}-api
      - salt://{{slspath}}/sources/{{pkg_name}}-api.service
      - salt://{{slspath}}/sources/{{pkg_name}}-api.environment
      - salt://{{slspath}}/sources/{{pkg_name}}-master
      - salt://{{slspath}}/sources/{{pkg_name}}-master.service
      - salt://{{slspath}}/sources/{{pkg_name}}-master.environment
      - salt://{{slspath}}/sources/{{pkg_name}}-minion
      - salt://{{slspath}}/sources/{{pkg_name}}-minion.service
      - salt://{{slspath}}/sources/{{pkg_name}}-minion.environment
      - salt://{{slspath}}/sources/{{pkg_name}}-syndic
      - salt://{{slspath}}/sources/{{pkg_name}}-syndic.service
      - salt://{{slspath}}/sources/{{pkg_name}}-syndic.environment
      - salt://{{slspath}}/sources/{{pkg_name}}.bash
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}-tests.patch

{% endif %}
```

The initial part of the init.sls expands required values which are then used to state the package name (sls_name) and version. Note that the Salt package in this example is retrieved from Python Package Index website, reducing the need to store salt’s versioned tarball (example of using a local salt versioned tarball is commented out).  slspath is defined in salt and expands to the package’s location on the Salt Master.  

For example, if the base path is `/srv/salt` for this example, `slspath` would expand as follows:

`/srv/salt/pkg/salt/2015_8_7`

### Debian / Ubuntu - init.sls

On Debian and Ubuntu the build process has not yet been converted to be driven by pillar data (it is hoped to upgrade to being by pillar data in the future when time allows), it is entirely driven by the init.sls file.  Hence, using Salt’s 2015.8.7 init.sls file for Debian 8 as an example:

```yaml
{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'salt' %}
{% set version = '2015.8.7' %}
{% set release_nameadd = '+ds' %}
{% set release_ver = '2' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}{{release_nameadd}}.orig.tar.gz
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.xz
      - {{name}}-api_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-cloud_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-common_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-master_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-minion_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-ssh_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-syndic_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_debian.tar.xz
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}-{{version}}.tar.gz
```

The contents of the init.sls are simpler that shown for Redhat init.sls files, due to simpler use of jinja templating, however it is planned to eventually update Debian / Ubuntu to be driven by pillar data since this simplifies specifying versions of packages and their dependencies.

Note that salt’s spec file is a tarball containing the various debian files, such as control, changelog, service files, etc.  The spec file can also be a dsc file on Debian and Ubuntu, for example the init.sls for python-urllib3 on Debian 8:

```yaml
{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'urllib3' %}
{% set name = 'python-' ~ pypi_name %}
{% set name3 = 'python3-' ~ pypi_name %}
{% set version = '1.10.4' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}-{{release_ver}}_all.deb
      - {{name}}-whl_{{version}}-{{release_ver}}_all.deb
      - {{name3}}_{{version}}-{{release_ver}}_all.deb
      - {{name}}_{{version}}.orig.tar.gz
      - {{name}}_{{version}}-{{release_ver}}.dsc
      - {{name}}_{{version}}-{{release_ver}}.debian.tar.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}.debian.tar.xz
```

# Building Salt and Dependencies

Individual packages can be built separately or all packages can be built using highstate.

The highstate is controlled by redhat_pkg.sls, debian_pkg.sls and ubuntu_pkg.sls as stated in the Overview, and contain all of the dependencies for salt on that platform, for example Ubuntu:

`versions/2015_8_7/ubuntu_pkg.sls` 

```yaml
{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1404' %}

   - pkg.libsodium.1_0_3.ubuntu1404
   - pkg.python-enum34.1_0_4.ubuntu1404
   - pkg.python-future.0_14_3.ubuntu1404
   - pkg.python-futures.3_0_3.ubuntu1404
   - pkg.python-ioflo.1_3_8.ubuntu1404
   - pkg.python-libcloud.0_15_1.ubuntu1404
   - pkg.python-libnacl.4_1.ubuntu1404
   - pkg.python-raet.0_6_3.ubuntu1404
   - pkg.python-timelib.0_2_4.ubuntu1404
   - pkg.python-tornado.4_2_1.ubuntu1404
   - pkg.salt.2015_8_7.ubuntu1404
   - pkg.zeromq.4_0_4.ubuntu1404

{% elif buildcfg.build_release == 'ubuntu1204' %}

   - pkg.libsodium.1_0_3.ubuntu1204
   - pkg.python-backports-ssl_match_hostname.3_4_0_2.ubuntu1204
   - pkg.python-croniter.0_3_4.ubuntu1204
   - pkg.python-crypto.2_6_1.ubuntu1204
   - pkg.python-enum34.1_0_4.ubuntu1204
   - pkg.python-future.0_14_3.ubuntu1204
   - pkg.python-futures.3_0_3.ubuntu1204
   - pkg.python-ioflo.1_3_8.ubuntu1204
   - pkg.python-libcloud.0_14_1.ubuntu1204
   - pkg.python-libnacl.4_1.ubuntu1204
   - pkg.python-msgpack.0_3_0.ubuntu1204
   - pkg.python-pyzmq.14_0_1.ubuntu1204
   - pkg.python-raet.0_6_3.ubuntu1204
   - pkg.python-requests.2_0_0.ubuntu1204
   - pkg.python-timelib.0_2_4.ubuntu1204
   - pkg.python-tornado.4_2_1.ubuntu1204
   - pkg.python-urllib3.1_7_1.ubuntu1204
   - pkg.salt.2015_8_7.ubuntu1204
   - pkg.zeromq.4_0_4.ubuntu1204

{% endif %}
```
Hence to build salt 2015.8.7 and it’s dependencies for Ubuntu 12.04 and then create a repository (after signing as outlined above):

```bash
salt u12m state.highstate pillar='{ "build_dest" : "/srv/ubuntu/2015.8.7/pkgs", "build_release" : "ubuntu1204" , "build_version" : "2015_8_7" }'
```

```bash
salt u12m state.sls repo.ubuntu.ubuntu12  pillar='{ "build_dest" : "/srv/ubuntu/2015.8.7/pkgs", "build_release" : "ubuntu1204", "keyid" : "ABCDEF12" , "build_version" : "2015_8_7" }'
```

This command shall place the product of building in destination /srv/ubuntu/2015.8.7/pkgs.

Similarly for Redhat 6 32-bit:

```bash
salt redhat7_minion state.highstate  pillar='{ "build_dest" : "/srv/redhat/2015.8.7/pkgs", "build_release" : "rhel6", "build_arch" : "i386" , "build_version" : "2015_8_7"  }'
```

```bash
salt redhat7_minion state.sls repo.redhat.rhel6  pillar='{ "build_dest" : "/srv/redhat/2015.8.7/pkgs", "keyid" : "ABCDEF12", "build_release" : "rhel6", "build_arch" : "i386"  , "build_version" : "2015_8_7" }'
```

To individually build Salt 2015.8.7 for Redhat 7 :

```bash
salt redhat7_minion state.sls pkg.salt.2015_8_7.rhel7  pillar='{ "build_dest" : "/srv/redhat/2015.8.7/pkgs" , "build_version" : "2015_8_7" }'
```

Note: that currently the building of 32-bit packages on Debian and Ubuntu does not work.  It had worked in early development of salt-pack but for some as yet undetermined reason it stopped working.  Given the movement to 64-bit architectures, 32-bit support is a low priority task.

