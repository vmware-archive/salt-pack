{% import "setup/amazon/map.jinja" as buildcfg %}

{% set repo_keyid = pillar.get('keyid', 'None') %}

include:
  - repo.amazon

{{buildcfg.build_dest_dir}}:
  pkgbuild.repo:
    - order: last
{% if repo_keyid != 'None' %}
    - keyid: {{repo_keyid}}
    - use_passphrase: True
    - gnupghome: {{buildcfg.build_gpg_keydir}}
    - runas: {{buildcfg.build_runas}}
    - env:
        ORIGIN : 'SaltStack'
{% endif %}
