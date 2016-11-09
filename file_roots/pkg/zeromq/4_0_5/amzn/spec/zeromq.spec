Name:           zeromq
Version:        4.0.5
Release:        4%{?dist}
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.zeromq.org
Source0:        http://download.zeromq.org/zeromq-%{version}.tar.gz
Patch0:         zeromq-4.0.5-downgrade-attack.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  glib2-devel
%if ! (0%{?rhel} > 5)
BuildRequires:  e2fsprogs-devel
%else
BuildRequires:  libuuid-devel
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


%prep
%setup -q
%patch0 -p1

# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure


%build
%configure \
  --with-pgm \
  --disable-static \
  --with-pic
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# remove *.la
find %{buildroot} -name \*.la -print0 | xargs -r0 rm -v

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*
%{_mandir}/man3/zmq*
%{_mandir}/man7/zmq*


%changelog
* Wed Nov  4 2015 Salt Stack Packaging Team <packaging@salttstack.com> - 4.0.5-4
- Update to ZeroMQ 4.0.5-4 stable release.

* Fri Apr 10 2015 Erik Johnson <erik@saltstack.com> - 4.0.5-1
- Update to ZeroMQ 4.0.5 stable release.

* Thu Sep  4 2014 Erik Johnson <erik@saltstack.com> - 4.0.4-1
- Update to ZeroMQ 4.0.4 stable release.

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
