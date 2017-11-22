{% import "setup/ubuntu/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.ubuntu

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: {{buildcfg.repo_use_passphrase}}
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - timeout: {{buildcfg.repo_sign_timeout}}
{% endif %}
    - env:
{%- if buildcfg.repo_use_passphrase %}    
        OPTIONS : 'ask-passphrase'
{%- endif %}
        ORIGIN : 'SaltStack'
        LABEL : 'salt_ubuntu14'
        CODENAME : 'trusty'
        ARCHS : 'amd64 i386 source'
        COMPONENTS : 'main'
        DESCRIPTION : 'SaltStack Ubuntu 14 package repo'

