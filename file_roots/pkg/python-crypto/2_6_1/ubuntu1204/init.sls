{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'crypto' %}
{% set name = 'python-' ~ pypi_name %}
{% set version = '2.6.1' %}
{% set release_nameadd = '+nmu' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{name}}_{{version}}{{release_nameadd}}{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{version}}{{release_nameadd}}{{release_ver}}.orig.tar.gz
      - {{name}}_{{version}}{{release_nameadd}}{{release_ver}}.debian.tar.gz
      - {{name}}_{{version}}{{release_nameadd}}{{release_ver}}.dsc
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}{{release_nameadd}}{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}{{release_nameadd}}{{release_ver}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}{{release_nameadd}}{{release_ver}}.debian.tar.gz
