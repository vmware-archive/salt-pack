%global __python2 /usr/bin/python2.6
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")

%global srcname urllib3

Name:           python-urllib3
Version:        1.5
Release:        8%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

Group:          Development/Languages
License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz

# Patch to change default behaviour to check SSL certs for validity
# https://bugzilla.redhat.com/show_bug.cgi?id=855320
# https://bugzilla.redhat.com/show_bug.cgi?id=1124060
Patch0:         python-urllib3-default-ssl-cert-validate-el5.patch

### TODO: Send this to upstream urllib3
# make all imports of things in packages try system copies first
Patch1:         python-urllib3-unbundle.patch

# Fix accept header when behind a proxy
#https://github.com/shazow/urllib3/pull/93
#https://github.com/shazow/urllib3/pull/93.patch
Patch2:         python-urllib3-accept-header-for-proxy.patch

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python26-devel
BuildRequires:  python26-distribute
BuildRequires:  python26-ordereddict
Requires:       openssl
Requires:       python26
Requires:       python26-backports-ssl_match_hostname
Requires:       python26-ordereddict
Requires:       python26-six

%description
Python HTTP module with connection pooling and file POST abilities.

%package -n python26-%{srcname}
Summary:        Python HTTP library with thread-safe connection pooling and file post
Group:          Development/Languages
Requires:       openssl
Requires:       python26
Requires:       python26-backports-ssl_match_hostname
Requires:       python26-ordereddict
Requires:       python26-six

%description -n python26-%{srcname}
Python HTTP module with connection pooling and file POST abilities.

%prep
%setup -q -n %{srcname}-%{version}

rm -rf urllib3/packages/

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}
 
%files -n python26-%{srcname}
%defattr(-,root,root,-)
%doc CHANGES.rst LICENSE.txt README.rst CONTRIBUTORS.txt
%{python2_sitelib}/*

%changelog
* Thu Jul 24 2014 Erik Johnson <erik@saltstack.com> - 1.5-8
- Initial EL5 build

* Mon Oct 28 2013 Ralph Bean <rbean@redhat.com> - 1.5-7
- Update patch to find ca_certs in the correct place.

* Tue Jun 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-6
- Fix Requires of python-ordereddict to only apply to RHEL

* Fri Mar  1 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-5
- Unbundling finished!

* Fri Mar 01 2013 Ralph Bean <rbean@redhat.com> - 1.5-4
- Upstream patch to fix Accept header when behind a proxy.
- Reorganize patch numbers to more clearly distinguish them.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.5-3
- Renamed patches to python-urllib3-*
- Fixed ssl check patch to use the correct cert path for Fedora.
- Included dependency on ca-certificates
- Cosmetic indentation changes to the .spec file.

* Tue Feb  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- python3-tornado BR and run all unittests on python3

* Mon Feb 04 2013 Toshio Kuratomi <toshio@fedoraproject.org> 1.5-1
- Initial fedora build.

