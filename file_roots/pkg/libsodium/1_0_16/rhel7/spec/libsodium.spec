# Fedora spec file for libsodium
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global libname libsodium
%global soname  23

Name:           libsodium
Version:        1.0.16
Release:        1%{?dist}
Summary:        The Sodium crypto library
License:        ISC
URL:            http://libsodium.org/
Source0:        http://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz

# manage update from 3rd party repository
Obsoletes:      %{libname}%{soname} <= %{version}


%description
Sodium is a new, easy-to-use software library for encryption, decryption, 
signatures, password hashing and more. It is a portable, cross-compilable, 
installable, packageable fork of NaCl, with a compatible API, and an extended 
API to improve usability even further. Its goal is to provide all of the core 
operations needed to build higher-level cryptographic tools. The design 
choices emphasize security, and "magic constants" have clear rationales.

The same cannot be said of NIST curves, where the specific origins of certain 
constants are not described by the standards. And despite the emphasis on 
higher security, primitives are faster across-the-board than most 
implementations of the NIST standards.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{libname}%{soname}-devel <= %{version}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.

%package        static
Summary:        Static library for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes:      %{libname}%{soname}-static <= %{version}

%description    static
This package contains the static library for statically
linking applications to use %{name}.


%prep
%setup -q


%build
%configure \
  --disable-silent-rules \
  --disable-opt

%make_build


%install
%make_install

rm -f %{buildroot}%{_libdir}/%{libname}.la


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,exp,h}
%doc test/quirks/quirks.h
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc

%files static
%{_libdir}/libsodium.a


%changelog
* Wed Jan 17 2018 Remi Collet <remi@remirepo.net> - 1.0.16-1
- update to 1.0.16
- soname bump to 23 (libsodium13 compat package exists)
- manage update from libsodium23 (3rd party repository)
- Add static library subpackage
- fix license management

* Sun Oct 25 2015 Christopher Meng <rpm@cicku.me> - 1.0.5-1
- Update to 1.0.5

* Mon Jul 13 2015 Christopher Meng <rpm@cicku.me> - 1.0.3-1
- Update to 1.0.3

* Fri Jan 23 2015 Christopher Meng <rpm@cicku.me> - 1.0.2-1
- Update to 1.0.2

* Sat Nov 22 2014 Christopher Meng <rpm@cicku.me> - 1.0.1-1
- Update to 1.0.1

* Sat Oct 18 2014 Christopher Meng <rpm@cicku.me> - 1.0.0-1
- Update to 1.0.0

* Sun Aug 24 2014 Christopher Meng <rpm@cicku.me> - 0.7.0-1
- Update to 0.7.0

* Thu Jul 17 2014 Christopher Meng <rpm@cicku.me> - 0.6.1-1
- Update to 0.6.1

* Thu Jul 03 2014 Christopher Meng <rpm@cicku.me> - 0.6.0-1
- Update to 0.6.0

* Fri May 16 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-1
- Update to 0.5.0

* Mon Dec 09 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-3
- Disable silent build rules.
- Preserve the timestamp.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-2
- Add doc for devel package.
- Add support for EPEL6.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-1
- Update to 0.4.5

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-2
- Drop useless files.
- Improve the description.

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-1
- Initial Package.
