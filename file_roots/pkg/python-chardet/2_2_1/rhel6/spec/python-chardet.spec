## %{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global python python27
%global python2_version 2.7
%global __python2 %{_bindir}/python%{python2_version}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%global __os_install_post %{__python27_os_install_post}
%global srcname chardet

Name:           %{python}-%{srcname}
Version:        2.2.1
Release:        3%{?dist}
Summary:        Character encoding auto-detection in Python

Group:          Development/Languages
License:        LGPLv2
URL:            http://chardet.feedparser.org
Source0:        https://pypi.python.org/packages/source/c/chardet/chardet-2.2.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  %{python}-devel
BuildRequires:  %{python}-tools
BuildRequires:  %{python}-setuptools
Requires: %{python}
Provides: python-chardet = %{version}-%{release}
## Obsoletes: python-chardet < %{version}-%{release}

%description
Character encoding auto-detection in Python. As 
smart as your browser. Open source.

## %package -n %{python}-%{srcname}
## Summary:        Character encoding auto-detection in Python
## Group:          Development/Languages
## Requires:       %{python}
## 
## %description -n %{python}-%{srcname}
## Character encoding auto-detection in Python. As smart as your browser. Open
## source.

%prep
%setup -q -n chardet-%{version}
sed -ie '1d' chardet/chardetect.py


%build
# Remove CFLAGS=... for noarch packages (unneeded)
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}/%{_bindir}/chardetect ${RPM_BUILD_ROOT}/%{_bindir}/%{python}-chardetect


%clean
rm -rf $RPM_BUILD_ROOT


%files -n %{python}-%{srcname}
%defattr(-,root,root,-)
%doc LICENSE README.rst
# For noarch packages: sitelib
%{python2_sitelib}/*
%{_bindir}/%{python}-chardetect


%changelog
* Mon Jul 24 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2.2.1-3
- Allow for parallel install

* Mon Jul 17 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2.2.1-2
- Alter to support Python 2.7 on Redhat 6

* Mon Apr 13 2015 Matej Stuchlik <mstuchli@redhat.com> - 2.2.1-1
- Update to 2.2.1
Resolves: rhbz#1176251

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 2.0.1-2
- Rebuild for RHEL 6.7
Resolves: rhbz#1176251

* Wed Jan 13 2010 Kushal Das <kushal@fedoraproject.org> 2.0.1-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Aug 04 2008 Kushal Das <kushal@fedoraproject.org> 1.0.1-1
- Initial release

