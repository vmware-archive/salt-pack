%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __os_install_post %{__python27_os_install_post}
%endif

%global srcname python-pycurl

Name:           python%{?__python_ver}-pycurl
Version:        7.19.0
Release:        10%{?dist}
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Patch0:         python-pycurl-no-static-libs.patch
Patch1:		    python-pycurl-do_curl_reset-reinitialize-handle.patch
Patch2:		    python-pycurl-do_curl_reset-refcount.patch
Patch3:         python-pycurl-7.19.0-tls12.patch

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  openssl-devel

# libcurl-devel-7.19.7-43.el6 or newer is needed for CURL_SSLVERSION_TLSv1_[0-2]
BuildRequires:  libcurl-devel >= 7.19.7-43.el6

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%define libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%define curlver_h /usr/include/curl/curlver.h
%define libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:       libcurl >= %{libcurl_ver}

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup0 -q -n pycurl-%{version}
%patch0 -p0
%patch1 -p1 -b .reinitialize-handle
%patch2 -p1
%patch3 -p1
chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" %{__python} setup.py build

%check
export PYTHONPATH=$PWD/build/lib*
%{__python} tests/test_internals.py -q

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING2 ChangeLog README TODO examples doc tests
%{python_sitearch}/*

%changelog
* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 7.19.0-10
- Updated to use Python 2.7 on Redhat 6

* Mon Sep 07 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.0-9
- introduce SSLVERSION_TLSv1_[0-2] (#1260406)

* Tue Jan 25 2011 Karel Klic <kklic@redhat.com> - 7.19.0-8
- Revert previous change; remove patch suffix for the reset-refcount
  patch
  Related: rhbz#624559

* Tue Jan 25 2011 Karel Klic <kklic@redhat.com> - 7.19.0-7
- Exclude patch files from tests directory
  Related: rhbz#624559

* Tue Jan 25 2011 Karel Klic <kklic@redhat.com> - 7.19.0-6
- Added do_curl_reset-refcount.patch: Fixed reference counting of
  Py_None in reset function
  Resolves: rhbz#624559
- Added do_curl_reset-reinitialize-handle.patch: Proper
  re-initialization of internal settings in reset function
  Resolves: rhbz#565654

* Thu Feb 25 2010 Karel Klic <kklic@redhat.com> - 7.19.0-5
- Package COPYING2 file
- Added MIT as a package license

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 7.19.0-4.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-3
- fix typo in the previous change

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-2
- add a require to reflect a dependency on libcurl version (#496308)

* Thu Mar  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-1
- Update to 7.19.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.18.2-2
- Rebuild for Python 2.6

* Thu Jul  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.2-1
- Update to 7.18.2
- Thanks to Ville Skyttä re-enable the tests and fix a minor problem
  with the setup.py. (Bug # 45400)

* Thu Jun  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.1-1
- Update to 7.18.1
- Disable tests because it's not testing the built library, it's trying to
  test an installed library.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.16.4-3
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-2
- BR openssl-devel

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-1
- Update to 7.16.4
- Update license tag.

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.2.1-1
- Update to released version.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.0-0.1.20061207
- Update to a CVS snapshot since development has a newer version of curl than is in FC <= 6

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-4
- Add -DHAVE_CURL_OPENSSL to fix PPC build problem.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-3
- Don't forget to Provide: pycurl!!!

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-2
- Remove INSTALL from the list of documentation
- Use python_sitearch for all of the files

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-1
- First version for Fedora Extras
