{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

## {% set pypi_name = '' %}
## {% set name = 'python' ~ pypi_name %}
{% set name = 'bsdmainutils' %}
{% set version = '9.0.3' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}.dsc
      - {{name}}_{{version}}.tar.gz
      - {{name}}_{{version}}_{{buildcfg.build_arch}}.deb
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.tar.gz


