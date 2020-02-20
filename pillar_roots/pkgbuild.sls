# set version to build
{% set build_version = 'master' %}


{% if build_version != '' %}
include:
    - versions.{{build_version}}.pkgbuild
{% endif %}
