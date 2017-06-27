{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'libcloud' %}
{% set name = 'python-' ~ pypi_name %}
{% set version = '1.5.0' %}
{% set release_ver = '1' %}
{% set release_nameadd = '+ds' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{name}}_{{version}}{{release_nameadd}}-{{release_ver}}_all.deb
      - {{pypi_name}}_{{version}}{{release_nameadd}}.orig.tar.bz2
      - {{pypi_name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
      - {{pypi_name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pypi_name}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - env:
        DEB_BUILD_OPTIONS : 'nocheck'
    - sources:
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}{{release_nameadd}}.orig.tar.bz2
      - salt://{{slspath}}/sources/{{pypi_name}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.gz

