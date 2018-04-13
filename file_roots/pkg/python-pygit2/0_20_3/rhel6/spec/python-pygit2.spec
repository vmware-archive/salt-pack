
%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%else
%global python python
%global __python_ver %{nil}
%endif

%global pkgname pygit2

%if 0%{?fedora} < 20 || 0%{?rhel} < 7
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so
%endif

Name:           python%{?__python_ver}-%{pkgname}
Version:        0.20.3
Release:        5%{?dist}
Summary:        Python 2.x bindings for libgit2
URL:            http://www.pygit2.org
Source:         http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
Patch:          disable_tests.patch
License:        GPLv2 with linking exception
BuildRequires:  openssl-devel
%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-libgit2-devel
BuildRequires:  python%{?__python_ver}-devel
## BuildRequires:  python-sphinx
BuildRequires:  python%{?__python_ver}-nose
BuildRequires:  python%{?__python_ver}-setuptools
%else
BuildRequires:  libgit2-devel
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python-nose
BuildRequires:  python-setuptools
%endif

%description
pygit2 is a set of Python bindings to the libgit2 library, which implements 
the core of Git. Pygit2 works with Python 2.6, 2.7, 3.1, 3.2 and 3.3.
%if 0%{?with_explicit_python27}
Build for use with Python 2.7
%endif

## %package        doc
## Summary:        Documentation for %{name}
## BuildArch:      noarch
## 
## %description    doc
## Documentation for %{name}.

%prep
%setup -qn %{pkgname}-%{version}
# Disable tests which require network access
%patch -p1

%build
CFLAGS="%{optflags}" %{__python} setup.py build
## make -C docs html

%install
%{__python} setup.py install --prefix=%{_prefix} -O1 --skip-build --root=%{buildroot}
find %{_builddir} -name '.buildinfo' -delete
# Correct the permissions.
find %{buildroot} -name '*.so' -exec chmod 755 {} ';'

%check
%{__python} setup.py test

%files
%doc COPYING README.rst TODO.txt
%{python_sitearch}/%{pkgname}-%{version}-py%{python_version}.egg-info
%{python_sitearch}/%{pkgname}
%{python_sitearch}/_%{pkgname}.so

## %files doc
## %doc docs/_build/html/*

%changelog
* Thu Apr 12 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.20.3-5
- Updated to use Python 2.7 on Redhat 6

* Fri Feb 13 2015 Erik Johnson <erik@saltstack.com> - 0.20.3-4
- Initial EL6 build

* Sat Jun 21 2014 Christopher Meng <rpm@cicku.me> - 0.20.3-1
- Update to 0.20.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Mar 09 2014 Christopher Meng <rpm@cicku.me> - 0.20.2-1
- Update to 0.20.2

* Sun Dec 08 2013 Christopher Meng <rpm@cicku.me> - 0.20.0-1
- Update to 0.20.0
- Clarify the license

* Tue Oct 08 2013 Christopher Meng <rpm@cicku.me> - 0.19.1-2
- Split out -doc subpackage.
- Correct the libs permissions.

* Mon Oct 07 2013 Christopher Meng <rpm@cicku.me> - 0.19.1-1
- Update to 0.19.1

* Sat Aug 17 2013 Christopher Meng <rpm@cicku.me> - 0.19.0-4
- Add missing sphinx BR.

* Tue Aug 13 2013 Christopher Meng <rpm@cicku.me> - 0.19.0-3
- Remove unneeded files.

* Mon Aug 12 2013 Christopher Meng <rpm@cicku.me> - 0.19.0-2
- Add missing nose BR.
- Add docs.

* Thu Aug 01 2013 Christopher Meng <rpm@cicku.me> - 0.19.0-1
- Update to new release.

* Fri Apr 26 2013 Christopher Meng <rpm@cicku.me> - 0.18.1-1
- Update to new release.

* Mon Sep 24 2012 Christopher Meng <rpm@cicku.me> - 0.17.3-1
- Update to new release.

* Sun Jul 29 2012 Christopher Meng <rpm@cicku.me> - 0.17.2-1
- Update to new release.

* Fri Mar 30 2012 Christopher Meng <rpm@cicku.me> - 0.16.1-1
- Update to new release.

* Thu Mar 01 2012 Christopher Meng <rpm@cicku.me> - 0.16.0-1
- Initial Package.
