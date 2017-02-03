{% import "setup/ubuntu/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.ubuntu

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: True
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - timeout: 100.0
{% endif %}
    - env:
        OPTIONS : 'ask-passphrase'
        ORIGIN : 'SaltStack'
        LABEL : 'salt_ubuntu14'
        CODENAME : 'trusty'
        ARCHS : 'amd64 i386 source'
        COMPONENTS : 'main'
        DESCRIPTION : 'SaltStack Ubuntu 14 package repo'

