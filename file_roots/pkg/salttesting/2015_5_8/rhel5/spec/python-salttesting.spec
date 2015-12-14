%{!?__python2: %global __python2 /usr/bin/python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global srcname SaltTesting

Name:           python-salttesting
Version:        2015.5.8
Release:        3%{?dist}
Summary:        Testing library for SaltStack projects

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/saltstack/salt-testing/
Source0:        https://pypi.python.org/packages/source/S/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Required testing tools needed in the several SaltStack projects.

%prep
%setup -q -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%{python2_sitelib}/*
%{_bindir}/*
%doc README.rst AUTHORS.rst
%{!?_licensedir:%global license %%doc}
%license LICENSE

%changelog
* Fri May 22 2015 Erik Johnson <erik@saltstack.com> - 2015.5.8-3
- Fixed prep and removed string_format.py

* Thu May 21 2015 Erik Johnson <erik@saltstack.com> - 2015.5.8-2
- Fixed license and doc

* Thu May 21 2015 Erik Johnson <erik@saltstack.com> - 2015.5.8-1
- Updated to 2015.5.8

* Tue Sep  2 2014 Erik Johnson <erik@saltstack.com> - 2014.8.5-1
- Updated to 2014.8.5

* Wed Oct 23 2013 Erik Johnson <erik@saltstack.com> - 0.5.1-3
- Remove unneeded cd to build dir

* Wed Oct 23 2013 Erik Johnson <erik@saltstack.com> - 0.5.1-2
- Remove pre-built egg, added python2-devel as build dep.

* Mon Oct 21 2013 Erik Johnson <erik@saltstack.com> - 0.5.1-1
- Initial build.
