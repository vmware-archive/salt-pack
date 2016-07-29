# Import base config
{% import "setup/debian/map.jinja" as debian_cfg %}

build_pkgs:
  pkg.installed:
    - pkgs:
      - build-essential
      - devscripts
      - dh-make
      - fakeroot
      - debootstrap
      - pbuilder
      - reprepro
      - git
      - debhelper
      - gnupg
      - gnupg-agent
      - python-support
      - python-setuptools
      - python-gnupg
      - pkg-config
      - ccache
##      - dh-systemd

{{debian_cfg.build_runas}}:
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
    - user: {{debian_cfg.build_runas}}
    - group: {{debian_cfg.build_runas}} 
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode
    - require:
      - file: build_cache_result_clean
