%global __python26 /usr/bin/python2.6
%global python26_sitearch %{_libdir}/python2.6/site-packages

# Fix byte-compilation:
%define __os_install_post %{__python26_os_install_post}


Name:           python26-pycurl
Version:        7.15.5.1
Release:        9%{?dist}
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python26-devel
BuildRequires:  curl-devel >= 7.15.5

# Fixes errors on the documentation files reported by xmllint.
Patch0:         python-pycurl-7.15.5.1-xml_validity.patch

Requires:       python(abi) = 2.6

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup -q -n pycurl-%{version}
%patch0 -p1 -b .xml_validity
rm -f doc/*.xml_validity
chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" %{__python26} setup.py build

%check
%{__python26} tests/test_internals.py -q

%install
rm -rf %{buildroot}
%{__python26} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python26_sitearch}/pycurl.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO examples doc tests
%{python26_sitearch}/*

%changelog
* Sun Mar 6 2011 Steve Traylen <steve.traylen@cern.ch> - 7.15.5.1-9
- Adapt RHEL5 .spec file to for python26 package in EPEL.
- Correct license from GPL to LGPL.

* Wed Sep 29 2010 Karel Klic <kklic@redhat.com> - 7.15.5.1-8
- Do not include unpatched files in the doc directory

* Wed Sep 29 2010 Karel Klic <kklic@redhat.com> - 7.15.5.1-7
- Added a patch to fix errors reported by xmllint

* Mon Sep 27 2010 Marek Grac <mgrac@redhat.com> - 7.15.5.1-6
- Update package number

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-4
- Add -DHAVE_CURL_OPENSSL to fix PPC build problem.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-3
- Don't forget to Provide: pycurl!!!

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-2
- Remove INSTALL from the list of documentation
- Use python_sitearch for all of the files

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-1
- First version for Fedora Extras

