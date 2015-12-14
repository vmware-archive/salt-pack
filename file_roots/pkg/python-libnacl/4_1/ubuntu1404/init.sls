{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'nacl' %}
{% set version = '4.1' %}
{% set release_date = '20110221' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - lib{{name}}-dev_{{release_date}}-{{version}}_{{buildcfg.build_arch}}.deb
      - {{name}}-tools_{{release_date}}-{{version}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{release_date}}.orig.tar.bz2
      - {{name}}_{{release_date}}-{{version}}.dsc
      - {{name}}_{{release_date}}-{{version}}.debian.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{release_date}}-{{version}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{release_date}}.orig.tar.bz2
      - salt://{{slspath}}/sources/{{name}}_{{release_date}}-{{version}}.debian.tar.gz

