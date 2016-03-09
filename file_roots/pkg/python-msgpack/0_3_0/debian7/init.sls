{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'msgpack' %}
{% set name = 'python-' ~ pypi_name %}
{% set name3 = 'python3-' ~ pypi_name %}
{% set rname = pypi_name ~ '-python' %}
{% set version = '0.3.0' %}
{% set release_ver = '1' %}
{% set release_nameadd = '~bpo70+2' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name3}}_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{rname}}_{{version}}.orig.tar.gz
      - {{rname}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
      - {{rname}}_{{version}}-{{release_ver}}{{release_nameadd}}.debian.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{rname}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{rname}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{rname}}_{{version}}-{{release_ver}}{{release_nameadd}}.debian.tar.gz
