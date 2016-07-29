# Import base config
{% import "setup/ubuntu/map.jinja" as ubuntu_cfg %}

build_pkgs:
  pkg.installed:
    - pkgs:
      - debhelper
      - build-essential
      - ubuntu-dev-tools
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - reprepro
      - git
      - python-setuptools
      - python-gnupg
      - gnupg
      - gnupg-agent
      - pkg-config
      - packaging-dev


{{ubuntu_cfg.build_runas}}:
  user.present:
    - groups:
      - adm
    - require:
      - pkg: build_pkgs


build_cache_result_clean:
  file.absent:
    - name: /var/cache/pbuilder/result


build_cache_result_dir:
  file.directory:
    - name: /var/cache/pbuilder/result
    - user: {{ubuntu_cfg.build_runas}}
    - group: {{ubuntu_cfg.build_runas}} 
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode
    - require:
      - file: build_cache_result_clean
