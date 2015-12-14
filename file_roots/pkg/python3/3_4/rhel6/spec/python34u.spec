# ======================================================
# Conditionals and other variables controlling the build
# ======================================================

# NOTES ON BOOTSTRAPPING PYTHON 3.4:
#
# Due to dependency cycle between Python, pip, setuptools and
# wheel caused by the rewheel patch, one has to build in the
# following order:
#
# 1) python34u with_rewheel 0
# 2) python34u-setuptools build_rewheel 0
# 3) python34u-pip build_rewheel 0
# 4) python34u-wheel
# 5) python34u-setuptools build_rewheel 1
# 6) python34u-pip build_rewheel 1
# 7) python34u with_rewheel 1

%global with_rewheel 1

%global pybasever 3.4

# pybasever without the dot:
%global pyshortver 34

%global iusver %{pyshortver}u

%if 0%{?rhel} >= 7
%global _brpdir /usr/lib/rpm
%global _macrosdir %{_rpmconfigdir}/macros.d
%else
%global _brpdir /usr/lib/rpm/redhat
%global _macrosdir %{_sysconfdir}/rpm
%endif

%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload

# SOABI is defined in the upstream configure.in from Python-3.2a2 onwards,
# for PEP 3149:
#   http://www.python.org/dev/peps/pep-3149/

# ("configure.in" became "configure.ac" in Python 3.3 onwards, and in
# backports)

# ABIFLAGS, LDVERSION and SOABI are in the upstream Makefile
# With Python 3.3, we lose the "u" suffix due to PEP 393
%global ABIFLAGS_optimized m
%global ABIFLAGS_debug     dm

%global LDVERSION_optimized %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug     %{pybasever}%{ABIFLAGS_debug}

%global SOABI_optimized cpython-%{pyshortver}%{ABIFLAGS_optimized}
%global SOABI_debug     cpython-%{pyshortver}%{ABIFLAGS_debug}

# All bytecode files are now in a __pycache__ subdirectory, with a name
# reflecting the version of the bytecode (to permit sharing of python libraries
# between different runtimes)
# See http://www.python.org/dev/peps/pep-3147/
# For example,
#   foo/bar.py
# now has bytecode at:
#   foo/__pycache__/bar.cpython-34.pyc
#   foo/__pycache__/bar.cpython-34.pyo
%global bytecode_suffixes .cpython-34.py?

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{LDVERSION_optimized}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug     libpython%{LDVERSION_debug}.so.%{py_SOVERSION}

%global with_debug_build 1

%global with_gdb_hooks 1

%global with_systemtap 1

# some arches don't have valgrind so we need to disable its support on them
%ifnarch s390 ppc64le
%global with_valgrind 1
%else
%global with_valgrind 0
%endif

%global with_gdbm 1

# Change from yes to no to turn this off
%global with_computed_gotos yes

# Turn this to 0 to turn off the "check" phase:
%if 0%{?with_rewheel}
%global run_selftest_suite 1
%else
%global run_selftest_suite 0
%endif

# We want to byte-compile the .py files within the packages using the new
# python3 binary.
# 
# Unfortunately, rpmbuild's infrastructure requires us to jump through some
# hoops to avoid byte-compiling with the system python 2 version:
#   /usr/lib/rpm/redhat/macros sets up build policy that (amongst other things)
# defines __os_install_post.  In particular, "brp-python-bytecompile" is
# invoked without an argument thus using the wrong version of python
# (/usr/bin/python, rather than the freshly built python), thus leading to
# numerous syntax errors, and incorrect magic numbers in the .pyc files.  We
# thus override __os_install_post to avoid invoking this script:
%global __os_install_post %{_brpdir}/brp-compress \
  %{!?__debug_package:%{_brpdir}/brp-strip %{__strip}} \
  %{_brpdir}/brp-strip-static-archive %{__strip} \
  %{_brpdir}/brp-strip-comment-note %{__strip} %{__objdump} \
  %{_brpdir}/brp-python-hardlink
# to remove the invocation of brp-python-bytecompile, whilst keeping the
# invocation of brp-python-hardlink (since this should still work for python3
# pyc/pyo files)


# We need to get a newer configure generated out of configure.in for the following
# patches:
#   patch 55 (systemtap)
#   patch 113 (more config flags)
#
# For patch 55 (systemtap), we need to get a new header for configure to use
#
# configure.in requires autoconf-2.65, but the version in Fedora is currently
# autoconf-2.66
#
# For now, we'll generate a patch to the generated configure script and
# pyconfig.h.in on a machine that has a local copy of autoconf 2.65
#
# Instructions on obtaining such a copy can be seen at
#   http://bugs.python.org/issue7997
#
# To make it easy to regenerate the patch, this specfile can be run in two
# ways:
# (i) regenerate_autotooling_patch  0 : the normal approach: prep the
# source tree using a pre-generated patch to the "configure" script, and do a
# full build
# (ii) regenerate_autotooling_patch 1 : intended to be run on a developer's
# workstation: prep the source tree without patching configure, then rerun a
# local copy of autoconf-2.65, regenerate the patch, then exit, without doing
# the rest of the build
%global regenerate_autotooling_patch 0


# ==================
# Top-level metadata
# ==================
Summary: Version 3 of the Python programming language aka Python 3000
Name: python%{iusver}
Version: %{pybasever}.3
Release: 2.ius%{?dist}
License: Python
Group: Development/Languages
# conflict with other IUS python3 packages
Conflicts: python33
Conflicts: python32
Conflicts: python31


# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf
BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: db4-devel >= 4.7

# expat 2.1.0 added the symbol XML_SetHashSalt without bumping SONAME.  Fedora
# requires this version to account for CVE-2012-0876.  However, that symbol was
# backported when the CVE was patched in el6, so I don't believe we need it for
# IUS.
#
# $ rpm -qf /lib64/libexpat.so.1
# expat-2.0.1-11.el6_2.x86_64
# $ strings /lib64/libexpat.so.1 | grep XML_SetHash
# XML_SetHashSalt
#
# https://rhn.redhat.com/errata/RHSA-2012-0731.html#Red Hat Enterprise Linux Server (v. 6)
# https://bugzilla.redhat.com/show_bug.cgi?id=821337
BuildRequires: expat-devel

BuildRequires: findutils
BuildRequires: gcc-c++
%if %{with_gdbm}
BuildRequires: gdbm-devel
%endif
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: net-tools
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
# (this introduces a dependency on "python", in that systemtap-sdt-devel's
# /usr/bin/dtrace is a python 2 script)
%global tapsetdir      /usr/share/systemtap/tapset
%endif # with_systemtap

BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel

%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

BuildRequires: xz-devel
BuildRequires: zlib-devel

%if 0%{?with_rewheel}
BuildRequires: python%{iusver}-setuptools
BuildRequires: python%{iusver}-pip
%endif


# =======================
# Source code and patches
# =======================

Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

# Avoid having various bogus auto-generated Provides lines for the various
# python c modules' SONAMEs:
Source1: find-provides-without-python-sonames.sh
%global _use_internal_dependency_generator 0
%global __find_provides %{SOURCE1}

# Supply various useful macros for building python 3 modules:
#  __python3, python3_sitelib, python3_sitearch
Source2: macros.python%{pybasever}

# Supply an RPM macro "py_byte_compile" for the python3-devel subpackage
# to enable specfiles to selectively byte-compile individual files and paths
# with different Python runtimes as necessary:
Source3: macros.pybytecompile%{pybasever}

# Systemtap tapset to make it easier to use the systemtap static probes
# (actually a template; LIBRARY_PATH will get fixed up during install)
# Written by dmalcolm; not yet sent upstream
Source5: libpython.stp

# Example systemtap script using the tapset
# Written by wcohen, mjw, dmalcolm; not yet sent upstream
Source6: systemtap-example.stp

# Another example systemtap script that uses the tapset
# Written by dmalcolm; not yet sent upstream
Source7: pyfuntop.stp

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Written by bkabrda
Source8: check-pyc-and-pyo-timestamps.py

# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Was Patch0 in ivazquez' python3000 specfile:
Patch1:         Python-3.1.1-rpath.patch

# Some tests were removed due to audiotest.au not being packaged. This was
# however added to the archive in 3.3.1, so we no longer delete the tests.
#  Patch3: 00003-remove-mimeaudio-tests.patch

# 00055 #
# Systemtap support: add statically-defined probe points
# Patch sent upstream as http://bugs.python.org/issue14776
# with some subsequent reworking to cope with LANG=C in an rpmbuild
# (where sys.getfilesystemencoding() == 'ascii')
Patch55: 00055-systemtap.patch

Patch102: 00102-lib64.patch

# 00104 #
# Only used when "%{_lib}" == "lib64"
# Another lib64 fix, for distutils/tests/test_install.py; not upstream:
Patch104: 00104-lib64-fix-for-test_install.patch

# 00111 #
# Patch the Makefile.pre.in so that the generated Makefile doesn't try to build
# a libpythonMAJOR.MINOR.a (bug 550692):
# Downstream only: not appropriate for upstream
Patch111: 00111-no-static-lib.patch

# 00112 #
# Patch112: python-2.7rc1-debug-build.patch: this is not relevant to Python 3,
# for 3.2 onwards

# 00113 #
# Add configure-time support for the COUNT_ALLOCS and CALL_PROFILE options
# described at http://svn.python.org/projects/python/trunk/Misc/SpecialBuilds.txt
# so that if they are enabled, they will be in that build's pyconfig.h, so that
# extension modules will reliably use them
# Not yet sent upstream
Patch113: 00113-more-configuration-flags.patch

# 00114 #
# Upstream as of Python 3.4.0.b2
#  Patch114: 00114-statvfs-f_flag-constants.patch

# 00125 #
# COUNT_ALLOCS is useful for debugging, but the upstream behaviour of always
# emitting debug info to stdout on exit is too verbose and makes it harder to
# use the debug build.  Add a "PYTHONDUMPCOUNTS" environment variable which
# must be set to enable the output on exit
# Not yet sent upstream
Patch125: 00125-less-verbose-COUNT_ALLOCS.patch

# 00130 #
# Python 2's:
#   Patch130: python-2.7.2-add-extension-suffix-to-python-config.patch
# is not relevant to Python 3 (for 3.2 onwards)

# 00131 #
# The four tests in test_io built on top of check_interrupted_write_retry
# fail when built in Koji, for ppc and ppc64; for some reason, the SIGALRM
# handlers are never called, and the call to write runs to completion
# (rhbz#732998)
Patch131: 00131-disable-tests-in-test_io.patch

# 00132 #
# Add non-standard hooks to unittest for use in the "check" phase below, when
# running selftests within the build:
#   @unittest._skipInRpmBuild(reason)
# for tests that hang or fail intermittently within the build environment, and:
#   @unittest._expectedFailureInRpmBuild
# for tests that always fail within the build environment
#
# The hooks only take effect if WITHIN_PYTHON_RPM_BUILD is set in the
# environment, which we set manually in the appropriate portion of the "check"
# phase below (and which potentially other python-* rpms could set, to reuse
# these unittest hooks in their own "check" phases)
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch

# 00133 #
# 00133-skip-test_dl.patch is not relevant for python3: the "dl" module no
# longer exists

# 00134 #
# Fix a failure in test_sys.py when configured with COUNT_ALLOCS enabled
# Not yet sent upstream
Patch134: 00134-fix-COUNT_ALLOCS-failure-in-test_sys.patch

# 00135 #
# test_weakref's test_callback_in_cycle_resurrection doesn't work with
# COUNT_ALLOCS, as the metrics keep "C" alive.  Work around this for our
# debug build:
# Not yet sent upstream
Patch135: 00135-fix-test-within-test_weakref-in-debug-build.patch

# 00136 #
# Patch136: 00136-skip-tests-of-seeking-stdin-in-rpmbuild.patch does not seem
# to be needed by python3

# 00137 #
# Some tests within distutils fail when run in an rpmbuild:
Patch137: 00137-skip-distutils-tests-that-fail-in-rpmbuild.patch

# 00138 #
# Patch138: 00138-fix-distutils-tests-in-debug-build.patch is not relevant for
# python3

# 00139 #
# ARM-specific: skip known failure in test_float:
#  http://bugs.python.org/issue8265 (rhbz#706253)
Patch139: 00139-skip-test_float-known-failure-on-arm.patch

# ideally short lived patch disabling a test thats fragile on different arches
Patch140: python3-arm-skip-failing-fragile-test.patch

# Patch140: 00140-skip-test_ctypes-known-failure-on-sparc.patch does not appear
# to be relevant for python3

# 00141 #
# Fix tests for case when  tests for case when configured with
# COUNT_ALLOCS (debug build): http://bugs.python.org/issue19527
# Applies to: test_gc, test_module, test_io, test_logging, test_warnings,
#             test_threading
Patch141: 00141-fix-tests_with_COUNT_ALLOCS.patch

# 00143 #
# Fix the --with-tsc option on ppc64, and rework it on 32-bit ppc to avoid
# aliasing violations (rhbz#698726)
# Sent upstream as http://bugs.python.org/issue12872
Patch143: 00143-tsc-on-ppc.patch

# 00144 #
# (Optionally) disable the gdbm module:
# python.spec's
#   Patch144: 00144-no-gdbm.patch
# is not needed in python3.spec

# 00145 #
# python.spec's
#   Patch145: 00145-force-sys-platform-to-be-linux2.patch
# is upstream for Python 3 as of 3.2.2

# 00146 #
# Support OpenSSL FIPS mode (e.g. when OPENSSL_FORCE_FIPS_MODE=1 is set)
# - handle failures from OpenSSL (e.g. on attempts to use MD5 in a
#   FIPS-enforcing environment)
# - add a new "usedforsecurity" keyword argument to the various digest
#   algorithms in hashlib so that you can whitelist a callsite with
#   "usedforsecurity=False"
# (sent upstream for python 3 as http://bugs.python.org/issue9216 ; see RHEL6
# python patch 119)
# - enforce usage of the _hashlib implementation: don't fall back to the _md5
#   and _sha* modules (leading to clearer error messages if fips selftests
#   fail)
# - don't build the _md5 and _sha* modules; rely on the _hashlib implementation
#   of hashlib
# (rhbz#563986)
# Note: Up to Python 3.4.0.b1, upstream had their own implementation of what
# they assumed would become sha3. This patch was adapted to give it the
# usedforsecurity argument, even though it did nothing (OpenSSL didn't have
# sha3 implementation at that time).In 3.4.0.b2, sha3 implementation was reverted
# (see http://bugs.python.org/issue16113), but the alterations were left in the
# patch, since they may be useful again if upstream decides to rerevert sha3
# implementation and OpenSSL still doesn't support it. For now, they're harmless.
Patch146: 00146-hashlib-fips.patch

# 00147 #
# Add a sys._debugmallocstats() function
# Sent upstream as http://bugs.python.org/issue14785
# Upstream as of Python 3.3.0
#  Patch147: 00147-add-debug-malloc-stats.patch

# 00148 #
# Upstream as of Python 3.2.3:
#  Patch148: 00148-gdbm-1.9-magic-values.patch

# 00149 #
# Upstream as of Python 3.2.3:
#  Patch149: 00149-backport-issue11254-pycache-bytecompilation-fix.patch

# 00150 #
# temporarily disable rAssertAlmostEqual in test_cmath on PPC (bz #750811)
# caused by a glibc bug. This patch can be removed when we have a glibc with
# the patch mentioned here:
#   http://sourceware.org/bugzilla/show_bug.cgi?id=13472
Patch150: 00150-disable-rAssertAlmostEqual-cmath-on-ppc.patch

# 00151 #
# python.spec had:
#  Patch151: 00151-fork-deadlock.patch

# 00152 #
# Fix a regex in test_gdb so that it doesn't choke when gdb provides a full
# path to Python/bltinmodule.c:
# Committed upstream as 77824:abcd29c9a791 as part of fix for
# http://bugs.python.org/issue12605
#  Patch152: 00152-fix-test-gdb-regex.patch

# 00153 #
# Strip out lines of the form "warning: Unable to open ..." from gdb's stderr
# when running test_gdb.py; also cope with change to gdb in F17 onwards in
# which values are printed as "v@entry" rather than just "v":
# Not yet sent upstream
# Upstream as of 3.4.3
#  Patch153: 00153-fix-test_gdb-noise.patch

# 00154 #
# python3.spec on f15 has:
#  Patch154: 00154-skip-urllib-test-requiring-working-DNS.patch

# 00155 #
# Avoid allocating thunks in ctypes unless absolutely necessary, to avoid
# generating SELinux denials on "import ctypes" and "import uuid" when
# embedding Python within httpd (rhbz#814391)
Patch155: 00155-avoid-ctypes-thunks.patch

# 00156 #
# Recent builds of gdb will only auto-load scripts from certain safe
# locations.  Turn off this protection when running test_gdb in the selftest
# suite to ensure that it can load our -gdb.py script (rhbz#817072):
# Upsream as of 3.4.3
#  Patch156: 00156-gdb-autoload-safepath.patch

# 00157 #
# Update uid/gid handling throughout the standard library: uid_t and gid_t are
# unsigned 32-bit values, but existing code often passed them through C long
# values, which are signed 32-bit values on 32-bit architectures, leading to
# negative int objects for uid/gid values >= 2^31 on 32-bit architectures.
#
# Introduce _PyObject_FromUid/Gid to convert uid_t/gid_t values to python
# objects, using int objects where the value will fit (long objects otherwise),
# and _PyArg_ParseUid/Gid to convert int/long to uid_t/gid_t, with -1 allowed
# as a special case (since this is given special meaning by the chown syscall)
#
# Update standard library to use this throughout for uid/gid values, so that
# very large uid/gid values are round-trippable, and -1 remains usable.
# (rhbz#697470)
Patch157: 00157-uid-gid-overflows.patch

# 00158 #
# Upstream as of Python 3.3.1

# 00159 #
#  Patch159: 00159-correct-libdb-include-path.patch
# in python.spec
# TODO: python3 status?

# 00160 #
# Python 3.3 added os.SEEK_DATA and os.SEEK_HOLE, which may be present in the
# header files in the build chroot, but may not be supported in the running
# kernel, hence we disable this test in an rpm build.
# Adding these was upstream issue http://bugs.python.org/issue10142
# Not yet sent upstream
Patch160: 00160-disable-test_fs_holes-in-rpm-build.patch

# 00161 #
# (Was only needed for Python 3.3.0b1)

# 00162 #
# (Was only needed for Python 3.3.0b1)

# 00163 #
# Some tests within test_socket fail intermittently when run inside Koji;
# disable them using unittest._skipInRpmBuild
# Not yet sent upstream
Patch163: 00163-disable-parts-of-test_socket-in-rpm-build.patch

# 0164 #
# some tests in test._io interrupted_write-* fail on PPC (rhbz#846849)
# testChainingDescriptors  test in test_exceptions fails on PPc, too (rhbz#846849)
# disable those tests so that rebuilds on PPC can continue
Patch164: 00164-disable-interrupted_write-tests-on-ppc.patch

# 00165 #
# python.spec has:
#   Patch165: 00165-crypt-module-salt-backport.patch
# which is a backport from 3.3 and thus not relevant to "python3"

# 00166 #
#  Patch166: 00166-fix-fake-repr-in-gdb-hooks.patch
# in python.spec
# TODO: python3 status?

# 00167 #
#  Patch167: 00167-disable-stack-navigation-tests-when-optimized-in-test_gdb.patch
# in python.spec
# TODO: python3 status?

# 00168 #
#  Patch168: 00168-distutils-cflags.patch
# in python.spec
# TODO: python3 status?

# 00169 #
#  Patch169: 00169-avoid-implicit-usage-of-md5-in-multiprocessing.patch
# in python.spec
# TODO: python3 status?

# 00170 #
#  Patch170: 00170-gc-assertions.patch
# in python.spec
# TODO: python3 status?

# 00171 #
# python.spec had:
#  Patch171: 00171-raise-correct-exception-when-dev-urandom-is-missing.patch
# TODO: python3 status?

# 00172 #
# python.spec had:
#  Patch172: 00172-use-poll-for-multiprocessing-socket-connection.patch
# TODO: python3 status?

# 00173 #
# Workaround for ENOPROTOOPT seen in Koji withi test.support.bind_port()
# (rhbz#913732)
Patch173: 00173-workaround-ENOPROTOOPT-in-bind_port.patch

# 00174 #
#  Patch174: 00174-fix-for-usr-move.patch
# TODO: python3 status?

# 00175 #
# Upstream as of Python 3.3.2
#  Patch175: 00175-fix-configure-Wformat.patch

# 00176 #
# Fixed upstream as of Python 3.3.1
#  Patch176: 00176-upstream-issue16754-so-extension.patch

# 00177 #
# Fixed upstream as of Python 3.4.0.b2
#  Patch177: 00177-platform-unicode.patch

# 00178 #
# Don't duplicate various FLAGS in sysconfig values
# http://bugs.python.org/issue17679
# Does not affect python2 AFAICS (different sysconfig values initialization)
Patch178: 00178-dont-duplicate-flags-in-sysconfig.patch

# 00179 #
# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=951802
# Reported upstream in http://bugs.python.org/issue17737
# This patch basically looks at every frame and if it is somehow corrupted,
# it just stops printing the traceback - it doesn't fix the actual bug.
# This bug seems to only affect ARM.
# Doesn't seem to affect Python 2 AFAICS.
Patch179: 00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch

# 00180 #
# Enable building on ppc64p7
# Not appropriate for upstream, Fedora-specific naming
Patch180: 00180-python-add-support-for-ppc64p7.patch

# 00181 #
# python.spec has
#  Patch181: 00181-allow-arbitrary-timeout-in-condition-wait.patch
# Does not affect python3

# 00182 #
# Fixed upstream as of Python 3.3.2
#  Patch182: 00182-fix-test_gdb-test_threads.patch

# 00183 #
# Fixed upstream as of Python 3.4.0a4
#  Patch183: 00183-cve-2013-2099-fix-ssl-match_hostname-dos.patch

# 00184 #
# Fix for https://bugzilla.redhat.com/show_bug.cgi?id=979696
# Fixes build of ctypes against libffi with multilib wrapper
# Python recognizes ffi.h only if it contains "#define LIBFFI_H",
# but the wrapper doesn't contain that, which makes the build fail
# We patch this by also accepting "#define ffi_wrapper_h"
Patch184: 00184-ctypes-should-build-with-libffi-multilib-wrapper.patch

# 00185 #
# Fixed upstream as of Python 3.4.0a4
#  Patch185: 00185-CVE-2013-4238-hostname-check-bypass-in-SSL-module.patch

# 00186 #
# Fix for https://bugzilla.redhat.com/show_bug.cgi?id=1023607
# Previously, this fixed a problem where some *.py files were not being
# bytecompiled properly during build. This was result of py_compile.compile
# raising exception when trying to convert test file with bad encoding, and
# thus not continuing bytecompilation for other files.
# This was fixed upstream, but the test hasn't been merged yet, so we keep it
Patch186: 00186-dont-raise-from-py_compile.patch

# 00187 #
# Fixed upstream as of Python 3.4.0b1
#  Patch187: 00187-remove-pthread-atfork.patch

# 00188 #
# Downstream only patch that should be removed when we compile all guaranteed
# hashlib algorithms properly. The problem is this:
# - during tests, test_hashlib is imported and executed before test_lib2to3
# - if at least one hash function has failed, trying to import it triggers an
#   exception that is being caught and exception is logged:
#   http://hg.python.org/cpython/file/2de806c8b070/Lib/hashlib.py#l217
# - logging the exception makes logging module run basicConfig
# - when lib2to3 tests are run again, lib2to3 runs basicConfig again, which
#   doesn't do anything, because it was run previously
#   (logging.root.handlers != []), which means that the default setup
#   (most importantly logging level) is not overriden. That means that a test
#   relying on this will fail (test_filename_changing_on_output_single_dir)
Patch188: 00188-fix-lib2to3-tests-when-hashlib-doesnt-compile-properly.patch

# 00189 #
#
# Add the rewheel module, allowing to recreate wheels from already installed
# ones
# https://github.com/bkabrda/rewheel
%if 0%{with_rewheel}
Patch189: 00189-add-rewheel-module.patch
%endif

# 00190 #
#
# Fix tests with SQLite >= 3.8.4
# http://bugs.python.org/issue20901
# http://hg.python.org/cpython/rev/4d626a9df062
# FIXED UPSTREAM
# Patch190: 00190-fix-tests-with-sqlite-3.8.4.patch

# 00193
#
# Skip correct number of *.pyc file bytes in ModuleFinder.load_module
# rhbz#1060338
# http://bugs.python.org/issue20778
# FIXED UPSTREAM
# Patch193: 00193-skip-correct-num-of-pycfile-bytes-in-modulefinder.patch

# 00194
#
# Tests requiring SIGHUP to work don't work in Koji
# see rhbz#1088233
Patch194: temporarily-disable-tests-requiring-SIGHUP.patch

# 00195
#
# Don't declare Werror=declaration-after-statement for extension
# modules through setup.py
# http://bugs.python.org/issue21121
# FIXED UPSTREAM
# Patch195: 00195-dont-add-Werror-declaration-after-statement.patch

# 00203
#
# test_threading fails in koji dues to it's handling of signals
Patch203: 00203-disable-threading-test-koji.patch


# (New patches go here ^^^)
#
# When adding new patches to "python" and "python3" in Fedora 17 onwards,
# please try to keep the patch numbers in-sync between the two specfiles:
#
#   - use the same patch number across both specfiles for conceptually-equivalent
#     fixes, ideally with the same name
#
#   - when a patch is relevant to both specfiles, use the same introductory
#     comment in both specfiles where possible (to improve "diff" output when
#     comparing them)
#
#   - when a patch is only relevant for one of the two specfiles, leave a gap
#     in the patch numbering in the other specfile, adding a comment when
#     omitting a patch, both in the manifest section here, and in the "prep"
#     phase below
#
# Hopefully this will make it easier to ensure that all relevant fixes are
# applied to both versions.

# This is the generated patch to "configure"; see the description of
#   %{regenerate_autotooling_patch}
# above:
Patch5000: 05000-autotool-intermediates.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root

# ======================================================
# Additional metadata, and subpackages
# ======================================================

URL: http://www.python.org/

# See notes in bug 532118:
Provides: python(abi) = %{pybasever}

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%if 0%{with_rewheel}
Requires: python%{iusver}-setuptools
Requires: python%{iusver}-pip
%endif

%description
Python 3 is a new version of the language that is incompatible with the 2.x
line of releases. The language is mostly the same, but many details, especially
how built-in objects like dictionaries and strings work, have changed
considerably, and a lot of deprecated features have finally been removed.

%package libs
Summary:        Python 3 runtime libraries
Group:          Development/Libraries
#Requires:       %{name} = %{version}-%{release}

# expat 2.1.0 added the symbol XML_SetHashSalt without bumping SONAME.  Fedora
# requires this version to account for CVE-2012-0876.  However, that symbol was
# backported when the CVE was patched in el6, so I don't believe we need it for
# IUS.
#
# $ rpm -qf /lib64/libexpat.so.1
# expat-2.0.1-11.el6_2.x86_64
# $ strings /lib64/libexpat.so.1 | grep XML_SetHash
# XML_SetHashSalt
#
# https://rhn.redhat.com/errata/RHSA-2012-0731.html#Red Hat Enterprise Linux Server (v. 6)
# https://bugzilla.redhat.com/show_bug.cgi?id=821337
Requires: expat

%description libs
This package contains files used to embed Python 3 into applications.

%package devel
Summary: Libraries and header files needed for Python 3 development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: %{name} < %{version}-%{release}

%description devel
This package contains libraries and header files used to build applications 
with and native libraries for Python 3

%package tools
Summary: A collection of tools included with Python 3
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}

%description tools
This package contains several tools included with Python 3

%package tkinter
Summary: A GUI toolkit for Python 3
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

%package test
Summary: The test modules from the main python 3 package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

%description test
The test modules from the main %{name} package.
These are in a separate package to save space, as they are almost never used
in production.

You might want to install the %{name}-test package if you're developing
python 3 code that uses more than just unittest and/or test_support.py.

%if 0%{?with_debug_build}
%package debug
Summary: Debug version of the Python 3 runtime
Group: Applications/System

# The debug build is an all-in-one package version of the regular build, and
# shares the same .py/.pyc files and directories as the regular build.  Hence
# we depend on all of the subpackages of the regular build:
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-tkinter%{?_isa} = %{version}-%{release}
Requires: %{name}-tools%{?_isa} = %{version}-%{release}

%description debug
%{name}-debug provides a version of the Python 3 runtime with numerous debugging
features enabled, aimed at advanced Python users, such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python 3 build,
but is useful for tracking down reference-counting issues, and other bugs.

The bytecodes are unchanged, so that .pyc files are compatible between the two
versions of Python 3, but the debugging features mean that C/C++ extension
modules are ABI-incompatible with those built for the standard runtime.

It shares installation directories with the standard Python 3 runtime, so that
.py and .pyc files can be shared.  All compiled extension modules gain a "_d"
suffix ("foo_d.so" rather than "foo.so") so that each Python 3 implementation
can load its own extensions.
%endif # with_debug_build

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%setup -q -n Python-%{version}
chmod +x %{SOURCE1}

%if 0%{?with_systemtap}
# Provide an example of usage of the tapset:
cp -a %{SOURCE6} .
cp -a %{SOURCE7} .
%endif # with_systemtap

# Ensure that we're using the system copy of various libraries, rather than
# copies shipped by upstream in the tarball:
#   Remove embedded copy of expat:
rm -r Modules/expat || exit 1

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

#   Remove embedded copy of zlib:
rm -r Modules/zlib || exit 1

# Don't build upstream Python's implementation of these crypto algorithms;
# instead rely on _hashlib and OpenSSL.
#
# For example, in our builds hashlib.md5 is implemented within _hashlib via
# OpenSSL (and thus respects FIPS mode), and does not fall back to _md5
# TODO: there seems to be no OpenSSL support in Python for sha3 so far
# when it is there, also remove _sha3/ dir
for f in md5module.c sha1module.c sha256module.c sha512module.c; do
    rm Modules/$f
done

#
# Apply patches:
#
%patch1 -p1
# 3: upstream as of Python 3.3.1

%if 0%{?with_systemtap}
%patch55 -p1 -b .systemtap
%endif

%if "%{_lib}" == "lib64"
%patch102 -p1
%patch104 -p1
%endif


%patch111 -p1
# 112: not for python3
%patch113 -p1
# 00114: Upstream as of Python 3.4.0.b2

%patch125 -p1 -b .less-verbose-COUNT_ALLOCS

%ifarch ppc %{power64}
%patch131 -p1
%endif

%patch132 -p1
# 00133: not for python3
%patch134 -p1
%patch135 -p1
# 00136: not for python3
%patch137 -p1
# 00138: not for python3
%ifarch %{arm}
%patch139 -p1
%patch140 -p1
%endif
# 00140: not for python3
%patch141 -p1
%patch143 -p1 -b .tsc-on-ppc
# 00144: not for python3
# 00145: not for python3
%patch146 -p1
# 00147: upstream as of Python 3.3.0
# 00148: upstream as of Python 3.2.3
# 00149: upstream as of Python 3.2.3
%ifarch ppc %{power64}
%patch150 -p1
%endif
# 00151: not for python3
# 00152: upstream as of Python 3.3.0b2
# 00153: upstream as of Python 3.4.3
# 00154: not for this branch
%patch155 -p1
# 00156: upstream as of 3.4.3
%patch157 -p1
#00158: FIXME
#00159: FIXME
%patch160 -p1
# 00161: was only needed for Python 3.3.0b1
# 00162: was only needed for Python 3.3.0b1
%patch163 -p1
%ifarch ppc %{power64}
%patch164 -p1
%endif
#00165: TODO
#00166: TODO
#00167: TODO
#00168: TODO
#00169: TODO
#00170: TODO
#00171: TODO
#00172: TODO
%patch173 -p1
#00174: TODO
# 00175: upstream as of Python 3.3.2
# 00176: upstream as of Python 3.3.1
# 00177: upstream as of Python 3.4.0.b2
%patch178 -p1
%patch179 -p1
%patch180 -p1
# 00181: not for python3
# 00182: upstream as of Python 3.3.2
# 00183  upstream as of Python 3.4.0a4
%patch184  -p1
# 00185  upstream as of Python 3.4.0a4
%patch186 -p1
# 00187: upstream as of Python 3.4.0b1
%patch188 -p1

%if 0%{with_rewheel}
%patch189 -p1
%endif

# 00190: upstream as of Python 3.4.1
# 00193: upstream as of Python 3.4.1
%patch194 -p1
# 00195: upstream as of Python 3.4.2
%patch203 -p1

# Currently (2010-01-15), http://docs.python.org/library is for 2.6, and there
# are many differences between 2.6 and the Python 3 library.
#
# Fix up the URLs within pydoc to point at the documentation for this
# MAJOR.MINOR version:
#
sed --in-place \
    --expression="s|http://docs.python.org/library|http://docs.python.org/%{pybasever}/library|g" \
    Lib/pydoc.py || exit 1

%if ! 0%{regenerate_autotooling_patch}
# Normally we apply the patch to "configure"
# We don't apply the patch if we're working towards regenerating it
%patch5000 -p0 -b .autotool-intermediates
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
topdir=$(pwd)
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="`pkg-config --cflags-only-I libffi`"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
export CFLAGS="$CFLAGS `pkg-config --cflags openssl`"
export LDFLAGS="$RPM_LD_FLAGS `pkg-config --libs-only-L openssl`"

%if 0%{regenerate_autotooling_patch}
# If enabled, this code regenerates the patch to "configure", using a
# local copy of autoconf-2.65, then exits the build
#
# The following assumes that the copy is installed to ~/autoconf-2.65/bin
# as per these instructions:
#   http://bugs.python.org/issue7997

for f in pyconfig.h.in configure ; do
    cp $f $f.autotool-intermediates ;
done

# Rerun the autotools:
autoreconf

# Regenerate the patch:
gendiff . .autotool-intermediates > %{PATCH5000}


# Exit the build
exit 1
%endif

# Define a function, for how to perform a "build" of python for a given
# configuration:
BuildPython() {
  ConfName=$1
  BinaryName=$2
  SymlinkName=$3
  ExtraConfigArgs=$4
  PathFixWithThisBinary=$5
  MoreCFlags=$6

  ConfDir=build/$ConfName

  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir

  pushd $ConfDir

  # Use the freshly created "configure" script, but in the directory two above:
  %global _configure $topdir/configure

%configure \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=%{with_computed_gotos} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
%if 0%{?with_systemtap}
  --with-systemtap \
%endif
%if 0%{?with_valgrind}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

  # Set EXTRA_CFLAGS to our CFLAGS (rather than overriding OPT, as we've done
  # in the past).
  # This should fix a problem with --with-valgrind where it adds
  #   -DDYNAMIC_ANNOTATIONS_ENABLED=1
  # to OPT which must be passed to all compilation units in the build,
  # otherwise leading to linker errors, e.g.
  #    missing symbol AnnotateRWLockDestroy
  #
  # Invoke the build:
  make EXTRA_CFLAGS="$CFLAGS $MoreCFlags" %{?_smp_mflags}

  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfDir
}

# Use "BuildPython" to support building with different configurations:

%if 0%{?with_debug_build}
BuildPython debug \
  python-debug \
  python%{pybasever}-debug \
%ifarch %{ix86} x86_64 ppc %{power64}
  "--with-pydebug --with-tsc --with-count-allocs --with-call-profile --without-ensurepip" \
%else
  "--with-pydebug --with-count-allocs --with-call-profile --without-ensurepip" \
%endif
  false \
  -O1
%endif # with_debug_build

BuildPython optimized \
  python \
  python%{pybasever} \
  "--without-ensurepip" \
  true

# ======================================================
# Installing the built code:
# ======================================================

%install
topdir=$(pwd)
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}

InstallPython() {

  ConfName=$1	      
  PyInstSoName=$2
  MoreCFlags=$3

  ConfDir=build/$ConfName

  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir

  pushd $ConfDir

make install DESTDIR=%{buildroot} INSTALL="install -p" EXTRA_CFLAGS="$MoreCFlags"

  popd

  # We install a collection of hooks for gdb that make it easier to debug
  # executables linked against libpython3* (such as /usr/bin/python3 itself)
  #
  # These hooks are implemented in Python itself (though they are for the version
  # of python that gdb is linked with, in this case Python 2.7)
  #
  # gdb-archer looks for them in the same path as the ELF file, with a -gdb.py suffix.
  # We put them in the debuginfo package by installing them to e.g.:
  #  /usr/lib/debug/usr/lib/libpython3.2.so.1.0.debug-gdb.py
  #
  # See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
  # information
  #
  # Copy up the gdb hooks into place; the python file will be autoloaded by gdb
  # when visiting libpython.so, provided that the python file is installed to the
  # same path as the library (or its .debug file) plus a "-gdb.py" suffix, e.g:
  #  /usr/lib/debug/usr/lib64/libpython3.2.so.1.0.debug-gdb.py
  # (note that the debug path is /usr/lib/debug for both 32/64 bit)
  #
  # Initially I tried:
  #  /usr/lib/libpython3.1.so.1.0-gdb.py
  # but doing so generated noise when ldconfig was rerun (rhbz:562980)
  #
%if 0%{?with_gdb_hooks}
  DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
  PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName.debug-gdb.py

  mkdir -p %{buildroot}$DirHoldingGdbPy
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
%endif # with_gdb_hooks

  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

# Use "InstallPython" to support building with different configurations:

# Install the "debug" build first, so that we can move some files aside
%if 0%{?with_debug_build}
InstallPython debug \
  %{py_INSTSONAME_debug} \
  -O1
%endif # with_debug_build

# Now the optimized build:
InstallPython optimized \
  %{py_INSTSONAME_optimized}

install -d -m 0755 ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/__pycache__

mv ${RPM_BUILD_ROOT}%{_bindir}/2to3 ${RPM_BUILD_ROOT}%{_bindir}/python3-2to3

# Development tools
install -m755 -d ${RPM_BUILD_ROOT}%{pylibdir}/Tools
install Tools/README ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/freeze ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/i18n ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/pynche ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/scripts ${RPM_BUILD_ROOT}%{pylibdir}/Tools/

# Documentation tools
install -m755 -d %{buildroot}%{pylibdir}/Doc
cp -ar Doc/tools %{buildroot}%{pylibdir}/Doc/

# Demo scripts
cp -ar Tools/demo %{buildroot}%{pylibdir}/Tools/

# Fix for bug #136654
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au

%if "%{_lib}" == "lib64"
install -d -m 0755 %{buildroot}/usr/lib/python%{pybasever}/site-packages/__pycache__
%endif

# Make python3-devel multilib-ready (bug #192747, #139911)
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h

%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64
%global _pyconfig_h %{_pyconfig64_h}
%else
%global _pyconfig_h %{_pyconfig32_h}
%endif

# ABIFLAGS, LDVERSION and SOABI are in the upstream Makefile
%global ABIFLAGS_optimized m
%global ABIFLAGS_debug     dm

%global LDVERSION_optimized %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug     %{pybasever}%{ABIFLAGS_debug}

%global SOABI_optimized cpython-%{pyshortver}%{ABIFLAGS_optimized}
%global SOABI_debug     cpython-%{pyshortver}%{ABIFLAGS_debug}

%if 0%{?with_debug_build}
%global PyIncludeDirs python%{LDVERSION_optimized} python%{LDVERSION_debug}

%else
%global PyIncludeDirs python%{LDVERSION_optimized}
%endif

for PyIncludeDir in %{PyIncludeDirs} ; do
  mv %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h \
     %{buildroot}%{_includedir}/$PyIncludeDir/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
done

# Fix for bug 201434: make sure distutils looks at the right pyconfig.h file
# Similar for sysconfig: sysconfig.get_config_h_filename tries to locate
# pyconfig.h so it can be parsed, and needs to do this at runtime in site.py
# when python starts up (bug 653058)
#
# Split this out so it goes directly to the pyconfig-32.h/pyconfig-64.h
# variants:
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

# Switch all shebangs to refer to the specific Python version.
LD_LIBRARY_PATH=./build/optimized ./build/optimized/python \
  Tools/scripts/pathfix.py \
  -i "%{_bindir}/python%{pybasever}" \
  %{buildroot}

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# .xpm and .xbm files should not be executable:
find %{buildroot} \
  \( -name \*.xbm -o -name \*.xpm -o -name \*.xpm.1 \) \
  -exec chmod a-x {} \;

# Remove executable flag from files that shouldn't have it:
chmod a-x \
  %{buildroot}%{pylibdir}/distutils/tests/Setup.sample \
  %{buildroot}%{pylibdir}/Tools/README

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;

# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;
rm -f %{buildroot}%{pylibdir}/LICENSE.txt
# Junk, no point in putting in -test sub-pkg
rm -f ${RPM_BUILD_ROOT}/%{pylibdir}/idlelib/testcode.py*

# Get rid of stray patch file from buildroot:
rm -f %{buildroot}%{pylibdir}/test/test_imp.py.apply-our-changes-to-expected-shebang # from patch 4

# Fix end-of-line encodings:
find %{buildroot}/ -name \*.py -exec sed -i 's/\r//' {} \;

# Fix an encoding:
iconv -f iso8859-1 -t utf-8 %{buildroot}/%{pylibdir}/Demo/rpc/README > README.conv && mv -f README.conv %{buildroot}/%{pylibdir}/Demo/rpc/README

# Note that 
#  %{pylibdir}/Demo/distutils/test2to3/setup.py
# is in iso-8859-1 encoding, and that this is deliberate; this is test data
# for the 2to3 tool, and one of the functions of the 2to3 tool is to fixup
# character encodings within python source code

# Do bytecompilation with the newly installed interpreter.
# This is similar to the script in macros.pybytecompile
# compile *.pyo
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2]) for f in sys.argv[1:]]' || :
# compile *.pyc
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2], optimize=0) for f in sys.argv[1:]]' || :

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} \
    -perm 555 -exec chmod 755 {} \;

# Install macros for rpm:
install -Dm0644 %{SOURCE2} %{buildroot}%{_macrosdir}/macros.python%{pybasever}
install -Dm0644 %{SOURCE3} %{buildroot}%{_macrosdir}/macros.pybytecompile%{pybasever}

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so (bug 539917)
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)

# Ensure that the debug modules are linked against the debug libpython, and
# likewise for the optimized modules and libpython:
for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *.%{SOABI_debug})
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)
            
        ;;
    *.%{SOABI_optimized})
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_debug} ; exit 1)
        ;;
    esac
done

# Create "/usr/bin/python3-debug", a symlink to the python3 debug binary, to
# avoid the user having to know the precise version and ABI flags.  (see
# e.g. rhbz#676748):
%if 0%{?with_debug_build}
ln -s \
  %{_bindir}/python%{LDVERSION_debug} \
  %{buildroot}%{_bindir}/python3-debug
%endif

#
# Systemtap hooks:
#
%if 0%{?with_systemtap}
# Install a tapset for this libpython into tapsetdir, fixing up the path to the
# library:
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64
%global libpython_stp_optimized libpython%{pybasever}-64.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-64.stp
%else
%global libpython_stp_optimized libpython%{pybasever}-32.stp
%global libpython_stp_debug     libpython%{pybasever}-debug-32.stp
%endif

sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_optimized}|" \
   %{_sourcedir}/libpython.stp \
   > %{buildroot}%{tapsetdir}/%{libpython_stp_optimized}

%if 0%{?with_debug_build}
# In Python 3, python3 and python3-debug don't point to the same binary,
# so we have to replace "python3" with "python3-debug" to get systemtap
# working with debug build
sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME_debug}|" \
   -e 's|"python3"|"python3-debug"|' \
   %{_sourcedir}/libpython.stp \
   > %{buildroot}%{tapsetdir}/%{libpython_stp_debug}
%endif # with_debug_build

%endif # with_systemtap

# Rename the script that differs on different arches to arch specific name
mv %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-{,`uname -m`-}config
echo -e '#!/bin/sh\nexec `dirname $0`/python%{LDVERSION_optimized}-`uname -m`-config "$@"' > \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
echo '[ $? -eq 127 ] && echo "Could not find python%{LDVERSION_optimized}-`uname -m`-config. Look around to see available arches." >&2' >> \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
  chmod +x %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config

# ======================================================
# Running the upstream test suite
# ======================================================

%check

# first of all, check timestamps of bytecode files
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} %{SOURCE8}


topdir=$(pwd)
CheckPython() {
  ConfName=$1	      
  ConfDir=$(pwd)/build/$ConfName

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  # Run the upstream test suite, setting "WITHIN_PYTHON_RPM_BUILD" so that the
  # our non-standard decorators take effect on the relevant tests:
  #   @unittest._skipInRpmBuild(reason)
  #   @unittest._expectedFailureInRpmBuild
  #
  # test_readline.TestReadline fails on el < 7
  # http://bugs.python.org/issue19884
  # http://bugs.python.org/issue22773
  WITHIN_PYTHON_RPM_BUILD= \
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    %if 0%{?with_rewheel}
    -x test_distutils \
    -x test_venv \
    %endif
    %if 0%{?rhel} < 7
    -x test_readline \
    %endif
    --verbose --findleaks

  echo FINISHED: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

}

%if 0%{run_selftest_suite}

# Check each of the configurations:
%if 0%{?with_debug_build}
CheckPython debug
%endif # with_debug_build
CheckPython optimized

%endif # run_selftest_suite


# ======================================================
# Cleaning up
# ======================================================

%clean
rm -fr %{buildroot}


# ======================================================
# Scriptlets
# ======================================================

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig



%files
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python3
%{_bindir}/python%{pybasever}
%{_bindir}/python%{pybasever}m
%{_bindir}/pyvenv
%{_bindir}/pyvenv-%{pybasever}
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/_bisect.%{SOABI_optimized}.so
%{dynload_dir}/_bz2.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_cn.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_hk.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_jp.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_kr.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_tw.%{SOABI_optimized}.so
%{dynload_dir}/_crypt.%{SOABI_optimized}.so
%{dynload_dir}/_csv.%{SOABI_optimized}.so
%{dynload_dir}/_ctypes.%{SOABI_optimized}.so
%{dynload_dir}/_curses.%{SOABI_optimized}.so
%{dynload_dir}/_curses_panel.%{SOABI_optimized}.so
%{dynload_dir}/_dbm.%{SOABI_optimized}.so
%{dynload_dir}/_decimal.%{SOABI_optimized}.so
%{dynload_dir}/_elementtree.%{SOABI_optimized}.so
%if %{with_gdbm}
%{dynload_dir}/_gdbm.%{SOABI_optimized}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_optimized}.so
%{dynload_dir}/_heapq.%{SOABI_optimized}.so
%{dynload_dir}/_json.%{SOABI_optimized}.so
%{dynload_dir}/_lsprof.%{SOABI_optimized}.so
%{dynload_dir}/_lzma.%{SOABI_optimized}.so
%{dynload_dir}/_multibytecodec.%{SOABI_optimized}.so
%{dynload_dir}/_multiprocessing.%{SOABI_optimized}.so
%{dynload_dir}/_opcode.%{SOABI_optimized}.so
%{dynload_dir}/_pickle.%{SOABI_optimized}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_optimized}.so
%{dynload_dir}/_random.%{SOABI_optimized}.so
%{dynload_dir}/_socket.%{SOABI_optimized}.so
%{dynload_dir}/_sqlite3.%{SOABI_optimized}.so
%{dynload_dir}/_ssl.%{SOABI_optimized}.so
%{dynload_dir}/_struct.%{SOABI_optimized}.so
%{dynload_dir}/array.%{SOABI_optimized}.so
%{dynload_dir}/audioop.%{SOABI_optimized}.so
%{dynload_dir}/binascii.%{SOABI_optimized}.so
%{dynload_dir}/cmath.%{SOABI_optimized}.so
%{dynload_dir}/_datetime.%{SOABI_optimized}.so
%{dynload_dir}/fcntl.%{SOABI_optimized}.so
%{dynload_dir}/grp.%{SOABI_optimized}.so
%{dynload_dir}/math.%{SOABI_optimized}.so
%{dynload_dir}/mmap.%{SOABI_optimized}.so
%{dynload_dir}/nis.%{SOABI_optimized}.so
%{dynload_dir}/ossaudiodev.%{SOABI_optimized}.so
%{dynload_dir}/parser.%{SOABI_optimized}.so
%{dynload_dir}/pyexpat.%{SOABI_optimized}.so
%{dynload_dir}/readline.%{SOABI_optimized}.so
%{dynload_dir}/resource.%{SOABI_optimized}.so
%{dynload_dir}/select.%{SOABI_optimized}.so
%{dynload_dir}/spwd.%{SOABI_optimized}.so
%{dynload_dir}/syslog.%{SOABI_optimized}.so
%{dynload_dir}/termios.%{SOABI_optimized}.so
%{dynload_dir}/time.%{SOABI_optimized}.so
%{dynload_dir}/unicodedata.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited.%{SOABI_optimized}.so
%{dynload_dir}/zlib.%{SOABI_optimized}.so

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README
%{pylibdir}/*.py
%dir %{pylibdir}/__pycache__/
%{pylibdir}/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/asyncio/
%dir %{pylibdir}/asyncio/__pycache__/
%{pylibdir}/asyncio/*.py
%{pylibdir}/asyncio/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/collections/
%dir %{pylibdir}/collections/__pycache__/
%{pylibdir}/collections/*.py
%{pylibdir}/collections/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/
%dir %{pylibdir}/concurrent/__pycache__/
%{pylibdir}/concurrent/*.py
%{pylibdir}/concurrent/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/futures/
%dir %{pylibdir}/concurrent/futures/__pycache__/
%{pylibdir}/concurrent/futures/*.py
%{pylibdir}/concurrent/futures/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/ctypes/
%dir %{pylibdir}/ctypes/__pycache__/
%{pylibdir}/ctypes/*.py
%{pylibdir}/ctypes/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/ctypes/macholib

%{pylibdir}/curses

%dir %{pylibdir}/dbm/
%dir %{pylibdir}/dbm/__pycache__/
%{pylibdir}/dbm/*.py
%{pylibdir}/dbm/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/distutils/
%dir %{pylibdir}/distutils/__pycache__/
%{pylibdir}/distutils/*.py
%{pylibdir}/distutils/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command

%dir %{pylibdir}/email/
%dir %{pylibdir}/email/__pycache__/
%{pylibdir}/email/*.py
%{pylibdir}/email/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/email/mime
%doc %{pylibdir}/email/architecture.rst

%{pylibdir}/encodings

%dir %{pylibdir}/ensurepip/
%dir %{pylibdir}/ensurepip/__pycache__/
%{pylibdir}/ensurepip/*.py
%{pylibdir}/ensurepip/__pycache__/*%{bytecode_suffixes}
%if 0%{?with_rewheel}
%exclude %{pylibdir}/ensurepip/_bundled
%endif

%if 0%{?with_rewheel}
%dir %{pylibdir}/ensurepip/rewheel/
%dir %{pylibdir}/ensurepip/rewheel/__pycache__/
%{pylibdir}/ensurepip/rewheel/*.py
%{pylibdir}/ensurepip/rewheel/__pycache__/*%{bytecode_suffixes}
%endif

%{pylibdir}/html
%{pylibdir}/http
%{pylibdir}/idlelib

%dir %{pylibdir}/importlib/
%dir %{pylibdir}/importlib/__pycache__/
%{pylibdir}/importlib/*.py
%{pylibdir}/importlib/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/json/
%dir %{pylibdir}/json/__pycache__/
%{pylibdir}/json/*.py
%{pylibdir}/json/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/lib2to3
%exclude %{pylibdir}/lib2to3/tests
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%{pylibdir}/plat-linux
%{pylibdir}/pydoc_data

%dir %{pylibdir}/sqlite3/
%dir %{pylibdir}/sqlite3/__pycache__/
%{pylibdir}/sqlite3/*.py
%{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/test/
%dir %{pylibdir}/test/__pycache__/
%dir %{pylibdir}/test/support/
%dir %{pylibdir}/test/support/__pycache__/
%{pylibdir}/test/__init__.py
%{pylibdir}/test/__pycache__/__init__%{bytecode_suffixes}
%{pylibdir}/test/support/__init__.py
%{pylibdir}/test/support/__pycache__/__init__%{bytecode_suffixes}

%exclude %{pylibdir}/turtle.py
%exclude %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

%dir %{pylibdir}/unittest/
%dir %{pylibdir}/unittest/__pycache__/
%{pylibdir}/unittest/*.py
%{pylibdir}/unittest/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/urllib

%dir %{pylibdir}/venv/
%dir %{pylibdir}/venv/__pycache__/
%{pylibdir}/venv/*.py
%{pylibdir}/venv/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/venv/scripts

%{pylibdir}/wsgiref
%{pylibdir}/xml
%{pylibdir}/xmlrpc

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/__pycache__/
%endif

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config-%{LDVERSION_optimized}/
%{pylibdir}/config-%{LDVERSION_optimized}/Makefile
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}
%{_libdir}/libpython3.so
%if 0%{?with_systemtap}
%{tapsetdir}/%{libpython_stp_optimized}
%doc systemtap-example.stp pyfuntop.stp
%endif

%files devel
%defattr(-,root,root)
%{pylibdir}/config-%{LDVERSION_optimized}/*
%exclude %{pylibdir}/config-%{LDVERSION_optimized}/Makefile
%{_includedir}/python%{LDVERSION_optimized}/*.h
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_bindir}/python3-config
%{_bindir}/python%{pybasever}-config
%{_bindir}/python%{LDVERSION_optimized}-config
%{_bindir}/python%{LDVERSION_optimized}-*-config
%{_libdir}/libpython%{LDVERSION_optimized}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python3.pc
%{_macrosdir}/macros.python%{pybasever}
%{_macrosdir}/macros.pybytecompile%{pybasever}

%files tools
%defattr(-,root,root,755)
%{_bindir}/python3-2to3
%{_bindir}/2to3-%{pybasever}
%{_bindir}/idle*
%{pylibdir}/Tools
%doc %{pylibdir}/Doc

%files tkinter
%defattr(-,root,root,755)
%{pylibdir}/tkinter
%exclude %{pylibdir}/tkinter/test
%{dynload_dir}/_tkinter.%{SOABI_optimized}.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}

%files test
%defattr(-, root, root)
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test
%{dynload_dir}/_ctypes_test.%{SOABI_optimized}.so
%{dynload_dir}/_testbuffer.%{SOABI_optimized}.so
%{dynload_dir}/_testcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_optimized}.so
%{pylibdir}/lib2to3/tests
%{pylibdir}/tkinter/test
%{pylibdir}/unittest/test


# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if 0%{?with_debug_build}
%files debug
%defattr(-,root,root,-)

# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_debug}
%{_bindir}/python3-debug

# Analog of the -libs subpackage's files:
# ...with debug builds of the built-in "extension" modules:
%{dynload_dir}/_bisect.%{SOABI_debug}.so
%{dynload_dir}/_bz2.%{SOABI_debug}.so
%{dynload_dir}/_codecs_cn.%{SOABI_debug}.so
%{dynload_dir}/_codecs_hk.%{SOABI_debug}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_debug}.so
%{dynload_dir}/_codecs_jp.%{SOABI_debug}.so
%{dynload_dir}/_codecs_kr.%{SOABI_debug}.so
%{dynload_dir}/_codecs_tw.%{SOABI_debug}.so
%{dynload_dir}/_crypt.%{SOABI_debug}.so
%{dynload_dir}/_csv.%{SOABI_debug}.so
%{dynload_dir}/_ctypes.%{SOABI_debug}.so
%{dynload_dir}/_curses.%{SOABI_debug}.so
%{dynload_dir}/_curses_panel.%{SOABI_debug}.so
%{dynload_dir}/_dbm.%{SOABI_debug}.so
%{dynload_dir}/_decimal.%{SOABI_debug}.so
%{dynload_dir}/_elementtree.%{SOABI_debug}.so
%if %{with_gdbm}
%{dynload_dir}/_gdbm.%{SOABI_debug}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_debug}.so
%{dynload_dir}/_heapq.%{SOABI_debug}.so
%{dynload_dir}/_json.%{SOABI_debug}.so
%{dynload_dir}/_lsprof.%{SOABI_debug}.so
%{dynload_dir}/_lzma.%{SOABI_debug}.so
%{dynload_dir}/_multibytecodec.%{SOABI_debug}.so
%{dynload_dir}/_multiprocessing.%{SOABI_debug}.so
%{dynload_dir}/_opcode.%{SOABI_debug}.so
%{dynload_dir}/_pickle.%{SOABI_debug}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_debug}.so
%{dynload_dir}/_random.%{SOABI_debug}.so
%{dynload_dir}/_socket.%{SOABI_debug}.so
%{dynload_dir}/_sqlite3.%{SOABI_debug}.so
%{dynload_dir}/_ssl.%{SOABI_debug}.so
%{dynload_dir}/_struct.%{SOABI_debug}.so
%{dynload_dir}/array.%{SOABI_debug}.so
%{dynload_dir}/audioop.%{SOABI_debug}.so
%{dynload_dir}/binascii.%{SOABI_debug}.so
%{dynload_dir}/cmath.%{SOABI_debug}.so
%{dynload_dir}/_datetime.%{SOABI_debug}.so
%{dynload_dir}/fcntl.%{SOABI_debug}.so
%{dynload_dir}/grp.%{SOABI_debug}.so
%{dynload_dir}/math.%{SOABI_debug}.so
%{dynload_dir}/mmap.%{SOABI_debug}.so
%{dynload_dir}/nis.%{SOABI_debug}.so
%{dynload_dir}/ossaudiodev.%{SOABI_debug}.so
%{dynload_dir}/parser.%{SOABI_debug}.so
%{dynload_dir}/pyexpat.%{SOABI_debug}.so
%{dynload_dir}/readline.%{SOABI_debug}.so
%{dynload_dir}/resource.%{SOABI_debug}.so
%{dynload_dir}/select.%{SOABI_debug}.so
%{dynload_dir}/spwd.%{SOABI_debug}.so
%{dynload_dir}/syslog.%{SOABI_debug}.so
%{dynload_dir}/termios.%{SOABI_debug}.so
%{dynload_dir}/time.%{SOABI_debug}.so
%{dynload_dir}/unicodedata.%{SOABI_debug}.so
%{dynload_dir}/zlib.%{SOABI_debug}.so

# No need to split things out the "Makefile" and the config-32/64.h file as we
# do for the regular build above (bug 531901), since they're all in one package
# now; they're listed below, under "-devel":

%{_libdir}/%{py_INSTSONAME_debug}
%if 0%{?with_systemtap}
%{tapsetdir}/%{libpython_stp_debug}
%endif

# Analog of the -devel subpackage's files:
%{pylibdir}/config-%{LDVERSION_debug}
%{_includedir}/python%{LDVERSION_debug}
%{_bindir}/python%{LDVERSION_debug}-config
%{_libdir}/libpython%{LDVERSION_debug}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc

# Analog of the -tools subpackage's files:
#  None for now; we could build precanned versions that have the appropriate
# shebang if needed

# Analog  of the tkinter subpackage's files:
%{dynload_dir}/_tkinter.%{SOABI_debug}.so

# Analog  of the -test subpackage's files:
%{dynload_dir}/_ctypes_test.%{SOABI_debug}.so
%{dynload_dir}/_testbuffer.%{SOABI_debug}.so
%{dynload_dir}/_testcapi.%{SOABI_debug}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_debug}.so

%endif # with_debug_build

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from
# ldconfig (rhbz:562980).
# 
# The /usr/lib/rpm/redhat/macros defines %__debug_package to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
# 
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py 
# payload file would be unpackaged)


# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Fri May 22 2015 Carl George <carl.george@rackspace.com> - 3.4.3-2.ius
- Remove patch153 and patch156
- Skip test_readline with regrtest flag instead of with a patch
- Skip test_distutils and test_venv when using rewheel
- Switch to Fedora patches for skipping SIGHUP and threading tests
- Use same build flags as Fedora

* Wed Feb 25 2015 Carl George <carl.george@rackspace.com> - 3.4.3-1.ius
- Latest upstream
- Refresh patch137, patch156
- Refresh patch153 (partially merged upstream)
- Refresh patch196 (upstream tried to fix but failed)
- Add patch197

* Wed Oct 08 2014 Ben Harper <ben.harper@rackspace.com> - 3.4.2-1.ius
- update to lastest
- disable Patch195, patched upstream
- removed %files %{pylibdir}/turtledemo/*.txt
- update Patch156
- add Patch196

* Mon Aug 18 2014 Carl George <carl.george@rackspace.com> - 3.4.1-4.ius
- Update the rewheel module to be unicode safe, remove work around

* Wed Aug 13 2014 Carl George <carl.george@rackspace.com> - 3.4.1-3.ius
- Install macros in _rpmconfigdir on el7
- Point __os_install_post to correct brp-* files on el7
- In config script, use uname -m to write the arch
- Enable rewheel
- Work around unicode failures in test suite by setting LC_CTYPE=en_US.utf8

* Wed Jun 18 2014 Carl George <carl.george@rackspace.com> - 3.4.1-2.ius
- Macros in %{_rpmconfigdir}/macros.d are not automatically loaded, move them back to %{_sysconfdir}/rpm

* Thu May 29 2014 Carl George <carl.george@rackspace.com> - 3.4.1-1.ius
- Add conflicts for other IUS python3 packages
- Install macros in _rpmconfigdir
- Add macro %%python3_version_nodots
- Enable loading sqlite extensions (rhbz#1066938)
- Add iusver macro, and use it
- Don't add Werror=declaration-after-statement for extension modules through setup.py (PyBT#21121)
- Latest upstream source, patches 190 and 193 merged upstream
- Fix multilib dependencies (rhbz#1091815)
- Rename python3.Xm-config script to arch specific (rhbz#1091815)

* Wed Apr 16 2014 Ben Harper <ben.harper@rackspace.com> - 3.4.0-2.ius
- porting from koji SRPM, http://kojipkgs.fedoraproject.org//work/tasks/9935/6739935/python3-3.4.0-1.fc21.src.rpm

* Tue Apr 15 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-1
- Update to Python 3.4 final
- Add patch adding the rewheel module
- Merge patches from master

* Wed Jan 08 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.b2
- Update to Python 3.4 beta 2.
- Refreshed patches: 55 (systemtap), 146 (hashlib-fips), 154 (test_gdb noise)
- Dropped patches: 114 (statvfs constants), 177 (platform unicode)

* Mon Nov 25 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.b1
- Update to Python 3.4 beta 1.
- Refreshed patches: 102 (lib64), 111 (no static lib), 125 (less verbose COUNT
ALLOCS), 141 (fix COUNT_ALLOCS in test_module), 146 (hashlib fips),
157 (UID+GID overflows), 173 (ENOPROTOOPT in bind_port)
- Removed patch 00187 (remove pthread atfork; upstreamed)

* Mon Nov 04 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.a4
- Update to Python 3.4 alpha 4.
- Refreshed patches: 55 (systemtap), 102 (lib64), 111 (no static lib),
114 (statvfs flags), 132 (unittest rpmbuild hooks), 134 (fix COUNT_ALLOCS in
test_sys), 143 (tsc on ppc64), 146 (hashlib fips), 153 (test gdb noise),
157 (UID+GID overflows), 173 (ENOPROTOOPT in bind_port), 186 (dont raise
from py_compile)
- Removed patches: 129 (test_subprocess nonreadable dir - no longer fails in
Koji), 142 (the mock issue that caused this is fixed)
- Added patch 187 (remove thread atfork) - will be in next version
- Refreshed script for checking pyc and pyo timestamps with new ignored files.
- The fips patch is disabled for now until upstream makes a final decision
what to do with sha3 implementation for 3.4.0.

* Wed Oct 30 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-7
- Bytecompile all *.py files properly during build (rhbz#1023607)

* Fri Aug 23 2013 Matej Stuchlik <mstuchli@redhat.com> - 3.3.2-6
- Added fix for CVE-2013-4238 (rhbz#996399)

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> - 3.3.2-5
- fix up indentation in arm patch

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> - 3.3.2-4
- disable a test that fails on arm
- enable valgrind support on arm arches

* Tue Jul 02 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-3
- Fix build with libffi containing multilib wrapper for ffi.h (rhbz#979696).

* Mon May 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-2
- Add patch for CVE-2013-2099 (rhbz#963261).

* Thu May 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-1
- Updated to Python 3.3.2.
- Refreshed patches: 153 (gdb test noise)
- Dropped patches: 175 (configure -Wformat, fixed upstream), 182 (gdb
test threads)
- Synced patch numbers with python.spec.

* Thu May  9 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.1-4
- fix test.test_gdb.PyBtTests.test_threads on ppc64 (patch 181; rhbz#960010)

* Thu May 02 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-3
- Add patch that enables building on ppc64p7 (replace the sed, so that
we get consistent with python2 spec and it's more obvious that we're doing it.

* Wed Apr 24 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-2
- Add fix for gdb tests failing on arm, rhbz#951802.

* Tue Apr 09 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-1
- Updated to Python 3.3.1.
- Refreshed patches: 55 (systemtap), 111 (no static lib), 146 (hashlib fips),
153 (fix test_gdb noise), 157 (uid, gid overflow - fixed upstream, just
keeping few more downstream tests)
- Removed patches: 3 (audiotest.au made it to upstream tarball)
- Removed workaround for http://bugs.python.org/issue14774, discussed in
http://bugs.python.org/issue15298 and fixed in revision 24d52d3060e8.

* Mon Mar 25 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-10
- fix gcc 4.8 incompatibility (rhbz#927358); regenerate autotool intermediates

* Mon Mar 25 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-9
- renumber patches to keep them in sync with python.spec

* Fri Mar 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-8
- Fix error in platform.platform() when non-ascii byte strings are decoded to
  unicode (rhbz#922149)

* Thu Mar 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-7
- Fix up shared library extension (rhbz#889784)

* Thu Mar 07 2013 Karsten Hopp <karsten@redhat.com> 3.3.0-6
- add ppc64p7 build target, optimized for Power7

* Mon Mar  4 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-5
- add workaround for ENOPROTOOPT seen running selftests in Koji
(rhbz#913732)

* Mon Mar  4 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-4
- remove config flag from /etc/rpm/macros.{python3|pybytecompile}

* Mon Feb 11 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-3
- add aarch64 (rhbz#909783)

* Thu Nov 29 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-2
- add BR on bluez-libs-devel (rhbz#879720)

* Sat Sep 29 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-1
- 3.3.0rc3 -> 3.3.0; drop alphatag

* Mon Sep 24 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.6.rc3
- 3.3.0rc2 -> 3.3.0rc3

* Mon Sep 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.5.rc2
- 3.3.0rc1 -> 3.3.0rc2; refresh patch 55

* Mon Aug 27 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.4.rc1
- 3.3.0b2 -> 3.3.0rc1; refresh patches 3, 55

* Mon Aug 13 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.3.b2
- 3.3b1 -> 3.3b2; drop upstreamed patch 152; refresh patches 3, 102, 111,
134, 153, 160; regenenerate autotools patch; rework systemtap patch to work
correctly when LANG=C (patch 55); importlib.test was moved to
test.test_importlib upstream

* Mon Aug 13 2012 Karsten Hopp <karsten@redhat.com> 3.3.0-0.2.b1
- disable some failing checks on PPC* (rhbz#846849)

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.1.b1
- 3.2 -> 3.3: https://fedoraproject.org/wiki/Features/Python_3.3
- 3.3.0b1: refresh patches 3, 55, 102, 111, 113, 114, 134, 157; drop upstream
patch 147; regenenerate autotools patch; drop "--with-wide-unicode" from
configure (PEP 393); "plat-linux2" -> "plat-linux" (upstream issue 12326);
"bz2" -> "_bz2" and "crypt" -> "_crypt"; egg-info files are no longer shipped
for stdlib (upstream issues 10645 and 12218); email/test moved to
test/test_email; add /usr/bin/pyvenv[-3.3] and venv module (PEP 405); add
_decimal and _lzma modules; make collections modules explicit in payload again
(upstream issue 11085); add _testbuffer module to tests subpackage (added in
upstream commit 3f9b3b6f7ff0); fix test failures (patches 160 and 161);
workaround erroneously shared _sysconfigdata.py upstream issue #14774; fix
distutils.sysconfig traceback (patch 162); add BuildRequires: xz-devel (for
_lzma module); skip some tests within test_socket (patch 163)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.1.b1

* Fri Jun 22 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-10
- use macro for power64 (rhbz#834653)

* Mon Jun 18 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-9
- fix missing include in uid/gid handling patch (patch 157; rhbz#830405)

* Wed May 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.3-8
- fix tapset for debug build

* Tue May 15 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-7
- update uid/gid handling to avoid int overflows seen with uid/gid
values >= 2^31 on 32-bit architectures (patch 157; rhbz#697470)

* Fri May  4 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-6
- renumber autotools patch from 300 to 5000
- specfile cleanups

* Mon Apr 30 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-5
- fix test_gdb.py (patch 156; rhbz#817072)

* Fri Apr 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-4
- avoid allocating thunks in ctypes unless absolutely necessary, to avoid
generating SELinux denials on "import ctypes" and "import uuid" when embedding
Python within httpd (patch 155; rhbz#814391)

* Fri Apr 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-3
- add explicit version requirements on expat to avoid linkage problems with
XML_SetHashSalt

* Thu Apr 12 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-2
- fix test_gdb (patch 153)

* Wed Apr 11 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-1
- 3.2.3; refresh patch 102 (lib64); drop upstream patches 148 (gdbm magic
values), 149 (__pycache__ fix); add patch 152 (test_gdb regex)

* Thu Feb  9 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-13
- use newly installed python for byte compiling (now for real)

* Sun Feb  5 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-12
- use newly installed python for byte compiling (#787498)

* Wed Jan  4 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.2.2-11
- Build with $RPM_LD_FLAGS (#756863).
- Use xz-compressed source tarball.

* Wed Dec 07 2011 Karsten Hopp <karsten@redhat.com> 3.2.2-10
- disable rAssertAlmostEqual in test_cmath on PPC (#750811)

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.2.2-9
- python3-devel missing autogenerated pkgconfig() provides (#746751)

* Mon Oct 10 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-8
- cherrypick fix for distutils not using __pycache__ when byte-compiling
files (rhbz#722578)

* Fri Sep 30 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-7
- re-enable gdbm (patch 148; rhbz#742242)

* Fri Sep 16 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-6
- add a sys._debugmallocstats() function (patch 147)

* Wed Sep 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-5
- support OpenSSL FIPS mode in _hashlib and hashlib; don't build the _md5 and
_sha* modules, relying on _hashlib in hashlib (rhbz#563986; patch 146)

* Tue Sep 13 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-4
- disable gdbm module to prepare for gdbm soname bump

* Mon Sep 12 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-3
- renumber and rename patches for consistency with python.spec (8 to 55, 106
to 104, 6 to 111, 104 to 113, 105 to 114, 125, 131, 130 to 143)

* Sat Sep 10 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-2
- rewrite of "check", introducing downstream-only hooks for skipping specific
cases in an rpmbuild (patch 132), and fixing/skipping failing tests in a more
fine-grained manner than before; (patches 106, 133-142 sparsely, moving
patches for consistency with python.spec: 128 to 134, 126 to 135, 127 to 141)

* Tue Sep  6 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-1
- 3.2.2

* Thu Sep  1 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-7
- run selftests with "--verbose"
- disable parts of test_io on ppc (rhbz#732998)

* Wed Aug 31 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-6
- use "--findleaks --verbose3" when running test suite

* Tue Aug 23 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-5
- re-enable and fix the --with-tsc option on ppc64, and rework it on 32-bit
ppc to avoid aliasing violations (patch 130; rhbz#698726)

* Tue Aug 23 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-4
- don't use --with-tsc on ppc64 debug builds (rhbz#698726)

* Thu Aug 18 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-3
- add %%python3_version to the rpm macros (rhbz#719082)

* Mon Jul 11 2011 Dennis Gilmore <dennis@ausil.us> - 3.2.1-2
- disable some tests on sparc arches 

* Mon Jul 11 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-1
- 3.2.1; refresh lib64 patch (102), subprocess unit test patch (129), disabling
of static library build (due to Modules/_testembed; patch 6), autotool
intermediates (patch 300)

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-5
- use the gdb hooks from the upstream tarball, rather than keeping our own copy

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-4
- don't run test_openpty and test_pty in %%check

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-3
- cleanup of BuildRequires; add comment headings to specfile sections

* Tue Apr 19 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-2
- fix the libpython.stp systemtap tapset (rhbz#697730)

* Mon Feb 21 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-1
- 3.2
- drop alphatag
- regenerate autotool patch

* Mon Feb 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.13.rc3
- add a /usr/bin/python3-debug symlink within the debug subpackage

* Mon Feb 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.12.rc3
- 3.2rc3
- regenerate autotool patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.11.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.10.rc2
- 3.2rc2

* Mon Jan 17 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.9.rc1
- 3.2rc1
- rework patch 6 (static lib removal)
- remove upstreamed patch 130 (ppc debug build)
- regenerate patch 300 (autotool intermediates)
- updated packaging to reflect upstream rewrite of "Demo" (issue 7962)
- added libpython3.so and 2to3-3.2

* Wed Jan  5 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.8.b2
- set EXTRA_CFLAGS to our CFLAGS, rather than overriding OPT, fixing a linker
error with dynamic annotations (when configured using --with-valgrind)
- fix the ppc build of the debug configuration (patch 130; rhbz#661510)

* Tue Jan  4 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.7.b2
- add --with-valgrind to configuration (on architectures that support this)

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.6.b2
- work around test_subprocess failure seen in koji (patch 129)

* Tue Dec 28 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.5.b2
- 3.2b2
- rework patch 3 (removal of mimeaudio tests), patch 6 (no static libs),
patch 8 (systemtap), patch 102 (lib64)
- remove patch 4 (rendered redundant by upstream r85537), patch 103 (PEP 3149),
patch 110 (upstreamed expat fix), patch 111 (parallel build fix for grammar
fixed upstream)
- regenerate patch 300 (autotool intermediates)
- workaround COUNT_ALLOCS weakref issues in test suite (patch 126, patch 127,
patch 128)
- stop using runtest.sh in %%check (dropped by upstream), replacing with
regrtest; fixup list of failing tests
- introduce "pyshortver", "SOABI_optimized" and "SOABI_debug" macros
- rework manifests of shared libraries to use "SOABI_" macros, reflecting
PEP 3149
- drop itertools, operator and _collections modules from the manifests as py3k
commit r84058 moved these inside libpython; json/tests moved to test/json_tests
- move turtle code into the tkinter subpackage

* Wed Nov 17 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.5.a1
- fix sysconfig to not rely on the -devel subpackage (rhbz#653058)

* Thu Sep  9 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.4.a1
- move most of the content of the core package to the libs subpackage, given
that the libs aren't meaningfully usable without the standard libraries

* Wed Sep  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.3.a1
- Move test.support to core package (rhbz#596258)
- Add various missing __pycache__ directories to payload

* Sun Aug 22 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-0.2.a1
- Add __pycache__ directory for site-packages

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.2-0.1.a1
- on 64bit "stdlib" was still "/usr/lib/python*" (modify *lib64.patch)
- make find-provides-without-python-sonames.sh 64bit aware

* Sat Aug 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.0.a1
- 3.2a1; add alphatag
- rework %%files in the light of PEP 3147 (__pycache__)
- drop our configuration patch to Setup.dist (patch 0): setup.py should do a
better job of things, and the %%files explicitly lists our modules (r82746
appears to break the old way of doing things).  This leads to various modules
changing from "foomodule.so" to "foo.so".  It also leads to the optimized build
dropping the _sha1, _sha256 and _sha512 modules, but these are provided by
_hashlib; _weakref becomes a builtin module; xxsubtype goes away (it's only for
testing/devel purposes)
- fixup patches 3, 4, 6, 8, 102, 103, 105, 111 for the rebase
- remove upstream patches: 7 (system expat), 106, 107, 108 (audioop reformat
plus CVE-2010-1634 and CVE-2010-2089), 109 (CVE-2008-5983)
- add machinery for rebuilding "configure" and friends, using the correct
version of autoconf (patch 300)
- patch the debug build's usage of COUNT_ALLOCS to be less verbose (patch 125)
- "modulator" was removed upstream
- drop "-b" from patch applications affecting .py files to avoid littering the
installation tree

* Thu Aug 19 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-13
- Turn on computed-gotos.
- Fix for parallel make and graminit.c

* Fri Jul  2 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-12
- rebuild

* Fri Jul  2 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-11
- Fix an incompatibility between pyexpat and the system expat-2.0.1 that led to
a segfault running test_pyexpat.py (patch 110; upstream issue 9054; rhbz#610312)

* Fri Jun  4 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-10
- ensure that the compiler is invoked with "-fwrapv" (rhbz#594819)
- reformat whitespace in audioop.c (patch 106)
- CVE-2010-1634: fix various integer overflow checks in the audioop
module (patch 107)
- CVE-2010-2089: further checks within the audioop module (patch 108)
- CVE-2008-5983: the new PySys_SetArgvEx entry point from r81399 (patch 109)

* Thu May 27 2010 Dan Horák <dan[at]danny.cz> - 3.1.2-9
- reading the timestamp counter is available only on some arches (see Python/ceval.c)

* Wed May 26 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-8
- add flags for statvfs.f_flag to the constant list in posixmodule (i.e. "os")
(patch 105)

* Tue May 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-7
- add configure-time support for COUNT_ALLOCS and CALL_PROFILE debug options
(patch 104); enable them and the WITH_TSC option within the debug build

* Mon May 24 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-6
- build and install two different configurations of Python 3: debug and
standard, packaging the debug build in a new "python3-debug" subpackage
(patch 103)

* Tue Apr 13 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-5
- exclude test_http_cookies when running selftests, due to hang seen on
http://koji.fedoraproject.org/koji/taskinfo?taskID=2088463 (cancelled after
11 hours)
- update python-gdb.py from v5 to py3k version submitted upstream

* Wed Mar 31 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-4
- update python-gdb.py from v4 to v5 (improving performance and stability,
adding commands)

* Thu Mar 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-3
- update python-gdb.py from v3 to v4 (fixing infinite recursion on reference
cycles and tracebacks on bytes 0x80-0xff in strings, adding handlers for sets
and exceptions)

* Wed Mar 24 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-2
- refresh gdb hooks to v3 (reworking how they are packaged)

* Sun Mar 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-1
- update to 3.1.2: http://www.python.org/download/releases/3.1.2/
- drop upstreamed patch 2 (.pyc permissions handling)
- drop upstream patch 5 (fix for the test_tk and test_ttk_* selftests)
- drop upstreamed patch 200 (path-fixing script)

* Sat Mar 20 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-28
- fix typo in libpython.stp (rhbz:575336)

* Fri Mar 12 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-27
- add pyfuntop.stp example (source 7)
- convert usage of $$RPM_BUILD_ROOT to %%{buildroot} throughout, for
consistency with python.spec

* Mon Feb 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.1.1-26
- rebuild for new package of redhat-rpm-config (rhbz:564527)
- use 'install -p' when running 'make install'

* Fri Feb 12 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-25
- split configure options into multiple lines for easy of editing
- add systemtap static markers (wcohen, mjw, dmalcolm; patch 8), a systemtap
tapset defining "python.function.entry" and "python.function.return" to make
the markers easy to use (dmalcolm; source 5), and an example of using the
tapset to the docs (dmalcolm; source 6) (rhbz:545179)

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-24
- move the -gdb.py file from %%{_libdir}/INSTSONAME-gdb.py to
%%{_prefix}/lib/debug/%%{_libdir}/INSTSONAME.debug-gdb.py to avoid noise from
ldconfig (bug 562980), and which should also ensure it becomes part of the
debuginfo subpackage, rather than the libs subpackage
- introduce %%{py_SOVERSION} and %%{py_INSTSONAME} to reflect the upstream
configure script, and to avoid fragile scripts that try to figure this out
dynamically (e.g. for the -gdb.py change)

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-23
- add gdb hooks for easier debugging (Source 4)

* Thu Jan 28 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-22
- update python-3.1.1-config.patch to remove downstream customization of build
of pyexpat and elementtree modules
- add patch adapted from upstream (patch 7) to add support for building against
system expat; add --with-system-expat to "configure" invocation
- remove embedded copies of expat and zlib from source tree during "prep"

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-21
- introduce %%{dynload_dir} macro
- explicitly list all lib-dynload files, rather than dynamically gathering the
payload into a temporary text file, so that we can be sure what we are
shipping
- introduce a macros.pybytecompile source file, to help with packaging python3
modules (Source3; written by Toshio)
- rename "2to3-3" to "python3-2to3" to better reflect python 3 module packaging
plans

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-20
- change python-3.1.1-config.patch to remove our downstream change to curses
configuration in Modules/Setup.dist, so that the curses modules are built using
setup.py with the downstream default (linking against libncursesw.so, rather
than libncurses.so), rather than within the Makefile; add a test to %%install
to verify the dso files that the curses module is linked against the correct
DSO (bug 539917; changes _cursesmodule.so -> _curses.so)

* Fri Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-19
- add %%py3dir macro to macros.python3 (to be used during unified python 2/3
builds for setting up the python3 copy of the source tree)

* Wed Jan 20 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-18
- move lib2to3 from -tools subpackage to main package (bug 556667)

* Sun Jan 17 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-17
- patch Makefile.pre.in to avoid building static library (patch 6, bug 556092)

* Fri Jan 15 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-16
- use the %%{_isa} macro to ensure that the python-devel dependency on python
is for the correct multilib arch (#555943)
- delete bundled copy of libffi to make sure we use the system one

* Fri Jan 15 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-15
- fix the URLs output by pydoc so they point at python.org's 3.1 build of the
docs, rather than the 2.6 build

* Wed Jan 13 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-14
- replace references to /usr with %%{_prefix}; replace references to
/usr/include with %%{_includedir} (Toshio)

* Mon Jan 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-13
- fix permission on find-provides-without-python-sonames.sh from 775 to 755

* Mon Jan 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-12
- remove build-time requirements on tix and tk, since we already have
build-time requirements on the -devel subpackages for each of these (Thomas
Spura)
- replace usage of %%define with %%global (Thomas Spura)
- remove forcing of CC=gcc as this old workaround for bug 109268 appears to
longer be necessary
- move various test files from the "tools"/"tkinter" subpackages to the "test"
subpackage

* Thu Jan  7 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-11
- add %%check section (thanks to Thomas Spura)
- update patch 4 to use correct shebang line
- get rid of stray patch file from buildroot

* Tue Nov 17 2009 Andrew McNabb <amcnabb@mcnabbs.org> - 3.1.1-10
- switched a few instances of "find |xargs" to "find -exec" for consistency.
- made the description of __os_install_post more accurate.

* Wed Nov  4 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-9
- add macros.python3 to the -devel subpackage, containing common macros for use
when packaging python3 modules

* Tue Nov  3 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-8
- add a provides of "python(abi)" (see bug 532118)
- fix issues identified by a.badger in package review (bug 526126, comment 39):
  - use "3" thoughout metadata, rather than "3.*"
  - remove conditional around "pkg-config openssl"
  - use standard cleanup of RPM_BUILD_ROOT
  - replace hardcoded references to /usr with _prefix macro
  - stop removing egg-info files
  - use /usr/bin/python3.1 rather than /use/bin/env python3.1 when fixing
up shebang lines
  - stop attempting to remove no-longer-present .cvsignore files
  - move the post/postun sections above the "files" sections

* Thu Oct 29 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-7
- remove commented-away patch 51 (python-2.6-distutils_rpm.patch): the -O1
flag is used by default in the upstream code
- "Makefile" and the config-32/64.h file are needed by distutils/sysconfig.py
_init_posix(), so we include them in the core package, along with their parent
directories (bug 531901)

* Tue Oct 27 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-6
- reword description, based on suggestion by amcnabb
- fix the test_email and test_imp selftests (patch 3 and patch 4 respectively)
- fix the test_tk and test_ttk_* selftests (patch 5)
- fix up the specfile's handling of shebang/perms to avoid corrupting
test_httpservers.py (sed command suggested by amcnabb)

* Thu Oct 22 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-5
- fixup importlib/_bootstrap.py so that it correctly handles being unable to
open .pyc files for writing (patch 2, upstream issue 7187)
- actually apply the rpath patch (patch 1)

* Thu Oct 22 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-4
- update patch0's setup of the crypt module to link it against libcrypt
- update patch0 to comment "datetimemodule" back out, so that it is built
using setup.py (see Setup, option 3), thus linking it statically against
timemodule.c and thus avoiding a run-time "undefined symbol:
_PyTime_DoubleToTimet" failure on "import datetime"

* Wed Oct 21 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-3
- remove executable flag from various files that shouldn't have it
- fix end-of-line encodings
- fix a character encoding

* Tue Oct 20 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-2
- disable invocation of brp-python-bytecompile in postprocessing, since
it would be with the wrong version of python (adapted from ivazquez'
python3000 specfile)
- use a custom implementation of __find_provides in order to filter out bogus
provides lines for the various .so modules
- fixup distutils/unixccompiler.py to remove standard library path from rpath
(patch 1, was Patch0 in ivazquez' python3000 specfile)
- split out libraries into a -libs subpackage
- update summaries and descriptions, basing content on ivazquez' specfile
- fixup executable permissions on .py, .xpm and .xbm files, based on work in
ivazquez's specfile
- get rid of DOS batch files
- fixup permissions for shared libraries from non-standard 555 to standard 755
- move /usr/bin/python*-config to the -devel subpackage
- mark various directories as being documentation

* Thu Sep 24 2009 Andrew McNabb <amcnabb@mcnabbs.org> 3.1.1-1
- Initial package for Python 3.

