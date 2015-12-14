{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "pciutils" %}

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
      # Can't use the Google Code link because the URL causes Salt to cache the
      # file with a non-matching filename. TODO: Fix this.
      #- https://code.google.com/p/{{pkg_name}}/downloads/detail?name=libpgm-{{version}}.tar.gz
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}.tar.gz
      - salt://{{slspath}}/sources/{{pkg_name}}-havepread.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-dir-d.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-3.1.2-arm.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}-sysfsfill.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-3.0.2-multilib.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-3.0.1-superh-support.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-2.2.1-idpath.patch 
      - salt://{{slspath}}/sources/{{pkg_name}}-2.2.10-sparc-support.patch
      - salt://{{slspath}}/sources/{{pkg_name}}-2.1.10-scan.patch
{% endif %}
