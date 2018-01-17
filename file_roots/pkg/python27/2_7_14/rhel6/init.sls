{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "python27" %}
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
      - salt://{{slspath}}/sources/00111-no-static-lib.patch
      - salt://{{slspath}}/sources/00104-lib64-fix-for-test_install.patch
      - salt://{{slspath}}/sources/00102-2.7.12-lib64.patch
      - salt://{{slspath}}/sources/00055-systemtap.patch
      - salt://{{slspath}}/sources/00001-pydocnogui.patch
      - salt://{{slspath}}/sources/00133-skip-test_dl.patch
      - salt://{{slspath}}/sources/00132-add-rpmbuild-hooks-to-unittest.patch
      - salt://{{slspath}}/sources/00131-disable-tests-in-test_io.patch
      - salt://{{slspath}}/sources/00125-less-verbose-COUNT_ALLOCS.patch
      - salt://{{slspath}}/sources/00121-add-Modules-to-build-path.patch
      - salt://{{slspath}}/sources/00114-statvfs-f_flag-constants.patch
      - salt://{{slspath}}/sources/00113-more-configuration-flags.patch
      - salt://{{slspath}}/sources/00140-skip-test_ctypes-known-failure-on-sparc.patch
      - salt://{{slspath}}/sources/00139-skip-test_float-known-failure-on-arm.patch
      - salt://{{slspath}}/sources/00138-fix-distutils-tests-in-debug-build.patch
      - salt://{{slspath}}/sources/00137-skip-distutils-tests-that-fail-in-rpmbuild.patch
      - salt://{{slspath}}/sources/00136-skip-tests-of-seeking-stdin-in-rpmbuild.patch
      - salt://{{slspath}}/sources/00135-skip-test-within-test_weakref-in-debug-build.patch
      - salt://{{slspath}}/sources/00134-fix-COUNT_ALLOCS-failure-in-test_sys.patch
      - salt://{{slspath}}/sources/00147-add-debug-malloc-stats.patch
      - salt://{{slspath}}/sources/00146-hashlib-fips.patch
      - salt://{{slspath}}/sources/00144-no-gdbm.patch
      - salt://{{slspath}}/sources/00143-tsc-on-ppc.patch
      - salt://{{slspath}}/sources/00142-skip-failing-pty-tests-in-rpmbuild.patch
      - salt://{{slspath}}/sources/00141-fix-test_gc_with_COUNT_ALLOCS.patch
      - salt://{{slspath}}/sources/05000-autotool-intermediates.patch
      - salt://{{slspath}}/sources/00173-workaround-ENOPROTOOPT-in-bind_port.patch
      - salt://{{slspath}}/sources/00157-uid-gid-overflows.patch
      - salt://{{slspath}}/sources/00156-gdb-autoload-safepath.patch
      - salt://{{slspath}}/sources/00155-avoid-ctypes-thunks.patch
      - salt://{{slspath}}/sources/00153-fix-test_gdb-noise.patch
      - salt://{{slspath}}/sources/python-2.6.4-distutils-rpath.patch
      - salt://{{slspath}}/sources/python-2.5-cflags.patch
      - salt://{{slspath}}/sources/python-2.5.1-sqlite-encoding.patch
      - salt://{{slspath}}/sources/python-2.5.1-plural-fix.patch
      - salt://{{slspath}}/sources/pyfuntop.stp
      - salt://{{slspath}}/sources/macros.python27
      - salt://{{slspath}}/sources/libpython.stp
      - salt://{{slspath}}/sources/python-2.6-rpath.patch
      - salt://{{slspath}}/sources/python-2.7.2-add-extension-suffix-to-python-config.patch
      - salt://{{slspath}}/sources/python-2.7.1-fix_test_abc_with_COUNT_ALLOCS.patch
      - salt://{{slspath}}/sources/python-2.7.1-config.patch
      - salt://{{slspath}}/sources/systemtap-example.stp
      - salt://{{slspath}}/sources/pythondeps.sh
      - salt://{{slspath}}/sources/python-2.7rc1-socketmodule-constants.patch
      - salt://{{slspath}}/sources/python-2.7rc1-socketmodule-constants2.patch
      - salt://{{slspath}}/sources/python-2.7-lib64-sysconfig.patch
      - salt://{{slspath}}/sources/Python-2.7.14.tar.xz
      - salt://{{slspath}}/sources/00112-debug-build.patch
      - salt://{{slspath}}/sources/00900-skip-huntrleaks.patch

{% endif %}
