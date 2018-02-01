%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global oname  futures

Name:          python%{?__python_ver}-futures
Summary:       Backport of the concurrent.futures package from Python 3.2
Version:       3.0.3
Release:       3%{?dist}
License:       BSD
Group:         Development/Libraries
URL:           https://github.com/agronholm/pythonfutures
Source0:       https://pypi.python.org/packages/source/f/futures/futures-%{version}.tar.gz
BuildRequires: python%{?__python_ver}-setuptools
BuildArch:     noarch

%description
The concurrent.futures module provides a high-level interface for
asynchronously executing callables.

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc CHANGES LICENSE 
%{python_sitelib}/concurrent
%{python_sitelib}/futures-*.egg-info*

%changelog
* Mon Jan 22 2018 SaltStack Packaging Team <packaging@saltstack.com> - 3.0.3-3
- Removed os_install_post override

* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 3.0.3-2
- Updated to use Python 2.7 on Redhat 6

* Wed Jun 24 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.0.3-1
- 3.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.0.2-1
- 3.0.2

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.1.6-3
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Terje Rosten <terje.rosten@ntnu.no> - 2.1.6-1
- 2.1.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.1.3-1
- 2.1.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.1.2-2
- Remove old cruft
- Fix url and buildreq

* Mon Sep 26 2011 Terje Rosten <terje.rosten@ntnu.no> - 2.1.2-1
- initial package
