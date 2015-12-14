{% import "setup/ubuntu/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'zeromq' %}
{% set fullname = name ~ '3' %}
{% set libname = 'libzmq3' %}
{% set version = '4.0.4' %}
{% set release_nameadd = '+dfsg' %}
{% set release_ver = '2' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results: 
      - {{libname}}_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{libname}}-dbg_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{libname}}-dev_{{version}}{{release_nameadd}}-{{release_ver}}_{{buildcfg.build_arch}}.deb
      - {{fullname}}_{{version}}{{release_nameadd}}.orig.tar.gz
      - {{fullname}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc
      - {{fullname}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.gz
      - {{fullname}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.xz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{fullname}}_{{version}}{{release_nameadd}}-{{release_ver}}.dsc 
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}{{release_nameadd}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}{{release_nameadd}}-{{release_ver}}.debian.tar.xz
