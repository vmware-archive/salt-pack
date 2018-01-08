include:
  - setup.redhat
  - setup.redhat.fedora.gpg_agent

build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - pinentry-gtk

