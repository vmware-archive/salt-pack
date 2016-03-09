{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'futures' %}
{% set name = 'python-' ~ pypi_name %}
{% set fullname = 'python-concurrent.' ~ pypi_name %}
{% set version = '3.0.3' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{fullname}}_{{version}}-{{release_ver}}_all.deb
      - {{fullname}}_{{version}}.orig.tar.xz
      - {{fullname}}_{{version}}-{{release_ver}}.dsc
      - {{fullname}}_{{version}}-{{release_ver}}.debian.tar.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{fullname}}_{{version}}-{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}.orig.tar.xz
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}-{{release_ver}}.debian.tar.xz

