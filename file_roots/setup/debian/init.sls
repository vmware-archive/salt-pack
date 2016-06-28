# Import base config
{% import "setup/debian/map.jinja" as debian_cfg %}

build_pkgs:
  pkg.installed:
    - pkgs:
      - build-essential
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - reprepro
      - git
      - debhelper
      - gnupg
      - gnupg-agent
      - python-support
      - python-setuptools
      - python-gnupg
      - pkg-config
      - ccache
##      - dh-systemd

{{debian_cfg.build_runas}}:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs

