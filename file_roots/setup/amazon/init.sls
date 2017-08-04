# Import base config
{% import "setup/amazon/map.jinja" as build_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% set gpg_key_dir = build_cfg.build_gpg_keydir %}
{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}


lambda-epll-key:
  file.managed:
    - name: /etc/pki/rpm-gpg/RPM-GPG-KEY-lambda-epll
    - source: https://lambda-linux.io/RPM-GPG-KEY-lambda-epll
    - source_hash: md5=5e2aa10522edfd183a4e57d4a3385585
    - dir_mode: 755
    - mode: 644
    - makedirs: True


lambda-epll:
  pkgrepo.managed:
    - humanname: lambda-epll
    - comments:
      - '## Lambda Linux support for Amazon Linux'
    - mirrorlist: http://repo.lambda-linux.io/latest/epll/{{build_cfg.build_arch}}/os/mirror.list
    - gpgcheck: 1
    - gpgkey: file:///etc/pki/rpm-gpg/RPM-GPG-KEY-lambda-epll
    - require:
      - file: lambda-epll-key


salt-repo-key:
  file.managed:
    - name: /etc/pki/rpm-gpg/SALTSTACK-GPG-KEY.pub
    - source: http://repo.saltstack.com/yum/amazon/latest/x86_64/latest/SALTSTACK-GPG-KEY.pub
    - source_hash: md5=9e0d77c16ba1fe57dfd7f1c5c2130438
    - dir_mode: 755
    - mode: 644
    - makedirs: True


salt-repo:
  pkgrepo.managed:
    - humanname: salt-repo
    - comments:
      - '## SaltStack support for Amazon Linux'
    - baseurl: http://repo.saltstack.com/yum/amazon/latest/x86_64/latest
    - gpgcheck: 1
    - gpgkey: file:///etc/pki/rpm-gpg/SALTSTACK-GPG-KEY.pub
    - priority: 10
    - failovermethod: priority
    - require:
      - file: salt-repo-key


build_pkgs:
  pkg.installed:
    - pkgs:
      - createrepo
      - mock
      - rpmdevtools
      - rpm-sign
      - gnupg
      - gnupg2
      - python27-gnupg
    - require:
      - pkgrepo: lambda-epll


{{build_cfg.build_runas}}:
  user.present:
    - groups:
      - mock
    - require:
      - pkg: build_pkgs


manage_priv_key:
  file.managed:
    - name: {{build_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_priv_keyname'] }}
    - dir_mode: 700
    - mode: 600
    - contents_pillar: gpg_pkg_priv_key
    - show_changes: false
    - user: {{build_cfg.build_runas}}
    - group: mock
    - makedirs: True
    - require:
      - user: {{build_cfg.build_runas}}


manage_pub_key:
  file.managed:
    - name: {{build_cfg.build_gpg_keydir}}/{{ pillar['gpg_pkg_pub_keyname'] }}
    - dir_mode: 700
    - mode: 644
    - contents_pillar: gpg_pkg_pub_key
    - show_changes: false
    - user: {{build_cfg.build_runas}}
    - group: mock
    - makedirs: True
    - require:
      - file: manage_priv_key


gpg_load_pub_key:
  module.run:
    - name: gpg.import_key
    - kwargs:
        user: {{build_cfg.build_runas}}
        filename: {{pkg_pub_key_absfile}}
        gnupghome: {{gpg_key_dir}}
    - require:
      - file: manage_pub_key


gpg_load_priv_key:
  module.run:
    - name: gpg.import_key
    - kwargs:
        user: {{build_cfg.build_runas}}
        filename: {{pkg_priv_key_absfile}}
        gnupghome: {{gpg_key_dir}}
    - require:
      - module: gpg_load_pub_key


ensure_gpg_rights:
  file.directory:
    - name: {{gpg_key_dir}}
    - user: {{build_cfg.build_runas}}
    - group: {{build_cfg.build_runas}}
    - dir_mode: 700
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
    - user: {{build_cfg.build_runas}}
    - group: {{build_cfg.build_runas}}
    - mode: 644
    - ret: False
    - require:
      - file: ensure_gpg_rights
