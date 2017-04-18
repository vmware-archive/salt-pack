Name:           libtomcrypt
Version:        1.17
Release:        23%{?dist}
Summary:        A comprehensive, portable cryptographic toolkit

License:        Public Domain
URL:            http://www.libtom.org/?page=features&newsitems=5&whatfile=crypt
Source0:        http://www.libtom.org/files/crypt-%{version}.tar.bz2
Patch0:         %{name}-makefile.patch
Patch1:         %{name}-pkgconfig.patch
Patch2:         %{name}-two-key-triple-des.patch

BuildRequires:  ghostscript
BuildRequires:  libtommath-devel >= 0.42.0-3
BuildRequires:  libtool

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  tex(dvips)
BuildRequires:  tex(latex)
%else
BuildRequires:  tetex-dvips
BuildRequires:  tetex-latex
%endif

Requires:       libtommath >= 0.42.0

%description
A comprehensive, modular and portable cryptographic toolkit that provides
developers with a vast array of well known published block ciphers, one-way hash
functions, chaining modes, pseudo-random number generators, public key
cryptography and a plethora of other routines.

Designed from the ground up to be very simple to use. It has a modular and
standard API that allows new ciphers, hashes and PRNGs to be added or removed
without change to the overall end application. It features easy to use functions
and a complete user manual which has many source snippet examples. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < 1.17-19


%description    doc
The %{name}-doc package contains documentation for use with %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# No configure script ships with libtomcrypt. Its only requirement is ANSI C and
# libtommath. Explicitly force it to be built against libtommath.
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC"
make %{?_smp_mflags} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared 

# workaround only - ghostscript segfaults on ppc64le -> can't build docs
%ifnarch ppc64le
  DOCS="docs"
%endif
make %{?_smp_mflags} LIBPATH=%{_libdir} -f makefile $DOCS

%check
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC -DUSE_LTM"
make %{?_smp_mflags} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" test
./test

%install
# There is no configure script that ships with libtomcrypt but it does
# understand DESTDIR and its installs via that and the INSTALL_USER and
# INSTALL_GROUP environment variables.
export INSTALL_USER=$(id -un)
export INSTALL_GROUP=$(id -gn)
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC -DUSE_LTM"

make install DESTDIR=%{buildroot} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared
find %{buildroot} -name '*.h' -exec chmod 644 {} \;
find %{buildroot} -name '*.c' -exec chmod 644 {} \;
chmod 644 LICENSE

# Remove unneeded files
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name 'libtomcrypt_prof*' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libtomcrypt.pc

%files doc
%doc LICENSE doc/crypt.pdf

%changelog
* Tue Dec 08 2015 Jaromir Capik <jcapik@redhat.com> - 1.17-23
- Workaround for ghostscript segfault on ppc64le

* Thu May 15 2014 Paul Howarth <paul@city-fan.org> - 1.17-22
- Add two-key 3DES support, needed by pycrypto.

* Sun Sep 29 2013 Simone Caronni <negativo17@gmail.com> - 1.17-21
- Move headers to default location.

* Thu Aug 08 2013 Simone Caronni <negativo17@gmail.com> - 1.17-20
- Make doc package noarch.
- Remove executable bits from LICENSE file and source files.
- Require isaed library for devel subpackage.
- Require CVE fixed libtommath library.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Simone Caronni <negativo17@gmail.com> - 1.17-18
- Fix build requirements for RHEL 6 and Fedora 17.

* Tue Jun 04 2013 David Woodhouse <David.Woodhouse@intel.com> - 1.17-17
- Fix tex/latex BuildRequires

* Mon Jun 03 2013 Simone Caronni <negativo17@gmail.com> - 1.17-16
- Update SPEC, remove obsolete tags, fix formatting.
- Add patch for pkg config (libtomcrypt.pc).
- Add correct build requirements for Fedora 19+ and RHEL 7+.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.17-9
- Autorebuild for GCC 4.3

* Sun Nov 25 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.17-8
- Resolve multilib conflicts from Bug #342431 by splitting out 
  documentation to libtomcrypt-docs subpackage
- fix rpmlint Summary: warning

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.17-7
- Rebuild for selinux ppc32 issue.

* Tue Jul 10 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-6
- turn off optimization for ppc64 to work around Bug #239003

* Sat Jun 30 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-5
- removed package name from summary
- fixed URL and Source0 links
- really fixed linkage flag this time, added it to the build section not
  just the check.

* Fri Jun 29 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-4
- fixed linkage flag with correct tommath name
- added check section
- removed libtomcrypt_prof libraries from package
- remove package name from summary

* Wed Jun 27 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-3
- create makefile patch to ensure RPM_OPT_FLAGS is honored
- install headers into _includedir/tomcrypt
- add location of libtommath headers to CFLAGS

* Sat Jun 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-2
- update build process to pass LIBPATH to make

* Fri Jun 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.17-1
- Initial spec file creation
