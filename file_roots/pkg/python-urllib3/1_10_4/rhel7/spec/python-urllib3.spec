%global with_python3 1
%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __os_install_post %{__python27_os_install_post}
%endif

%global _description \
Python HTTP module with connection pooling and file POST abilities.

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname urllib3

Name:           python-%{srcname}
Version:        1.10.4
Release:        3%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz

# Only used for python3 (and for python2 on F22 and newer)
Source1:        ssl_match_hostname_py3.py

# Only used for F21.
Patch0:         python-urllib3-pyopenssl.patch

# Remove logging-clear-handlers from setup.cfg because it's not available in RHEL6's nose
Patch100:       python-urllib3-old-nose-compat.patch

BuildArch:      noarch

Requires:       ca-certificates

# Previously bundled things:
Requires:       python%{?__python_ver}-six

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
Requires: python%{?__python_ver}  >= 2.7.9-1
%else
%if 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
Requires:       python-ordereddict
BuildRequires:  python-backports-ssl_match_hostname
Requires:       python-backports-ssl_match_hostname
%endif

BuildRequires:  python2-devel

# See comment-block in the %%install section.
# https://bugzilla.redhat.com/show_bug.cgi?id=1231381
%if 0%{?fedora} && 0%{?fedora} <= 21
Requires:       python-backports-ssl_match_hostname
BuildRequires:  python-backports-ssl_match_hostname
%endif

%endif


## # For unittests
## BuildRequires:  python-nose
## BuildRequires:  python-mock
## BuildRequires:  python-six
## BuildRequires:  python-tornado

%description    %{_description}    

%package    -n  python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-six
%{?python_provide:%python_provide python-%{srcname}}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}
Python 2 version.


%if 0%{?with_python3}
%package    -n  python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
# For unittests
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-tornado
Requires:       ca-certificates
Requires:       python%{python3_pkgversion}-six

## %{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Provides:       python%{python3_pkgversion}-%{srcname}

# Note: Will not run with python3 < 3.2 (unless python3-backports-ssl_match_hostname is created)
%description -n python%{python3_pkgversion}-%{srcname} %{_description}
Python 3 version.
%endif # with_python3


%prep
%setup -n %{srcname}-%{version}

# Drop the dummyserver tests in koji.  They fail there in real builds, but not
# in scratch builds (weird).
rm -rf test/with_dummyserver/

%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
rm -rf %{buildroot}
%py2_install

rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python2_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py
ln -s ../../backports/ssl_match_hostname %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python2_sitelib}/dummyserver

%if 0%{?with_python3}
%py3_install

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python3_sitelib}/dummyserver
%endif # with_python3

#%check
#nosetests

#%if 0%{?with_python3}
#pushd %{py3dir}
#nosetests-%{python3_version}
#popd
#%endif # with_python3

%files -n python2-%{srcname}
%doc CHANGES.rst LICENSE.txt README.rst CONTRIBUTORS.txt
# For noarch packages: sitelib
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc LICENSE.txt
# For noarch packages: sitelib
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Wed Feb 07 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.10.4-3
- Add support for Python 3

* Tue Jan 16 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.10.4-2
- Support for Python 3 on RHEL 7 & 6
- Updated to use Python 2.7 on Redhat 6
- Removed support for RHEL 5

* Mon Apr 13 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.10.2-1
- Update to 1.10.2
Resolves: rhbz#1176257

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.5-6
- Rebuild for RHEL 6.7
Resolves: rhbz#1176257

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

