{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'salt' %}
{% set release_rc_ver = '' %}
{% set version = '2018.3.2' ~ release_rc_ver %}
{% set release_nameadd = '+ds' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}{{release_nameadd}}.orig.tar.gz
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.gz
      - {{name}}-api_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-cloud_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-common_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-master_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-minion_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-ssh_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{name}}-syndic_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_ubuntu.tar.xz
    - tgt: {{buildcfg.build_tgt}}
    - env:
        DEB_BUILD_OPTIONS : 'nocheck'
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}-{{version}}.tar.gz

