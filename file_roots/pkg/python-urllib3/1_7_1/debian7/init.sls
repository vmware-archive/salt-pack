{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'urllib3' %}
{% set name = 'python-' ~ pypi_name %}
{% set name3 = 'python3-' ~ pypi_name %}
{% set version = '1.7.1' %}
{% set release_ver = '1' %}
{% set release_nameadd = '~bpo70+1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}_all.deb
      - {{name3}}_{{version}}-{{release_ver}}{{release_nameadd}}_all.deb
      - {{name}}_{{version}}.orig.tar.gz
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.debian.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.debian.tar.gz
