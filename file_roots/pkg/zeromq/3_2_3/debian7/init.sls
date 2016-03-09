{% import "setup/debian/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set name = 'zeromq' %}
{% set fullname = name ~ '3' %}
{% set libname = 'libzmq3' %}
{% set version = '3.2.3' %}
{% set release_ver = '2' %}
{% set release_nameadd1 = '+dfsg' %}
{% set release_nameadd2 = '~bpo70+1' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - results:
      - {{libname}}_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}_{{buildcfg.build_arch}}.deb
      - {{libname}}-dbg_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}_{{buildcfg.build_arch}}.deb
      - {{libname}}-dev_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}_{{buildcfg.build_arch}}.deb
      - {{fullname}}_{{version}}{{release_nameadd1}}.orig.tar.gz
      - {{fullname}}_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}.dsc
      - {{fullname}}_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}.debian.tar.gz
    - force: {{force}}
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{fullname}}_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}.dsc
    - tgt: {{buildcfg.build_tgt}}
    - template: jinja
    - sources:
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}{{release_nameadd1}}.orig.tar.gz
      - salt://{{slspath}}/sources/{{fullname}}_{{version}}{{release_nameadd1}}-{{release_ver}}{{release_nameadd2}}.debian.tar.gz
