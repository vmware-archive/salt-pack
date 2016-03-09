{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'yaml' %}
{% set pypi_alt_name = 'pyyaml' %}
{% set name = 'python-' ~ pypi_name %}
{% set name3 = 'python3-' ~ pypi_name %}
{% set version = '3.10' %}
{% set release_ver = '4' %}
{% set release_nameadd = '+deb7u1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dbg_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name3}}_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name3}}-dbg_{{version}}-{{release_ver}}{{release_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{pypi_alt_name}}_{{version}}.orig.tar.gz
      - {{pypi_alt_name}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
      - {{pypi_alt_name}}_{{version}}-{{release_ver}}{{release_nameadd}}.diff.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pypi_alt_name}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{pypi_alt_name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{pypi_alt_name}}_{{version}}-{{release_ver}}{{release_nameadd}}.diff.gz
