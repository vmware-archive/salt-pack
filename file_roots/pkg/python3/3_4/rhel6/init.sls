{% import "setup/redhat/map.jinja" as buildcfg %}

{% if buildcfg.build_tgt != 'epel-6-i386' %}
{% set arch_ext = 'x86_64' %}
{% set arch_plt = 'x86_64' %}
{% else %}
{% set arch_ext = 'i686' %}
{% set arch_plt = 'i386' %}
{% endif %}

python343:
  pkgbuild.built:
    - runas: builder
    - results:
      - python34u-3.4.3-2.ius.el6.{{arch_ext}}.rpm
    - dest_dir: /srv/pkgs/rhel6
    - spec: salt://{{slspath}}/spec/python34u.spec
    - template: jinja
    - deps:
      - https://dl.iuscommunity.org/pub/ius/stable/Redhat/6/{{arch_plt}}/python34u-3.4.3-2.ius.el6.{{arch_ext}}.rpm
      - https://dl.iuscommunity.org/pub/ius/stable/Redhat/6/{{arch_plt}}/python34u-libs-3.4.3-2.ius.el6.{{arch_ext}}.rpm
      - https://dl.iuscommunity.org/pub/ius/stable/Redhat/6/{{arch_plt}}/python34u-pip-7.1.0-1.ius.el6.noarch.rpm
      - https://dl.iuscommunity.org/pub/ius/stable/Redhat/6/{{arch_plt}}/python34u-setuptools-18.0.1-1.ius.el6.noarch.rpm
    - tgt: {{buildcfg.build_tgt}}
    - sources: 
      - salt://{{slspath}}/sources/00055-systemtap.patch
      - salt://{{slspath}}/sources/00102-lib64.patch
      - salt://{{slspath}}/sources/00104-lib64-fix-for-test_install.patch
      - salt://{{slspath}}/sources/00111-no-static-lib.patch
      - salt://{{slspath}}/sources/00113-more-configuration-flags.patch
      - salt://{{slspath}}/sources/00125-less-verbose-COUNT_ALLOCS.patch
      - salt://{{slspath}}/sources/00131-disable-tests-in-test_io.patch
      - salt://{{slspath}}/sources/00132-add-rpmbuild-hooks-to-unittest.patch
      - salt://{{slspath}}/sources/00134-fix-COUNT_ALLOCS-failure-in-test_sys.patch
      - salt://{{slspath}}/sources/00135-fix-test-within-test_weakref-in-debug-build.patch
      - salt://{{slspath}}/sources/00137-skip-distutils-tests-that-fail-in-rpmbuild.patch
      - salt://{{slspath}}/sources/00139-skip-test_float-known-failure-on-arm.patch
      - salt://{{slspath}}/sources/00141-fix-tests_with_COUNT_ALLOCS.patch
      - salt://{{slspath}}/sources/00143-tsc-on-ppc.patch
      - salt://{{slspath}}/sources/00146-hashlib-fips.patch
      - salt://{{slspath}}/sources/00150-disable-rAssertAlmostEqual-cmath-on-ppc.patch
      - salt://{{slspath}}/sources/00155-avoid-ctypes-thunks.patch
      - salt://{{slspath}}/sources/00157-uid-gid-overflows.patch
      - salt://{{slspath}}/sources/00160-disable-test_fs_holes-in-rpm-build.patch
      - salt://{{slspath}}/sources/00163-disable-parts-of-test_socket-in-rpm-build.patch
      - salt://{{slspath}}/sources/00164-disable-interrupted_write-tests-on-ppc.patch
      - salt://{{slspath}}/sources/00173-workaround-ENOPROTOOPT-in-bind_port.patch
      - salt://{{slspath}}/sources/00178-dont-duplicate-flags-in-sysconfig.patch
      - salt://{{slspath}}/sources/00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch
      - salt://{{slspath}}/sources/00180-python-add-support-for-ppc64p7.patch
      - salt://{{slspath}}/sources/00184-ctypes-should-build-with-libffi-multilib-wrapper.patch
      - salt://{{slspath}}/sources/00186-dont-raise-from-py_compile.patch
      - salt://{{slspath}}/sources/00188-fix-lib2to3-tests-when-hashlib-doesnt-compile-properly.patch
      - salt://{{slspath}}/sources/00189-add-rewheel-module.patch
      - salt://{{slspath}}/sources/00203-disable-threading-test-koji.patch
      - salt://{{slspath}}/sources/05000-autotool-intermediates.patch
      - salt://{{slspath}}/sources/check-pyc-and-pyo-timestamps.py
      - salt://{{slspath}}/sources/find-provides-without-python-sonames.sh
      - salt://{{slspath}}/sources/libpython.stp
      - salt://{{slspath}}/sources/macros.pybytecompile3.4
      - salt://{{slspath}}/sources/macros.python3.4
      - salt://{{slspath}}/sources/pyfuntop.stp
      - salt://{{slspath}}/sources/Python-3.1.1-rpath.patch
      - salt://{{slspath}}/sources/python3-arm-skip-failing-fragile-test.patch
      - salt://{{slspath}}/sources/systemtap-example.stp
      - salt://{{slspath}}/sources/temporarily-disable-tests-requiring-SIGHUP.patch
      - https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz
