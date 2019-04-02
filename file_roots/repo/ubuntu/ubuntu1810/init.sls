{% import "setup/ubuntu/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.ubuntu

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
    - use_passphrase: {{buildcfg.repo_use_passphrase}}
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - timeout: {{buildcfg.repo_sign_timeout}}
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: {{buildcfg.repo_use_passphrase}}
{% endif %}
    - env:
{%- if buildcfg.repo_use_passphrase %}
        OPTIONS : 'ask-passphrase'
{%- endif %}
        ORIGIN : 'SaltStack'
        LABEL : 'salt_ubuntu1810'
        CODENAME : 'cosmic'
        ARCHS : 'amd64 source'
        COMPONENTS : 'main'
{%- if buildcfg.build_py3 %}
        DESCRIPTION : 'SaltStack Ubuntu 18.10 Python 3 package repo'
{%- else %}
        DESCRIPTION : 'SaltStack Ubuntu 18.10 Python 2 package repo'
{%- endif %}

