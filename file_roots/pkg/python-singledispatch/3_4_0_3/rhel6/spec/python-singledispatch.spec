%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if ( "0%{?dist}" == "0.amzn1" )
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}

# work-around Amazon Linux get_python_lib returning  /usr/lib64/python2.7/dist-packages
%global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%global python2_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%global __inst_layout --install-layout=unix
%endif

%if ( 0%{?rhel} == 6)
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%bcond_with tests

%global pypi_name singledispatch

Name:           python-%{pypi_name}
Version:        3.4.0.3
Release:        16%{?dist}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3

License:        MIT
URL:            http://docs.python.org/3/library/functools.html#functools.singledispatch
Source0:        https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-six

Requires:       python%{?__python_ver}-six

%description
PEP 443 proposed to expose a mechanism in the functools standard library
module in Python 3.4 that provides a simple form of generic programming 
known as single-dispatch generic functions.

This library is a backport of this functionality to Python 2.6 - 3.3.

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{pypi_name}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3

# python_provide does not exist in CBS Cloud buildroot
Provides:       python-%{pypi_name} = %{version}-%{release}
Obsoletes:      python-%{pypi_name} < 3.4.0.3-2

%description -n python%{?__python_ver}-%{pypi_name}
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
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if %{with tests}
%check
%{__python} setup.py test
%endif

%if 0%{?with_explicit_python27}
%files -n python%{?__python_ver}-%{pypi_name}
%doc README.rst
%{python_sitelib}/%{pypi_name}-%{version}*
%{python_sitelib}/%{pypi_name}.py*
%{python_sitelib}/%{pypi_name}_helpers.py*
%else
%files
%doc README.rst
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{pypi_name}.py*
%{python_sitelib}/%{pypi_name}_helpers.py*
%endif

%changelog
* Tue Jan 28 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.0.3-16
- Made support for Amazon Linux 1, RHEL 7 and 6, stripped Python 3 support, purely Python 2.7

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
