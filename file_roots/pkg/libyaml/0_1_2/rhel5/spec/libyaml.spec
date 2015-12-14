%define tarballname yaml

#====================================================================#

Name:       libyaml
Version:    0.1.2
Release:    8%{?dist}
Summary:    YAML 1.1 parser and emitter written in C

Group:      System Environment/Libraries
License:    MIT
URL:        http://pyyaml.org/
Source0:    http://pyyaml.org/download/libyaml/%{tarballname}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf, automake, libtool

# CVE-2013-6393
# https://bugzilla.redhat.com/show_bug.cgi?id=1033990
Patch0:     libyaml-CVE-2013-6393-string-overflow.patch
Patch1:     libyaml-CVE-2013-6393-node-id-hardening.patch
Patch2:     libyaml-CVE-2013-6393-indent-and-flow-overflow-1-of-3.patch
Patch3:     libyaml-CVE-2013-6393-indent-and-flow-overflow-2-of-3.patch
Patch4:     libyaml-CVE-2013-6393-indent-and-flow-overflow-3-of-3.patch
Patch5:     libyaml-CVE-2014-2525-URL-buffer-overflow.patch
Patch6:     libyaml-CVE-2014-9130.patch

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.


%package devel
Summary:   Development files for LibYAML applications
Group:     Development/Libraries
Requires:  libyaml = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use LibYAML.


%prep
%setup -q -n %{tarballname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
autoreconf -i -f
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/*.{la,a}


%check
make check


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/%{name}*.so.*


%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_libdir}/%{name}*.so
%{_includedir}/yaml.h


%changelog
* Mon Dec  1 2014 John Eckersberg <eck@redhat.com> - 0.1.2-8
- Add patch for CVE-2014-9130 (RHBZ#1169372)

* Thu Mar 27 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.2-7
- Add patch for CVE-2014-2525 (bz1078083)

* Tue Feb 11 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.2-6
- Add updated indent/flow patches for CVE-2013-6393 (bz1063867)

* Wed Jan 29 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.2-5
- Add patches for CVE-2013-6393 (bz1033990)

* Wed Jul 22 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-4
- Minor tweaks to spec file
- Enable %%check section
- Thanks Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-3
- Remove static libraries

* Thu Feb 26 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-2
- Remove README and LICENSE from docs on -devel package
- Remove -static package and merge contents into the -devel package

* Wed Feb 25 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-1
- Initial packaging for Fedora
