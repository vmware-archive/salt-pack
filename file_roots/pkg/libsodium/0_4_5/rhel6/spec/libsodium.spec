Name:           libsodium
Version:        0.4.5
Release:        3%{?dist}
Summary:        A fork of networking and cryptography library with compatible APIs
License:        ISC
URL:            https://github.com/jedisct1/libsodium
Source0:        http://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz

%description
Sodium is a portable, cross-compilable, installable, packageable library 
forked from NaCl(networking and cryptography library), with a compatible API. 
Its goal is to provide all of the core operations needed to build higher-level
cryptographic tools.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.

%prep
%setup -q
# EPEL6 hack.
%if 0%{?rhel} == 6
sed -i 's|_pkg_min_version=0.25|_pkg_min_version=0.23|g' configure
%endif

%build
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog LICENSE README.markdown THANKS
%{_libdir}/libsodium.so.*

%files devel
%doc test/default/*.{c,h}
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/libsodium.so
%{_libdir}/pkgconfig/libsodium.pc

%changelog
* Mon Dec 09 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-3
- Disable silent build rules.
- Preserve the timestamp.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-2
- Add doc for devel package.
- Add support for EPEL6.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-1
- New version.

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-2
- Drop useless files.
- Improve the description.

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-1
- Initial Package.
