{% import "setup/debian/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.debian

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: True
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - timeout: {{buildcfg.repo_sign_timeout}}
{% endif %}
    - env:
        OPTIONS : 'ask-passphrase'
        ORIGIN : 'SaltStack'
        LABEL : 'salt_debian8'
        SUITE: 'stable'
        CODENAME : 'jessie'
{% if buildcfg.build_arch == 'armhf' %}
        ARCHS : '{{buildcfg.build_arch}} source'
{% else %}
        ARCHS : 'amd64 i386 source'
{% endif %}
        COMPONENTS : 'main'
        DESCRIPTION : 'SaltStack Debian 8 package repo'

