# Import base config
{% import "setup/ubuntu/map.jinja" as ubuntu_cfg %}

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


{{ubuntu_cfg.build_runas}}:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs


manage_priv_key:
  file.managed:
    - name: /{{ubuntu_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_priv_keyname'] }}
    - dir_mode: 700
    - mode: 600
    - contents_pillar: gpg_pkg_priv_key
    - show_diff: false
    - user: {{ubuntu_cfg.build_runas}}
    - group: mock
    - makedirs: True


manage_pub_key:
  file.managed:
    - name: /{{ubuntu_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_pub_keyname'] }}
    - dir_mode: 700
    - mode: 644
    - contents_pillar: gpg_pkg_pub_key
    - show_diff: false
    - user: {{ubuntu_cfg.build_runas}}
    - group: mock
    - makedirs: True

