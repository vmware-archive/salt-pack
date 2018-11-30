%global backport_rhel6 1

%if 0%{?backport_rhel6}
%global with_python3 0

%global python python27
%global __python_ver 27
%global python2_version 2.7
%global __python2 %{_bindir}/python%{python2_version}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

%else
%global with_python3 1
%endif

%global pypi_name chardet
Name:           python-%{pypi_name}
Version:        3.0.4
Release:        8%{?dist}
Summary:        Character encoding auto-detection in Python

Group:          Development/Languages
License:        LGPLv2
URL:            https://github.com/%{pypi_name}/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?backport_rhel6}
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-tools
BuildRequires:  python%{?__python_ver}-setuptools
Requires: python%{?__python_ver}
Provides: python-chardet
%else
BuildRequires:  python2-devel, python2-setuptools
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools
%endif # with_python3

%global _description\
Character encoding auto-detection in Python. As\
smart as your browser. Open source.

%description %_description

%package -n python%{?__python_ver}-%{pypi_name}
Summary: %summary
## %%{?python_provide:%%python_provide %%{python}-%%{pypi_name}}
Requires: python%{?__python_ver}
Provides: python%{?__python_ver}-chardet

%description -n python%{?__python_ver}-%{pypi_name} %_description

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Character encoding auto-detection in Python 3

%description -n python3-%{pypi_name}
Character encoding auto-detection in Python. As 
smart as your browser. Open source.

Python 3 version.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
sed -ie '1d' %{pypi_name}/cli/chardetect.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Do Python 3 first not to overwrite the entrypoint
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_bindir}/{,python3-}chardetect
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}/%{_bindir}/chardetect ${RPM_BUILD_ROOT}/%{_bindir}/python%{?__python_ver}-chardetect

%files -n python%{?__python_ver}-%{pypi_name}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/python%{?__python_ver}-chardetect

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/python3-chardetect
%endif # with_python3


%changelog
* Tue Nov 20 2018 SaltStack Packaging Team <packaging@saltstack.com> - 3.0.4-8
- backport to RHEL 6 with Python 2.7 support

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.4-6
- Rebuilt for Python 3.7

* Sun Feb 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0.4-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.4-3
- Python 2 binary package renamed to python2-chardet
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Jeremy Cline <jeremy@jcline.org> - 3.0.4-1
- Update to 3.0.4 (#1441436)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.3.0-2
- Rebuild for Python 3.6

* Wed Jul 27 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-1
- Update to 2.3.0 (#1150536)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 2.2.1-4
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.2.1-2
- fix license handling

* Wed Jul 02 2014 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-1
- Updated to 2.2.1
- Introduced Python 3 subpackage (upstream has merged the codebase)
- Removed BuildRoot and python_sitelib definition
- Use python2 macros instead of just python

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 13 2010 Kushal Das <kushal@fedoraproject.org> 2.0.1-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Aug 04 2008 Kushal Das <kushal@fedoraproject.org> 1.0.1-1
- Initial release

