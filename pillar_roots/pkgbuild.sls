# set version to build
{% set build_version = '2017_7_7' %}


{% if build_version != '' %}
include:
    - .versions.{{build_version}}.pkgbuild
{% endif %}
