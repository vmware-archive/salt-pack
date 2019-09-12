%bcond_without python2
%bcond_with python3

Name:           python-typing
Version:        3.5.2.2
Release:        4%{?dist}
Summary:        Typing defines a standard notation for type annotations
License:        Python
URL:            https://pypi.python.org/pypi/typing
Source0:        https://files.pythonhosted.org/packages/source/t/typing/typing-%{version}.tar.gz
BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.

%if %{with python2}
%package -n python2-typing
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%{?python_provide:%python_provide python2-typing}

%description -n python2-typing
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.
%endif

%if %{with python3}
%package -n python34-typing
Summary:        %{summary}
BuildRequires:  python34-devel
BuildRequires:  python34-setuptools
%{?python_provide:%python_provide python34-typing}

%description -n python34-typing
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.
%endif


%prep
%setup -qc
%if %{with python2}
mv typing-%{version} python2
cp -al python2 python3
cp -al python2/{README.rst,LICENSE} .
%endif

%if %{with python3}
mv typing-%{version} python3
cp -al python3/{README.rst,LICENSE} .
%endif

%build
%if %{with python2}
cd python2
%{py2_build}
cd -
%endif
%if %{with python3}
cd python3
%{py3_build}
cd -
%endif

%install
%if %{with python2}
cd python2
%{py2_install}
cd -
%endif
%if %{with python3}
cd python3
%{py3_install}
cd -
%endif

%files -n python2-typing
%if %{with python2}
%doc README.rst
%license LICENSE
%{python2_sitelib}/typing*
%endif

%if %{with python3}
%files -n python34-typing
%doc README.rst
%license LICENSE
%{python3_sitelib}/typing*
%{python3_sitelib}/__pycache__/typing*
%endif

%changelog
* Wed Sep 11 2019 SaltStack Packaging Team <packaging@saltstack.com> 3.5.2.2-4
- Added conditional building for Python2 and Python 3, default only Python 2

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-3
- Bump release to supercede previous python2-typing

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-2
- Build python2/3 separately to ensure proper install

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-1
- Initial EPEL package
