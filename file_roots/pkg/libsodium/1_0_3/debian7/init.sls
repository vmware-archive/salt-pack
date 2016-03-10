{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'libsodium' %}
{% set version = '1.0.3' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}13_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dev_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dbg_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{version}}.orig.tar.gz
      - {{name}}_{{version}}-{{release_ver}}.debian.tar.xz
      - {{name}}_{{version}}-{{release_ver}}.dsc
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}.debian.tar.xz

