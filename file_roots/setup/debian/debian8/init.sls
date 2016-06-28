# Import base config
{% import "setup/debian/map.jinja" as debian_cfg %}

{% set os_codename = 'jessie' %}
{% set prefs_text = 'Package: *
        Pin: origin ""
        Pin-Priority: 1001
        Package: python3-*
        Pin: release a=testing
        Pin-Priority: 800
        Package: *
        Pin: release a=' ~ os_codename ~ '-backports
        Pin-Priority: 750
        Package: *
        Pin: release a=' ~ os_codename ~ '
        Pin-Priority: 720
        Package: *
        Pin: release a=stable
        Pin-Priority: 700
' %}


include:
  - setup.debian
  - setup.debian.gpg_agent


build_additional_pkgs:
  pkg.installed:
    - pkgs:
      - dh-systemd



build_pbldhookskeys_rm:
  file.absent:
    - name: /root/.pbuilder-hooks/G04importkeys


build_pbldhooks_rm_G05:
  file.absent:
    - name: /root/.pbuilder-hooks/G05apt-preferences


build_pbldrc_rm:
  file.absent:
    - name: /root/.pbuilderrc


build_prefs_rm:
  file.absent:
    - name: /etc/apt/preferences


build_pbldhookskeys_file:
  file.append:
    - name: /root/.pbuilder-hooks/G04importkeys
    - text: |
        /usr/bin/gpg --keyserver pgpkeys.mit.edu --recv 90FDDD2E
        /usr/bin/gpg --export --armor 90FDDD2E | apt-key add -


build_pbldhooks_file_G05:
  file.append:
    - name: /root/.pbuilder-hooks/G05apt-preferences
    - makedirs: True
    - text: |
        #!/bin/sh
        set -e
        cat > "/etc/apt/preferences" << @EOF
        {{prefs_text}}
        @EOF


build_pbldhooks_file_D04:
  file.append:
    - name: /root/.pbuilder-hooks/D04update_local_repo
    - makedirs: True
    - text: |
        #!/bin/sh
        # path to local repo
        LOCAL_REPO="{{debian_cfg.build_dest_dir}}"
        # Generate a Packages file
        ( cd ${LOCAL_REPO} ; /usr/bin/apt-ftparchive packages . > "${LOCAL_REPO}/Packages" )
        # Update to include any new packagers in the local repo
        apt-get --allow-unauthenticated update


build_pbldhooks_perms:
  file.directory:
    - name: /root/.pbuilder-hooks/
    - user: root
    - group: root
    - dir_mode: 755
    - file_mode: 755
    - recurse:
        - user
        - group
        - mode


build_pbldrc:
  file.append:
    - name: /root/.pbuilderrc
    - text: |
        DIST="{{os_codename}}"
        LOCAL_REPO="{{debian_cfg.build_dest_dir}}"
        ## export CCACHE_DIR='/var/cache/pbuilder/ccache'
        ## export PATH="/usr/lib/ccache":${PATH}

        # create local repository if it doesn't exist,
        # such as during initial 'pbuilder create'
        if [ ! -d ${LOCAL_REPO} ] ; then
            mkdir -p ${LOCAL_REPO}
        fi
        if [ ! -e ${LOCAL_REPO}/Packages ] ; then
            touch ${LOCAL_REPO}/Packages
        fi

        ## EXTRAPACKAGES="apt-utils ccache"
        ## BINDMOUNTS="${LOCAL_REPO} ${CCACHE_DIR}"
        EXTRAPACKAGES="apt-utils"
        BINDMOUNTS="${LOCAL_REPO}"
        if [ -n "${DIST}" ]; then
          TMPDIR=/tmp
          BASETGZ="`dirname $BASETGZ`/${DIST}-base.tgz"
          DISTRIBUTION=${DIST}
          APTCACHE="/var/cache/pbuilder/${DIST}/aptcache"
        fi
        HOOKDIR="${HOME}/.pbuilder-hooks"
{% if debian_cfg.build_arch == 'armhf' %}
        DEBOOTSTRAPOPTS=( 
            '--variant=buildd' 
            '--keyring' "${HOME}/.gnupg/pubring.gpg"
        )
        OTHERMIRROR="deb [trusted=yes] file:${LOCAL_REPO} ./ | deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi"
{% else %}
        OTHERMIRROR="deb [trusted=yes] file:${LOCAL_REPO} ./ | deb http://ftp.us.debian.org/debian/ stable main contrib | deb http://ftp.us.debian.org/debian/ testing main contrib "
{% endif %}


build_prefs:
  file.append:
    - name: /etc/apt/preferences
    - text: |
        {{prefs_text}}

