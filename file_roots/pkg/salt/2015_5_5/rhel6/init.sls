{% import "setup/redhat/map.jinja" as buildcfg %}
{% set force = salt['pillar.get']('build_force.all', False) or salt['pillar.get']('build_force.' ~ slspath, False) %}

{% set pypi_name = 'salt' %}
{% set name = 'salt' %}
{% set version = '2015.5.5' %}

{{name}}-{{version.replace('.', '_')}}:
  pkgbuild.built:
    - runas:{{buildcfg.build_runas}} 
    - force: {{force}}
    - results: foobar
    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{name}}.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}
    - sources:
      - salt://{{slspath}}/sources/logrotate.salt
      - salt://{{slspath}}/sources/README.fedora
      - salt://{{slspath}}/sources/{{name}}-2015.5.5.tar.gz
      - salt://{{slspath}}/sources/{{name}}-2015.5.5-tests.patch
      - salt://{{slspath}}/sources/{{name}}-api
      - salt://{{slspath}}/sources/{{name}}-api.service
      - salt://{{slspath}}/sources/{{name}}-master
      - salt://{{slspath}}/sources/{{name}}-master.service
      - salt://{{slspath}}/sources/{{name}}-minion
      - salt://{{slspath}}/sources/{{name}}-minion.service
      - salt://{{slspath}}/sources/{{name}}-syndic
      - salt://{{slspath}}/sources/{{name}}-syndic.service
      - salt://{{slspath}}/sources/{{name}}.bash
      - salt://{{slspath}}/sources/SaltTesting-2015.7.10.tar.gz
