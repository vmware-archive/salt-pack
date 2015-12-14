{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

## {% set pypi_name = '' %}
## {% set name = 'python' ~ pypi_name %}
{% set openname = 'openpgm' %}
{% set name = 'libpgm' ~ pypi_name %}
{% set version = '5.2.122' %}
{% set release_nameadd = '~dfsg' %}
{% set release_ver = '1' %}

{{openname}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{name}}-5.2-0_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dbg_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dev_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{version}}{{release_nameadd}}.orig.tar.xz
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.xz
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}{{release_nameadd}}.orig.tar.xz
      - salt://{{slspath}}/sources/{{name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.xz

