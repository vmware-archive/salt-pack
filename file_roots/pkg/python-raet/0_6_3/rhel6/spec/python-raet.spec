%if 0%{?rhel} < 7
%global with_python26 1
%define pybasever 2.6
%define __python_ver 26
%define __python %{_bindir}/python%{?pybasever}
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

%global srcname raet

Name:           python-%{srcname}
Version:        0.6.3
Release:        2%{?dist}
Summary:        Reliable Asynchronous Event Transport Protocol

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/RaetProtocol/raet
Source0:        http://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-ioflo >= 1.3.8-1
Requires:  python-libnacl >= 1.4.3-1
Requires:  python-six
Requires:  python-simplejson
Requires:  python-ioflo >= 1.3.8-1
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

%prep
%setup -q -n %{srcname}-%{version}

%install
%{__python} setup.py install --root %{buildroot}

%files
%{_bindir}/raetflo
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info

%changelog
* Thu Aug  6 2015 Packaging <packaging@saltstack.com> - 0.6.3-2
- Build 0.6.3 for Salt implementation on various versions Redhat


