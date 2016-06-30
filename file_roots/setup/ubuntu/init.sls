# Import base config
{% import "setup/ubuntu/map.jinja" as ubuntu_cfg %}

build_pkgs:
  pkg.installed:
    - pkgs:
      - debhelper
      - build-essential
      - ubuntu-dev-tools
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - reprepro
      - git
      - python-setuptools
      - python-gnupg
      - gnupg
      - gnupg-agent
      - pkg-config
      - packaging-dev


{{ubuntu_cfg.build_runas}}:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs

