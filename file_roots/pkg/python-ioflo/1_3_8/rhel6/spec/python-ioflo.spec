%if 0%{?fedora} > 12 || 0%{?rhel} > 8
%global with_python3 1
%else

%if 0%{?rhel} < 7
%global pybasever 2.6
%global __python_ver 26
%endif

%{!?__python2: %global __python2 /usr/bin/python%{?pybasever}}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%endif

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __os_install_post %{__python27_os_install_post}
%endif

%global srcname ioflo

Name:           python%{?__python_ver}-%{srcname}
Version:        1.3.8
Release:        2%{?dist}
Summary:        Flow-based programming interface

Group:          Development/Libraries
License:        MIT
URL:            http://ioflo.com
Source0:        http://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%else
BuildRequires:  python%{?__python_ver}-importlib
Requires:       python%{?__python_ver}-importlib

%endif 


%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Ioflo is a flow-based programming automated reasoning engine and automation
operation system, written in Python.


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:  Flow-based programming interface
Group:    Development/Libraries

%description -n python3-%{srcname}
Ioflo is a flow-based programming automated reasoning engine and automation
operation system, written in Python.
%endif

%prep
%setup -q -n %{srcname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
sed -i -e '1d' %{buildroot}%{python3_sitelib}/%{srcname}/app/test/example.py
sed -i -e '1d' %{buildroot}%{python3_sitelib}/%{srcname}/app/test/testStart.py
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}
## sed -i -e '1d' %{buildroot}%{python2_sitelib}/%{srcname}/app/test/example.py
## sed -i -e '1d' %{buildroot}%{python2_sitelib}/%{srcname}/app/test/testStart.py

%if 0%{?with_python3}
sed -i '1s|^#!%{__python3}|#!%{__python2}|' %{buildroot}/usr/bin/ioflo
%endif

%clean
rm -rf %{buildroot}

%if 0%{?with_python3}
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%endif

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/%{srcname}
%{_bindir}/%{srcname}2

%changelog
* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 
- Updated to use Python 2.7 on Redhat 6
- Removed support for Redhat 5

* Wed Aug  5 2015 Packaging <packaging@saltstack.com> - 1.3.8-1
- Build 1.3.8 for Salt implementation

* Tue May 26 2015 Erik Johnson <erik@saltstack.com> - 1.0.2-2
- Fix python dependency for Python 2 package

* Wed Nov 19 2014 Erik Johnson <erik@saltstack.com> - 1.0.2-1
- Updated to 1.0.2

* Thu Oct  2 2014 Erik Johnson <erik@saltstack.com> - 1.0.1-1
- Updated to 1.0.1

* Thu Aug 14 2014 Erik Johnson <erik@saltstack.com> - 0.9.39-2
- Fix dual deployment of ioflo executable

* Thu Jul 24 2014 Erik Johnson <erik@saltstack.com> - 0.9.39-1
- Updated to 0.9.39

* Wed Jul 23 2014 Erik Johnson <erik@saltstack.com> - 0.9.38-1
- Updated to 0.9.38

* Fri Jun 20 2014 Erik Johnson <erik@saltstack.com> - 0.9.35-1
- Initial build
