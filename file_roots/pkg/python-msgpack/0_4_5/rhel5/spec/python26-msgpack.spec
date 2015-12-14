%global __python26 /usr/bin/python2.6
%define python26_sitelib %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%{!?python_sitearch: %global python_sitearch %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global __os_install_post %{__python26_os_install_post}

%global srcname msgpack

Name:           python26-%{srcname}
Version:        0.4.5
Release:        1%{?dist}
Summary:        A Python MessagePack (de)serializer

Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/msgpack-python/
Source0:        http://pypi.python.org/packages/source/m/%{srcname}-python/%{srcname}-python-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  python26-devel
BuildRequires:  python26-distribute

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}


%description
MessagePack is a binary-based efficient data interchange format that is
focused on high performance. It is like JSON, but very fast and small.
This is a Python (de)serializer for MessagePack.


%prep
%setup -q -n %{srcname}-python-%{version}


%build
%{__python26} setup.py build


%install
rm -rf %{buildroot}
%{__python26} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{python_sitearch}/%{srcname}/
%{python_sitearch}/%{srcname}*.egg-info


%changelog
* Tue Feb 17 2015 Erik Johnson <erik@saltstack.com> - 0.4.5-1
- Updated to version 0.4.5

* Tue Jan 31 2012 Clint Savage <herlo1@gmail.com> - 0.1.12-2
- Python 2.6 version of upstream

* Tue Jan 31 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.12-1
- Updated to new upstream version 0.1.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.10-1
- Updated to new upstream version 0.1.10
- README is gone

* Tue Jul 12 2011 Dan Horák <dan[at]danny.cz> - 0.1.9-3
- fix build on big endian arches

* Fri Jun 24 2011 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.9-2
- Tests are failing, they are not active at the moment
- Filtering added

* Sat Mar 26 2011 Fabian Affolter <mail@fabian-affolter.ch> - 0.1.9-1
- Initial package
