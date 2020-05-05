# Import base config
{% import "setup/redhat/map.jinja" as build_cfg %}

include:
  - setup.redhat
  - setup.redhat.rhel7.base7_deps


build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - rpm-sign
      - nfs-utils


{% if build_cfg.build_py3 %}
build_additional_py3_pkgs:
  pkg.installed:
    - pkgs:
      - epel-release
      - python36
      - python36-devel
      - python36-setuptools
{% endif %}

