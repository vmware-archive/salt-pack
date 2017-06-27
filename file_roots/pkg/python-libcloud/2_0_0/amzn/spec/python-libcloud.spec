%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}

# work-around Amazon Linux get_python_lib returning  /usr/lib64/python2.7/dist-packages
## %global python2_sitelib  %{_libdir}/python2.7/site-packages 
## %global __inst_layout --install-layout=unix
%global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

%else
%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

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
Source0:        http://pypi.python.org/packages/source/a/apache-libcloud/%{tarball_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

%if 0%{?with_explicit_python27}
BuildRequires:  python27-setuptools
BuildRequires:  python27-devel
%else
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
%endif

%description %{_description}

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{srcname}
Summary:        %{summary}

%description -n python%{?__python_ver}-%{srcname} %{_description}
This package is meant to be used with Python 2.7.
%endif

%prep
%setup -n %{tarball_name}-%{version}

# Delete shebang lines in the demos
sed -i '1d' demos/gce_demo.py demos/compute_demo.py

%build
%{__python2} setup.py build

# Fix permissions for demos
chmod -x demos/gce_demo.py demos/compute_demo.py

%install
rm -rf %{buildroot}
%{__python2} setup.py install -O1 --skip-build %{?__inst_layout } --root %{buildroot}

# Don't package the test suite. We dont run it anyway
# because it requires some valid cloud credentials
rm -r $RPM_BUILD_ROOT%{python2_sitelib}/%{srcname}/test


%clean
rm -rf %{buildroot}


%files -n python%{?__python_ver}-%{srcname}
%doc README.rst demos/
%license LICENSE
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{eggname}-*.egg-info/


%changelog
* Mon Jun 05 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2.0.0-2
- Apache Libcloud version 2.0.0 upgrade for Amazon

* Wed Oct 19 2016 SaltStack Packaging Team <packaging@saltstack.com> - 0.20.0-2
- Ported to build on Amazon Linux 2016.09 natively

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
