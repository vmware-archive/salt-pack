{% import "setup/amazon/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "salt" %}
{% set pypi_name = sls_name %}

{% set pkg_info = pkg_data.get(sls_name, {}) %}
{% if "version" in pkg_info %}
  {% set pkg_name = pkg_info.get("name", sls_name) %}
  {% set version, release = pkg_info["version"].split("-", 1) %}
  {% if pkg_info.get("noarch", False) %}
    {% set arch = "noarch" %}
  {% else %}
    {% set arch = buildcfg.build_arch %}
  {% endif %}

{{ macros.includes(sls_name, pkg_data) }}

{{sls_name}}-{{version}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - force: {{force}}

{{ macros.results(sls_name, pkg_data) }}

    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pkg_name}}.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}

{{ macros.build_deps(sls_name, pkg_data) }}
{{ macros.requires(sls_name, pkg_data) }}

    - sources:
##      - {{ macros.pypi_source(pypi_name, version) }}
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}.tar.gz
      - {{ macros.pypi_source("SaltTesting", "2016.10.26") }}
      - salt://{{slspath}}/sources/{{pkg_name}}-common.logrotate
      - salt://{{slspath}}/sources/README.fedora
      - salt://{{slspath}}/sources/{{pkg_name}}-api
      - salt://{{slspath}}/sources/{{pkg_name}}-api.service
      - salt://{{slspath}}/sources/{{pkg_name}}-master
      - salt://{{slspath}}/sources/{{pkg_name}}-master.service
      - salt://{{slspath}}/sources/{{pkg_name}}-minion
      - salt://{{slspath}}/sources/{{pkg_name}}-minion.service
      - salt://{{slspath}}/sources/{{pkg_name}}-syndic
      - salt://{{slspath}}/sources/{{pkg_name}}-syndic.service
      - salt://{{slspath}}/sources/{{pkg_name}}.bash

{% endif %}
