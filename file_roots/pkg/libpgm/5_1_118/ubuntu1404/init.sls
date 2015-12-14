{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'libpgm' %}
{% set fullname = name ~ '-dev' %}
{% set version = '5.1.118' %}
{% set release_nameadd = '~dfsg' %}
{% set fullrelease_nameadd = release_nameadd ~ '-0.1ubuntu3' %}
{% set release_ver = '1' %}

{{fullname}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{name}}-5.1-0_{{version}}-{{release_ver}}{{fullrelease_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dbg_{{version}}-{{release_ver}}{{fullrelease_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name}}-dev_{{version}}-{{release_ver}}{{fullrelease_nameadd}}_{{buildcfg.build_arch}}.deb
      - {{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.orig.tar.gz
      - {{name}}_{{version}}-{{release_ver}}{{fullrelease_nameadd}}.dsc
      - {{name}}_{{version}}-{{release_ver}}{{fullrelease_nameadd}}.debian.tar.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}_{{version}}-{{release_ver}}{{fullrelease_nameadd}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}{{release_nameadd}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{name}}_{{version}}-{{release_ver}}{{fullrelease_nameadd}}.debian.tar.gz

