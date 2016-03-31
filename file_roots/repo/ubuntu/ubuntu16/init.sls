{% import "setup/ubuntu/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
{% endif %}
    - env:
        OPTIONS : 'ask-passphrase'
        ORIGIN : 'SaltStack'
        LABEL : 'salt_ubuntu16'
        CODENAME : 'xenial'
        ARCHS : 'amd64 i386 source'
        COMPONENTS : 'main'
        DESCRIPTION : 'SaltStack Ubuntu 16 package repo'

