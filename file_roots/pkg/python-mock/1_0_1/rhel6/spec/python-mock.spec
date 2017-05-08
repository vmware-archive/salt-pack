%if 0%{?fedora} > 12 || 0%{?rhel} >= 6
%global with_python3 0
%endif

# Not yet in Fedora buildroot
%{!?python3_pkgversion:%global python3_pkgversion 3}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __os_install_post %{__python27_os_install_post}
%endif

%global mod_name mock

Name:           python%{?__python_ver}-mock
Version:        1.0.1
Release:        11%{?dist}
Summary:        A Python Mocking and Patching Library for Testing

License:        BSD
URL:            http://www.voidspace.org.uk/python/%{mod_name}/
Source0:        http://pypi.python.org/packages/source/m/%{mod_name}/%{mod_name}-%{version}.tar.gz
Source1:        LICENSE.txt

BuildArch:      noarch

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:  python%{?__python_ver}-setuptools

# For tests
## %if 0%{?rhel} <= 7
## BuildRequires:  python%{?__python_ver}-unittest2
## %endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# For tests
#BuildRequires:  python%{python3_pkgversion}-unittest2
%endif

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver} >= 2.7.9-1
%endif



%description
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%package -n python2-mock
Summary:        A Python Mocking and Patching Library for Testing
%{?python_provide:%python_provide python2-%{mod_name}}

%description -n python2-mock
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-mock
Summary:        A Python Mocking and Patching Library for Testing
%{?python_provide:%python_provide python%{python3_pkgversion}-%{mod_name}}

%description -n python%{python3_pkgversion}-mock
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.
%endif


%prep
%setup -q -n %{mod_name}-%{version}
cp -p %{SOURCE1} .


%build
%{py2_build}
%if 0%{?with_python3}
%{py3_build}
%endif

## %check
## %{__python2} setup.py test
# Failing
#{__python3} setup.py test


%install
%if 0%{?with_python3}
%{py3_install}
%endif
%{py2_install}

 
%if 0%{?with_explicit_python27}
%files -n python%{?__python_ver}-mock
%else
%files -n python2-mock
%endif
%license LICENSE.txt
%doc docs/* README.txt PKG-INFO
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/%{mod_name}.py*

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-mock
%license LICENSE.txt
%doc docs/* README.txt PKG-INFO
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{mod_name}.py*
%{python3_sitelib}/__pycache__/%{mod_name}*
%endif


%changelog
* Mon May 08 2017 SalStack Packaging Team <packaging@saltstack.com> - 1.0.1-11
- Update to use Python 2.6 for Redhat 6

* Fri Oct 14 2016 Tim Orling <ticotimo@gmail.com> - 1.0.1-10
- Enable python3 for rhel >= 6 now that python34 is in el6
- Merge epel7 branch

* Wed Jan 6 2016 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-9
- Modernize spec
- Run python2 tests, python3 failing

* Mon Nov 02 2015 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 1.0.1-7
- Fix #1276771

* Thu Sep 18 2014 Praveen Kumar <kumarparaveen.nitdgp@gmail.com> 1.0.1-5
- Rebuild for RHEL-7
- Disable python3 features

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 1.0.1-3
- rebuild for python 3.4
- disable test suite deps missing

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Luke Macken <lmacken@redhat.com> - 1.0.1-1
- Update to 1.0.1
- Run the test suite
- Add python-unittest2 as a build requirement

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.8.0-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Ralph Bean <rbean@redhat.com> - 0.8.0-2
- Python3 support

* Thu Mar 22 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.8.0-1
- Updated to new version

* Fri Jul 22 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.7.2-1
- Initial RPM release
