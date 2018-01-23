%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora} > 12 || 0%{?rhel} > 7
# Should not build for Python 3 for Fedora releases that provide
# Python 3.4 (Fedora 22 or higher?).
%global with_python3 1
%endif

%if 0%{?rhel} == 6
%global with_python3 0

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

Name:           python%{?__python_ver}-enum34
Version:        1.0
Release:        6%{?dist}
Group:          Development/Libraries
Summary:        Backport of Python 3.4 Enum
License:        BSD
BuildArch:      noarch
URL:            https://pypi.python.org/pypi/enum34
Source0:        https://pypi.python.org/packages/source/e/enum34/enum34-%{version}.tar.gz

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel 
%else
BuildRequires:  python2-devel 
%endif
BuildRequires:  python%{?__python_ver}-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif # if with_python3

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%endif 


%description
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%if 0%{?with_python3}
%package -n python3-enum34
Summary:        Backport of Python 3.4 Enum
Group:          Development/Libraries

%description -n python3-enum34
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%endif # with_python3

%prep
%setup -q -n enum34-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python2} setup.py build

%check
pushd %{buildroot}/%{python2_sitelib}
%{__python2} enum/test_enum.py
popd
%if 0%{?with_python3}
pushd %{buildroot}/%{python3_sitelib}
%{__python3} enum/test_enum.py
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python3_sitelib}/enum/{LICENSE,README,doc}
popd
%endif # with_python3
%{__python2} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python2_sitelib}/enum/{LICENSE,README,doc}

%files
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-enum34
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Mon Jan 22 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.0-6
- Removed os_install_post override

* Mon May 08 2017 SaltStack Packaging Team <packaging@saltstack.com> - 1.0-5
- Updated to use Python 2.7 on Redhat 6

* Mon Jul 21 2014 Matěj Cepl <mcepl@redhat.com> - 1.0-4
- No, we don’t have python3 in RHEL-7 :'(

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 26 2014 Eric Smith <brouhaha@fedoraproject.org> 1.0-1
- Updated to latest upstream.

* Mon Mar 17 2014 Eric Smith <brouhaha@fedoraproject.org> 0.9.23-1
- Updated to latest upstream.
- Spec updated per review comments (#1033975).

* Sun Nov 24 2013 Eric Smith <brouhaha@fedoraproject.org> 0.9.19-1
- Initial version.
