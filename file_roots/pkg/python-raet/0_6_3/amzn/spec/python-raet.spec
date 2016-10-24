## echo "DGM this var dist is --%{dist}-- "

%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global pythonpath %(%{__python2} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")
%global __inst_layout --install_layout=unix

## echo "DGM this var __python_ver is --%{__python_ver}-- "

%else

%if 0%{?rhel} < 7
%global with_python26 1
%define pybasever 2.6
%define __python_ver 26
%define __python2 %{_bindir}/python%{?pybasever}
%endif

%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(%{__python2} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

## echo "DGM this wrong var __python_ver is --%{__python_ver}-- "

%endif

%global srcname raet

Name:           python-%{srcname}
Version:        0.6.3
Release:        3%{?dist}
Summary:        Reliable Asynchronous Event Transport Protocol

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/RaetProtocol/raet
Source0:        http://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-six
BuildRequires:  python%{?__python_ver}-ioflo >= 1.3.8
Requires:  python%{?__python_ver}-libnacl >= 1.4.3
Requires:  python%{?__python_ver}-six
Requires:  python%{?__python_ver}-simplejson
Requires:  python%{?__python_ver}-ioflo >= 1.3.8
BuildArch: noarch

%if "%{?pybasever}" == "2.6"
BuildRequires:  python-importlib
Requires:       python-importlib
%endif

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_setup
}

%description
A high level, stack based communication protocol for network and IPC communication

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{srcname}
Summary:        Reliable Asynchronous Event Transport Protocol
%{?python_provide:%python_provide python%{?__python_ver}-%{srcname}}

%description -n python%{?__python_ver}-%{srcname}
A high level, stack based communication protocol for network and IPC communication

This package is meant to be used with Python 2.7.
%endif

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_explicit_python27}
%files -n python%{?__python_ver}-%{srcname}
%{_bindir}/raetflo
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}*.egg-info
%else
%files
%{_bindir}/raetflo
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}*.egg-info
%endif

%changelog
* Fri Oct 21 2016 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.3-3
- Ported to build on Amazon Linux 2016.09 natively

* Thu Aug  6 2015 Packaging <packaging@saltstack.com> - 0.6.3-2
- Build 0.6.3 for Salt implementation on various versions Redhat


