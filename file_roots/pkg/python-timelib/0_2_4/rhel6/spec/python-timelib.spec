%if 0%{?fedora} > 12
%global with_python3 1
%else

%if 0%{?rhel} < 7
%global pybasever 2.6
%endif

%{!?__python2: %global __python2 /usr/bin/python%{?pybasever}}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%endif

%if 0%{?rhel} == 6
%global with_python3 0

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
%define debug_package %{nil}

%global srcname timelib

Name:           python%{?__python_ver}-%{srcname}
Version:        0.2.4
Release:        3%{?dist}
Summary:        Parse English textual date descriptions

Group:          Development/Languages

## License:        PHP and zlib
License:        MIT

URL:            http://pypi.python.org/pypi/timelib/
Source0:        http://pypi.python.org/packages/source/t/%{srcname}/%{srcname}-%{version}.zip

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
%filter_setup
}

%description
timelib is a short wrapper around php's internal timelib modules
It currently only provides a few functions:

timelib.strtodatetime
timelib.strtotime


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:  Parse English textual date descriptions
Group:    Development/Languages

%description -n python3-%{srcname}
timelib is a short wrapper around php's internal timelib modules
It currently only provides a few functions:

timelib.strtodatetime
timelib.strtotime
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
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}


%if 0%{?with_python3}
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%{python3_sitearch}/%{srcname}*.so
%{python3_sitearch}/%{srcname}*.egg-info
%endif

%files
%defattr(-,root,root,-)
%{python2_sitearch}/%{srcname}*.so
%{python2_sitearch}/%{srcname}*.egg-info

%changelog
* Mon Jan 22 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.2.4-3
- Removed os_install_post override

* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 0.2.4-2
- Updated to use Python 2.7 on Redhat 6
- Removed support for Redhat 5

* Fri Aug  7 2015 Packaging <packaging@saltstack.com> - 0.2.4-1
- Initial build 0.2.4 for Salt implementation

