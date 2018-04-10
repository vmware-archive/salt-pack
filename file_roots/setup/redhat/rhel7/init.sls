# Import base config
{% import "setup/redhat/map.jinja" as build_cfg %}

include:
  - setup.redhat
  - setup.redhat.rhel7.base7_deps


build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - rpm-sign


{% if build_cfg.build_py3 %}
build_additional_py3_pkgs:
  pkg.installed:
    - pkgs:
      - epel-release
      - python34
      - python34-devel
      - python34-setuptools
{% endif %}

