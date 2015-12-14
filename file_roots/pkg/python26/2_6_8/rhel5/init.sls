{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "python26" %}
{% set pypi_name = "python" %}

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
      - salt://{{slspath}}/sources/libpython-36a517ef7848cbd0b3dcc7371f32e47ac4c87eba.tar.gz
      - salt://{{slspath}}/sources/Python-2.6.8.tar.bz2
      - salt://{{slspath}}/sources/systemtap-example.stp
      - salt://{{slspath}}/sources/pythondeps.sh
      - salt://{{slspath}}/sources/python-2.6-rpath.patch
      - salt://{{slspath}}/sources/python-2.6-distutils_rpm.patch
      - salt://{{slspath}}/sources/python-2.6.8-wrap-_Py_HashSecret_Initialized-with-if-Py_DEBUG.patch
      - salt://{{slspath}}/sources/python-2.6.8-lib64.patch
      - salt://{{slspath}}/sources/python-2.6.8-force-sys-platform-to-be-linux2.patch
      - salt://{{slspath}}/sources/python-2.6.8-ctypes-noexecmem.patch
      - salt://{{slspath}}/sources/Python-2.6.5-parallel_build.patch
      - salt://{{slspath}}/sources/Python-2.6.5-ioctl_test.patch
      - salt://{{slspath}}/sources/python-2.6.4-no-static-lib.patch
      - salt://{{slspath}}/sources/python-2.6.4-expat-version.patch
      - salt://{{slspath}}/sources/python-2.6.4-dtrace.patch
      - salt://{{slspath}}/sources/python-2.6.4-distutils-rpath.patch
      - salt://{{slspath}}/sources/python-2.6.4-autotool-intermediates.patch
      - salt://{{slspath}}/sources/python-2.6.2-with-system-expat.patch
      - salt://{{slspath}}/sources/python-2.6.2-config.patch
      - salt://{{slspath}}/sources/python-2.6.2-binutils-no-dep.patch
      - salt://{{slspath}}/sources/python-2.5-cflags.patch
      - salt://{{slspath}}/sources/python-2.5.1-sqlite-encoding.patch
      - salt://{{slspath}}/sources/python-2.5.1-socketmodule-constants.patch
      - salt://{{slspath}}/sources/python-2.5.1-socketmodule-constants2.patch
      - salt://{{slspath}}/sources/python-2.5.1-plural-fix.patch
      - salt://{{slspath}}/sources/python-2.3.4-lib64-regex.patch
      - salt://{{slspath}}/sources/Python-2.2.1-pydocnogui.patch
      - salt://{{slspath}}/sources/macros.python26
      - salt://{{slspath}}/sources/libpython.stp
      - salt://{{slspath}}/sources/disable-pymalloc-on-valgrind-py26.patch
      - salt://{{slspath}}/sources/brp-multiple-python-bytecompile
{% endif %}
