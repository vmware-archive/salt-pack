build_pkgs:
  pkg.installed:
    - pkgs:
      - build-essential
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - gnupg-agent
      - reprepro
      - git
      - debhelper
      - python-support
      - python-setuptools
      - gnupg
      - pkg-config
##      - dh-systemd

builder:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs
