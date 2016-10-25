%if ( "0%{?dist}" == "0.amzn1" )
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")
%global __inst_layout --install-layout=unix

%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%endif

%global oname  futures

Summary:       Backport of the concurrent.futures package from Python 3.2
Name:          python-futures
Version:       3.0.3
Release:       2%{?dist}
License:       BSD
Group:         Development/Libraries
URL:           https://github.com/agronholm/pythonfutures
Source0:       https://pypi.python.org/packages/source/f/futures/futures-%{version}.tar.gz
BuildRequires: python-setuptools
BuildArch:     noarch

%description
The concurrent.futures module provides a high-level interface for
asynchronously executing callables.

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{oname}
Summary:       Backport of the concurrent.futures package from Python 3.2

%description -n python%{?__python_ver}-%{oname}
The concurrent.futures module provides a high-level interface for
asynchronously executing callables.

This package is meant to be used with Python 2.7.
%endif

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build %{?__inst_layout} --root %{buildroot}

%files -n python%{?__python_ver}-%{oname}
%doc CHANGES LICENSE 
%{python_sitelib}/concurrent
%{python_sitelib}/futures-*.egg-info*

%changelog
* Tue Oct 25 2016 SaltStack Packaging Team <packaging@saltstack.com> - 3.0.3-2
- Ported to build on Amazon Linux 2016.09 natively

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
