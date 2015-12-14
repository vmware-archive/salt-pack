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

%define debug_package %{nil}


%global srcname timelib

Name:           python-%{srcname}
Version:        0.2.4
Release:        1%{?dist}
Summary:        Parse English textual date descriptions

Group:          Development/Languages/Python

## License:        PHP and zlib
License:        MIT

URL:            http://pypi.python.org/pypi/timelib/
Source0:        http://pypi.python.org/packages/source/t/%{srcname}/%{srcname}-%{version}.zip

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if 0%{?rhel} == 5
BuildRequires:  python26
BuildRequires:  python26-devel
Requires:       python26
%else

BuildRequires:  python-devel
BuildRequires:  python-setuptools
%endif

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
Group:    Development/Languages/Python

%description -n python3-%{srcname}
timelib is a short wrapper around php's internal timelib modules
It currently only provides a few functions:

timelib.strtodatetime
timelib.strtotime
%endif

%if 0%{?rhel} == 5
%package -n python26-%{srcname}
Summary:  Parse English textual date descriptions
Group:    Development/Languages/Python
Requires: python26
Requires: python26-importlib

%description -n python26-%{srcname}
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

%if 0%{?rhel} == 5
%files -n python26-%{srcname}
%defattr(-,root,root,-)
%{python2_sitearch}/%{srcname}*.so
%{python2_sitearch}/%{srcname}*.egg-info
%else
%files
%defattr(-,root,root,-)
%{python2_sitearch}/%{srcname}*.so
%{python2_sitearch}/%{srcname}*.egg-info
%exclude %{_libdir}/debug/
%exclude %{_libdir}/../src/debug/
%endif

%changelog
* Fri Aug  7 2015 Packaging <packaging@saltstack.com> - 0.2.4-1
- Initial build 0.2.4 for Salt implementation

