# Import base config
{% import "setup/redhat/map.jinja" as redhat_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% set gpg_key_dir = redhat_cfg.build_gpg_keydir %}
{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}

epel_repo:
  pkgrepo.managed:
    - humanname: epel
    - mirrorlist: https://mirrors.fedoraproject.org/metalink?repo={{redhat_cfg.build_epel}}&arch=$basearch


build_pkgs:
  pkg.installed:
    - pkgs:
      - createrepo
      - mock
      - rpmdevtools
      - rpm-sign
      - gnupg2
      - python2-gnupg
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
    - show_changes: false
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
    - show_changes: false
    - user: {{redhat_cfg.build_runas}}
    - group: mock
    - makedirs: True
    - require:
      - file: manage_priv_key


gpg_load_pub_key:
  module.run:
    - name: gpg.import_key
    - user: {{redhat_cfg.build_runas}}
    - filename: {{pkg_pub_key_absfile}}
    - gnupghome: {{gpg_key_dir}}
    - require:
      - file: manage_pub_key


gpg_load_priv_key:
  module.run:
    - name: gpg.import_key
    - user: {{redhat_cfg.build_runas}}
    - filename: {{pkg_priv_key_absfile}}
    - gnupghome: {{gpg_key_dir}}
    - require:
      - module: gpg_load_pub_key


ensure_gpg_rights:
  file.directory:
    - name: {{gpg_key_dir}}
    - user: {{redhat_cfg.build_runas}}
    - group: {{redhat_cfg.build_runas}}
    - dir_mode: 755
    - file_mode: 600
    - recurse:
        - user
        - group
        - mode
    - require:
      - module: gpg_load_priv_key


ensure_pub_gpg_rights:
  module.run:
    - name: file.check_perms
    - m_name: {{gpg_key_dir}}/gpg_pkg_key.pub
    - user: {{redhat_cfg.build_runas}}
    - group: {{redhat_cfg.build_runas}}
    - mode: 644
    - ret: False
    - require:
      - file: ensure_gpg_rights



