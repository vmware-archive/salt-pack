%global with_python3 0

%{!?python3_pkgversion:%global python3_pkgversion 3}

Summary: Support for using OpenSSL in Python 3 scripts
Name: m2crypto
Version: 0.28.2
Release: 4%{?dist}
Source0: https://pypi.python.org/packages/4e/bd/690f9b8aa87b82b0905c6e928da4cb0ce3ac65b1fc43c8efd3f8104e345e/M2Crypto-0.28.2.tar.gz
# Should generally be available at pypi; for this release it has been obtained independently.
Source1: M2Crypto-0.28.2.tar.gz.asc
# Source1: https://pypi.python.org/packages/4e/bd/690f9b8aa87b82b0905c6e928da4cb0ce3ac65b1fc43c8efd3f8104e345e/M2Crypto-0.28.2.tar.gz.asc
# This is only precautionary, it does fix anything - not sent upstream
Patch0: m2crypto-0.26.4-gcc_macros.patch
Requires: python2-typing
Requires: openssl >= 1:1.0.2
 
License: MIT
Group: System Environment/Libraries
URL: https://gitlab.com/m2crypto/m2crypto/
BuildRequires: openssl >= 1:1.0.2
BuildRequires: openssl-devel >= 1:1.0.2
BuildRequires: python2-devel, python2-setuptools
BuildRequires: perl-interpreter, pkgconfig, python2-typing, swig, which

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-typing
%endif

%filter_provides_in %{python2_sitearch}/M2Crypto/__m2crypto.so
%filter_setup

%description
This package allows you to call OpenSSL functions from Python 2 scripts.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-m2crypto
Summary:    Support for using OpenSSL in Python 3 scripts
Requires:   python%{python3_pkgversion}-typing

%description -n python%{python3_pkgversion}-m2crypto
This package allows you to call OpenSSL functions from Python 3 scripts.
%endif

%prep
%setup -q -T -c -a 0

pushd M2Crypto-%{version}
%patch0 -p1 -b .gcc_macros

# __REGISTER_PREFIX__ is defined to unquoted $ on some platforms; gcc handles
# this fine, but swig chokes on it.
# __GNUC__ really should be included in gcc_macros.h, but this currently breaks
# builds on ppc64: https://bugzilla.redhat.com/show_bug.cgi?id=1317553 .
# __STDC_HOSTED__ really should be included as well, but that causes
# /usr/lib/gcc/*/*/include/stdint.h to try to #include_next <stdint.h>, which
# is unsupported by swig. Without it, gcc uses its own definitions, which better
# be the same as the glibc ones.
gcc -E -dM - < /dev/null | grep -v '__\(STDC\|REGISTER_PREFIX\|GNUC\|STDC_HOSTED\)__' \
	| sed 's/^\(#define \([^ ]*\) .*\)$/#undef \2\n\1/' > SWIG/gcc_macros.h
popd
cp -a M2Crypto-%{version} M2Crypto-python%{python3_pkgversion}

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

pushd M2Crypto-%{version}
%{__python2} setup.py build
popd
%if 0%{?with_python3}
pushd M2Crypto-python%{python3_pkgversion}
%{__python3} setup.py build
popd
%endif

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

pushd M2Crypto-%{version}
%{__python2} setup.py install --root=$RPM_BUILD_ROOT
popd
%if 0%{?with_python3}
pushd M2Crypto-python%{python3_pkgversion}
%{__python3} setup.py install --root=$RPM_BUILD_ROOT
popd
%endif

%check
pushd M2Crypto-%{version}
%{__python2} setup.py test
popd
%if 0%{?with_python3}
pushd M2Crypto-python%{python3_pkgversion}
## %%{__python3} setup.py test
popd
%endif

%files
%doc M2Crypto-%{version}/CHANGES M2Crypto-%{version}/LICENCE M2Crypto-%{version}/README.rst
%{python2_sitearch}/M2Crypto
%{python2_sitearch}/M2Crypto-*.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-m2crypto
%doc M2Crypto-python%{python3_pkgversion}/CHANGES M2Crypto-python%{python3_pkgversion}/LICENCE M2Crypto-python%{python3_pkgversion}/README.rst
%{python3_sitearch}/M2Crypto
%{python3_sitearch}/M2Crypto-*.egg-info
%endif

%changelog
* Tue Aug 28 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.28.2-4
- Added version check >= openssl 1:1.0.2

* Tue Mar 27 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.28.2-3
- Adjusted support for Python 3 for Redhat 7

* Sat Feb 17 2018 Miloslav Trmač <mitr@redhat.com> - 0.28.2-2
- Add a python3-m2crypto subpackage

* Sat Feb 17 2018 Miloslav Trmač <mitr@redhat.com> - 0.28.2-1
- Update to M2Crypto-0.28.2 (minimal update of Python 2 for now,
  Python 3 to come)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.27.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Oct 7 2017 Miloslav Trmač <mitr@redhat.com> - 0.27.0-1
- Update to M2Crypto-0.27.0

* Tue Sep 26 2017 Miloslav Trmač <mitr@redhat.com> - 0.26.4-1
- Update to M2Crypto-0.26.4

* Sat Sep 23 2017 Miloslav Trmač <mitr@redhat.com> - 0.26.3-1
- Update to M2Crypto-0.26.3

* Fri Sep 22 2017 Miloslav Trmač <mitr@redhat.com> - 0.26.2-1
- Update to M2Crypto-0.26.2
  Resolves: #1384010, #1439366, #1488196

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.1-3
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 26 2016 Miloslav Trmač <mitr@redhat.com> - 0.25.1-1
- Update to M2Crypto-0.25.1

* Mon Jul 25 2016 Miloslav Trmač <mitr@redhat.com> - 0.25.0-1
- Update to M2Crypto-0.25.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 10 2016 Than Ngo <than@redhat.com> - 0.23.0-2
- Filter out __GNUC__ to fix build failure on powerpc
- EXP ciphers is disable in openssl-1.0.2g, so remove test_ssl.MiscSSLClientTestCase.test_no_weak_cipher

* Tue Feb 9 2016 Miloslav Trmač <mitr@redhat.com> - 0.23.0-1
- Update to M2Crypto-0.23.0
- Filter out __REGISTER_PREFIX__ to allow building on MIPS.  Based on a patch by
  Michal Toman <michal.toman@gmail.com>.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 5 2015 Miloslav Trmač <mitr@redhat.com> - 0.22.5-2
- Fix a buffer overflow in EVP.pbkdf2
  Resolves: #1276630
- Update URL:

* Thu Oct 15 2015 Miloslav Trmač <mitr@redhat.com> - 0.22.5-1
- Update to M2Crypto-0.22.5

* Fri Oct 9 2015 Miloslav Trmač <mitr@redhat.com> - 0.21.1-21
- Fix spurious failures of test_cookie_str_changed_mac
  Resolves: #1270016
- Add support for IP addresses in subjectAltName
  Resolves: #1080142

* Sat Jul 11 2015 Miloslav Trmač <mitr@redhat.com> - 0.21.1-20
- Fix build with swig-3.0.5
- Update tests for OpenSSL disabling SSL 2.0 and 3.0 by default
- Update tests for OpenSSL using SHA-256 instead of SHA-1 in S/MIME signatures
  by default
  Resolves: #1239664

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 9 2014 Miloslav Trmač <mitr@redhat.com> - 0.21.1-17
- Update test_x509_name for OpenSSL 1.0.1h
  Resolves: #1106146

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Miloslav Trmač <mitr@redhat.com> - 0.21.1-15
- Sync %%multilib_arches with openssl.
  Resolves: #1070995

* Mon Jan 6 2014 Miloslav Trmač <mitr@redhat.com> - 0.21.1-14
- Don't assume that export ciphers are enabled in the test suite
  Resolves: #1048887
- Let the kernel allocate free ports for use by the test suite
  Resolves: #1048887

* Wed Dec 18 2013 Miloslav Trmač <mitr@redhat.com> - 0.21.1-13
- Use only ECC curves available in Fedora in the test suite
  Related: #904996
- Fix terminating test suite helper processes when running in Koji
  Related: #904996
- Run test suite in %%check, don't ship it in the package.  Based on a patch by
  Matěj Cepl <mcepl@redhat.com>.
  Resolves: #904996

* Tue Dec 17 2013 Miloslav Trmač <mitr@redhat.com> - 0.21.1-13
- Add minimal SNI support, based on a patch by Sander Steffann
  <sander@steffann.nl>
  Resolves: #1029246

* Sat Dec  7 2013 Miloslav Trmač <mitr@redhat.com> - 0.21.1-13
- Fix incorrect exception handling of SSL_CTX_new (manifesting in FIPS mode)
  Resolves: #879043

* Tue Nov 26 2013 Miloslav Trmač <mitr@redhat.com> - 0.21.1-13
- Fix occasional spurious failures in test_makefile_timeout_fires
  Resolves: #969077

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Miloslav Trmač <mitr@redhat.com> - 0.21.1-10
- Replace expired certificates in the test suite
- Fix running the test suite against recent OpenSSL versions

* Tue Aug 21 2012 Miloslav Trmač <mitr@redhat.com> - 0.21.1-10
- Drop no longer necessary %%clean and %%defattr commands.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Miloslav Trmač <mitr@redhat.com> - 0.21.1-8
- Fix HTTPS proxy support
  Resolves: #803554

* Tue Mar 13 2012 Miloslav Trmač <mitr@redhat.com> - 0.21.1-7
- Support IPv6 in M2Crypto.httpslib
  Resolves: #742914

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 12 2011 Miloslav Trmač <mitr@redhat.com> - 0.21.1-5
- Fix a memory leak in AES_crypt
  Resolves: #659881

* Tue May 10 2011 Miloslav Trmač <mitr@redhat.com> - 0.21.1-4
- Fix handling of buffer() objects as input data to SSL
  Resolves: #702766

* Mon Mar 28 2011 Miloslav Trmač <mitr@redhat.com> - 0.21.1-3
- Fix S/MIME documentation and examples
  Resolves: #618500

* Wed Feb 23 2011 Garrett Holmstrom <gholms@fedoraproject.org> - 0.21.1-3
- Use the %%__python macro for Python calls and locations
  Patch by Garrett Holmstrom <gholms@fedoraproject.org>

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Miloslav Trmač <mitr@redhat.com> - 0.21.1-1
- Update to m2crypto-0.21.1
- Make the test suite pass with Python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.20.2-9
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul  9 2010 Miloslav Trmač <mitr@redhat.com> - 0.20.2-8
- Allow overriding SSL.Connection.postConnectionCheck from m2urllib2
  Resolves: #610906

* Wed May 19 2010 Miloslav Trmač <mitr@redhat.com> - 0.20.2-7
- Make test suite pass in FIPS mode
  Resolves: #565662

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 0.20.2-6
- Filter out bogus Provides: __m2crypto.so
- Drop explicit Requires: python

* Mon Feb 15 2010 Miloslav Trmač <mitr@redhat.com> - 0.20.2-5
- Make test suite pass with OpenSSL 1.0.0
- Don't ship patch backup files in %%doc

* Tue Jan  5 2010 Miloslav Trmač <mitr@redhat.com> - 0.20.2-4
- s/%%define/%%global/

* Mon Dec  7 2009 Miloslav Trmač <mitr@redhat.com> - 0.20.2-3
- Don't use '!# /usr/bin/env python'
  Resolves: #521887

* Thu Oct 15 2009 Miloslav Trmač <mitr@redhat.com> - 0.20.2-2
- Add a dist tag.

* Wed Oct  7 2009 Miloslav Trmač <mitr@redhat.com> - 0.20.2-1
- Update to m2crypto-0.20.2
- Drop BuildRoot: and cleaning it at start of %%install

* Sun Aug 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.20.1-1
- Update to m2crypto-0.20.1
- Add upstream patch to build with OpenSSL 1.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.20-2
- rebuilt with new openssl

* Tue Aug 11 2009 Miloslav Trmač <mitr@volny.cz> - 0.20-1
- Update to m2crypto-0.20
- Fix incorrect merge in HTTPS CONNNECT proxy support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Miloslav Trmač <mitr@redhat.com> - 0.19.1-9
- Fix OpenSSL locking callback
  Resolves: #507903

* Wed Jun 10 2009 Miloslav Trmač <mitr@redhat.com> - 0.19.1-8
- Don't reject certificates with subjectAltName that does not contain a dNSName
  Resolves: #504060

* Wed Jun  3 2009 Miloslav Trmač <mitr@redhat.com> - 0.19.1-7
- Only send the selector in SSL HTTP requests.  Patch by James Bowes
  <jbowes@redhat.com>.
  Resolves: #491674

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Miloslav Trmač <mitr@redhat.com> - 0.19.1-5
- Close the connection when an m2urllib2 response is closed
  Resolves: #460692
- Work around conflicts between macros defined by gcc and swig

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.19.1-4
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.19.1-3
- Rebuild for Python 2.6

* Mon Nov 10 2008 Miloslav Trmač <mitr@redhat.com> - 0.19.1-2
- Import all gcc-defined macros into SWIG (recommended by Adam Tkac)

* Mon Oct 13 2008 Miloslav Trmač <mitr@redhat.com> - 0.19.1-1
- Update to m2crypto-0.19.1

* Mon Oct  6 2008 Miloslav Trmač <mitr@redhat.com> - 0.19-1
- Update to m2crypto-0.19
- Fix some rpmlint warnings

* Thu Sep 18 2008 Dennis Gilmore <dennis@ausil.us> - 0.18.2-8
- enable sparc arches

* Wed Jun 11 2008 Miloslav Trmač <mitr@redhat.com> - 0.18.2-7
- Update m2urllib2 to match the Python 2.5 code instead

* Sun Jun  8 2008 Miloslav Trmač <mitr@redhat.com> - 0.18.2-6
- Don't remove the User-Agent header from proxied requests
  Related: #448858
- Update m2urllib2.py to work with Python 2.5

* Sat Jun  7 2008 Miloslav Trmač <mitr@redhat.com> - 0.18.2-5
- Use User-Agent in HTTP proxy CONNECT requests
  Related: #448858

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.18.2-4
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Miloslav Trmač <mitr@redhat.com> - 0.18.2-3
- Ship Python egg information

* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 0.18.2-2
- Rebuild with openssl-0.9.8g

* Fri Oct 26 2007 Miloslav Trmač <mitr@redhat.com> - 0.18.2-1
- Update to m2crypto-0.18.2
- Remove BuildRequires: unzip

* Sun Sep 23 2007 Miloslav Trmač <mitr@redhat.com> - 0.18-2
- Add missing Host: header to CONNECT requests (patch by Karl Grindley)
  Resolves: #239034
- Fix License:

* Wed Aug  1 2007 Miloslav Trmač <mitr@redhat.com> - 0.18-1
- Update to m2crypto-0.18

* Wed Jul 11 2007 Miloslav Trmač <mitr@redhat.com> - 0.17-3
- Try to fix build on Alpha
  Resolves: #246828

* Fri Apr 27 2007 Miloslav Trmac <mitr@redhat.com> - 0.17-2
- Make m2xmlrpclib work with Python 2.5
  Resolves: #237902

* Wed Jan 17 2007 Miloslav Trmac <mitr@redhat.com> - 0.17-1
- Update to m2crypto-0.17
- Update for Python 2.5

* Thu Dec  7 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-8
- Rebuild with updated build tools to avoid DT_TEXTREL on s390x
  Resolves: #218578

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.16-7
- rebuild against python 2.5

* Mon Oct 23 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-6
- Add support for SSL socket timeouts (based on a patch by James Bowes
  <jbowes@redhat.com>)
  Resolves: #219966

* Fri Oct 20 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-5
- Backport the urllib2 wrapper (code by James Bowes <jbowes@redhat.com>)
  Resolves: #210956
- Add proxy support for https using CONNECT (original patch by James Bowes
  <jbowes@redhat.com>)
  Resolves: #210963

* Tue Sep 26 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-4
- Drop Obsoletes: openssl-python, openssl-python was last shipped in RHL 7.1
- Fix interpreter paths in demos

* Sat Sep 23 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-3
- Make more compliant with Fedora guidelines
- Update URL:

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.16-2.1
- rebuild

* Thu Jul  6 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-2
- Fix build with rawhide swig

* Thu Jul  6 2006 Miloslav Trmac <mitr@redhat.com> - 0.16-1
- Update to m2crypto-0.16

* Wed Apr 19 2006 Miloslav Trmac <mitr@redhat.com> - 0.15-4
- Fix SSL.Connection.accept (#188742)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.15-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.15-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Miloslav Trmac <mitr@redhat.com> - 0.15-3
- Add BuildRequires: swig

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Miloslav Trmac <mitr@redhat.com> - 0.15-2
- Rebuild with newer openssl

* Mon Aug 29 2005 Miloslav Trmac <mitr@redhat.com> - 0.15-1
- Update to m2crypto-0.15
- Drop bundled swig

* Tue Jun 14 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-5
- Better fix for #159898, by Dan Williams

* Thu Jun  9 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-4
- Fix invalid handle_error override in SSL.SSLServer (#159898, patch by Dan
  Williams)

* Tue May 31 2005 Miloslav Trmac <mitr@redhat.com> - 0.13-3
- Fix invalid Python version comparisons in M2Crypto.httpslib (#156979)
- Don't ship obsolete xmlrpclib.py.patch
- Clean up the build process a bit

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 0.13-2
- rebuild

* Tue Nov 23 2004 Karsten Hopp <karsten@redhat.de> 0.13-1
- update, remove now obsolete patches

* Mon Nov 22 2004 Karsten Hopp <karsten@redhat.de> 0.09-7
- changed pythonver from 2.3 to 2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Harald Hoyer <harald@redhat.com> - 0.09-5
- changed pythonver from 2.2 to 2.3
- patched setup.py to cope with include path

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Nalin Dahyabhai <nalin@redhat.com> 0.09-1
- Update to version 0.09
- Build using bundled copy of SWIG
- Pick up additional CFLAGS and LDFLAGS from OpenSSL's pkgconfig data, if
  there is any
- Handle const changes in new OpenSSL
- Remove unnecessary ldconfig calls in post/postun

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 0.07_snap3-2
- Update to version 0.07_snap3

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-4
- rebuild with Python 2.2

* Wed Apr 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-3
- remove a stray -L at link-time which prevented linking with libssl (#59985)

* Thu Aug 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-2
- drop patch which isn't needed because we know swig is installed

* Mon Apr  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.05_snap4-1
- break off from openssl-python
