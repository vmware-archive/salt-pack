# Import base config
{% import "setup/redhat/map.jinja" as redhat_cfg %}

epel_repo:
  pkgrepo.managed:
    - humanname: epel
    - mirrorlist: https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch

build_pkgs:
  pkg.installed:
    - pkgs:
      - createrepo
      - mock
      - rpmdevtools
      - rpm-sign
      - gnupg2
      - python-gnupg
    - require:
      - pkgrepo: epel_repo


{{redhat_cfg.build_runas}}:
  user.present:
    - groups:
      - mock
    - require:
      - pkg: build_pkgs


manage_priv_key:
  file.managed:
    - name: {{redhat_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_priv_keyname'] }}
    - dir_mode: 700
    - mode: 600
    - contents_pillar: gpg_pkg_priv_key
    - show_diff: false
    - user: {{redhat_cfg.build_runas}}
    - group: mock
    - makedirs: True
    - require:
      - user: {{redhat_cfg.build_runas}}

manage_pub_key:
  file.managed:
    - name: {{redhat_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_pub_keyname'] }}
    - dir_mode: 700
    - mode: 644
    - contents_pillar: gpg_pkg_pub_key
    - show_diff: false
    - user: {{redhat_cfg.build_runas}}
    - group: mock
    - makedirs: True
    - require:
      - file: manage_priv_key

