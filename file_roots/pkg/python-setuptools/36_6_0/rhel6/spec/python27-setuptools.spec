%global python python27
%global python2_version 2.7
%global __python2 %{_bindir}/python%{python2_version}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%global srcname setuptools
%global with_check 0

Name:           %{python}-%{srcname}
Version:        36.6.0
Release:        1.ius%{?dist}
Summary:        Easily build and distribute Python packages
Vendor:         IUS Community Project
Group:          Applications/System
License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.zip
BuildArch:      noarch
BuildRequires:  %{python}-devel >= 2.7.9-1
Requires:       %{python} >= 2.7.9-1
# Keep the python-distribute name active for a few releases.  Eventually we'll
# want to get rid of the Provides and just keep the Obsoletes
Provides:       %{python}-distribute = %{version}-%{release}
Obsoletes:      %{python}-distribute <= 0.6.49-2.ius%{?dist}
%if 0%{?with_check}
# we don't have IUS versions of these yet
BuildRequires:  %{python}-pytest
BuildRequires:  %{python}-mock
%endif


%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.


%prep
%setup -q -n %{srcname}-%{version}

# Strip shebangs
find setuptools -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --optimize 1 --skip-build --root %{buildroot}
rm -r docs/{Makefile,conf.py,_*}
rm %{buildroot}%{_bindir}/easy_install


%if 0%{?with_check}
%check
# Upstream has switched to 'setup.py ptr'.  We need to build
# python%{iusver}-mock and python%{iusver}-pytest to enable this.
LC_CTYPE=en_US.utf8 %{__python2} setup.py ptr
%endif


%files
%license LICENSE
%doc docs/*
%{python2_sitelib}/*
%{_bindir}/easy_install-%{python2_version}


%changelog
* Thu Nov 09 2017 Ben Harper <ben.harper@rackspace.com> - 36.6.0-1.ius
- Latest upstream
- drop EL5 stuff
- use license macro
- don't include exe files

* Mon Mar 06 2017 Carl George <carl.george@rackspace.com> - 33.1.1-1.ius
- Update to version 33
- Install LICENSE file
- Strip shebangs

* Mon Dec 05 2016 Ben Harper <ben.harper@rackspace.com> - 30.2.0-1.ius
- Monthly release

* Mon Nov 07 2016 Carl George <carl.george@rackspace.com> - 28.7.1-1.ius
- Latest version

* Mon Oct 03 2016 Carl George <carl.george@rackspace.com> - 27.3.1-1.ius
- Latest upstream

* Tue Sep 06 2016 Carl George <carl.george@rackspace.com> - 25.4.0-1.ius
- Latest upstream

* Mon Aug 01 2016 Carl George <carl.george@rackspace.com> - 24.3.1-1.ius
- Latest upstream

* Mon Jun 27 2016 Ben Harper <ben.harper@rackspace.com> - 22.0.5-1.ius
- Latest upstream

* Thu Jun 02 2016 Carl George <carl.george@rackspace.com> - 21.2.2-1.ius
- Latest upstream
- Switch Source0 URL to upstream recommendation
- License changed to MIT https://github.com/pypa/setuptools/commit/d0bd7a5

* Tue May 03 2016 Ben Harper <ben.harper@rackspace.com> - 20.10.1-1.ius
- updating to 20.10.1
- update Source0 url to pypi.io see
  https://bitbucket.org/pypa/pypi/issues/438/backwards-compatible-un-hashed-package

* Thu Feb 18 2016 Ben Harper <ben.harper@rackspace.com> - 19.7-1.ius
- updating to 19.7

* Mon Feb 01 2016 Ben Harper <ben.harper@rackspace.com> -19.6.2-1.ius
- Latest upstream

* Mon Jan 18 2016 Ben Harper <ben.harper@rackspace.com> - 19.4-1.ius
- Latest upstream

* Mon Jan 04 2016 Carl George <carl.george@rackspace.com> - 19.2-1.ius
- Latest upstream

* Tue Dec 15 2015 Carl George <carl.george@rackspace.com> - 18.8.1-1.ius
- Latest upstream

* Mon Nov 30 2015 Ben Harper <ben.harper@rackspace.com> - 18.7-1.ius
- Latest upstream

* Mon Nov 09 2015 Carl George <carl.george@rackspace.com> - 18.5-1.ius
- Latest upstream

* Mon Oct 12 2015 Ben Harper <ben.harper@rackspace.com> - 18.4-1.ius
- Latest upstream

* Wed Sep 23 2015 Carl George <carl.george@rackspace.com> - 18.3.2-1.ius
- Latest upstream

* Tue Sep 08 2015 Ben Harper <ben.harper@rackspace.com> - 18.3.1-1.ius
- Latest upstream

* Wed Aug 19 2015 Ben Harper <ben.harper@rackspace.com> - 18.2-1.ius
- Latest upstream

* Mon Aug 03 2015 Carl George <carl.george@rackspace.com> - 18.1-1.ius
- Latest upstream

* Mon Jun 29 2015 Carl George <carl.george@rackspace.com> - 18.0.1-1.ius
- Latest upstream

* Tue Jun 16 2015 Carl George <carl.george@rackspace.com> - 17.1.1-1.ius
- Latest upstream

* Fri May 29 2015 Carl George <carl.george@rackspace.com> - 17.0-1.ius
- Latest upstream

* Mon May 18 2015 Carl George <carl.george@rackspace.com> - 16.0-1.ius
- Latest upstream

* Mon Apr 27 2015 Carl George <carl.george@rackspace.com> - 15.2-1.ius
- Latest upstream

* Mon Apr 13 2015 Carl George <carl.george@rackspace.com> - 15.0-1.ius
- Latest upstream

* Mon Mar 30 2015 Carl George <carl.george@rackspace.com> - 14.3.1-1.ius
- Latest upstream

* Mon Mar 16 2015 Carl George <carl.george@rackspace.com> - 14.3-1.ius
- Latest upstream

* Thu Feb 26 2015 Carl George <carl.george@rackspace.com> - 12.2-1.ius
- Latest upstream

* Wed Feb 11 2015 Carl George <carl.george@rackspace.com> - 12.1-1.ius
- Latest upstream

* Mon Jan 26 2015 Carl George <carl.george@rackspace.com> - 12.0.5-1.ius
- Remove dependency on ssl_match_hostname backport, it's included in Python 2.7.9
- Latest upstream

* Tue Jan 13 2015 Carl George <carl.george@rackspace.com> - 11.3.1-1.ius
- Latest upstream

* Mon Jan 05 2015 Carl George <carl.george@rackspace.com> - 11.1-1.ius
- Latest upstream
- Disable test suite

* Fri Dec 26 2014 Carl George <carl.george@rackspace.com> - 8.3-1.ius
- Latest upstream

* Mon Dec 22 2014 Carl George <carl.george@rackspace.com> - 8.2.1-1.ius
- Latest upstream

* Mon Dec 15 2014 Carl George <carl.george@rackspace.com> - 8.0.3-1.ius
- Latest upstream

* Mon Oct 20 2014 Ben Harper <ben.harper@rackspace.com> - 7.0-1.ius
- Latest sources from upstream

* Mon Oct 13 2014 Carl George <carl.george@rackspace.com> - 6.1-1.ius
- Latest upstream

* Tue Sep 30 2014 Carl George <carl.george@rackspace.com> - 6.0.2-1.ius
- Latest upstream

* Mon Sep 29 2014 Carl George <carl.george@rackspace.com> - 6.0.1-1.ius
- Latest upstream

* Fri Sep 19 2014 Carl George <carl.george@rackspace.com> - 5.8-1.ius
- Latest upstream

* Fri Aug 15 2014 Carl George <carl.george@rackspace.com> - 5.7-1.ius
- Latest upstream

* Fri Aug 15 2014 Carl George <carl.george@rackspace.com> - 5.6-1.ius
- Latest upstream

* Mon Aug 11 2014 Carl George <carl.george@rackspace.com> - 5.5.1-1.ius
- Latest upstream

* Mon Aug 04 2014 Ben Harper <ben.harper@rackspace.com> - 5.4.2-1.ius
- Latest upstream

* Mon Jul 07 2014 Carl George <carl.george@rackspace.com> - 5.4.1-1.ius
- Latest upstream

* Mon Jun 30 2014 Carl George <carl.george@rackspace.com> - 5.3-1.ius
- Latest upstream

* Tue Jun 24 2014 Carl George <carl.george@rackspace.com> - 5.2-1.ius
- Latest upstream

* Mon Jun 16 2014 Carl George <carl.george@rackspace.com> - 5.1-1.ius
- Latest upstream

* Wed Jun 04 2014 Carl George <carl.george@rackspace.com> - 4.0.1-1.ius
- Latest upstream
- Override __os_install_post to fix .pyc/pyo magic
- Workaround UTF-8 tests by setting LC_CTYPE

* Thu May 08 2014 Carl George <carl.george@rackspace.com> - 3.6-1.ius
- Latest upstream

* Wed May 07 2014 Carl George <carl.george@rackspace.com> - 3.5.1-1.ius
- Initial port from Fedora to IUS
- Latest upstream
- Macro change: *python* to *python2*

* Wed Apr 23 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.0-2
- Add a switch to build setuptools as wheel

* Mon Dec  9 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0-1
- Update to new upstream release with a few things removed from the API:
  Changelog: https://pypi.python.org/pypi/setuptools#id139

* Mon Nov 18 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-1
- Update to 1.4 that gives easy_install pypi credential handling

* Thu Nov  7 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-1
- Minor upstream update to reign in overzealous warnings

* Mon Nov  4 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-1
- Upstream update that pulls in our security patches

* Mon Oct 28 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.7-1
- Update to newer upstream release that has our patch to the unittests
- Fix for http://bugs.python.org/issue17997#msg194950 which affects us since
  setuptools copies that code. Changed to use
  python-backports-ssl_match_hostname so that future issues can be fixed in
  that package.

* Sat Oct 26 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.6-1
- Update to newer upstream release.  Some minor incompatibilities listed but
  they should affect few, if any consumers.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.6-1
- Upstream update -- just fixes python-2.4 compat

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5
  - package_index can handle hashes other than md5
  - Fix security vulnerability in SSL certificate validation
  - https://bugzilla.redhat.com/show_bug.cgi?id=963260

* Fri Jul  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8-1
- Update to upstream 0.8  release.  Codebase now runs on anything from
  python-2.4 to python-3.3 without having to be translated by 2to3.

* Wed Jul  3 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.7-1
- Update to 0.7.7 upstream release

* Mon Jun 10 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-2
- Update to the setuptools-0.7 branch that merges distribute and setuptools

* Thu Apr 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.36-1
- Update to upstream 0.6.36.  Many bugfixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.6.28-2
- remove rhel logic from with_python3 conditional

* Mon Jul 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.28-1
- New upstream release:
  - python-3.3 fixes
  - honor umask when setuptools is used to install other modules

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-2
- Fix easy_install.py having a python3 shebang in the python2 package

* Thu Jun  7 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.27-1
- Upstream bugfix

* Tue May 15 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-2
- Upstream bugfix

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.24-1
- Upstream bugfix
- Compile the win32 launcher binary using mingw

* Sun Aug 21 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.21-1
- Upstream bugfix release

* Thu Jul 14 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.19-1
- Upstream bugfix release

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-7
- Switch to patch that I got in to upstream

* Tue Feb 22 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-6
- Fix build on python-3.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Tue Aug 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.14-3
- Update description to mention this is distribute

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-2
- bump for building against python 2.7

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.14-1
- update to new version
- all patches are upsteam

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-7
- generalize path of easy_install-2.6 and -3.1 to -2.* and -3.*

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.13-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-5
- Upstream patch for compatibility problem with setuptools
- Minor spec cleanups
- Provide python-distribute for those who see an import distribute and need
  to get the proper package.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-4
- Fix race condition in unittests under the python-2.6.x on F-14.

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-3
- Fix few more buildroot macros

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-2
- Include data that's needed for running tests

* Thu Jun 10 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.13-1
- Update to upstream 0.6.13
- Minor specfile formatting fixes

* Thu Feb 04 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-3
- First build with python3 support enabled.
  
* Fri Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-2
- Really disable the python3 portion

* Fri Jan 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.10-1
- Update the python3 portions but disable for now.
- Update to 0.6.10
- Remove %%pre scriptlet as the file has a different name than the old
  package's directory

* Tue Jan 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-4
- Fix install to make /usr/bin/easy_install the py2 version
- Don't need python3-tools since the library is now in the python3 package
- Few other changes to cleanup style

* Fri Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.9-2
- add python3 subpackage

* Mon Dec 14 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.9-1
- New upstream bugfix release.

* Sun Dec 13 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-2
- Test rebuild

* Mon Nov 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.8-1
- Update to 0.6.8.
- Fix directory => file transition when updating from setuptools-0.6c9.

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-2
- Fix duplicate inclusion of files.
- Only Obsolete old versions of python-setuptools-devel

* Tue Nov 3 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.7-1
- Move easy_install back into the main package as the needed files have been
  moved from python-devel to the main python package.
- Update to 0.6.7 bugfix.

* Fri Oct 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.6-1
- Upstream bugfix release.

* Mon Oct 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-1
- First build from the distribute codebase -- distribute-0.6.4.
- Remove svn patch as upstream has chosen to go with an easier change for now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6c9-4
- Apply SVN-1.6 versioning patch (rhbz #511021)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6c9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
