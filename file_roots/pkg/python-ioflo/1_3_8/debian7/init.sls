{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'ioflo' %}
{% set name = 'python-' ~ pypi_name %}
{% set version = '1.3.8' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{name}}_{{version}}-{{release_ver}}_all.deb
      - {{pypi_name}}_{{version}}.orig.tar.gz
      - {{pypi_name}}_{{version}}-{{release_ver}}.dsc
      - {{pypi_name}}_{{version}}-{{release_ver}}.debian.tar.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pypi_name}}_{{version}}-{{release_ver}}.dsc 
    - env:
        DEB_BUILD_OPTIONS : 'nocheck'
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}-{{release_ver}}.debian.tar.xz

