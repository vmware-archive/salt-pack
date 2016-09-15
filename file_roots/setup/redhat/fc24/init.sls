include:
  - setup.redhat
  - setup.redhat.fc24.gpg_agent

build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - pinentry-gtk

