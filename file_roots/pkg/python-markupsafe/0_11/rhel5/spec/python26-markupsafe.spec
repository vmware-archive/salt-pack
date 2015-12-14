%global __python26 /usr/bin/python2.6
%global python26_sitearch %{_libdir}/python2.6/site-packages
%global __os_install_post %{__python26_os_install_post}

Name: python26-markupsafe
Version: 0.11
Release: 3%{?dist}
Summary: Implements a XML/HTML/XHTML Markup safe string for Python

Group: Development/Languages
License: BSD
URL: http://pypi.python.org/pypi/MarkupSafe
Source0: http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python26-devel python26-distribute

Requires: python(abi) = 2.6

%description
A library for safe markup escaping.

%prep
%setup -q -n MarkupSafe-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python26} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python26} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# C code errantly gets installed
rm $RPM_BUILD_ROOT/%{python26_sitearch}/markupsafe/*.c
# Corecct permissons on one file.
chmod 755 $RPM_BUILD_ROOT/%{python26_sitearch}/markupsafe/_speedups.so

%check
%{__python26} setup.py test

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python26_sitearch}/markupsafe/
%{python26_sitearch}/MarkupSafe-%{version}-py2.6.egg-info/

%changelog
* Tue Jan 11 2011 Steve Traylen <steve.traylen@cern.ch> - 0.11-3
- Do not hardcode lib64 path, be more particular about
  files that are include. rhbz#668591

* Mon Dec 13 2010 Steve Traylen <steve.traylen@cern.ch> - 0.11-2
- Adapt F15 .spec file for python26 EPEL5 package.

* Thu Sep 30 2010 Luke Macken <lmacken@redhat.com> - 0.11-1
- Update to 0.11

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.9.2-5
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-3
- Fix missing setuptools BuildRequires.

* Thu Jun 24 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-2
- Fixed sitearch and python3 definitions to work better with older Fedora/RHEL.

* Wed Jun 23 2010 Kyle VanderBeek <kylev@kylev.com> - 0.9.2-1
- Initial version.
