Name:           libtommath
Version:        0.42.0
Release:        4%{?dist}
Summary:        A portable number theoretic multiple-precision integer library
License:        Public Domain
URL:            http://www.libtom.org/?page=features&newsitems=5&whatfile=ltm

Source0:        http://www.libtom.org/files/ltm-%{version}.tar.bz2
Patch0:         %{name}-makefile.patch

BuildRequires:  ghostscript
BuildRequires:  libtool

%if 0%{?rhel} == 6
BuildRequires:  libtiff
%else
BuildRequires:  libtiff-tools
%endif

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  tex(dvips)
BuildRequires:  tex(latex)
%else
BuildRequires:  tetex-dvips
BuildRequires:  tetex-latex
%endif

%description
A free open source portable number theoretic multiple-precision integer library
written entirely in C. (phew!). The library is designed to provide a simple to
work with API that provides fairly efficient routines that build out of the box
without configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.42-1

%description    doc
The %{name}-doc package contains PDF documentation for using %{name}.

%prep
%setup -q
%patch0 -p1 -b .makefile

%build
# no configure script ships with libtommath. Its only requirement is ANSI C.
export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} LIBPATH=%{_libdir} -f makefile.shared 
%ifnarch ppc64le
  DOCS="docs"
%endif
make %{?_smp_mflags} -f makefile poster manual $DOCS

%install
# There is no configure script that ships with libtommath but it does understand
# DESTDIR and it installs via that and the INSTALL_USER and INSTALL_GROUP
# environment variables.
export INSTALL_USER=$(id -un)
export INSTALL_GROUP=$(id -gn)
make install DESTDIR=%{buildroot} LIBPATH=%{_libdir} -f makefile.shared
find %{buildroot} -name '*.h' -exec chmod 644 {} \;
find %{buildroot} -name '*.c' -exec chmod 644 {} \;
chmod 644 LICENSE

find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so

%files doc
%doc bn.pdf poster.pdf tommath.pdf

%changelog
* Mon Dec 07 2015 Jaromir Capik <jcapik@redhat.com> - 0.42.0-4
- Workaround for ghostscript segfault on ppc64le

* Sun Sep 29 2013 Simone Caronni <negativo17@gmail.com> - 0.42.0-3
- Move headers to default location.

* Thu Aug 08 2013 Simone Caronni <negativo17@gmail.com> - 0.42.0-2
- Fix changelog entries.
- Remove executable bits from LICENSE file and source files.

* Thu Aug 08 2013 Simone Caronni <negativo17@gmail.com> - 0.42.0-1
- Update to 0.42.
- Make doc package noarch and not requiring base package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Simone Caronni <negativo17@gmail.com> - 0.41-16
- SPEC file cleanup, remove obsolete tags.
- Fix tex/latex BuildRequires.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.41-11
- fix bugs #555445 and #591543

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.41-8
- Autorebuild for GCC 4.3

* Sun Nov 25 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.41-7
- Resolve multilib conflicts from Bug #342441 by splitting out
  documentation to libtommath-docs subpackage
- fix rpmlint Summary: warning

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.41-6
- Rebuild for selinux ppc32 issue.

* Fri Jun 29 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.41-5
- removed package name from summary
 
* Wed Jun 27 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.41-4
- changed patch to honor RPM_OPT_FLAGS
- changed patch to allow INCPATH to be set externally
- changed installation of headers to _includedir/tommath

* Sun Jun 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.41-3
- changed patch to bring it into line with the style of libtomcrypt 

* Sat Jun 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.41-2
- add patch to makefile.shared to allow for /usr/lib64 installs
- update spec to pass libdir build and install process

* Fri Jun 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.41-1
- Initial spec file creation
