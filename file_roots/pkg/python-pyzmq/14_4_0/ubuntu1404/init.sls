{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_short_name = 'zmq' %}
{% set pypi_name = 'py' ~ pypi_short_name  %}
{% set name = 'python-' ~ pypi_name %}
{% set version = '14.4.0' %}
{% set release_ver = '1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - pypy-{{pypi_short_name}}_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - python-{{pypi_short_name}}_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - python-{{pypi_short_name}}-dbg_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - python3-{{pypi_short_name}}_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - python3-{{pypi_short_name}}-dbg_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{pypi_name}}_{{version}}.orig.tar.gz
      - {{pypi_name}}_{{version}}-{{release_ver}}.dsc
      - {{pypi_name}}_{{version}}-{{release_ver}}.debian.gz
      - {{pypi_name}}_{{version}}-{{release_ver}}.debian.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pypi_name}}_{{version}}-{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - env:
        DEB_BUILD_OPTIONS : 'nocheck'
    - sources:
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}-{{release_ver}}.debian.tar.xz
