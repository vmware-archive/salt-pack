%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?el5}
%global with_python26 1
%global py26dir %{_builddir}/python26-%{name}-%{version}-%{release}
%global __python26 /usr/bin/python2.6
%global python26_sitelib /usr/lib/python2.6/site-packages
# Disable byte compiling. Do ourselves later.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g') 
%endif


%if 0%{?with_python26}
BuildRequires:  python26-devel
BuildRequires:  python26-distribute
%endif


Name:           babel
Version:        0.9.5
Release:        2%{?dist}
Summary:        Tools for internationalizing Python applications

Group:          Development/Languages
License:        BSD
URL:            http://babel.edgewall.org/
Source0:        http://ftp.edgewall.com/pub/babel/Babel-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-babel
Requires:       python-setuptools

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if 0%{?with_python26}
%package -n python26-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages
Requires:       python(abi) = 2.6

%description -n python26-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.
%endif


%package -n python-babel
Summary:        Library for internationalizing Python applications
Group:          Development/Languages

%description -n python-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%prep
%setup0 -q -n Babel-%{version}
chmod a-x babel/messages/frontend.py doc/logo.png doc/logo_small.png
%{__sed} -i -e '/^#!/,1d' babel/messages/frontend.py

%if 0%{?with_python26}
rm -rf %{py26dir}
mkdir -p %{py26dir}
cp -r . %{py26dir}
%endif



%build
%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py build
popd
%endif

%{__python} setup.py build


%install
rm -rf %{buildroot}
%if 0%{?with_python26}
pushd %{py26dir}
%{__python26} setup.py install --skip-build --no-compile --root %{buildroot}
popd
# remove the 2.6 version of the command we just installed.
rm %{buildroot}%{_bindir}/pybabel
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
 
# Now do our own byte compiling.
%if 0%{?with_python26}
%{__python} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitelib}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitelib}", 1)' > /dev/null
%{__python26} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitelib}"'", 10, "%{python26_sitelib}", 1)' > /dev/null
%{__python26} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitelib}"'", 10, "%{python26_sitelib}", 1)' > /dev/null
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README.txt doc/cmdline.txt
%{_bindir}/pybabel

%files -n python-babel
%defattr(-,root,root,-)
%doc doc
%{python_sitelib}/*

%if 0%{?with_python26}
%files -n python26-babel
%defattr(-,root,root,-)
%doc doc
%{python26_sitelib}/Babel-%{version}-py*.egg-info
%{python26_sitelib}/babel
%endif

%changelog
* Sun Dec 12 2010 Steve Traylen <steve.traylen@cern.ch> - 0.9.5-2
- Add python26 subpackage

* Wed Apr  7 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-1
- This release contains a small number of bugfixes over the 0.9.4
- release.
- 
- What's New:
- -----------
- * Fixed the case where messages containing square brackets would break
-  with an unpack error
- * Fuzzy matching regarding plurals should *NOT* be checked against
-  len(message.id) because this is always 2, instead, it's should be
-  checked against catalog.num_plurals (ticket #212).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Robert Scheck <robert@fedoraproject.org> - 0.9.4-4
- Added missing requires to python-setuptools for pkg_resources

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.4-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 10 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.3-1
- Update to 0.9.3

* Sun Dec 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.1-1
- Update to 0.9.1

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-1
- Update to 0.9

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-1
- Update to 0.8.1
- Remove upstreamed patch.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-3
- Replace patch with one that actually applies.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-2
- Apply upstream patch to rename command line script to "pybabel" - BZ#246208

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-1
- First version for Fedora

