%define __python /usr/bin/python2.6
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define py_basever 26
%define real_name python-nose
%define name python%{py_basever}-nose

# Fix byte-compilation:
%define __os_install_post %{__python26_os_install_post}

Name:           %{name} 
Version:        0.11.1
Release:        4%{?dist}
Summary:        A discovery-based unittest extension for Python

Group:          Development/Languages
License:        LGPLv2
URL:            http://somethingaboutorange.com/mrl/projects/nose/
Source0:        http://somethingaboutorange.com/mrl/projects/nose/nose-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python%{py_basever}-devel python%{py_basever}-setuptools
Requires:       python%{py_basever}-setuptools
Requires:       python%{py_basever}


%description
nose: a discovery-based unittest extension.

nose provides an alternate test discovery and running process for unittest,
one that is intended to mimic the behavior of py.test as much as is
reasonably possible without resorting to too much magic.

%prep
%setup -q -n nose-%{version}

%build
%{__python} setup.py build

%install
/bin/rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} \
        --single-version-externally-managed --install-data=%{_datadir}

/bin/rm -f %{buildroot}%{_bindir}/nosetests
/bin/mv %{buildroot}%{_mandir}/man1/nosetests.1 %{buildroot}%{_mandir}/man1/nosetests26.1

%clean
/bin/rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG lgpl.txt NEWS README.txt
%{_bindir}/nosetests-2.6
%{_mandir}/man1/nosetests26.1.gz
%{python_sitelib}/nose-%{version}-py%{pyver}.egg-info
%{python_sitelib}/nose

%changelog
* Tue Feb 17 2015 Erik Johnson <erik@saltstack.com> - 0.11.1-4
- Rev'ed the release number because COPR sucks

* Sun Apr 25 2010 David Malcolm <dmalcolm@redhat.com> - 0.11.1-3
- remove unnecessary explicit "coreutils" BR
- replace env vars with rpm macros 

* Wed Mar 17 2010 David Malcolm <dmalcolm@redhat.com> - 0.11.1-2
- targetting EPEL5: drop "ius" from release
- fix byte-compilation for 2.6
- drop CFLAGS from build: this is a noarch package

* Mon Aug 17 2009 BJ Dierkes <wdierkes@rackspace.com> 0.11.1-1.ius
- Rebuilding for IUS and python26
- Only require python26-setuptools (no -devel package there)
- Latest stable release

* Sat Aug 02 2008 Luke Macken <lmacken@redhat.com> 0.10.3-1
- Update to 0.10.3

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> 0.10.1-1
- Update to 0.10.1

* Mon Dec  3 2007 Luke Macken <lmacken@redhat.com> 0.10.0-2
- Add python-setuptools to Requires (Bug #408491)

* Tue Nov 27 2007 Luke Macken <lmacken@redhat.com> 0.10.0-1
- 0.10.0

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> 0.10.0-0.3.b1
- Update for python-setuptools changes in rawhide

* Tue Aug 21 2007 Luke Macken <lmacken@redhat.com> 0.10.0-0.2.b1
- 0.10.0b1
- Update license tag to LGPLv2

* Fri Jun 20 2007 Luke Macken <lmacken@redhat.com> 0.10.0-0.1.a2
- 0.10.0a2

* Sat Jun  2 2007 Luke Macken <lmacken@redhat.com> 0.9.3-1
- Latest upstream release
- Remove python-nose-0.9.2-mandir.patch

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> 0.9.2-1
- Add nosetests(1) manpage, and python-nose-0.9.2-mandir.patch to put it in
  the correct location.
- 0.9.2

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> 0.9.1-2
- Rebuild for python 2.5

* Fri Nov 24 2006 Luke Macken <lmacken@redhat.com> 0.9.1-1
- 0.9.1

* Fri Sep  8 2006 Luke Macken <lmacken@redhat.com> 0.9.0-1
- 0.9.0

* Wed Apr 19 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.7.2-1
- Initial RPM release
