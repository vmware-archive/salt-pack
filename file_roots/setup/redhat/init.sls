# Import base config
{% import "setup/redhat/map.jinja" as redhat_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% set gpg_key_dir = redhat_cfg.build_gpg_keydir %}
{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}

{% if redhat_cfg.build_epel == 'epel-7' %}
{% set epel_source_hash = '58fa8ae27c89f37b08429f04fd4a88cc' %}
{% else %}
## assume epel-6
{% set epel_source_hash = 'd865e6b948a74cb03bc3401c0b01b785' %}
{% endif %}

os_pkgs_repo_key:
  file.managed:
    - name: /etc/pki/rpm-gpg/RPM-GPG-KEY-{{redhat_cfg.build_epel|upper}}
    - source: https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-{{redhat_cfg.build_epel|upper}}
    - source_hash: md5={{epel_source_hash}}
    - dir_mode: 755
    - mode: 644
    - makedirs: True


os_pkgs_repo:
  pkgrepo.managed:
    - humanname: os_packages_repo_epel
    - mirrorlist: https://mirrors.fedoraproject.org/metalink?repo={{redhat_cfg.build_epel}}&arch=$basearch
    - comments:
      - '## Fedora Project support for epel-release {{redhat_cfg.build_epel}}'
    - gpgcheck: 1
    - gpgkey: file:///etc/pki/rpm-gpg/RPM-GPG-KEY-{{redhat_cfg.build_epel|upper}}
    - require:
      - file: os_pkgs_repo_key


build_pkgs:
  pkg.installed:
    - pkgs:
      - createrepo
      - mock
      - rpmdevtools
      - gnupg2
      - python2-gnupg
    - require:
      - pkgrepo: os_pkgs_repo


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
    - kwargs:
        user: {{redhat_cfg.build_runas}}
        filename: {{pkg_pub_key_absfile}}
        gnupghome: {{gpg_key_dir}}
    - require:
      - file: manage_pub_key


gpg_load_priv_key:
  module.run:
    - name: gpg.import_key
    - kwargs:
        user: {{redhat_cfg.build_runas}}
        filename: {{pkg_priv_key_absfile}}
        gnupghome: {{gpg_key_dir}}
    - require:
      - module: gpg_load_pub_key


ensure_gpg_rights:
  file.directory:
    - name: {{gpg_key_dir}}
    - user: {{redhat_cfg.build_runas}}
    - group: {{redhat_cfg.build_runas}}
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
    - user: {{redhat_cfg.build_runas}}
    - group: {{redhat_cfg.build_runas}}
    - mode: 644
    - ret: False
    - require:
      - file: ensure_gpg_rights



