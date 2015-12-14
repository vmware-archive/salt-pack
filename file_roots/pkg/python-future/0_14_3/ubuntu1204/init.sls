{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'future' %}
{% set name = 'python-' ~ pypi_name %}
{% set version = '0.14.3' %}
{% set release_ver = '2' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{name}}_{{version}}-{{release_ver}}_all.deb
      - {{name}}-doc_{{version}}-{{release_ver}}_all.deb
      - {{name}}_{{version}}.orig.tar.xz
      - {{name}}_{{version}}-{{release_ver}}.debian.tar.gz
      - {{name}}_{{version}}-{{release_ver}}.dsc
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.orig.tar.xz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}.debian.tar.gz

