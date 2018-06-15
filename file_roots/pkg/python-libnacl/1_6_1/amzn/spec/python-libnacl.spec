%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python2 %{_bindir}/python%{?pybasever}
%global __inst_layout --install-layout=unix

%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%else
%if 0%{?fedora} > 12 
%global with_python3 1
%endif

%{!?python3_pkgversion:%global python3_pkgversion 3}

%{!?__python2: %global __python2 /usr/bin/python%{?pybasever}}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname libnacl

Name:           python-%{srcname}
Version:        1.6.1
Release:        2%{?dist}
Summary:        Python bindings for libsodium/tweetnacl based on ctypes

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/saltstack/libnacl
Source0:        https://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  libsodium
Requires:       libsodium

BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description
This library is used to gain direct access to the functions exposed by Daniel
J. Bernstein's nacl library via libsodium or tweetnacl. It has been constructed
to maintain extensive documentation on how to use nacl as well as being
completely portable. The file in libnacl/__init__.py can be pulled out and
placed directly in any project to give a single file binding to all of nacl.

This is the Python 2 build of the module.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Python bindings for libsodium/tweetnacl based on ctypes
Group:    Development/Libraries
Requires: libsodium

%description -n python%{python3_pkgversion}-%{srcname}
This library is used to gain direct access to the functions exposed by Daniel
J. Bernstein's nacl library via libsodium or tweetnacl. It has been constructed
to maintain extensive documentation on how to use nacl as well as being
completely portable. The file in libnacl/__init__.py can be pulled out and
placed directly in any project to give a single file binding to all of nacl.

This is the Python 3 build of the module.
%endif


%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{srcname}
Summary:        Python bindings for libsodium/tweetnacl based on ctypes
Group:          Development/Libraries
BuildRequires:  python%{?__python_ver}
BuildRequires:  libsodium
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
Requires:       python%{?__python_ver}
Requires:       libsodium

%description -n python%{?__python_ver}-%{srcname}
This library is used to gain direct access to the functions exposed by Daniel
J. Bernstein's nacl library via libsodium or tweetnacl. It has been constructed
to maintain extensive documentation on how to use nacl as well as being
completely portable. The file in libnacl/__init__.py can be pulled out and
placed directly in any project to give a single file binding to all of nacl.

This package is meant to be used with Python 2.7.
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
%{__python2} setup.py install --skip-build %{?__inst_layout} --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%clean
rm -rf %{buildroot}

%files -n python%{?__python_ver}-%{srcname}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%doc LICENSE

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc LICENSE
%endif

%changelog
* Fri Jun 08 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.6.1-2
- added python27-setuptools as a BuildRequires for Amazon

* Fri Apr 20 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.6.1-1
- Update to 1.6.1, removed Redhat 5 and adjusted Python 3 support

* Fri Oct 21 2016 SaltStack Packaging Team <packaging@saltstack.com> - 1.4.3-2
- Ported to build on Amazon Linux 2016.09 natively

* Thu Aug  6 2015 Packaging <pqackaging@saltstack.com> - 1.4.3-1
- Updated to 1.4.3, altered license to doc

* Wed May 27 2015 Erik Johnson <erik@saltstack.com> - 1.4.2-1
- Updated to 1.4.2, added license file

* Thu Sep  4 2014 Erik Johnson <erik@saltstack.com> - 1.3.5-1
- Updated to 1.3.5

* Fri Aug 22 2014 Erik Johnson <erik@saltstack.com> - 1.3.3-1
- Updated to 1.3.3

* Fri Aug  8 2014 Erik Johnson <erik@saltstack.com> - 1.3.2-1
- Updated to 1.3.2

* Fri Aug  8 2014 Erik Johnson <erik@saltstack.com> - 1.3.1-1
- Updated to 1.3.1

* Thu Aug  7 2014 Erik Johnson <erik@saltstack.com> - 1.3.0-1
- Updated to 1.3.0

* Fri Jun 20 2014 Erik Johnson <erik@saltstack.com> - 1.0.0-1
- Initial build
