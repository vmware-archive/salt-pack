Name:          openpgm
Version:       5.2.122
Release:       2%{?dist}
Summary:       An implementation of the PGM reliable multicast protocol

Group:         System Environment/Libraries
# The license is LGPLv2.1
License:       LGPLv2
URL:           http://openpgm.googlecode.com/
Source0:       http://openpgm.googlecode.com/files/libpgm-%{version}~dfsg.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python


%description
OpenPGM is an open source implementation of the Pragmatic General
Multicast (PGM) specification in RFC 3208.


%package devel
Summary:       Development files for openpgm
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains OpenPGM related development libraries and header files.


%prep
%setup -q -n libpgm-%{version}~dfsg/openpgm/pgm

%build
%configure
make %{_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm %{buildroot}%{_libdir}/libpgm.{a,la}

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING LICENSE
%{_libdir}/*.so.*


%files devel
%doc examples/
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/openpgm-5.2.pc


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.2.122-1
- Update to 5.2.122

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.118-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-3
- Build requires python (no longer available by default in F18+ buildroots)

* Fri Dec 21 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-2
- Renamed the tarball (replaced '%7E' by '~')
- Removed the defattr lines

* Wed Dec 19 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-1
- Change license from LGPLv2.1 to LGPLv2 (867182#c13)

* Tue Dec 18 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-0
- First Fedora specfile

# vim:set ai ts=4 sw=4 sts=4 et:
