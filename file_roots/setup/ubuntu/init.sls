build_pkgs:
  pkg.installed:
    - pkgs:
      - debhelper
      - build-essential
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - gnupg-agent
      - reprepro
      - git
      - python-support
      - python-setuptools
      - libjs-sphinxdoc
      - sphinx-common
      - python-sphinx
      - gnupg
      - pkg-config
      - ubuntu-dev-tools
      - packaging-dev


builder:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs
