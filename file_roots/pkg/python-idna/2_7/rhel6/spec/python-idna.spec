%global backport_rhel6 1

%if 0%{?backport_rhel6}
%global with_python3 0
%bcond_with tests

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%else
%global with_python3 1
%global __python_ver 2
%endif

%global srcname idna

Name:           python-%{srcname}
Version:        2.7
Release:        4%{?dist}
Summary:        Internationalized Domain Names in Applications (IDNA)

License:        BSD and Python and Unicode
URL:            https://github.com/kjd/idna
Source0:        https://pypi.io/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?backport_rhel6}
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
Requires: python%{?__python_ver}  >= 2.7.9-1
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif # with_python3

%description
A library to support the Internationalised Domain Names in Applications (IDNA)
protocol as specified in RFC 5891 <http://tools.ietf.org/html/rfc5891>.  This
version of the protocol is often referred to as "IDNA2008" and can produce
different results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement for the
"encodings.idna" module that comes with the Python standard library but
currently only supports the older 2003 specification.

%package -n python%{?__python_ver}-%{srcname}
Summary:        Internationalized Domain Names in Applications (IDNA)
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python%{?__python_ver}-%{srcname}
A library to support the Internationalised Domain Names in Applications (IDNA)
protocol as specified in RFC 5891 <http://tools.ietf.org/html/rfc5891>.  This
version of the protocol is often referred to as "IDNA2008" and can produce
different results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement for the
"encodings.idna" module that comes with the Python standard library but
currently only supports the older 2003 specification.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Internationalized Domain Names in Applications (IDNA)
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
A library to support the Internationalised Domain Names in Applications (IDNA)
protocol as specified in RFC 5891 <http://tools.ietf.org/html/rfc5891>.  This
version of the protocol is often referred to as "IDNA2008" and can produce
different results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement for the
"encodings.idna" module that comes with the Python standard library but
currently only supports the older 2003 specification.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%if 0%{?with_python3}
%py3_install
%endif # with_python3

%py2_install

%check
%{__python2} setup.py test

%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3


%files -n python%{?__python_ver}-%{srcname}
%license LICENSE.rst
%doc README.rst HISTORY.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.rst
%doc README.rst HISTORY.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif # with_python3

%changelog
* Tue Nov 13 2018 SaltStack Packaging Team >packaging@saltstack.com> - 2.7-4
- Backport to support RHEL 6 for Python 2.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7-2
- Rebuilt for Python 3.7

* Tue Jun 12 2018 Jeremy Cline <jeremy@jcline.org> - 2.7-1
- Update to v2.7 (rhbz 1589803)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.5-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 07 2017 Jeremy Cline <jeremy@jcline.org> - 2.5-1
- Update to version 2.5

* Wed Mar 01 2017 Jeremy Cline <jeremy@jcline.org> - 2.4-1
- Update to version 2.4

* Tue Feb 28 2017 Paul Wouters <pwouters@redhat.com> - 2.3-1
- Resolves: rhbz#1427499 Update to 2.3 for IDNAError bugfix and memory improvement

* Thu Feb 09 2017 Jeremy Cline <jeremy@jcline.org> - 2.2-1
- Update to version 2.2 (#1406757)

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.1-3
- Rebuild for Python 3.6

* Mon Nov 28 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1-2
- Ship python2-idna
- Enable python3 for EPEL
- Modernize spec

* Mon Oct 17 2016 tom.prince@ualberta.net - 2.1-1
- Bump version.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 2.0-2
- Rebuilt for Python3.5 rebuild

* Thu Aug 13 2015 Paul Wouters <pwouters@redhat.com> - 2.0-1
- Update to 2.0 which is required by python-cryptography

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 31 2014 tom.prince@ualberta.net - 1.0-1
- Bump version.

* Mon Oct 27 2014 tom.prince@ualberta.net - 0.8-3
- Update licences.

* Sat Jul 12 2014 tom.prince@ualberta.net - 0.8-2
- Be more specfic about .egg-info directories.
- Use python2-devel

* Sat Jul 12 2014 tom.prince@ualberta.net - 0.8-1
- Initial package.
