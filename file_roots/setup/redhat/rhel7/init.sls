include:
  - setup.redhat
  - setup.redhat.rhel7.base7_deps

build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - rpm-sign
