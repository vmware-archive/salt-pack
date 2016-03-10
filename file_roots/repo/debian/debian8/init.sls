{% import "setup/debian/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
{% endif %}
    - env:
        OPTIONS : 'ask-passphrase'
        ORIGIN : 'SaltStack'
        LABEL : 'salt_debian8'
        SUITE: 'stable'
        CODENAME : 'jessie'
        ARCHS : 'amd64 i386 source'
        COMPONENTS : 'main'
        DESCRIPTION : 'SaltStack Debian 8 package repo'

