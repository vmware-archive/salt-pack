%global with_python3 0

%global tarball_name apache-libcloud
%global srcname libcloud
%global eggname apache_libcloud
%global _description \
libcloud is a client library for interacting with many of \
the popular cloud server providers.  It was created to make \
it easy for developers to build products that work between \
any of the services that it supports.

# Don't duplicate the same documentation
%global _docdir_fmt %{name}


Name:           python-libcloud
Version:        2.0.0
Release:        2%{?dist}
Summary:        A Python library to address multiple cloud provider APIs

Group:          Development/Languages
License:        ASL 2.0
URL:            http://libcloud.apache.org/
Source0:        http://www-us.apache.org/dist/libcloud/%{tarball_name}/%{tarball_name}-%{version}.tar.gz

BuildArch:      noarch

%description %{_description}

%package -n python2-%{srcname}
Summary:        %{summary}
## BuildRequires:  python2-devel
## BuildRequires:  python2-setuptools
BuildRequires:  python-devel
BuildRequires:  python-setuptools
##%{?python_provide:%python_provide python2-%{srcname}}
%python_provide python-%{srcname}

%description -n python2-%{srcname} %{_description}
Python 2 version.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}
Python 3 version.
%endif

%prep
%autosetup -n %{tarball_name}-%{version}

# Delete shebang lines in the demos
sed -i '1d' demos/gce_demo.py demos/compute_demo.py

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

# Fix permissions for demos
chmod -x demos/gce_demo.py demos/compute_demo.py

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Don't package the test suite. We dont run it anyway
# because it requires some valid cloud credentials
rm -r $RPM_BUILD_ROOT%{python2_sitelib}/%{srcname}/test

%if 0%{?with_python3}
rm -r $RPM_BUILD_ROOT%{python3_sitelib}/%{srcname}/test
%endif

%files -n python2-%{srcname}
%doc README.rst demos/
%license LICENSE
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{eggname}-*.egg-info/


%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst demos/
%license LICENSE
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{eggname}-*.egg-info/
%endif

%changelog
* Thu May 25 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2.0.0-2
- Removed support for Python 3, and support for RHEL

* Wed Apr 19 2017 Daniel Bruno <dbruno@fedoraproject.org> - 2.0.0-1
- Apache Libcloud version 2.0.0 upgrade

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-3
- Rebuild for Python 3.6

* Wed Nov 16 2016 Dominika Krejci <dkrejci@redhat.com> - 1.3.0-2
- Add python3 subpackage
- Include the upstream demos
- Don't package the test suite

* Mon Oct 24 2016 Daniel Bruno <dbruno@fedoraproject.org> - 1.3.0-1
- Python Libcloud 1.3.0 release

* Tue Jul 12 2016 Daniel Bruno <dbruno@fedoraproject.org> - 1.1.0-1
- Python Libcloud 1.1.0 release

* Sun Jan 24 2016 Daniel Bruno <dbruno@fedoraprojec.org> - 0.20.1-1
- This is a bug-fix release of the 0.20 series.

* Thu Jan 07 2016 Daniel Bruno dbruno@fedoraproject.org - 0.20.0-1
- Release 0.20.0 with new features and improvements

* Mon Aug 10 2015 Daniel Bruno <dbruno@fedoraproject.org> - 0.18.0-1
- Apache Libcloud 0.18.0 release with bug fixes and new features

* Fri Feb 20 2015 Daniel Bruno <dbruno@fedoraproject.org> - 0.17.0-1
- Apache Libcloud 0.17.0 release

* Wed Nov 12 2014 Daniel Bruno <dbruno@fedoraproject.org> - 0.16.0-1
- First release in the 0.16 series

* Mon Jul 21 2014 Daniel Bruno <dbruno@fedoraproject.org - 0.15.1-2
- Libcloud 0.15.1 bug-fix release

* Fri Jun 27 2014 Daniel Bruno <dbruno@fedoraproject.org> - 0.15.0-1
- First release in the 0.15 series which it brings many new features,
  improvements and bug fixes

* Mon Feb 10 2014 Daniel Bruno <dbruno@fedoraproject.org> - 0.14.1-1
- Release 0.14.1 includes some bug-fixes, improvements and new features

* Fri Jan 31 2014 Daniel Bruno <dbruno@fedoraproject.org> - 0.14.0-1
- Libcloud new release 0.14.0

* Fri Jan 03 2014 Daniel Bruno <dbruno@fedoraproject.org> - 0.13.3-1
- Security Fix - BUG: 1047867 1047868

* Thu Sep 19 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.13.2-11
- Some bug fixes from Upstream

* Mon Sep 09 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.13.1-10
- Update to upstream release 0.13.1

* Mon Jul 01 2013 Daniel Bruno dbruno@fedoraproject.org - 0.13.0-9
- Update to upstream release 0.13.0, more details on Release Notes.

* Thu May 16 2013 Daniel Bruno dbruno@fedoraproject.org - 0.12.4-8
- Update to upstream version 0.12.4

* Tue Mar 26 2013 Daniel Bruno dbruno@fedoraproject.org - 0.12.3-6
- Update to upstream version 0.12.3

* Tue Feb 19 2013 Daniel Bruno dbruno@fedoraproject.org - 0.12.1-5
- Update to upstream version 0.12.1

* Wed Oct 10 2012 Daniel Bruno dbruno@fedoraproject.org - 0.11.3-4
- Update to 0.11.3

* Thu Aug 02 2012 Daniel Bruno dbruno@fedoraproject.org - 0.11.1-3
- Updating to upstream release 0.11.1

* Fri Jun 15 2012 Daniel Bruno dbruno@fedoraproject.org - 0.9.1-2
- Update to upstream version 0.10.1

* Mon Apr 16 2012 Daniel Bruno dbruno@fedoraproject.org - 0.9.1-1
- update to 0.9.1

* Mon Mar 26 2012 Daniel Bruno dbruno@fedoraproject.org - 0.8.0-4
- Updating release to 0.8.0

* Fri Dec 30 2011 Daniel Bruno dbruno@fedoraproject.org - 0.6.2-3
- Standardizing the description

* Tue Nov 22 2011 Daniel Bruno dbruno@fedoraproject.org - 0.6.2-2
- First build package build

