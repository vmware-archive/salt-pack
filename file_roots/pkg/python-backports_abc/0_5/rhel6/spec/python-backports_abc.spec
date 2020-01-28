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

%global srcname backports_abc
%global sum A backport of recent additions to the 'collections.abc' module

Name:           python-%{srcname}
Version:        0.5
Release:        11%{?dist}
Summary:        %{sum}

License:        Python
URL:            https://pypi.python.org/pypi/backports_abc
Source0:        https://files.pythonhosted.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch


%if 0%{?with_explicit_python27}
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
%else
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%endif


%description
%{sum}.

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{srcname}
Summary:        %{sum}

%description -n python%{?__python_ver}-%{srcname}
%{sum}.
%endif


%prep
%autosetup -n %{srcname}-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if %{with tests}
%check
%{__python2} setup.py test
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%if 0%{?with_explicit_python27}
%files -n python%{?__python_ver}-%{srcname}
%license LICENSE
%doc CHANGES.rst README.rst
%{python2_sitelib}/*
%else
%files 
%license LICENSE
%doc CHANGES.rst README.rst
%{python_sitelib}/*
%endif


%changelog
* Tue Jan 28 2020 SaltStack Packaging Team <packaging@saltstack.com> - 0.5-11
- Made support for Amazon Linux 1, stripped Python 3 support, purely Python 2.7

* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 0.5-10
- Made support for Python 2 optional and Python3 default

* Thu Feb 07 2019 SaltStack Packaging Team <packaging@#saltstack.com> -0.5-9
- Support for Python 3 on Amazon Linux 2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> -0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5-7
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.5-2
- Rebuild for Python 3.6

* Tue Nov 22 2016 Orion Poplawski <orion@cora.nwra.com> - 0.5-1
- Update to 0.5

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 18 2016 Orion Poplawski <orion@cora.nwra.com> - 0.4-3
- Use %%{python3_pkgversion}

* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 0.4-2
- Fix python3 package file ownership

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 0.4-1
- Initial package
