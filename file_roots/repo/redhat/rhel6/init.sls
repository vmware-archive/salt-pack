{% import "setup/redhat/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.redhat

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
    - order: last
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: True
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - timeout: 100.0
    - env:
        ORIGIN : 'SaltStack'
{% endif %}
