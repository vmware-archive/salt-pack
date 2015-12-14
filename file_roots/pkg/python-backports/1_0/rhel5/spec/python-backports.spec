%global __python2 /usr/bin/python2.6
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global srcname backports

Name:           python-%{srcname}
Version:        1.0
Release:        4%{?dist}
Summary:        Namespace for backported Python features

Group:          Development/Languages
# Only code is sourced from http://www.python.org/dev/peps/pep-0382/
License:        Public Domain
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        backports.py

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python26-devel
Requires:       python26

%description
The backports namespace is a namespace reserved for features backported from
the Python standard library to older versions of Python 2.

Packages that exist in the backports namespace in Fedora should not provide
their own backports/__init__.py, but instead require this package.

Backports to earlier versions of Python 3, if they exist, do not need this
package because of changes made in Python 3.3 in PEP 420
(http://www.python.org/dev/peps/pep-0420/).

%package -n python26-%{srcname}
Summary:        Namespace for backported Python features
Group:          Development/Languages
Requires:       python26

%description -n python26-%{srcname}
The backports namespace is a namespace reserved for features backported from
the Python standard library to older versions of Python 2.

Packages that exist in the backports namespace in Fedora should not provide
their own backports/__init__.py, but instead require this package.

Backports to earlier versions of Python 3, if they exist, do not need this
package because of changes made in Python 3.3 in PEP 420
(http://www.python.org/dev/peps/pep-0420/).

%prep


%build


%install
rm -rf %{buildroot}
mkdir -pm 755 %{buildroot}%{python2_sitelib}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python2_sitelib}/backports/__init__.py
%if "%{python2_sitelib}" != "%{python2_sitearch}"
mkdir -pm 755 %{buildroot}%{python2_sitearch}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python2_sitearch}/backports/__init__.py
%endif

%clean
rm -rf %{buildroot}
 
%files -n python26-%{srcname}
%defattr(-,root,root,-)
%{python2_sitelib}/backports
%if "%{python2_sitelib}" != "%{python2_sitearch}"
%{python2_sitearch}/backports
%endif


%changelog
* Fri Jul 25 2014 Erik Johnson <erik@saltstack.com> - 1.0-4
- Initial EL5 build

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 1.0-3
- Install to both python_sitelib and python_sitearch

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 1.0-2
- Install to the correct location

* Fri Aug 16 2013 Ian Weller <iweller@redhat.com> - 1.0-1
- Initial package build
