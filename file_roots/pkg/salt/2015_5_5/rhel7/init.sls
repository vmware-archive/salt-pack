{% import "setup/redhat/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}
{% set name = 'salt' %}
{% set version = '2015.5.5' %}

{{name}}-{{version}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - force: {{force}}
    - results: foobar
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}
    - sources:
      - https://pypi.python.org/packages/source/s/{{name}}/{{name}}-{{version}}.tar.gz
      - https://pypi.python.org/packages/source/S/SaltTesting/SaltTesting-2015.7.10.tar.gz
      - salt://{{slspath}}/sources/logrotate.{{name}}
      - salt://{{slspath}}/sources/README.fedora
      - salt://{{slspath}}/sources/{{name}}-{{version}}.tar.gz
      - salt://{{slspath}}/sources/{{name}}-{{version}}-tests.patch
      - salt://{{slspath}}/sources/{{name}}-api
      - salt://{{slspath}}/sources/{{name}}-api.service
      - salt://{{slspath}}/sources/{{name}}-master
      - salt://{{slspath}}/sources/{{name}}-master.service
      - salt://{{slspath}}/sources/{{name}}-minion
      - salt://{{slspath}}/sources/{{name}}-minion.service
      - salt://{{slspath}}/sources/{{name}}-syndic
      - salt://{{slspath}}/sources/{{name}}-syndic.service
      - salt://{{slspath}}/sources/{{name}}.bash
