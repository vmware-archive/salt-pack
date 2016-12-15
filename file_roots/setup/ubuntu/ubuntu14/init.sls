# Import base config
{% import "setup/ubuntu/map.jinja" as build_cfg %}

{% set os_codename = 'trusty' %}
{% set prefs_text = 'Package: *
        Pin: origin ""
        Pin-Priority: 1001
        Package: *
        Pin: release a=' ~ os_codename ~ '-backports
        Pin-Priority: 750
        Package: *
        Pin: release a=' ~ os_codename ~ '-security
        Pin-Priority: 740
        Package: *
        Pin: release a=' ~ os_codename ~ '-updates
        Pin-Priority: 730
        Package: *
        Pin: release a=main
        Pin-Priority: 700
        Package: *
        Pin: release a=restricted
        Pin-Priority: 650
        Package: *
        Pin: release a=universe
        Pin-Priority: 600
        Package: *
        Pin: release a=multiverse
        Pin-Priority: 550
' %}


include:
  - setup.ubuntu
  - setup.ubuntu.gpg_agent


build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - python-support


build_pbldhooks_rm_G05:
  file.absent:
    - name: {{build_cfg.build_homedir}}/.pbuilder-hooks/G05apt-preferences


build_pbldhooks_rm_D04:
  file.absent:
    - name: {{build_cfg.build_homedir}}t/.pbuilder-hooks/D04update_local_repo


build_pbldrc_rm:
  file.absent:
    - name: {{build_cfg.build_homedir}}/.pbuilderrc


build_prefs_rm:
  file.absent:
    - name: /etc/apt/preferences


build_pbldhooks_file_G05:
  file.append:
    - name: {{build_cfg.build_homedir}}/.pbuilder-hooks/G05apt-preferences
    - makedirs: True
    - text: |
        #!/bin/sh
        set -e
        cat > "/etc/apt/preferences" << EOF
        {{prefs_text}}
        EOF


build_pbldhooks_file_D04:
  file.append:
    - name: {{build_cfg.build_homedir}}/.pbuilder-hooks/D04update_local_repo
    - makedirs: True
    - text: |
        #!/bin/sh
        # path to local repo
        LOCAL_REPO="{{build_cfg.build_dest_dir}}"
        # Generate a Packages file
        ( cd ${LOCAL_REPO} ; /usr/bin/apt-ftparchive packages . > "${LOCAL_REPO}/Packages" )
        # Update to include any new packagers in the local repo
        apt-get --allow-unauthenticated update


build_pbldhooks_perms:
  file.directory:
    - name: {{build_cfg.build_homedir}}/.pbuilder-hooks/
    - user: {{build_cfg.build_runas}}
    - group: {{build_cfg.build_runas}}
    - dir_mode: 755
    - file_mode: 755
    - recurse:
        - user
        - group
        - mode


build_pbldrc:
  file.append:
    - name: {{build_cfg.build_homedir}}/.pbuilderrc
    - text: |
        DIST="{{os_codename}}"
        LOCAL_REPO="{{build_cfg.build_dest_dir}}"

        # create local repository if it doesn't exist,
        # such as during initial 'pbuilder create'
        if [ ! -d ${LOCAL_REPO} ] ; then
            mkdir -p ${LOCAL_REPO}
        fi
        if [ ! -e ${LOCAL_REPO}/Packages ] ; then
            touch ${LOCAL_REPO}/Packages
        fi

        BINDMOUNTS="${LOCAL_REPO}"
        EXTRAPACKAGES="apt-utils"
        if [ -n "${DIST}" ]; then
          TMPDIR=/tmp
          BASETGZ="`dirname $BASETGZ`/${DIST}-base.tgz"
          DISTRIBUTION=${DIST}
          APTCACHE="/var/cache/pbuilder/${DIST}/aptcache"
        fi
        HOOKDIR="${HOME}/.pbuilder-hooks"
        OTHERMIRROR="deb [trusted=yes] file:${LOCAL_REPO} ./ | deb http://us.archive.ubuntu.com/ubuntu trusty main restricted | deb http://us.archive.ubuntu.com/ubuntu trusty-updates main restricted | deb http://us.archive.ubuntu.com/ubuntu trusty universe | deb http://us.archive.ubuntu.com/ubuntu trusty-updates universe | deb http://us.archive.ubuntu.com/ubuntu trusty multiverse | deb http://us.archive.ubuntu.com/ubuntu trusty-updates multiverse | deb http://us.archive.ubuntu.com/ubuntu trusty-backports main restricted universe multiverse | deb http://us.archive.ubuntu.com/ubuntu trusty-security main restricted | deb http://us.archive.ubuntu.com/ubuntu trusty-security universe | deb http://us.archive.ubuntu.com/ubuntu trusty-security multiverse"


build_prefs:
  file.append:
    - name: /etc/apt/preferences
    - text: |
        {{prefs_text}}

