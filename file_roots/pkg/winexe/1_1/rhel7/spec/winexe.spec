Name: winexe
Version: 1.1
Release: b787d2%{?dist}
Summary: Remote Windows command executor.


Group: Applications/System
License: GPLv3
URL: http://sourceforge.net/projects/winexe/
Source0: %{name}-%{version}.tar.gz


AutoReqProv: no
BuildRequires: gcc
BuildRequires: perl
BuildRequires: mingw-binutils-generic
BuildRequires: mingw-filesystem-base
BuildRequires: mingw32-binutils
BuildRequires: mingw32-cpp
BuildRequires: mingw32-crt
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-headers
BuildRequires: mingw64-binutils
BuildRequires: mingw64-cpp
BuildRequires: mingw64-crt
BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-headers
BuildRequires: libcom_err-devel
BuildRequires: popt-devel
BuildRequires: zlib-devel
BuildRequires: zlib-static
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: python-devel
BuildRequires: git
BuildRequires: gnutls-devel
BuildRequires: libacl-devel
BuildRequires: openldap-devel
Requires: samba4-libs >= 4.0.0
Requires: glibc >= 2.17
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
Winexe remotely executes commands on Windows
NT/2000/XP/2003/Vista/7/2008/8/2012 systems from GNU/Linux.


%prep
cd ../SOURCES
tar -xf winexe-1.1.tar.gz
chmod +x ./generatetarball
./generatetarball


%setup -q


%build
cd source
./waf --samba-dir=../../samba configure build


%install
echo %{buildroot}
rm -rf %{buildroot}
%__install -d %{buildroot}/usr/bin
%__install source/build/winexe %{buildroot}/usr/bin


%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%attr(755,root,root) /usr/bin/winexe


%changelog
* Sun Feb 14 2016 Randy Thompson <randy@heroictek.com> - 1.1-b787d2
- b787d2a2c4b1abc3653bad10aec943b8efcd7aab from git://git.code.sf.net/p/winexe/winexe-waf
- a6bda1f2bc85779feb9680bc74821da5ccd401c5 from git://git.samba.org/samba.git
