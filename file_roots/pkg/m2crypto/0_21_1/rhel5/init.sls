{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "python-m2crypto" %}
{% set pypi_name = "M2crypto" %}

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
      - {{ macros.pypi_source(pypi_name, version) }}
      - salt://{{slspath}}/sources/m2crypto-0.21.1-timeouts.patch
      - salt://{{slspath}}/sources/m2crypto-0.21.1-smime-doc.patch
      - salt://{{slspath}}/sources/m2crypto-0.21.1-memoryview.patch
      - salt://{{slspath}}/sources/m2crypto-0.21.1-gcc_macros.patch
      - salt://{{slspath}}/sources/m2crypto-0.21.1-AES_crypt.patch
      - salt://{{slspath}}/sources/m2crypto-0.20.2-check.patch
{% endif %}
