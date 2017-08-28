%if 0%{?rhel} < 7
%global with_python26 1
%define pybasever 2.6
%define __python_ver 26
%define __python %{_bindir}/python%{?pybasever}
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __os_install_post %{__python27_os_install_post}
%endif

%global srcname raet

Name:           python%{?__python_ver}-%{srcname}
Version:        0.6.6
Release:        2%{?dist}
Summary:        Reliable Asynchronous Event Transport Protocol

License:        ASL 2.0
URL:            https://github.com/RaetProtocol/raet
Source0:        http://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-six
BuildRequires:  python%{?__python_ver}-ioflo >= 1.3.8-1
Requires:  python%{?__python_ver}-libnacl >= 1.4.3-1
Requires:  python%{?__python_ver}-six

%if ! 0%{?with_explicit_python27}
Requires:  python%{?__python_ver}-simplejson
%endif 

Requires:  python%{?__python_ver}-ioflo >= 1.3.8-1
BuildArch: noarch

%if "%{?pybasever}" == "2.6"
BuildRequires:  python-importlib
Requires:       python-importlib
%endif

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
Provides: python-%{srcname} = %{version}-%{release}
Obsoletes: python-%{srcname} < %{version}-%{release}
%endif 

Patch0:         raet-0.6.6.patch


# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_setup
}

%description
A high level, stack based communication protocol for network and IPC communication

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

%install
%{__python} setup.py install --root %{buildroot}

%files
%{_bindir}/raetflo
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info
%exclude %{python_sitelib}/systest*

%changelog
* Mon Jul 17 2017 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.6-2
- Updated to use Python 2.7 on Redhat 6

* Tue Jan 17 2017 Packaging <packaging@saltstack.com> - 0.6.6-1
- Patched fix to overcome lack of kwargs support with decode in python2.6

* Wed Dec  7 2016 Packaging <packaging@saltstack.com> - 0.6.5-1
- Build 0.6.5 for Salt implementation on various versions Redhat

* Thu Aug  6 2015 Packaging <packaging@saltstack.com> - 0.6.3-2
- Build 0.6.3 for Salt implementati
on on various versions Redhat


