{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{# {% set pypi_name = '2.7' %} #}
{% set name = 'python2.7' %}
{% set version = '2.7.12' %}
{% set release_ver = '1' %}

{{name.replace('.', '_')}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}-dev_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dbg_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-minimal_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{name}}-doc_{{version}}-{{release_ver}}_all.deb
      - {{name}}-examples_{{version}}-{{release_ver}}_all.deb
      - idle-{{name}}_{{version}}-{{release_ver}}_all.deb
      - lib{{name}}_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - lib{{name}}-dbg_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - lib{{name}}-dev_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - lib{{name}}-stdlib_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - lib{{name}}-minimal_{{version}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - lib{{name}}-testsuite_{{version}}-{{release_ver}}_all.deb
      - {{name}}_{{version}}-{{release_ver}}.diff.gz
      - {{name}}_{{version}}-{{release_ver}}.dsc
      - {{name}}_{{version}}.orig.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}.diff.gz
