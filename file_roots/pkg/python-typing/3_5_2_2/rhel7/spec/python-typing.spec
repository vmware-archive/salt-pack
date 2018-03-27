Name:           python-typing
Version:        3.5.2.2
Release:        3%{?dist}
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


%prep
%setup -qc
mv typing-%{version} python2
cp -al python2 python3
cp -al python2/{README.rst,LICENSE} .

%build
cd python2
%{py2_build}
cd -
cd python3
%{py3_build}
cd -

%install
cd python2
%{py2_install}
cd -
cd python3
%{py3_install}
cd -

%files -n python2-typing
%doc README.rst
%license LICENSE
%{python2_sitelib}/typing*

%files -n python34-typing
%doc README.rst
%license LICENSE
%{python3_sitelib}/typing*
%{python3_sitelib}/__pycache__/typing*

%changelog
* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-3
- Bump release to supercede previous python2-typing

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-2
- Build python2/3 separately to ensure proper install

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-1
- Initial EPEL package
