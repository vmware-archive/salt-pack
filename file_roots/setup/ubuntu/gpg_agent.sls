# state file to setup gpg-agent and config on minion
{% import "setup/ubuntu/map.jinja" as build_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% if pkg_pub_key_file!= 'None' and pkg_priv_key_file != 'None' %}

{% set gpg_key_dir = build_cfg.build_gpg_keydir %}
{% set gpg_config_file = gpg_key_dir ~ '/gpg.conf' %}
{% set gpg_tty_info = gpg_key_dir ~ '/gpg-tty-info-salt' %}
{% set gpg_agent_config_file = gpg_key_dir ~ '/gpg-agent.conf' %}

{% if build_cfg.build_release == 'ubuntu1404' %}
{% set write_env_file_prefix = '--' %}
{% set write_env_file = 'write-env-file ' ~  gpg_key_dir ~ '/gpg-agent-info-salt' %}
{% set pinentry_parms = '' %}
{% set pinentry_text = '' %}
{% else %}
{% set write_env_file_prefix = '' %}
{% set write_env_file = '' %}
{% set pinentry_parms = '
        pinentry-timeout 20
        allow-loopback-pinentry' %}
{% set pinentry_text = 'pinentry-program /usr/bin/pinentry-tty' %}
{% endif %}

{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}

{% set gpg_agent_log_file = '/root/gpg-agent.log' %}

{% set gpg_agent_text = '# enable-ssh-support
        ' ~ write_env_file  ~ '
        default-cache-ttl 300
        default-cache-ttl-ssh 300
        max-cache-ttl 300
        max-cache-ttl-ssh 300
        allow-preset-passphrase
        daemon
        debug-all
        ## debug-pinentry
        log-file ' ~ gpg_agent_log_file ~ '
        verbose
        # PIN entry program
        ' ~ pinentry_text ~ pinentry_parms
%}



gpg_agent_stop:
  cmd.run:
    - name: killall -v -w gpg-agent
    - use_vt: True
    - onlyif: ps -ef | grep -v 'grep' | grep  gpg-agent


gpg_dir_rm:
  file.absent:
    - name: {{gpg_key_dir}}


gpg_clear_agent_log:
  file.absent:
    - name: {{gpg_agent_log_file}}


manage_priv_key:
  file.managed:
    - name: {{pkg_priv_key_absfile}}
    - dir_mode: 700
    - mode: 600
    - contents_pillar: gpg_pkg_priv_key
    - show_changes: False
    - user: {{build_cfg.build_runas}}
    - group: adm
    - makedirs: True


manage_pub_key:
  file.managed:
    - name: {{pkg_pub_key_absfile}}
    - dir_mode: 700
    - mode: 644
    - contents_pillar: gpg_pkg_pub_key
    - show_changes: False
    - user: {{build_cfg.build_runas}}
    - group: adm
    - makedirs: True


gpg_conf_file_exists:
  file.touch:
    - name: {{gpg_config_file}}
    - makedirs: True


gpg_tty_file_exists:
  file.touch:
    - name: {{gpg_tty_info}}
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


gpg_agent_conf_file:
  file.append:
    - name: {{gpg_agent_config_file}}
    - makedirs: True
    - text: |
        {{gpg_agent_text}}


gpg_agent_start:
  cmd.run:
    - name: |
        eval $(gpg-agent --homedir {{gpg_key_dir}} {{write_env_file_prefix}}{{write_env_file}} --allow-preset-passphrase --max-cache-ttl 300 --daemon)
        GPG_TTY=$(tty)
        export GPG_TTY
        echo "GPG_TTY=${GPG_TTY}" > {{gpg_tty_info}}
#    - python_shell: True
    - use_vt: True
    - runas: {{build_cfg.build_runas}}
    - reload_modules: True
    - require:
      - cmd: gpg_agent_stop


gpg_load_pub_key:
  module.run:
    - name: gpg.import_key
    - kwargs:
        user: {{build_cfg.build_runas}}
        filename: {{pkg_pub_key_absfile}}
        gnupghome: {{gpg_key_dir}}


gpg_load_priv_key:
  module.run:
    - name: gpg.import_key
    - kwargs:
        user: {{build_cfg.build_runas}}
        filename: {{pkg_priv_key_absfile}}
        gnupghome: {{gpg_key_dir}}

{% endif %}

