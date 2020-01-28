%global pypi_name singledispatch
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%bcond_with python2
%bcond_without python3
%bcond_with tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%endif


Name:           python-%{pypi_name}
Version:        3.4.0.3
Release:        15%{?dist}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3

License:        MIT
URL:            http://docs.python.org/3/library/functools.html#functools.singledispatch
Source0:        https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
PEP 443 proposed to expose a mechanism in the functools standard library
module in Python 3.4 that provides a simple form of generic programming 
known as single-dispatch generic functions.

This library is a backport of this functionality to Python 2.6 - 3.3.

%if %{with python2}
%package -n python2-%{pypi_name}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3
%{?python_provide:%python_provide python2-%{pypi_name}}
# python_provide does not exist in CBS Cloud buildroot
Provides:       python-%{pypi_name} = %{version}-%{release}
Obsoletes:      python-%{pypi_name} < 3.4.0.3-2

%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six

Requires:       python2-six

%description -n python2-%{pypi_name}
PEP 443 proposed to expose a mechanism in the functools standard library
module in Python 3.4 that provides a simple form of generic programming 
known as single-dispatch generic functions.

This library is a backport of this functionality to Python 2.6 - 3.3.
%endif

# python3 packaging stuff
%if %{with python3}
%package -n python3-%{pypi_name}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3
%{?python_provide:%python_provide python3-%{pypi_name}}

%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
Requires:       python3-six

%description -n python3-%{pypi_name}
PEP 443 proposed to expose a mechanism in the functools standard library
module in Python 3.4 that provides a simple form of generic programming 
known as single-dispatch generic functions.

This library is a backport of this functionality to Python 2.6 - 3.3.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}

# remove /usr/bin/env python from scripts
sed -i '1d' singledispatch.py
sed -i '1d' singledispatch_helpers.py

%build
%if %{with python2}
%{__python2} setup.py build
%endif

%if %{with python3}
%{__python3} setup.py build
%endif

%install
%if %{with python2}
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif

%if %{with python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%if %{with tests}
%check
%if %{with python3}
%{__python2} setup.py test
%endif

%if %{with python3}
%{__python3} setup.py test
%endif
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}_helpers.py*
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{pypi_name}.py*
%{python3_sitelib}/%{pypi_name}_helpers.py*
%{python3_sitelib}/__pycache__/*
%endif

%changelog
* Tue Jun 11 2019 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.0.3-15
- Made support for Python 2 optional

* Thu Feb 07 2019 SaltStack Packaging Team <packaging@#saltstack.com> - 3.4.0.3-14
- Support for Python 3 on Amazon Linux 2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.4.0.3-12
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.4.0.3-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 3.4.0.3-9
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 3.4.0.3-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.3-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Sep 06 2015 Matthias Runge <mrunge@redhat.com> - 3.4.0.3-2
- fix provides and obsoletes

* Fri Sep 04 2015 Chandan Kumar <chkumar246@gmail.com> - 3.4.0.3-1
- Added python2 and python3 subpackage
- updated the package to 3.4.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Matthias Runge <mrunge@redhat.com> - 3.4.0.2-2
- add support for epel6

* Tue Mar 18 2014 Matthias Runge <mrunge@redhat.com> - 3.4.0.2-1
- Initial package.
