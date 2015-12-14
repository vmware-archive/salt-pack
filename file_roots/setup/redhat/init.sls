epel_repo:
  pkgrepo.managed:
    - humanname: epel
    - mirrorlist: https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch

build_pkgs:
  pkg.installed:
    - pkgs:
      - createrepo
      - mock
      - rpmdevtools
    - require:
      - pkgrepo: epel_repo

builder:
  user.present:
    - groups:
      - mock
    - require:
      - pkg: build_pkgs
