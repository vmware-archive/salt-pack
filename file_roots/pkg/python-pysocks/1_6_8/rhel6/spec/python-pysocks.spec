%global backport_rhel6 1

%if 0%{?backport_rhel6}
%global with_python2 1

%global with_python3 0
%global with_python3_tests 0
%global python3_other_pkgversion 0

%bcond_with tests

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
## %global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%else
%bcond_without tests

%if 0%{?rhel}
%global with_python2 1
%endif
%if 0%{?fedora}
# FIXME maybe Fedora 31+ without python2 subpackage
# https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
# when needed, uncomment build conditional and later drop this block entirely
#%%if 0%%{?fedora} <= 31
%global with_python2 1
#%%endif
%endif
%if 0%{?rhel} >= 7
%global with_python3 1
%endif
%if 0%{?fedora}
%global with_python3 1
%global with_python3_tests 1
%endif
%endif

%global pypi_name   PySocks
%global modname     pysocks
%global sum         A Python SOCKS client module

Name:               python-%{modname}
Version:            1.6.8
Release:            7%{?dist}
Summary:            %{sum}

License:            BSD
URL:                https://github.com/Anorov/%{pypi_name}
## Source0:            %%pypi_source
Source0:            https://files.pythonhosted.org/packages/source/P/PySocks/PySocks-%{version}.tar.gz

BuildArch:          noarch
Patch0:             https://github.com/Anorov/PySocks/commit/d74c3f1d34d07a001656453823a153ea0c865449.patch
Provides:           python-pysocks

%global _description \
A fork of SocksiPy with bug fixes and extra features.\
\
Acts as a drop-in replacement to the socket module. Featuring:\
\
- SOCKS proxy client for Python 2.6 - 3.x\
- TCP and UDP both supported\
- HTTP proxy client included but not supported or recommended (you should use\
  urllib2's or requests' own HTTP proxy interface)\
- urllib2 handler included.

%description
%_description

%if 0%{?with_python2}
%package -n python%{?__python_ver}-%{modname}
Summary:            %{sum}
%if 0%{?backport_rhel6}
BuildRequires:      python%{?__python_ver}-devel
BuildRequires:      python%{?__python_ver}-setuptools
Requires:           python%{?__python_ver} >= 2.7.9-1
## %{?python_provide:%python_provide python2-%{modname}}
Provides:   python%{?__python_ver}-%{modname}
%else
BuildRequires:      python2-devel
BuildRequires:      python2-setuptools
%{?python_provide:%python_provide python2-%{modname}}
%endif
%if %{with tests}
# for tests
BuildRequires:      python2-pytest
BuildRequires:      python2-psutil
#BuildRequires:      python2-test_server
%endif

# SocksiPy is retired in F30, drop when Fedora 29 becomes EOL
# https://bugzilla.redhat.com/show_bug.cgi?id=1334407
%if 0%{?fedora} && 0%{?fedora} < 30
Obsoletes:  python-SocksiPy
Obsoletes:  python2-SocksiPy
Provides:   python-SocksiPy
Provides:   python2-SocksiPy
%endif

%description -n python%{?__python_ver}-%{modname}
%_description
This package is for Python2 only.
%endif

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{modname}
Summary:            %{sum}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
# for tests
%if 0%{?with_python3_tests}
BuildRequires:      python%{python3_pkgversion}-pytest
BuildRequires:      python%{python3_pkgversion}-psutil
#BuildRequires:      python%%{python3_pkgversion}-test_server
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

# This package doesn't actually exist...
# but if it did, we would conflict with it.
Conflicts:  python%{python3_pkgversion}-SocksiPy

%description -n python%{python3_pkgversion}-%{modname}
%_description
This package is for Python3 version %{python3_version} only.
%endif

%if 0%{?python3_other_pkgversion}
%package -n python%{python3_other_pkgversion}-%{modname}
Summary:            %{sum}
BuildRequires:      python%{python3_other_pkgversion}-devel
BuildRequires:      python%{python3_other_pkgversion}-setuptools
# for tests
%if 0%{?with_python3_tests}
BuildRequires:      python%{python3_other_pkgversion}-pytest
BuildRequires:      python%{python3_other_pkgversion}-psutil
#BuildRequires:      python%%{python3_other_pkgversion}-test_server
%endif
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{modname}}

%description -n python%{python3_other_pkgversion}-%{modname}
%_description
This package is for Python3 version %{python3_other_version} only.
%endif


%prep
## %%autosetup -n %%{pypi_name}-%%{version}
%setup -n %{pypi_name}-%{version}
%patch0 -p1
# drop useless 3rdparty code
rm -rfv test/bin

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%{?python3_other_pkgversion: %py3_other_build}
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%{?python3_other_pkgversion: %py3_other_install}
%endif

%check
# https://github.com/Anorov/PySocks/issues/37
# FIXME python module named test_server is needed but not packaged
%if 0
%{?with_python2: %{__python2} setup.py test}
%if 0%{?with_python3_tests}
%{?with_python3: %{__python3} setup.py test}
%{?python3_other_pkgversion: %{__python3_other} setup.py test}
%endif
%endif


%if 0%{?with_python2}
%files -n python%{?__python_ver}-%{modname}
%doc README.md
%license LICENSE
%{python2_sitelib}/socks.py*
%{python2_sitelib}/sockshandler.py*
%{python2_sitelib}/%{pypi_name}-%{version}*
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{modname}
%doc README.md
%license LICENSE
%{python3_sitelib}/socks.py*
%{python3_sitelib}/sockshandler.py*
%{python3_sitelib}/__pycache__/*socks*
%{python3_sitelib}/%{pypi_name}-%{version}-*
%endif

%if 0%{?python3_other_pkgversion}
%files -n python%{python3_other_pkgversion}-%{modname}
%doc README.md
%license LICENSE
%{python3_other_sitelib}/socks.py*
%{python3_other_sitelib}/sockshandler.py*
%{python3_other_sitelib}/__pycache__/*socks*
%{python3_other_sitelib}/%{pypi_name}-%{version}-*
%endif


%changelog
* Tue Nov 13 2018 SaltStack Packaging Team >packaging@saltstack.com> - 1.6.8-7
- Backport for RHEL 7 with support for Python 2.7 only

* Sun Nov 11 2018 Kevin Fenzi <kevin@scrye.com> - 1.6.8-6
- Add upstream patch to avoid DeprecationWarning. Fixes bug #1648583

* Wed Oct 03 2018 Raphael Groner <projects.rg@smart.ms> - 1.6.8-5
- add python3_other subpackage for epel7
- prepare removal of python2 subpackage in Fedora
- use pypi macros
- try to enable tests provided actually from tarball

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.8-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Kevin Fenzi <kevin@scrye.com> - 1.6.8-1
- Update to 1.6.8. Fixes bug #1528490

* Mon Sep 11 2017 Carl George <carl@george.computer> - 1.6.7-1
- Latest upstream
- Add setuptools dependency

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.5.7-3
- Rebuild for Python 3.6

* Mon Nov 28 2016 Tim Orling <ticotimo@gmail.com> - 1.5.7-2
- Ship python34-pysocks in EL6

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 1.5.7-1
- Update to 1.5.7

* Fri Sep 16 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.6-6
- Ship python34-pysocks in EPEL7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-4
- Change our conflicts on python-SocksiPy to an obsoletes/provides.
  https://bugzilla.redhat.com/show_bug.cgi?id=1334407

* Mon May 09 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-3
- Fix typo in explicit conflicts.

* Tue May 03 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-2
- We don't actually need setuptools here.

* Mon May 02 2016 Ralph Bean <rbean@redhat.com> - 1.5.6-1
- Initial package for Fedora
