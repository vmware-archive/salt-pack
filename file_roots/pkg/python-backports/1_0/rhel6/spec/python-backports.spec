# https://bugzilla.redhat.com/show_bug.cgi?id=998047

%if 0%{?rhel} == 6
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:           python%{?__python_ver}-backports
Version:        1.0
Release:        7%{?dist}
Summary:        Namespace for backported Python features

# Only code is sourced from http://www.python.org/dev/peps/pep-0382/
License:        Public Domain
URL:            https://pypi.python.org/pypi/backports
Source0:        backports.py

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
%else
BuildRequires:  python2-devel
%endif

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%endif 


%description
The backports namespace is a namespace reserved for features backported from
the Python standard library to older versions of Python 2.

Packages that exist in the backports namespace in RHEL should not provide
their own backports/__init__.py, but instead require this package.

Backports to earlier versions of Python 3, if they exist, do not need this
package because of changes made in Python 3.3 in PEP 420
(http://www.python.org/dev/peps/pep-0420/).


%prep


%build


%install
mkdir -pm 755 %{buildroot}%{python2_sitelib}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python2_sitelib}/backports/__init__.py
%if "%{python2_sitelib}" != "%{python2_sitearch}"
mkdir -pm 755 %{buildroot}%{python2_sitearch}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python2_sitearch}/backports/__init__.py
%endif

 
%files
%{python2_sitelib}/backports
%if "%{python2_sitelib}" != "%{python2_sitearch}"
%{python2_sitearch}/backports
%endif


%changelog
* Mon Jan 22 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.0-7
- Removed os_install_post override

* Fri Sep 22 2017 SaltStack Packaging Team <packaging@saltstack.com> - 1.0-6
- Updated to use Python 2.7 on Redhat 6

* Wed Apr 29 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.0-5
- Fix description
Resolves: rhbz#1208226

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.0-4
- Rebuild for RHEL 6.7
Resolves: rhbz#1183141

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 1.0-3
- Install to both python_sitelib and python_sitearch

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 1.0-2
- Install to the correct location

* Fri Aug 16 2013 Ian Weller <iweller@redhat.com> - 1.0-1
- Initial package build
