# state file to setup gpg-agent and config on minion
{% import "setup/redhat/map.jinja" as build_cfg %}

{% set pkg_pub_key_file = pillar.get('gpg_pkg_pub_keyname', None) %}
{% set pkg_priv_key_file = pillar.get('gpg_pkg_priv_keyname', None) %}

{% if pkg_pub_key_file!= 'None' and pkg_priv_key_file != 'None' %}

{% set gpg_key_dir = build_cfg.build_gpg_keydir %}
{% set gpg_config_file = gpg_key_dir ~ '/gpg.conf' %}
{% set gpg_agent_config_file = gpg_key_dir ~ '/gpg-agent.conf' %}

{% set pinentry_text = 'pinentry-program /usr/bin/pinentry-curses' %}

{% set pkg_pub_key_absfile = gpg_key_dir ~ '/' ~ pkg_pub_key_file %}
{% set pkg_priv_key_absfile = gpg_key_dir ~ '/' ~ pkg_priv_key_file %}

{% set gpg_agent_text = '# enable-ssh-support
        default-cache-ttl 300
        default-cache-ttl-ssh 300
        max-cache-ttl 300
        max-cache-ttl-ssh 300
        ## debug-all

        # PIN entry program
        ' ~ pinentry_text
%}


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


gpg_agent_conf_file_rm:
  file.absent:
    - name: {{gpg_agent_config_file}}


gpg_agent_conf_file:
  file.append:
    - name: {{gpg_agent_config_file}}
    - makedirs: True
    - text: |
        {{gpg_agent_text}}
    - require:
      - file: gpg_agent_conf_file_rm


ensure_gpg_conf_rights:
  module.run:
    - name: file.check_perms
    - kwargs:
        m_name: {{gpg_config_file}}
        user: {{build_cfg.build_runas}}
        group: {{build_cfg.build_runas}}
        mode: 644
        ret: False
    - require:
      - file: gpg_agent_conf_file

e
nsure_gpg_agent_conf_rights:
  module.run:
    - name: file.check_perms
    - kwargs:
        m_name: {{gpg_agent_config_file}}
        user: {{build_cfg.build_runas}}
        group: {{build_cfg.build_runas}}
        mode: 644
        ret: False


gpg_agent_stop:
  cmd.run:
    - name: killall gpg-agent
    - use_vt: True
    - onlyif: ps -ef | grep  gpg-agent | grep -v 'grep'


gpg_agent_start:
  cmd.run:
    - name: |
        eval $(gpg-agent --homedir {{gpg_key_dir}} --allow-preset-passphrase --max-cache-ttl 300 --daemon)
        GPG_TTY=$(tty)
        export GPG_TTY
#    - python_shell: True
    - use_vt: True
    - runas: {{build_cfg.build_runas}}
    - reload_modules: True
    - require:
      - cmd: gpg_agent_stop

{% endif %}
