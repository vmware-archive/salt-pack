# set version to build
{% set build_version = '2018_11' %}


{% if build_version != '' %}
include:
    - .versions.{{build_version}}.pkgbuild
{% endif %}
