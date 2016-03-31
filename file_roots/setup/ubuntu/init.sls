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
      - python-setuptools
      - gnupg
      - pkg-config
      - ubuntu-dev-tools
      - packaging-dev
##      - python-support


builder:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs
