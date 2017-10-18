%bcond_without pgm

Name:           zeromq
Version:        4.1.4
Release:        6%{?dist}
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.zeromq.org
# VCS:          git:http://github.com/zeromq/zeromq2.git
Source0:        http://download.zeromq.org/zeromq-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/zeromq/cppzmq/master/zmq.hpp
Source2:        https://raw.githubusercontent.com/zeromq/cppzmq/master/LICENSE

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libsodium-devel

BuildRequires:  glib2-devel
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
BuildRequires:  e2fsprogs-devel
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%else
BuildRequires:  libuuid-devel
%endif
%if %{with pgm}
BuildRequires:  openpgm-devel
BuildRequires:  krb5-devel
%endif

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n cppzmq-devel
Summary:        Development files for cppzmq
Group:          Development/Libraries
License:        MIT
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}


%description -n cppzmq-devel
The cppzmq-devel package contains libraries and header files for
developing applications that use the C++ header files of %{name}.


%prep
%setup -q
cp -a %{SOURCE2} .

# zeromq.x86_64: W: file-not-utf8 /usr/share/doc/zeromq/ChangeLog
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure

# Sed version number of openpgm into configure
%global openpgm_pc $(basename %{_libdir}/pkgconfig/openpgm*.pc .pc)
sed -i "s/openpgm-[0-9].[0-9]/%{openpgm_pc}/g" \
    configure*


%build
autoreconf -fi
# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure
%configure \
%if %{with pgm}
            --with-pgm \
            --with-libgssapi_krb5 \
%endif
            --disable-static
make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -m 644 -p %{SOURCE1} %{buildroot}%{_includedir}/

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la


## %%check
## make check V=1


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog MAINTAINERS NEWS
%license COPYING COPYING.LESSER
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.*

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*.h
%{_mandir}/man3/zmq*
%{_mandir}/man7/zmq*

%files -n cppzmq-devel
%license LICENSE
%{_includedir}/zmq.hpp


%changelog
* Tue Oct 17 2017 SaltStack Packaging Team <packaging@saltstack.com> - 4.1.4-6
- Disabled check due to build failue on RHEL 7

* Mon Mar 07 2016 Remi Collet <remi@fedoraproject.org> - 4.1.4-5
- rebuild for new libsodium soname

* Sun Feb 14 2016 Thomas Spura <tomspur@fedoraproject.org> - 4.1.4-4
- Remove Werror from compile flags

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Thomas Spura <tomspur@fedoraproject.org> - 4.1.4-2
- Enable krb5 and fix building of pgm (#1301197)

* Sat Dec 19 2015 Thomas Spura <tomspur@fedoraproject.org> - 4.1.4-1
- update to 4.1.4 (#1292814)
- refresh zmq.hpp

* Mon Aug 24 2015 Thomas Spura <tomspur@fedoraproject.org> - 4.1.3-1
- update to 4.1.3 (#1256209)
- ipv6 patch included upstream
- refresh zmq.hpp

* Tue Jun 23 2015 Thomas Spura <tomspur@fedoraproject.org> - 4.1.2-1
- update to 4.1.2
- add upstream patch to fix problem with ipv6

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Thomas Spura <tomspur@fedoraproject.org> - 4.0.5-4
- Add zmq.hpp, which originally belonged to zeromq:
  https://github.com/zeromq/cppzmq/issues/48

* Tue May 19 2015 Thomas Spura <tomspur@fedoraproject.org> - 4.0.5-3
- Cherry-pick patch for protocol downgrade attack (#1221666, CVE-2014-9721)
- Remove Obsoletes:zeromq-utils
- Remove %%defattr

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.0.5-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Nov 17 2014 Thomas Spura <tomspur@fedoraproject.org> - 4.0.5-1
- update to 4.0.5

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-7
- Rebuilt for openpm-5.2 and sed correct version into configure (#963894)

* Wed Mar 27 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-6
- run autoreconf before configure so aarch64 is supported (#926859)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-4
- delete foreign files with dubious license in %%prep (#892111)

* Mon Dec 24 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-3
- add bcond_without pgm macro (Jose Pedro Oliveira, #867182)
- remove bundled pgm
- build against openpgm

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Sat Jan  7 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.11-1
- update to 2.1.11 (as part of rebuilding with gcc-4.7)

* Tue Sep 20 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-1
- update to 2.1.9
- add check section

* Wed Apr  6 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-1
- update to new version (#690199)

* Wed Mar 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.3-1
- update to new version (#690199)
- utils subpackage was removed upstream
  (obsolete it)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Pavel Zhukov <pavel@zhukoff.net> - 2.0.10-1
- update version
- add rpath delete
- change includedir filelist

* Fri Aug 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-1
- update to new version

* Fri Jul 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-4
- upstream VCS changed
- remove buildroot / %%clean
- change descriptions

* Tue Jul 20 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-3
- move binaries to seperate utils package

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-2
- remove BR: libstdc++-devel
- move man3 to the devel package
- change group to System Environment/Libraries

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.7-1
- initial package (based on upstreams example one)
