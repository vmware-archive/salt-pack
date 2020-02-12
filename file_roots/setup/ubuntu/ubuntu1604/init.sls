# Import base config
{% import "setup/ubuntu/map.jinja" as build_cfg %}

include:
  - setup.ubuntu.ubuntu1604.ubuntu1604_setup
  - setup.ubuntu.gpg_agent

