%{!?__python_ver:%global __python_ver EMPTY}
%global __python_ver 26
%global unicode ucs4

# Note: bcond_without adds the '--without tests' build condition.
# Building 'with tests' is the default.
%bcond_without tests

%global _default_patch_fuzz 2

%if "%{__python_ver}" != "EMPTY"
%global main_python 0
%global python python%{__python_ver}
%global tkinter tkinter%{__python_ver}
%else
%global main_python 1
%global python python
%global tkinter tkinter
%endif

%global pybasever 2.6
%global pylibdir %{_libdir}/python%{pybasever}
%global tools_dir %{pylibdir}/Tools
%global demo_dir %{pylibdir}/Demo
%global doc_tools_dir %{pylibdir}/Doc/tools
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages

# We need to get a newer configure generated out of configure.in for the following
# patches:
#   patch 4 (CFLAGS)
#   patch 52 (valgrind)
#   patch 55 (systemtap)
# For patch 55 (systemtap), we need to get a new header for configure to use
#
# configure.in requires autoconf 2.61, but the version in RHEL 5 is 2.59
#
# For now, we'll generate a patch to the generated configure script on a
# machine that has a local copy of autoconf 2.61
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
# local copy of autoconf-2.61, regenerate the patch, then exit, without doing
# the rest of the build
%global regenerate_autotooling_patch 0

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME libpython%{pybasever}.so.%{py_SOVERSION}

%global with_gdb_hooks 0

%global with_systemtap 0

%global with_system_expat 0

# ppc in Koji doesn't seem to be able to locate valgrind-devel, for some reason
%ifarch ppc
%global with_valgrind 0
%else
%global with_valgrind 1
%endif

# Redefine __os_install_post, removing the invocation of brp-python-bytecompile
# (this is normally defined in /usr/lib/rpm/redhat/macros)
#
# brp-python-bytecompile is normally called without a parameter, which
# effectively hardcodes the use of /usr/bin/python, leaving the .pyc/.pyo files
# with an ABI version of 2.4, rather than 2.6
#
# This can be checked with "hexdump -C".
# A python 2.6 .pyo file should begin with:
#     d1 f2 0d 0a
# corresponding to MAGIC=62161 = 0xF2D1
# 
# whereas a python 2.4 .pyo file should begin with:
#     6d f2 0d 0a
# corresponding to MAGIC=62061 = 0xF26D

%global __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
    /usr/lib/rpm/redhat/brp-java-repack-jars \
%{nil}


Summary: An interpreted, interactive, object-oriented programming language
Name: %{python}
Version: 2.6.8
Release: 3%{?dist}
License: Python
Group: Development/Languages
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2


# We install a collection of hooks for gdb that make it easier to debug
# executables linked against libpython (such as /usr/lib/python itself)
#
# These hooks are implemented in Python itself
#
# gdb-archer looks for them in the same path as the ELF file, with a -gdb.py suffix.
# We put them in the debuginfo package by installing them to e.g.:
#  /usr/lib/debug/usr/lib/libpython2.6.so.1.0.debug-gdb.py
#
# See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
# information
#
# Downloaded from:
# http://fedorapeople.org/gitweb?p=dmalcolm/public_git/libpython.git;a=snapshot;h=36a517ef7848cbd0b3dcc7371f32e47ac4c87eba;sf=tgz
Source1: libpython-36a517ef7848cbd0b3dcc7371f32e47ac4c87eba.tar.gz


# Work around bug 562906 until it's fixed in rpm-build by providing a fixed
# version of pythondeps.sh:
Source2: pythondeps.sh
%global __python_requires %{SOURCE2}

# Systemtap tapset to make it easier to use the systemtap static probes
# (actually a template; LIBRARY_PATH will get fixed up during install)
# Written by dmalcolm; not yet sent upstream
Source3: libpython.stp


# Example systemtap script using the tapset
# Written by wcohen, mjw, dmalcolm; not yet sent upstream
Source4: systemtap-example.stp


# Similarly to how we needed to redefine __os_install_post (see above), drop
# a file into /etc/rpm/macros providing an alternative definition of that macro
#
# This defines a __python26_os_install_post macro, so that a specfile for a
# module should merely need to redefine __os_install_post to this in order to
# be byte-compiled using python2.6
Source5: macros.python26

# An alternative script that allows packages to build against python and python26
# via the same source.
Source7: brp-multiple-python-bytecompile


# Modules/Setup.dist is ultimately used by the "makesetup" script to construct
# the Makefile and config.c
#
# Upstream leaves many things disabled by default, to try to make it easy as
# possible to build the code on as many platforms as possible.
#
# TODO: many modules can also now be built by setup.py after the python binary
# has been built; need to assess if we should instead build things there
#
# We patch it downstream as follows:
#   - various modules are built by default by upstream as static libraries;
#   we built them as shared libraries
#   - build the "readline" module (appears to also be handled by setup.py now)
#   - enable the build of the following modules:
#     - array arraymodule.c	# array objects
#     - cmath cmathmodule.c # -lm # complex math library functions
#     - math mathmodule.c # -lm # math library functions, e.g. sin()
#     - _struct _struct.c	# binary structure packing/unpacking
#     - time timemodule.c # -lm # time operations and variables
#     - operator operator.c	# operator.add() and similar goodies
#     - _weakref _weakref.c	# basic weak reference support
#     - _testcapi _testcapimodule.c    # Python C API test module
#     - _random _randommodule.c	# Random number generator
#     - _collections _collectionsmodule.c # Container types
#     - itertools itertoolsmodule.c
#     - strop stropmodule.c
#     - _functools _functoolsmodule.c
#     - _bisect _bisectmodule.c	# Bisection algorithms
#     - unicodedata unicodedata.c    # static Unicode character database
#     - _locale _localemodule.c
#     - fcntl fcntlmodule.c	# fcntl(2) and ioctl(2)
#     - spwd spwdmodule.c		# spwd(3) 
#     - grp grpmodule.c		# grp(3)
#     - select selectmodule.c	# select(2); not on ancient System V
#     - mmap mmapmodule.c  # Memory-mapped files
#     - _csv _csv.c  # CSV file helper
#     - _socket socketmodule.c  # Socket module helper for socket(2)
#     - _ssl _ssl.c
#     - crypt cryptmodule.c -lcrypt	# crypt(3)
#     - nis nismodule.c -lnsl	# Sun yellow pages -- not everywhere
#     - termios termios.c	# Steen Lumholt's termios module
#     - resource resource.c	# Jeremy Hylton's rlimit interface
#     - audioop audioop.c	# Operations on audio samples
#     - imageop imageop.c	# Operations on images
#     - _md5 md5module.c md5.c
#     - _sha shamodule.c
#     - _sha256 sha256module.c
#     - _sha512 sha512module.c
#     - linuxaudiodev linuxaudiodev.c
#     - timing timingmodule.c
#     - _tkinter _tkinter.c tkappinit.c
#     - dl dlmodule.c
#     - gdbm gdbmmodule.c
#     - _bsddb _bsddb.c
#     - binascii binascii.c
#     - parser parsermodule.c
#     - cStringIO cStringIO.c
#     - cPickle cPickle.c
#     - zlib zlibmodule.c
#     - _multibytecodec cjkcodecs/multibytecodec.c
#     - _codecs_cn cjkcodecs/_codecs_cn.c
#     - _codecs_hk cjkcodecs/_codecs_hk.c
#     - _codecs_iso2022 cjkcodecs/_codecs_iso2022.c
#     - _codecs_jp cjkcodecs/_codecs_jp.c
#     - _codecs_kr cjkcodecs/_codecs_kr.c
#     - _codecs_tw cjkcodecs/_codecs_tw.c
Patch0: python-2.6.2-config.patch

# Removes the "-g" option from "pydoc", for some reason; I believe
# (dmalcolm 2010-01-29) that this was introduced in this change:
# - fix pydoc (#68082)
# in 2.2.1-12 as a response to the -g option needing TkInter installed
# (Red Hat Linux 8)
# Not upstream
Patch1: Python-2.2.1-pydocnogui.patch

# Fixup configure.in and setup.py to build against system expat library.
# Adapted from http://svn.python.org/view?view=rev&revision=77169
Patch3: python-2.6.2-with-system-expat.patch

# Add $(CFLAGS) to the linker arguments when linking the "python" binary
# since some architectures (sparc64) need this (rhbz:199373).
# Not yet filed upstream
Patch4: python-2.5-cflags.patch

# Work around a bug in Python' gettext module relating to the "Plural-Forms"
# header (rhbz:252136)
# Related to upstream issues:
#   http://bugs.python.org/issue1448060 and http://bugs.python.org/issue1475523
# though the proposed upstream patches are, alas, different
Patch6: python-2.5.1-plural-fix.patch

# This patch was listed in the changelog as: 
#  * Fri Sep 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-11
#  - fix encoding of sqlite .py files to work around weird encoding problem 
#  in Turkish (#283331)
# A traceback attached to rhbz 244016 shows the problem most clearly: a
# traceback on attempting to import the sqlite module, with:
#   "SyntaxError: encoding problem: with BOM (__init__.py, line 1)"
# This seems to come from Parser/tokenizer.c:check_coding_spec
# Our patch changes two source files within sqlite3, removing the
# "coding: ISO-8859-1" specs and character E4 = U+00E4 = 
# LATIN SMALL LETTER A WITH DIAERESIS from in ghaering's surname. 
#
# It may be that the conversion of "ISO-8859-1" to "iso-8859-1" is thwarted
# by the implementation of "tolower" in the Turkish locale; see:
#   https://bugzilla.redhat.com/show_bug.cgi?id=191096#c9
# 
# TODO: Not yet sent upstream, and appears to me (dmalcolm 2010-01-29) that
# it may be papering over a symptom
Patch7: python-2.5.1-sqlite-encoding.patch

# FIXME: Lib/ctypes/util.py posix implementation defines a function
# _get_soname(f).  Upstreams's implementation of this uses objdump to read the
# SONAME from a library; we avoid this, apparently to minimize space
# requirements on the live CD:
# (rhbz:307221)
Patch10: python-2.6.2-binutils-no-dep.patch

# Add various constants to the socketmodule (rhbz#436560):
# TODO: these patches were added in 2.5.1-22 and 2.5.1-24 but appear not to
# have been sent upstream yet:
Patch13: python-2.5.1-socketmodule-constants.patch
Patch14: python-2.5.1-socketmodule-constants2.patch

# Remove an "-rpath $(LIBDIR)" argument from the linkage args in configure.in:
# FIXME: is this for OSF, not Linux?
Patch16: python-2.6-rpath.patch

# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Adapted from Patch0 in ivazquez' python3000 specfile, removing usage of
# super() as it's an old-style class
Patch17: python-2.6.4-distutils-rpath.patch

# Fix distutils to follow the Fedora/RHEL/CentOS policies of having .pyo files
Patch51: python-2.6-distutils_rpm.patch

# Automatically disable arena allocator when run under valgrind:
# From http://bugs.python.org/issue2422
#   http://bugs.python.org/file9872/disable-pymalloc-on-valgrind-py26.patch
# with the "configure" part removed; appears to be identical to the version committed to 2.7
Patch52: disable-pymalloc-on-valgrind-py26.patch

# Systemtap support: add statically-defined probe points
# Patch based on upstream bug: http://bugs.python.org/issue4111
# fixed up by mjw and mcohen for 2.6.2, then fixed up by dmalcolm for 2.6.4
# then rewritten by mjw (attachment 390110 of rhbz 545179)
Patch55: python-2.6.4-dtrace.patch

# "lib64 patches"
# This patch seems to be associated with bug 122304, which was
#  http://sourceforge.net/tracker/?func=detail&atid=105470&aid=931848&group_id=5470
# and is now
#  http://bugs.python.org/issue931848
# However, as it stands this patch is merely a copy of:
#  http://svn.python.org/view/python/trunk/Lib/test/test_re.py?r1=35825&r2=35824&pathrev=35825
# which is already upstream
# Earlier versions of the patch (from the "dist-pkgs" CVS repo within RH)
# contained additional changes that applied fixes to the internals of the regex
# module, but these appear to have all been applied as part of 
#  http://bugs.python.org/issue931848
Patch101: python-2.3.4-lib64-regex.patch

# Only used when "%{_lib}" == "lib64"
# Fixup various paths throughout the build and in distutils from "lib" to "lib64",
# and add the /usr/lib64/pythonMAJOR.MINOR/site-packages to sitedirs, in front of
# /usr/lib/pythonMAJOR.MINOR/site-packages
# Not upstream
Patch102: python-2.6.8-lib64.patch

# rhbz#488396: rework the ctypes module to use ffi_closure_alloc and
# ffi_closure_free, rather than malloc_closure.c, since the latter tries to
# mmap pages with PROT_READ | PROT_WRITE | PROT_EXEC, which SELinux frowns upon.
# 
# Patch sent upstream as http://bugs.python.org/issue5504 which also contains
# a rebasing of the upstream copy of libffi to one containing the
# memory-management hooks. 
#
# This appears to be the same as that patch, but without the rebasing of libffi
# (since we use the system copy of libffi):
Patch110: python-2.6.8-ctypes-noexecmem.patch

# Patch the Makefile.pre.in so that the generated Makefile doesn't try to build
# a libpythonMAJOR.MINOR.a (bug 550692):
Patch111: python-2.6.4-no-static-lib.patch

# Resolves http://bugs.python.org/issue10013
# Title: fix `./libpython2.6.so: undefined reference to `_PyParser_Grammar` in 
# parallel builds
Patch119: Python-2.6.5-parallel_build.patch

# Resolves Issue 7564: test_ioctl may fail when run in background
#
# http://bugs.python.org/issue7564
# http://svn.python.org/view?view=revision&revision=83839
Patch120: Python-2.6.5-ioctl_test.patch

# Forces sys.platform to linux2
#
# http://bugs.python.org/issue12326
#
# Patch provided by dmalcolm patch 145:
# http://pkgs.fedoraproject.org/cgit/python.git/commit/?id=bc10ab792a3c042e5b9e89a39290bab24af5e799
Patch121: python-2.6.8-force-sys-platform-to-be-linux2.patch

# Patch up pyexpat.h so it will build against RHEL-5's pyexpat-devel:
Patch200: python-2.6.4-expat-version.patch

# Patch assert(_Py_HashSecret_Initialized) to only be used when Py_DEBUG is set
# (in case of building with C asserts enabled without Py_DEBUG):
Patch201: python-2.6.8-wrap-_Py_HashSecret_Initialized-with-if-Py_DEBUG.patch

# This is the generated patch to "configure"; see the description of
#   %{regenerate_autotooling_patch}
# above:
Patch300: python-2.6.4-autotool-intermediates.patch

%if %{main_python}
Obsoletes: python2 < 2.6.5
Provides: python2 = %{version}
Obsoletes: python-elementtree <= 1.2.6
Obsoletes: python-sqlite < 2.3.2
Provides: python-sqlite = 2.3.2
Obsoletes: python-ctypes < 1.0.1
Provides: python-ctypes = 1.0.1
Obsoletes: python-hashlib < 20081120
Provides: python-hashlib = 20081120
Obsoletes: python-uuid < 1.31
Provides: python-uuid = 1.31
%endif

Requires: python26-libs
Requires: libffi

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: readline-devel, openssl-devel, gmp-devel
BuildRequires: ncurses-devel, gdbm-devel, zlib-devel, expat-devel
BuildRequires: libGL-devel tk tix gcc-c++ libX11-devel glibc-devel
BuildRequires: bzip2 tar findutils pkgconfig tcl-devel tk-devel
BuildRequires: tix-devel bzip2-devel sqlite-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel


# Valgrind headers were in core valgrind subpackage on EL5, but were moved to
# a valgrind-devel subpackage in 3.5.0-1.el5
%if 0%{with_valgrind}
BuildRequires: valgrind-devel
%endif


%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
%global tapsetdir      /usr/share/systemtap/tapset
%endif

URL: http://www.python.org/

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface. This package contains most of the standard
Python modules, as well as modules for interfacing to the Tix widget
set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires: %{name} = %{version}-%{release}
# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to 
use python as an embedded scripting language.  The python-libs package 
provides the libraries needed for this.

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{python} = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: %{python} < %{version}-%{release}
%if %{main_python}
Obsoletes: python2-devel < 2.6.5
Provides: python2-devel = %{version}-%{release}
%endif

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{tkinter} = %{version}-%{release}
%if %{main_python}
Obsoletes: python2-tools < 2.6.5
Provides: python2-tools = %{version}
%endif

%description tools
This package includes several tools to help with the development of Python   
programs, including IDLE (an IDE with editing and debugging facilities), a 
color editor (pynche), and a python gettext program (pygettext.py).  

%package -n %{tkinter}
Summary: A graphical user interface for the Python scripting language
Group: Development/Languages
BuildRequires:  tcl, tk
Requires: %{name} = %{version}-%{release}
%if %{main_python}
Obsoletes: tkinter2 < 2.6.5
Provides: tkinter2 = %{version}
%endif

%description -n %{tkinter}

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.

%prep
%setup -q -n Python-%{version}

# Unpack source archive 1 into this same dir without deleting (-D; -T suppress
# trying to unpack source 0 again):
%if 0%{?with_gdb_hooks}
%setup -q -n Python-%{version} -T -D -a 1
%endif # with_gdb_hooks

%if 0%{?with_systemtap}
# Provide an example of usage of the tapset:
cp -a %{SOURCE4} .
%endif # with_systemtap

# Ensure that we're using the system copy of various libraries, rather than
# copies shipped by upstream in the tarball:
#   Remove embedded copy of expat:
%if 0%{?with_system_expat}
rm -r Modules/expat || exit 1
%endif

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

#   Remove embedded copy of zlib:
rm -r Modules/zlib || exit 1

#
# Apply patches:
#
%patch0 -p1 -b .rhconfig
%patch3 -p1 -b .expat
%patch1 -p1 -b .no_gui
%patch4 -p1 -b .cflags
%patch6 -p1 -b .plural
%patch7 -p1

# Try not disabling egg-infos, bz#414711
#patch50 -p1 -b .egginfo

%patch101 -p1 -b .lib64-regex

%if "%{_lib}" == "lib64"
%patch102 -p1 -b .lib64
%endif

%patch10 -p1 -b .binutils-no-dep
%patch13 -p1 -b .socketmodule
%patch14 -p1 -b .socketmodule2
%patch16 -p1 -b .rpath
%patch17 -p1 -b .distutils-rpath

%patch51 -p1 -b .brprpm
%if 0%{with_valgrind}
%patch52 -p1 -b .valgrind
%endif
%if 0%{?with_systemtap}
%patch55 -p1 -b .systemtap
%endif

%patch110 -p1 -b .selinux

%patch111 -p1 -b .no-static-lib

%patch119 -p1 -b .parallel_build
%patch120 -p1 -b .ioctl_test
%patch121 -p1 -b .configure

%if 0%{?with_system_expat}
%patch200 -p1 -b .expat-version
%endif

%patch201 -p1

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

%if ! 0%{regenerate_autotooling_patch}
# Normally we apply the patch to "configure"
# We don't apply the patch if we're working towards regenerating it
%patch300 -p0 -b .autotool-intermediates
%endif

%build
topdir=$(pwd)
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
  export LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi
# Force CC
export CC=gcc

%if 0%{regenerate_autotooling_patch}
# If enabled, this code regenerates the patch to "configure", using a
# local copy of autoconf-2.61, then exits the build
#
# The following assumes that the copy is installed to ~/autoconf-2.61/bin
# as per these instructions:
#   http://bugs.python.org/issue7997

cp configure configure.autotool-intermediates
PATH=~/autoconf-2.61/bin:$PATH autoconf

# Regenerate the patch:
gendiff . .autotool-intermediates > %{PATCH300}

# Exit the build
exit 0
%endif

# Use the patched "configure" script:
%configure \
  --enable-ipv6 \
  --enable-unicode=%{unicode} \
  --enable-shared \
  --with-system-ffi \
%if 0%{?with_system_expat}
  --with-system-expat \
%endif
%if 0%{?with_systemtap}
  --with-dtrace \
  --with-tapset-install-dir=%{tapsetdir} \
%endif
%if 0%{with_valgrind}
  --with-valgrind \
%endif
%{nil}


make OPT="$CFLAGS" %{?_smp_mflags}
LD_LIBRARY_PATH="$topdir" $topdir/python Tools/scripts/pathfix.py -i "%{_bindir}/env python%{pybasever}" .
# Rebuild with new python
# We need a link to a versioned python in the build directory
ln -s python python%{pybasever}
LD_LIBRARY_PATH="$topdir" PATH=$PATH:$topdir make -s OPT="$CFLAGS" %{?_smp_mflags}



%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}

# Clean up patched .py files that are saved as .lib64
for f in distutils/command/install distutils/sysconfig; do
    rm -f Lib/$f.py.lib64
done

make install DESTDIR=%{buildroot}
# Fix the interpreter path in binaries installed by distutils 
# (which changes them by itself)
# Make sure we preserve the file permissions
for fixed in %{buildroot}%{_bindir}/pydoc; do
    sed 's,#!.*/python$,#!%{_bindir}/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
done

# Junk, no point in putting in -test sub-pkg
rm -f %{buildroot}/%{pylibdir}/idlelib/testcode.py*

# don't include tests that are run at build time in the package
# This is documented, and used: rhbz#387401
if /bin/false; then
 # Move this to -test subpackage.
mkdir save_bits_of_test
for i in test_support.py __init__.py; do
  cp -a %{buildroot}/%{pylibdir}/test/$i save_bits_of_test
done
rm -rf %{buildroot}/%{pylibdir}/test
mkdir %{buildroot}/%{pylibdir}/test
cp -a save_bits_of_test/* %{buildroot}/%{pylibdir}/test
fi

%if %{main_python}
ln -s python %{buildroot}%{_bindir}/python2
%else
mv %{buildroot}%{_bindir}/python %{buildroot}%{_bindir}/%{python}
mv %{buildroot}/%{_mandir}/man1/python.1 %{buildroot}/%{_mandir}/man1/python%{pybasever}.1
rm %{buildroot}%{_bindir}/python-config
%endif

# tools

mkdir -p ${RPM_BUILD_ROOT}%{site_packages}

#modulator
cat > ${RPM_BUILD_ROOT}%{_bindir}/modulator << EOF
#!/bin/bash
exec %{site_packages}/modulator/modulator.py
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/modulator
cp -r Tools/modulator \
  ${RPM_BUILD_ROOT}%{site_packages}/

#pynche
cat > ${RPM_BUILD_ROOT}%{_bindir}/pynche << EOF
#!/bin/bash
exec %{site_packages}/pynche/pynche
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/pynche
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche \
  ${RPM_BUILD_ROOT}%{site_packages}/

mv Tools/modulator/README Tools/modulator/README.modulator
mv Tools/pynche/README Tools/pynche/README.pynche

#gettext
install -m755  Tools/i18n/pygettext.py %{buildroot}%{_bindir}/
install -m755  Tools/i18n/msgfmt.py %{buildroot}%{_bindir}/

# Useful development tools
install -m755 -d %{buildroot}%{tools_dir}/scripts
install Tools/README %{buildroot}%{tools_dir}/
install Tools/scripts/*py %{buildroot}%{tools_dir}/scripts/

# Documentation tools
install -m755 -d %{buildroot}%{doc_tools_dir}
#install -m755 Doc/tools/mkhowto %{buildroot}%{doc_tools_dir}

# Useful demo scripts
install -m755 -d %{buildroot}%{demo_dir}
cp -ar Demo/* %{buildroot}%{demo_dir}

# Get rid of crap
find %{buildroot}/ -name "*~"|xargs rm -f
find %{buildroot}/ -name ".cvsignore"|xargs rm -f
find %{buildroot}/ -name "*.bat"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f %{buildroot}%{site_packages}/modulator/Templates/copyright

rm -f %{buildroot}%{pylibdir}/LICENSE.txt


#make the binaries install side by side with the main python
%if !%{main_python}
pushd %{buildroot}%{_bindir}
mv idle idle%{__python_ver}
mv modulator modulator%{__python_ver}
mv pynche pynche%{__python_ver}
mv pygettext.py pygettext%{__python_ver}.py
mv msgfmt.py msgfmt%{__python_ver}.py
mv smtpd.py smtpd%{__python_ver}.py
mv pydoc pydoc%{__python_ver}
popd
%endif

# Fix for bug #136654
rm -f %{buildroot}%{pylibdir}/email/test/data/audiotest.au %{buildroot}%{pylibdir}/test/audiotest.au

# Fix bug #143667: python should own /usr/lib/python2.x on 64-bit machines
%if "%{_lib}" == "lib64"
install -d %{buildroot}/usr/lib/python%{pybasever}/site-packages
%endif

# Make python-devel multilib-ready (bug #192747, #139911)
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h

%ifarch ppc64 s390x x86_64 ia64 alpha sparc64
%global _pyconfig_h %{_pyconfig64_h}
%else
%global _pyconfig_h %{_pyconfig32_h}
%endif
mv %{buildroot}%{_includedir}/python%{pybasever}/pyconfig.h \
   %{buildroot}%{_includedir}/python%{pybasever}/%{_pyconfig_h}
cat > %{buildroot}%{_includedir}/python%{pybasever}/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
ln -s ../../libpython%{pybasever}.so %{buildroot}%{pylibdir}/config/libpython%{pybasever}.so

# Fix for bug 201434: make sure distutils looks at the right pyconfig.h file
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" %{buildroot}%{pylibdir}/distutils/sysconfig.py

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
  %{buildroot}%{pylibdir}/Demo/comparisons/patterns \
  %{buildroot}%{pylibdir}/Demo/rpc/test \
  %{buildroot}%{pylibdir}/Tools/README \
  %{buildroot}%{pylibdir}/Demo/scripts/newslist.doc \
  %{buildroot}%{pylibdir}/Demo/md5test/foo

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so (bug 539917)
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)


# Copy up the gdb hooks into place; the python file will be autoloaded by gdb
# when visiting libpython.so, provided that the python file is installed to the
# same path as the library (or its .debug file) plus a "-gdb.py" suffix, e.g:
#  /usr/lib/debug/usr/lib64/libpython2.6.so.1.0.debug-gdb.py
# (note that the debug path is /usr/lib/debug for both 32/64 bit)
# 
# Initially I tried:
#  /usr/lib/libpython2.6.so.1.0-gdb.py
# but doing so generated noise when ldconfig was rerun (rhbz:562980)
#
%if 0%{?with_gdb_hooks}
%global dir_holding_gdb_py %{_prefix}/lib/debug/%{_libdir}
%global path_of_gdb_py %{dir_holding_gdb_py}/%{py_INSTSONAME}.debug-gdb.py

mkdir -p %{buildroot}%{dir_holding_gdb_py}
cp libpython/libpython.py %{buildroot}%{path_of_gdb_py}

# Manually byte-compile the file, in case find-debuginfo.sh is run before
# brp-python-bytecompile, so that the .pyc/.pyo files are properly listed in
# the debuginfo manifest:
LD_LIBRARY_PATH=. ./python -c "import compileall; import sys; compileall.compile_dir('%{buildroot}%{dir_holding_gdb_py}', ddir='%{dir_holding_gdb_py}')"

LD_LIBRARY_PATH=. ./python -O -c "import compileall; import sys; compileall.compile_dir('%{buildroot}%{dir_holding_gdb_py}', ddir='%{dir_holding_gdb_py}')"
%endif # with_gdb_hooks

#
# Systemtap hooks:
#
%if 0%{?with_systemtap}
# Install a tapset for this libpython into tapsetdir, fixing up the path to the
# library:
mkdir -p %{buildroot}%{tapsetdir}
%ifarch ppc64 s390x x86_64 ia64 alpha sparc64
%global libpython_stp libpython%{pybasever}-64.stp
%else
%global libpython_stp libpython%{pybasever}-32.stp
%endif

sed \
   -e "s|LIBRARY_PATH|%{_libdir}/%{py_INSTSONAME}|" \
   %{SOURCE3} \
   > %{buildroot}%{tapsetdir}/%{libpython_stp}
%endif # with_systemtap

# Drop the rpm macros file into place, to make it easy for modules to be
# byte-compiled using this python runtime:
mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/rpm/macros.python26

# Provide an alternative os_install_post bytecompile script which handles
# multiple python versions
mkdir -p %{buildroot}/usr/lib/rpm/
install -p -m 755 %{SOURCE7} %{buildroot}/usr/lib/rpm/brp-multiple-python-bytecompile

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} \
    -perm 555 -exec chmod 755 {} \;

%check
%if %{with tests}
# Run the upstream test suite, skipping known failures
export EXTRATESTOPTS="-x test_distutils test_dl test_file test_subprocess test_socket test_urllib2"
make test

# Known/expected failures:
# Seen on all architectures:
#   + cat OUT/test_distutils.out
#   test_distutils
#   /usr/bin/ld: cannot find -lpython2.6
#   collect2: ld returned 1 exit status
#   test test_distutils failed -- Traceback (most recent call last):
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/tests/test_build_ext.py", line 261, in test_get_outputs
#       cmd.run()
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/command/build_ext.py", line 340, in run
#       self.build_extensions()
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/command/build_ext.py", line 449, in build_extensions
#       self.build_extension(ext)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/command/build_ext.py", line 531, in build_extension
#       target_lang=language)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/ccompiler.py", line 769, in link_shared_object
#       extra_preargs, extra_postargs, build_temp, target_lang)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/distutils/unixccompiler.py", line 268, in link
#       raise LinkError, msg
#   LinkError: command 'gcc' failed with exit status 1
#
# Seen on x86_64 only:
#   + cat OUT/test_dl.out
#   test test_dl crashed -- <type 'exceptions.SystemError'>: module dl requires sizeof(int) == sizeof(long) == sizeof(char*)
#
# Seen on all architectures:
#   + cat OUT/test_file.out
#   test test_file failed -- Traceback (most recent call last):
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/test/test_file.py", line 201, in testStdin
#       self.assertRaises(IOError, sys.stdin.seek, -1)
#   AssertionError: IOError not raised
#
# Seen on all architectures:
#   + cat OUT/test_socket.out
#   test test_socket failed -- Traceback (most recent call last):
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/test/test_socket.py", line 482, in testSockName
#       my_ip_addr = socket.gethostbyname(socket.gethostname())
#   gaierror: [Errno -3] Temporary failure in name resolution
#
# Seen on all architectures:
#   + cat OUT/test_subprocess.out
#   test test_subprocess failed -- Traceback (most recent call last):
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/test/test_subprocess.py", line 500, in test_leaking_fds_on_error
#       stderr=subprocess.PIPE)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/subprocess.py", line 633, in __init__
#       errread, errwrite)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/subprocess.py", line 1139, in _execute_child
#       raise child_exception
#   OSError: [Errno 13] Permission denied
#
# Seen on all architectures:
#   + cat OUT/test_urllib2.out
#   test test_urllib2 failed -- Traceback (most recent call last):
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/test/test_urllib2.py", line 712, in test_file
#       h.file_open, Request(url))
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/unittest.py", line 336, in failUnlessRaises
#       callableObj(*args, **kwargs)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/urllib2.py", line 1257, in file_open
#       return self.open_local_file(req)
#     File "/builddir/build/BUILD/Python-2.6.5/Lib/urllib2.py", line 1289, in open_local_file
#       (not port and socket.gethostbyname(host) in self.get_names()):
#   gaierror: [Errno -3] Temporary failure in name resolution
#

%endif # with tests

%clean
rm -fr %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/%{python}
%if %{main_python}
%{_bindir}/python2
%endif
%{_bindir}/python%{pybasever}
%{_mandir}/*/*
%config(noreplace) %{_sysconfdir}/rpm/macros.python26
/usr/lib/rpm/brp-multiple-python-bytecompile

%dir %{pylibdir}
%dir %{dynload_dir}
%{dynload_dir}/Python-%{version}-py%{pybasever}.egg-info
%{dynload_dir}/_bisectmodule.so
%{dynload_dir}/_bsddb.so
%{dynload_dir}/_bytesio.so
%{dynload_dir}/_codecs_cn.so
%{dynload_dir}/_codecs_hk.so
%{dynload_dir}/_codecs_iso2022.so
%{dynload_dir}/_codecs_jp.so
%{dynload_dir}/_codecs_kr.so
%{dynload_dir}/_codecs_tw.so
%{dynload_dir}/_collectionsmodule.so
%{dynload_dir}/_csv.so
%{dynload_dir}/_ctypes.so
%{dynload_dir}/_curses.so
%{dynload_dir}/_curses_panel.so
%{dynload_dir}/_elementtree.so
%{dynload_dir}/_fileio.so
%{dynload_dir}/_functoolsmodule.so
%{dynload_dir}/_hashlib.so
%{dynload_dir}/_heapq.so
%{dynload_dir}/_hotshot.so
%{dynload_dir}/_json.so
%{dynload_dir}/_localemodule.so
%{dynload_dir}/_lsprof.so
%{dynload_dir}/_md5module.so
%{dynload_dir}/_multibytecodecmodule.so
%{dynload_dir}/_multiprocessing.so
%{dynload_dir}/_randommodule.so
%{dynload_dir}/_sha256module.so
%{dynload_dir}/_sha512module.so
%{dynload_dir}/_shamodule.so
%{dynload_dir}/_socketmodule.so
%{dynload_dir}/_sqlite3.so
%{dynload_dir}/_ssl.so
%{dynload_dir}/_struct.so
%{dynload_dir}/_weakref.so
%{dynload_dir}/arraymodule.so
%{dynload_dir}/audioop.so
%{dynload_dir}/binascii.so
%{dynload_dir}/bz2.so
%{dynload_dir}/cPickle.so
%{dynload_dir}/cStringIO.so
%{dynload_dir}/cmathmodule.so
%{dynload_dir}/cryptmodule.so
%{dynload_dir}/datetime.so
%{dynload_dir}/dbm.so
%{dynload_dir}/dlmodule.so
%{dynload_dir}/fcntlmodule.so
%{dynload_dir}/future_builtins.so
%{dynload_dir}/gdbmmodule.so
%{dynload_dir}/grpmodule.so
%{dynload_dir}/imageop.so
%{dynload_dir}/itertoolsmodule.so
%{dynload_dir}/linuxaudiodev.so
%{dynload_dir}/mathmodule.so
%{dynload_dir}/mmapmodule.so
%{dynload_dir}/nismodule.so
%{dynload_dir}/operator.so
%{dynload_dir}/ossaudiodev.so
%{dynload_dir}/parsermodule.so
%{dynload_dir}/pyexpat.so
%{dynload_dir}/readline.so
%{dynload_dir}/resource.so
%{dynload_dir}/selectmodule.so
%{dynload_dir}/spwdmodule.so
%{dynload_dir}/stropmodule.so
%{dynload_dir}/syslog.so
%{dynload_dir}/termios.so
%{dynload_dir}/timemodule.so
%{dynload_dir}/timingmodule.so
%{dynload_dir}/unicodedata.so
%{dynload_dir}/xxsubtype.so
%{dynload_dir}/zlibmodule.so

%dir %{site_packages}
%{site_packages}/README
%{pylibdir}/*.py*
%{pylibdir}/*.doc
%{pylibdir}/wsgiref.egg-info
%dir %{pylibdir}/bsddb
%{pylibdir}/bsddb/*.py*
%{pylibdir}/compiler
%dir %{pylibdir}/ctypes
%{pylibdir}/ctypes/*.py*
%{pylibdir}/ctypes/macholib
%{pylibdir}/curses
%dir %{pylibdir}/distutils
%{pylibdir}/distutils/*.py*
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%dir %{pylibdir}/email
%{pylibdir}/email/*.py*
%{pylibdir}/email/mime
%{pylibdir}/encodings
%{pylibdir}/hotshot
%{pylibdir}/idlelib
%dir %{pylibdir}/json
%{pylibdir}/json/*.py*
%{pylibdir}/lib2to3
%{pylibdir}/logging
%{pylibdir}/multiprocessing
%{pylibdir}/plat-linux2
%dir %{pylibdir}/sqlite3
%{pylibdir}/sqlite3/*.py*
%dir %{pylibdir}/test
%{pylibdir}/test/test_support.py*
%{pylibdir}/test/__init__.py*
%{pylibdir}/wsgiref
%{pylibdir}/xml
%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config
%{pylibdir}/config/Makefile
%dir %{_includedir}/python%{pybasever}
%{_includedir}/python%{pybasever}/%{_pyconfig_h}

%files libs
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/%{py_INSTSONAME}
%if 0%{?with_systemtap}
%{tapsetdir}/%{libpython_stp}
%doc systemtap-example.stp
%endif

%files devel
%defattr(-,root,root,-)
%{pylibdir}/config/*
%exclude %{pylibdir}/config/Makefile
%{_includedir}/python%{pybasever}/*.h
%exclude %{_includedir}/python%{pybasever}/%{_pyconfig_h}
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%if %{main_python}
%{_bindir}/python-config
%endif
%{_bindir}/python%{pybasever}-config
%{_libdir}/libpython%{pybasever}.so

%files tools
%defattr(-,root,root,755)
%doc Tools/modulator/README.modulator
%doc Tools/pynche/README.pynche
%{site_packages}/modulator
%{site_packages}/pynche
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*
%{_bindir}/modulator*
%{_bindir}/pynche*
%{_bindir}/pygettext*.py*
%{_bindir}/msgfmt*.py*
%{tools_dir}
%{demo_dir}
%{pylibdir}/Doc

%files -n %{tkinter}
%defattr(-,root,root,755)
%{pylibdir}/lib-tk
%{dynload_dir}/_tkinter.so

%files test
%defattr(-, root, root, -)
%{pylibdir}/bsddb/test
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/email/test
%{pylibdir}/json/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test/*
# These two are shipped in the main subpackage:
%exclude %{pylibdir}/test/test_support.py*
%exclude %{pylibdir}/test/__init__.py*
%{dynload_dir}/_ctypes_test.so
%{dynload_dir}/_testcapimodule.so

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

%changelog
* Wed Nov 07 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.6.8-2
- Patch 121 forces sys.platform to linux2
  related to issue http://bugs.python.org/issue12326

* Thu Apr 12 2012 David Malcolm <dmalcolm@redhat.com> - 2.6.8-1
- 2.6.8: refresh patch 102 (lib64), patch 52 (valgrind) and patch 110
(ctypes/SELinux); drop upstream patch 11 (tolower), patch 116 (CVE-2010-1634),
patch 117 (CVE-2010-2089), patch 118 (CVE-2008-5983); add patch 200 (Py_DEBUG
and _Py_HashSecret_Initialized); regenerate the autotool intermediates patch
(patch 300)

* Fri Feb 18 2011 BJ Dierkes <wdierkes@rackspace.com> - 2.6.5-6
- Added support for packages that build against stock python, and python26
  Resolves BZ#678690
- Added brp-multiple-python-bytecompile
- Added __multiple_python_os_install_post macro to macros.python26
- Added --without tests option to make building without tests optional
- Added Patch119: Python-2.6.5-parallel_build.patch.  Resolves Python 
  bug #10013: undefined reference to `_PyParser_Grammar` in parallel builds
  http://bugs.python.org/issue10013
- Added Patch120: Python-2.6.5-ioctl_test.patch.  Resolves Python
  bug #7564: test_ioctl may fail when run in background.
  http://bugs.python.org/issue7564
- Use 'make test' to run test suite, passing known failures via 
  EXTRATESTOPTS env variable. (deprecates ./runtests.sh).  Removes 
  Source6: runtests.sh

* Fri Jun  4 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.5-5
- ensure that the compiler is invoked with "-fwrapv" (rhbz#594819)
- CVE-2010-1634: fix various integer overflow checks in the audioop
module (patch 116)
- CVE-2010-2089: further checks within the audioop module (patch 117)
- CVE-2008-5983: the new PySys_SetArgvEx entry point from r81399 (patch 118)

* Tue May  4 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.5-4
- don't delete wsgiref.egg-info (rhbz:588426)

* Tue Apr  6 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.5-3
- drop the use of _isa as RHEL5's rpmbuild doesn't support it
- fix permissions on various data files and scripts
- mark /etc/macros.python26 as a config file

* Mon Mar 29 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.5-2
- add a %%check section, running the regression test suite and failing the
build if an unexpected error occurs
- fix stray doublelisting of config directory wildcard in devel subpackage
- valgrind grew a -devel subpackage in el5 ; disable for now on ppc

* Mon Mar 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.5-1
- update to 2.6.5: http://www.python.org/download/releases/2.6.5/
- update patch 110 so that it still applies in the face of upstream r78380
- regenerate autotooling patch
- fix permissions on macros.python26, suppress some noise from rpmlint, and
remove unnecessary arch-conditionality for patch 101 (Steve Traylen)

* Tue Mar 16 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-23
- add a macros.python26 file, to make it easy for modules to ensure that they
are byte-compiled with the correct python runtime (source 5)

* Mon Mar 15 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-22
- fixup distutils/unixccompiler.py to remove standard library path from
rpath (patch 17)
- really delete DOS batch files

* Thu Mar  4 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-21
- initial version of python26, based on python-2.6.4-20.fc13, setting
the __python_ver definition to 26
- update python-2.6.2-config.patch to use DBLIBVER=4.3, rather than 4.7
- drop the patches for using db-4.8 (we're using 4.3)
- turn off with_gdb_hooks and with_systemtap
- patch pyexpat.h to build against RHEL5's pyexpat-devel (patch 200), disabled
for now as it shows segfaults in testing
- change build requirement from valgrind-devel to valgrind (reflecting earlier
version of valgrind package)
- redefine __os_install_post to avoid using brp-python-bytecompile, and
thus ending up with .pyc/o files with the wrong magic value
- avoid shadowing /usr/bin/python-config
- drop trailing period from Summary of tkinter subpackage
- carry a patch against the configure script within the srpm, rather than
rerunning autoconf, as RHEL5's autoconf is too early to do this; add support to
the specfile for a maintainer to regenerate this patch
- remove shebang lines from .py files that aren't executable, and remove
executability from .py files that don't have a shebang line
- delete DOS batch files

* Thu Feb 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-20
- avoid having the "test" subdirectory and the files within it that are in the
core subpackage also be owned by the test subpackage (rhbz:467588)

* Wed Feb 10 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-19
- revise the systemtap patch (patch 55:python-2.6.4-dtrace.patch) to the
new version by mjw in attachment 390110 of rhbz:545179, as this should
eliminate the performance penalty for the case where the probes aren't in
use, and eliminate all architecture-specific code (rhbz:563541; except on
sparc)

* Tue Feb  9 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-18
- add a systemtap tapset defining "python.function.entry" and
"python.function.return" to make it easy to use the static probepoint within
Python; add an example of using the tapset to the docs

* Tue Feb  9 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-17
- add systemtap static probes (wcohen; patch 55; rh bug #545179)
- update some comments in specfile relating to gdb work
- manually byte-compile the gdb.py file with the freshly-built python to ensure
that .pyx and .pyo files make it into the debuginfo manifest if they are later
byte-compiled after find-debuginfo.sh is run

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-16
- move the -gdb.py file from %%{_libdir}/INSTSONAME-gdb.py to
%%{_prefix}/lib/debug/%%{_libdir}/INSTSONAME.debug-gdb.py to avoid noise from
ldconfig (bug 562980), and which should also ensure it becomes part of the
debuginfo subpackage, rather than the libs subpackage
- introduce %%{py_SOVERSION} and %%{py_INSTSONAME} to reflect the upstream
configure script, and to avoid fragile scripts that try to figure this out
dynamically (e.g. for the -gdb.py change)

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-15
- work around bug 562906 by supplying a fixed version of pythondeps.sh
- set %%{_python_bytecompile_errors_terminate_build} to 0 to prevent the broken
test files from killing the build on buildroots where python is installed

* Fri Feb  5 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-14
- add gdb hooks for easier debugging

* Fri Jan 29 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-13
- document all patches, and remove the commented-out ones

* Tue Jan 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-12
- Address some of the issues identified in package review (bug 226342):
  - update libs requirement on base package to use %%{name} for consistency's
sake
  - convert from backticks to $() syntax throughout
  - wrap value of LD_LIBRARY_PATH in quotes
  - convert "/usr/bin/find" requirement to "findutils"
  - remove trailing periods from summaries of -devel and -tools subpackages
  - fix spelling mistake in description of -test subpackage
  - convert usage of $$RPM_BUILD_ROOT to %%{buildroot} throughout, for
stylistic consistency
  - supply dirmode arguments to defattr directives

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-11
- update python-2.6.2-config.patch to remove downstream customization of build
of pyexpat and elementtree modules
- add patch adapted from upstream (patch 3) to add support for building against
system expat; add --with-system-expat to "configure" invocation
- remove embedded copy of expat from source tree during "prep"

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-10
- introduce macros for 3 directories, replacing expanded references throughout:
%%{pylibdir}, %%{dynload_dir}, %%{site_packages}
- explicitly list all lib-dynload files, rather than dynamically gathering the
payload into a temporary text file, so that we can be sure what we are
shipping; remove now-redundant testing for presence of certain .so files
- remove embedded copy of zlib from source tree before building

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-9
- change python-2.6.2-config.patch to remove our downstream change to curses
configuration in Modules/Setup.dist, so that the curses modules are built using
setup.py with the downstream default (linking against libncursesw.so, rather
than libncurses.so), rather than within the Makefile; add a test to %%install
to verify the dso files that the curses module is linked against the correct
DSO (bug 539917; changes _cursesmodule.so -> _curses.so)

* Fri Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-8
- rebuild (bug 556975)

* Wed Jan 20 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-7
- move lib2to3 from -tools subpackage to main package (bug 556667)

* Mon Jan 18 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-6
- patch Makefile.pre.in to avoid building static library (patch111, bug 556092)
- split up the "configure" invocation flags onto individual lines

* Fri Jan 15 2010 David Malcolm <dmalcolm@redhat.com> - 2.6.4-5
- replace usage of %%define with %%global
- use the %%{_isa} macro to ensure that the python-devel dependency on python
is for the correct multilib arch (#555943)
- delete bundled copy of libffi to make sure we use the system one
- replace references to /usr with %%{_prefix}; replace references to
/usr/include with %%{_includedir}

* Wed Dec 16 2009 David Malcolm <dmalcolm@redhat.com> - 2.6.4-4
- automatically disable arena allocator when run under valgrind (upstream
issue 2422; patch 52)
- add patch from Josh Boyer containing diff against upstream PyBSDDB to make
the bsddb module compile against db-4.8 (patch 53, #544275); bump the necessary
version of db4-devel to 4.8
- patch setup.py so that it searches for db-4.8, and enable debug output for
said search; make Setup.dist use db-4.8 (patch 54)

* Thu Nov 12 2009 David Malcolm <dmalcolm@redhat.com> - 2.6.4-3
- fixup the build when __python_ver is set (Zach Sadecki; bug 533989); use
pybasever in the files section

* Thu Oct 29 2009 David Malcolm <dmalcolm@redhat.com> - 2.6.4-2
- "Makefile" and the config-32/64.h file are needed by distutils/sysconfig.py
_init_posix(), so we include them in the core package, along with their parent
directories (bug 531901)

* Mon Oct 26 2009 David Malcolm <dmalcolm@redhat.com> - 2.6.4-1
- Update to 2.6.4

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.6.2-2
- rebuilt with new openssl

* Mon Jul 27 2009 James Antill <james.antill@redhat.com> - 2.6.2-1
- Update to 2.6.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 4 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.6-10
- Move python-config to devel subpackage (#506153)
- Update BuildRoot for new standard

* Sun Jun 28 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.6-9
- Update python-tools description (#448940)

* Wed Apr 15 2009 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 2.6-8
- Replace python-hashlib and python-uuid (#484715)

* Tue Mar 17 2009 James Antill <james@fedoraproject.org> - 2.6-7
- Use system libffi
- Resolves: bug#490573
- Fix SELinux execmem problems
- Resolves: bug#488396

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.6-4
- rebuild with new openssl

* Tue Jan  6 2009 James Antill <james.antill@redhat.com> - 2.6-3
- Fix distutils generated rpms.
- Resolves: bug#236535

* Wed Dec 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.6-2
- Enable -lcrypt for cryptmodule

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.6-1
- Update to 2.6

* Tue Sep 30 2008 James Antill <james.antill@redhat.com> - 2.5.2-1
- Move to 2.5.2
- Fix CVE-2008-2316 hashlib overflow.

* Thu Jul 17 2008 Jeremy Katz <katzj@redhat.com> - 2.5.1-30
- Fix up the build for new rpm
- And actually build against db4-4.7 (#455170)

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-27
- fix license tag
- enable support for db4-4.7

* Sun Jun 15 2008 James Antill <jantill@redhat.com> - 2.5.1-26
- Fix sporadic listdir problem
- Resolves: bug#451494

* Mon Apr  7 2008 James Antill <jantill@redhat.com> - 2.5.1-25
- Rebuild to re-gen autoconf file due to glibc change.
- Resolves: bug#441003

* Tue Mar 25 2008 James Antill <jantill@redhat.com> - 2.5.1-24
- Add more constants to socketmodule

* Sat Mar  8 2008 James Antill <jantill@redhat.com> - 2.5.1-22
- Add constants to socketmodule
- Resolves: bug#436560

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.1-22
- Autorebuild for GCC 4.3

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-21
- rebuild for new tk in rawhide

* Mon Jan  7 2008 James Antill <jantill@redhat.com> - 2.5.1-20
- Add valgrind support files, as doc, to python-devel
- Relates: rhbz#418621
- Add new API from 2.6, set_wakeup_fd ... use at own risk, presumably won't
- change but I have no control to guarantee that.
- Resolves: rhbz#427794
- Add gdbinit support file, as doc, to python-devel

* Fri Jan  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-19
- rebuild for new tcl/tk in rawhide

* Fri Dec  7 2007 James Antill <jantill@redhat.com> - 2.5.1-18
- Create a python-test sub-module, over 3MB of stuff noone wants.
- Don't remove egginfo files, try this see what happens ... may revert.
- Resolves: rhbz#414711

* Mon Dec  3 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-17
- rebuild for new libssl

* Fri Nov 30 2007 James Antill <jantill@redhat.com> - 2.5.1-16
- Fix pyconfig.h comment typo.
- Add back test_support.py and the __init__.py file.
- Resolves: rhbz#387401

* Tue Oct 30 2007 James Antill <jantill@redhat.com> - 2.5.1-15
- Do codec lowercase in C Locale.
- Resolves: 207134 191096
- Fix stupid namespacing in pysqlite, minimal upgrade to 2.3.3 pysqlite
- Resolves: 263221

* Wed Oct 24 2007 James Antill <jantill@redhat.com> - 2.5.1-14
- Remove bintuils dep. for live CD ... add work around for ctypes

* Mon Oct 22 2007 James Antill <jantill@redhat.com> - 2.5.1-13
- Add tix buildprereq
- Add tkinter patch
- Resolves: #281751
- Fix ctypes loading of libraries, add requires on binutils
- Resolves: #307221
- Possible fix for CVE-2007-4965 possible exploitable integer overflow
- Resolves: #295971

* Tue Oct 16 2007 Mike Bonnet <mikeb@redhat.com> - 2.5.1-12
- fix marshalling of objects in xmlrpclib (python bug #1739842)

* Fri Sep 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-11
- fix encoding of sqlite .py files to work around weird encoding problem 
  in Turkish (#283331)

* Mon Sep 10 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-10
- work around problems with multi-line plural specification (#252136)

* Tue Aug 28 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-9
- rebuild against new expat

* Tue Aug 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-8
- build against db4.6

* Tue Aug 14 2007 Dennis Gilmore <dennis@ausil.us> - 2.5.1-7
- add sparc64 to the list of archs for _pyconfig64_h

* Fri Aug 10 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-6
- fix ctypes again on some arches (Hans de Goede, #251637)

* Fri Jul  6 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-5
- link curses modules with ncursesw (#246385)

* Wed Jun 27 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-4
- fix _elementtree.so build (#245703)
- ensure that extension modules we expect are actually built rather than 
  having them silently fall out of the package

* Tue Jun 26 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-3
- link with system expat (#245703)

* Thu Jun 21 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-2
- rebuild to take advantage of hardlinking between identical pyc/pyo files

* Thu May 31 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-1
- update to python 2.5.1

* Mon Mar 19 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-12
- fix alpha build (#231961)

* Tue Feb 13 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-11
- tcl/tk was reverted; rebuild again

* Thu Feb  1 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-10
- rebuild for new tcl/tk

* Tue Jan 16 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.5.3-9
- link with ncurses

* Sat Jan  6 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-8
- fix extensions to use shared libpython (#219564)
- all 64bit platforms need the regex fix (#122304)

* Wed Jan  3 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-7
- fix ctypes to not require execstack (#220669)

* Fri Dec 15 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-6
- don't link against compat-db (Robert Scheck)

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> - 2.5.3-5
- fix invalid assert in debug mode (upstream changeset 52622)

* Tue Dec 12 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-4
- obsolete/provide python-ctypes (#219256)

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-3
- fix atexit traceback with failed syslog logger (#218214)
- split libpython into python-libs subpackage for multilib apps 
  embedding python interpreters

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-2
- disable installation of .egg-info files for now

* Tue Dec  5 2006 Jeremy Katz <katzj@redhat.com>
- support db 4.5
- obsolete python-elementtree; since it requires some code tweaks, don't 
  provide it
- obsolete old python-sqlite; provide the version that's actually included

* Mon Oct 30 2006 Jeremy Katz <katzj@redhat.com>
- fix _md5 and _sha modules (Robert Sheck)
- no longer provide optik compat; it's been a couple of years now
- no longer provide the old shm module; if this is still needed, let's 
  build it separately
- no longer provide japanese codecs; should be a separate package

* Mon Oct 23 2006 Jeremy Katz <katzj@redhat.com> - 2.5-0
- update to 2.5.0 final

* Fri Aug 18 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.c1
- Updated to 2.5c1. Merged fixes from FC6 too:
- Fixed bug #199373 (on some platforms CFLAGS is needed when linking)
- Fixed bug #198971 (case conversion not locale safe in logging library)
- Verified bug #201434 (distutils.sysconfig is confused by the change to make
  python-devel multilib friendly) is fixed upstream

* Sun Jul 16 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.b2
- Updated to 2.5b2 (which for comparison reasons is re-labeled 2.4.99.b2)

* Fri Jun 23 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.b1
- Updated to 2.5b1 (which for comparison reasons is re-labeled 2.4.99.b1)

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-11.FC6
- and fix it for real

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-10.FC6
- fix python-devel on ia64

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-9
- Fixed python-devel to be multilib friendly (bug #192747, #139911)

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-8
- Only copying mkhowto from the Docs - we don't need perl dependencies from
  python-tools.

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-7
- Fixed bug #121198 (webbrowser.py should use the user's preferences first)

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-6
- Fixed bug #192592 (too aggressive assertion fails) - SF#1257960
- Fixed bug #167468 (Doc/tools not included) - added in the python-tools package

* Thu Jun  8 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-5
- Fixed bug #193484 (added pydoc in the main package)

* Mon Jun  5 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-4
- Added dist in the release

* Mon May 15 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3
- rebuilt to fix broken libX11 dependency

* Wed Apr 12 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-2
- rebuild with new gcc to fix #188649

* Thu Apr  6 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-1
- Updated to 2.4.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.2.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3.2
- rebuilt for newer tix

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Mihai Ibanescu <misa@redhat.com> 2.4.2-3
- fixed #136654 for another instance of audiotest.au

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 19 2005 Bill Nottingham <notting@redhat.com> 2.4.2-2
- fix build for modular X, remove X11R6 path references

* Tue Nov 15 2005 Mihai Ibanescu <misa@redhat.com> 2.4.2-1
- Upgraded to 2.4.2
- BuildRequires autoconf

* Wed Nov  9 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-16
- Rebuilding against newer openssl.
- XFree86-devel no longer exists

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-14
- Once more -- this time, to fix -EPERM when you run it in a directory
  you can't read from.

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-13
- So, 5 or 6 people have said it works for them with this patch...

* Sun Sep 25 2005 Peter Jones <pjones@redhat.com> 2.4.1-12
- Fixed bug #169159 (check for argc>0 and argv[0] == NULL, not just
    argv[0][0]='\0')
  Reworked the patch from -8 a bit more.

* Fri Sep 23 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-10
- Fixed bug #169159 (don't let python core dump if no arguments are passed in)
  Reworked the patch from -8 a bit more.

* Thu Sep 22 2005 Peter Jones <pjones@redhat.com> 2.4.1-8
- Fix bug #169046 more correctly.

* Thu Sep 22 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-7
- Fixed bug #169046 (realpath is unsafe); thanks to 
  Peter Jones <pjones@redhat.com> and Arjan van de Ven <arjanv@redhat.com> for
  diagnosing and the patch.

* Tue Sep 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-4
- Fixed bug #168655 (fixes for building as python24)

* Tue Jul 26 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-3
- Fixed bug #163435 (pynche doesn't start))

* Wed Apr 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-2
- Fixed bug #143667 (python should own /usr/lib/python* on 64-bit systems, for
  noarch packages)
- Fixed bug #143419 (BuildRequires db4 is not versioned)

* Wed Apr  6 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-1
- updated to 2.4.1

* Mon Mar 14 2005 Mihai Ibanescu <misa@redhat.com> 2.4-6
- building the docs from a different source rpm, to decouple bootstrapping
  python from having tetex installed

* Fri Mar 11 2005 Dan Williams <dcbw@redhat.com> 2.4-5
- Rebuild to pick up new libssl.so.5

* Wed Feb  2 2005 Mihai Ibanescu <misa@redhat.com> 2.4-4
- Fixed security issue in SimpleXMLRPCServer.py (#146647)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.4-3
- Rebuilt for new readline.

* Mon Dec  6 2004 Jeff Johnson <jbj@jbj.org> 2.4-2
- db-4.3.21 returns DB_BUFFER_SMALL rather than ENOMEM (#141994).
- add Provide: python(abi) = 2.4
- include msgfmt/pygettext *.pyc and *.pyo from brp-python-bytecompile.

* Fri Dec  3 2004 Mihai Ibanescu <misa@redhat.com> 2.4-1
- Python-2.4.tar.bz2 (final)

* Fri Nov 19 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.c1.1
- Python-2.4c1.tar.bz2 (release candidate 1)

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.4-0.b2.4
- rebuild against db-4.3.21.

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.3
- fix the lib64 patch so that 64bit arches still look in /usr/lib/python...

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.2
- cryptmodule still needs -lcrypt (again)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.b2.1
- Updated to python 2.4b2 (and labeled it 2.4-0.b2.1 to avoid breaking rpm's
  version comparison)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-13
- Fixed bug #138112 (python overflows stack buffer) - SF bug 105470

* Tue Nov  2 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-12
- Fixed bugs #131439 #136023 #137863 (.pyc/.pyo files had the buildroot added)

* Tue Oct 26 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-11
- Fixed bug #136654 (python has sketchy audio clip)

* Tue Aug 31 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-10
- Fixed bug #77418 (Demo dir not packaged)
- More tweaking on #19347 (Moved Tools/ under /usr/lib/python2.3/Tools)

* Fri Aug 13 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-8
- Fixed bug #129769: Makefile in new python conflicts with older version found
  in old python-devel
- Reorganized the spec file to get rid of the aspython2 define; __python_ver
  is more powerful.

* Tue Aug  3 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-7
- Including html documentation for non-i386 arches
- Fixed #125362 (python-doc html files have japanese character encoding)
- Fixed #128923 (missing dependency between python and python-devel)

* Fri Jul 30 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-6
- Fixed #128030 (help() not printing anything)
- Fixed #125472 (distutils.sysconfig.get_python_lib() not returning the right
  path on 64-bit systems)
- Fixed #127357 (building python as a shared library)
- Fixed  #19347 (including the contents of Tools/scripts/ in python-tools)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-3
- Added an optik.py that provides the same interface from optparse for
  backward compatibility; obsoleting python-optik

* Mon Jun  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-2
- Patched bdist_rpm to allow for builds of multiple binary rpms (bug #123598)

* Fri Jun  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-1
- Updated to 2.3.4-1 with Robert Scheck's help (bug #124764)
- Added BuildRequires: tix-devel (bug #124918)

* Fri May  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-6
- Correct fix for #122304 from upstream:
  http://sourceforge.net/tracker/?func=detail&atid=105470&aid=931848&group_id=5470

* Thu May  6 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-4
- Fix for bug #122304 : splitting the domain name fails on 64-bit arches
- Fix for bug #120879 : including Makefile into the main package

- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 16 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-3
- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 19 2003 Jeff Johnson <jbj@jbj.org> 2.3.3-1
- upgrade to 2.3.3.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-9
- rebuild against db-4.2.52.

* Fri Dec 12 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-8
- more rebuilding for new tcl/tk

* Wed Dec  3 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-7.1
- rebuild against db-4.2.42.

* Fri Nov 28 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-7
- rebuilt against newer tcl/tk

* Mon Nov 24 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-6
- added a Provides: python-abi

* Wed Nov 12 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-5
- force CC (#109268)

* Sun Nov  9 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-4
- cryptmodule still needs -lcrypt

* Wed Nov  5 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-2
- Added patch for missing mkhowto

* Thu Oct 16 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-1
- Updated to 2.3.2

* Thu Sep 25 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-1
- 2.3.1 final

* Tue Sep 23 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-0.8.RC1
- Building the python 2.3.1 release candidate
- Updated the lib64 patch

* Wed Jul 30 2003 Mihai Ibanescu <misa@redhat.com> 2.3-0.2
- Building python 2.3
- Added more BuildRequires
- Updated the startup files for modulator and pynche; idle installs its own
  now.

* Thu Jul  3 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-4
- Rebuilt against newer db4 packages (bug #98539)

* Mon Jun 9 2003 Elliot Lee <sopwith@redhat.com> 2.2.3-3
- rebuilt

* Wed Jun  7 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-2
- Rebuilt

* Tue Jun  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-1
- Upgraded to 2.2.3

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-28
- Rebuilt

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-27
- Modified the ftpuri patch conforming to http://ietf.org/rfc/rfc1738.txt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-25
- Fixed bug #84886: pydoc dies when run w/o arguments
- Fixed bug #84205: add python shm module back (used to be shipped with 1.5.2)
- Fixed bug #84966: path in byte-compiled code still wrong

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-23
- ftp uri's should be able to specify being rooted at the root instead of 
  where you login via ftp (#84692)

* Mon Feb 10 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-22
- Using newer Japanese codecs (1.4.9). Thanks to 
  Peter Bowen <pzb@datastacks.com> for pointing this out.

* Thu Feb  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-21
- Rebuild

* Wed Feb  5 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-20
- Release number bumped really high: turning on UCS4 (ABI compatibility
  breakage)

* Fri Jan 31 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-13
- Attempt to look both in /usr/lib64 and /usr/lib/python2.2/site-packages/:
  some work on python-2.2.2-lib64.patch

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-12
- Rebuild to incorporate the removal of .lib64 and - files.

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-11.7.3
- Fixed bug #82544: Errata removes most tools
- Fixed bug #82435: Python 2.2.2 errata breaks redhat-config-users
- Removed .lib64 and - files that get installed after we fix the multilib
  .py files.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 2.2.2-10
- rebuild to update tkinter's tcltk deps
- convert changelog to utf-8

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.2-9
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- pick up OpenSSL cflags and ldflags from pkgconfig if available

* Thu Jan  2 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-8
- urllib2 didn't support non-anonymous ftp.  add support based on how 
  urllib did it (#80676, #78168)

* Mon Dec 16 2002 Mihai Ibanescu <misa@redhat.com> 2.2.2-7
- Fix bug #79647 (Rebuild of SRPM fails if python isn't installed)
- Added a bunch of missing BuildRequires found while fixing the
  above-mentioned bug

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 2.2.2-6
- rebuild to fix broken tcltk deps for tkinter

* Fri Nov 22 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.7.3
- Recompiled for 7.3 (to fix the -lcrypt bug)
- Fix for the spurious error message at the end of the build (build-requires
  gets confused by executable files starting with """"): make the tests
  non-executable.

* Wed Nov 20 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-5
- Fixed configuration patch to add -lcrypt when compiling cryptmodule.c

2.2.2-4
- Spec file change from Matt Wilson <msw@redhat.com> to disable linking 
  with the C++ compiler.

* Mon Nov 11 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.*
- Merged patch from Karsten Hopp <karsten@redhat.de> from 2.2.1-17hammer to
  use %%{_libdir}
- Added XFree86-libs as BuildRequires (because of tkinter)
- Fixed duplicate listing of plat-linux2
- Fixed exclusion of lib-dynload/japanese
- Added lib64 patch for the japanese codecs
- Use setup magic instead of using tar directly on JapaneseCodecs

* Tue Nov  5 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-2
- Fix #76912 (python-tools contains idle, which uses tkinter, but there is no
  requirement of tkinter from python-tools).
- Fix #74013 (rpm is missing the /usr/lib/python2.2/test directory)

* Mon Nov  4 2002 Mihai Ibanescu <misa@redhat.com>
- builds as python2 require a different libdb
- changed the buildroot name of python to match python2 builds

* Fri Nov  1 2002 Mihai Ibanescu <misa@redhat.com>
- updated python to 2.2.2 and adjusted the patches accordingly

* Mon Oct 21 2002 Mihai Ibanescu <misa@redhat.com>
- Fix #53930 (Python-2.2.1-buildroot-bytecode.patch)
- Added BuildPrereq dependency on gcc-c++

* Fri Aug 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-17
- security fix for _execvpe

* Tue Aug 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-16
- Fix  #71011,#71134, #58157

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-15
- Resurrect tkinter
- Fix for distutils (#67671)
- Fix #69962

* Thu Jul 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-14
- Obsolete tkinter/tkinter2 (#69838)

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-13
- Doc fixes (#53951) - not on alpha at the momemt

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-12
- fix pydoc (#68082)

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-11
- Add db4-devel as a BuildPrereq

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.2.1-10
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-9
- Add Japanese codecs (#66352)

* Tue Jun 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-8
- No more tkinter...

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-7
- Rebuild

* Tue May 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-6
- Add the email subcomponent (#65301)

* Fri May 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-5
- Rebuild

* Thu May 02 2002 Than Ngo <than@redhat.com> 2.2.1-4
- rebuild i new enviroment

* Tue Apr 23 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Use ucs2, not ucs4, to avoid breaking tkinter (#63965)

* Mon Apr 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-2
- Make it use db4

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-1
- 2.2.1 - a bugfix-only release

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-16
- the same, but in builddirs - this will remove them from the 
  docs package, which doesn't look in the buildroot for files.

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-15
- Get rid of temporary files and .cvsignores included 
  in the tarball and make install

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-14
- Don't own lib-tk in main package, only in tkinter (#62753)

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-13
- rebuild

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-12
- rebuild

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-11
- Add a not to the Distutils obsoletes test (doh!)

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-10
- Rebuild

* Mon Feb 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-9
- Only obsolete Distutils when built as python

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-8
- Make files in /usr/bin install side by side with python 1.5 when
- Drop explicit requirement of db4
  built as python2

* Thu Jan 31 2002 Elliot Lee <sopwith@redhat.com> 2.2-7
- Use version and pybasever macros to make updating easy
- Use _smp_mflags macro

* Tue Jan 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-6
- Add db4-devel to BuildPrereq

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.2-5
- disable ndbm support, which is db2 in disguise (really interesting things
  can happen when you mix db2 and db4 in a single application)

* Thu Jan 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-4
- Obsolete subpackages if necesarry 
- provide versioned python2
- build with db4

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-3
- Alpha toolchain broken. Disable build on alpha.
- New openssl

* Wed Dec 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-1
- 2.2 final

* Fri Dec 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.11c1
- 2.2 RC 1
- Don't include the _tkinter module in the main package - it's 
  already in the tkiter packace
- Turn off the mpzmodule, something broke in the buildroot

* Wed Nov 28 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.10b2
- Use -fPIC for OPT as well, in lack of a proper libpython.so

* Mon Nov 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.9b2
- changed DESTDIR to point to / so that distutils will install dynload
  modules properly in the installroot

* Fri Nov 16 2001 Matt Wilson <msw@redhat.com> 2.2-0.8b2
- 2.2b2

* Fri Oct 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.7b1
- python2ify

* Fri Oct 19 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.5b1
- 2.2b1

* Sun Sep 30 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.4a4
- 2.2a4
- Enable UCS4 support
- Enable IPv6
- Provide distutils
- Include msgfmt.py and pygettext.py

* Fri Sep 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.3a3
- Obsolete Distutils, which is now part of the main package
- Obsolete python2

* Thu Sep 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.2a3
- Add docs, tools and tkinter subpackages, to match the 1.5 layout

* Wed Sep 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.1a3
- 2.2a3
- don't build tix and blt extensions

* Mon Aug 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add tk and tix to build dependencies

* Sat Jul 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.1 bugfix release - with a GPL compatible license

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add new build dependencies (#49753)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- build with -fPIC

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1
- reorganization of file includes

* Wed Dec 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the "requires" clause, it lacked a space causing problems
- use %%{_tmppath}
- don't define name, version etc
- add the available patches from the Python home page

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- added devel subpackage

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- modify all files to use "python2.0" as the intrepter
- don't build the Expat bindings
- build against db1

* Mon Oct 16 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0 final

* Mon Oct  9 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0c1
- build audioop, imageop, and rgbimg extension modules
- include xml.parsers subpackage
- add test.xml.out to files list

* Thu Oct  5 2000 Jeremy Hylton <jeremy@beopen.com>
- added bin/python2.0 to files list (suggested by Martin v. L?)

* Tue Sep 26 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for release 1 of 2.0b2
- use .bz2 version of Python source

* Tue Sep 12 2000 Jeremy Hylton <jeremy@beopen.com>
- Version 2 of 2.0b1
- Make the package relocatable.  Thanks to Suchandra Thapa.
- Exclude Tkinter from main RPM.  If it is in a separate RPM, it is
  easier to track Tk releases.
