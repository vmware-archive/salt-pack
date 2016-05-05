# state file to setup gpg-agent and config on minion
{% import "setup/debian/map.jinja" as build_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% if pkg_pub_key_file!= 'None' and pkg_priv_key_file != 'None' %}

{% set gpg_key_dir = build_cfg.build_gpg_keydir %}
{% set gpg_config_file = gpg_key_dir ~ '/gpg.conf' %}
{% set gpg_agent_info = gpg_key_dir ~ '/gpg-agent-info-salt' %}

{# {% set gpg_agent_config_file = gpg_key_dir ~ '/gpg-agent.conf' %} #}

{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}


manage_priv_key:
  file.managed:
    - name: {{pkg_priv_key_absfile}}
    - dir_mode: 700
    - mode: 600
    - contents_pillar: gpg_pkg_priv_key
    - show_diff: False
    - user: {{build_cfg.build_runas}}
    - group: adm
    - makedirs: True

manage_pub_key:
  file.managed:
    - name: {{pkg_pub_key_absfile}}
    - dir_mode: 700
    - mode: 644
    - contents_pillar: gpg_pkg_pub_key
    - show_diff: False
    - user: {{build_cfg.build_runas}}
    - group: adm
    - makedirs: True

gpg_conf_file_exists:
  file.touch:
    - name: {{gpg_config_file}}
    - makedirs: True

gpg_conf_file:
  file.replace:
    - name: {{gpg_config_file}}
    - pattern: |
        ^#\s*use-agent\s*\.*
    - repl: |
        use-agent
    - count: 1
    - append_if_not_found: True
    - require:
      - file: gpg_conf_file_exists

gpg_agent_stop:
  module.run:
    - name: cmd.run
    - cmd: killall gpg-agent

gpg_agent_start:
  module.run:
    - name: cmd.run
    - cmd: |
        gpg-agent --homedir {{gpg_key_dir}} --write-env-file {{gpg_agent_info}} --allow-preset-passphrase --max-cache-ttl 7300 --daemon
    - user: {{build_cfg.build_runas}}
    - python_shell: True
    - require:
      - module: gpg_agent_stop

gpg_load_pub_key:
  module.run:
    - name: gpg.import_key
    - user: {{build_cfg.build_runas}}
    - filename: {{pkg_pub_key_absfile}}
    - gnupghome: {{gpg_key_dir}}
    - require:
      - module: gpg_agent_start

gpg_load_priv_key:
  module.run:
    - name: gpg.import_key
    - user: {{build_cfg.build_runas}}
    - filename: {{pkg_priv_key_absfile}}
    - gnupghome: {{gpg_key_dir}}
    - require:
      - module: gpg_agent_start

{% endif %}

