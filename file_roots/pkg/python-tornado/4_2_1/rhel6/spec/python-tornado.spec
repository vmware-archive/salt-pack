%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?rhel} > 6 || 0%{?fedora} > 12
%global __python2 /usr/bin/python
%else
%global __python2 /usr/bin/python2.6
%endif

# Fix lack of rhel macro on COPR
# (https://bugzilla.redhat.com/show_bug.cgi?id=1213482)
## %if 0%{?rhel} == 0 && 0%{?fedora} == 0
## %global rhel5 1  # remove support for Redhat 5
## %endif

%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?rhel} == 6
%global with_python3 0

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __os_install_post %{__python27_os_install_post}
%endif

%global pkgname tornado
%global srcname python-%{pkgname}

Name:           python%{?__python_ver}-%{pkgname}
Version:        4.2.1
Release:        2%{?dist}
Summary:        Scalable, non-blocking web server and tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://pypi.python.org/packages/source/t/tornado/tornado-%{version}.tar.gz
# Patch to use system CA certs instead of certifi
Patch0:         python-tornado-cert.patch
Patch1:         python-tornado-netutil-cert.patch

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-unittest2

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%else
BuildRequires:  python-backports-ssl_match_hostname
Requires:       python-backports-ssl_match_hostname
%endif 

Requires:       python-pycurl

%if 0%{?with_python3}
BuildRequires:  python2-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%endif


%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package doc
Summary:        Examples for python-tornado
Group:          Documentation
Requires:       python-tornado = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.


%if 0%{?with_python3}
%package -n python3-tornado
Summary:        Scalable, non-blocking web server and tools
Group:          Development/Libraries
%description -n python3-tornado
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package -n python3-tornado-doc
Summary:        Examples for python-tornado
Group:          Documentation
Requires:       python3-tornado = %{version}-%{release}

%description -n python3-tornado-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%endif # with_python3


%prep 
%setup -qc 
mv %{pkgname}-%{version} python2
pushd python2
%patch0 -p1 -b .cert
%patch1 -p1 -b .cert
# remove shebang from files
%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
%endif # with_python3

%build
%if 0%{?with_python3}
pushd python3
    %{__python3} setup.py build
popd
%endif # with_python3

pushd python2
    %{__python2} setup.py build
popd


%install
%if 0%{?with_python3}
pushd python3
    PATH=$PATH:%{buildroot}%{python3_sitearch}/%{pkgname}
    %{__python3} setup.py install --root=%{buildroot}
popd
%endif # with_python3

pushd python2
    PATH=$PATH:%{buildroot}%{python2_sitearch}/%{pkgname}
    %{__python2} setup.py install --root=%{buildroot}
popd


%check
%if ! 0%{?rhel} > 6 || 0%{?fedora} > 12
    %if 0%{?with_python3}
    pushd python3
        PYTHONPATH=%{python3_sitearch} \
        %{__python3} -m tornado.test.runtests --verbose
    popd
    %endif # with_python3
    pushd python2
        PYTHONPATH=%{python2_sitearch} \
        %{__python2} -m tornado.test.runtests --verbose
    popd
%endif


%files
%doc python2/README.rst python2/PKG-INFO

%{python2_sitearch}/%{pkgname}/
%{python2_sitearch}/%{pkgname}-%{version}-*.egg-info

%files doc
%doc python2/demos


%if 0%{?with_python3}
%files -n python3-tornado
%doc python3/README.rst python3/PKG-INFO

%{python3_sitearch}/%{pkgname}/
%{python3_sitearch}/%{pkgname}-%{version}-*.egg-info

%files -n python3-tornado-doc
%doc python3/demos
%endif


%changelog
* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 4.2.1-2
- Updated to use Python 2.7 on Redhat 6

* Thu Aug 20 2015 SaltStack Packaging Team <packaging@saltstack.com> - 4.2.1-1
- Picking up security fix for 4.2.1-1

* Mon Apr 20 2015 Erik Johnson <erik@saltstack.com> - 4.1-3
- Fix broken COPR for EL5

* Mon Apr 20 2015 Erik Johnson <erik@saltstack.com> - 4.1-2
- Extend rawhide spec to cover RHEL 5 through 7

* Sun Mar 1 2015 Orion Poplawski <orion@cora.nwra.com> - 4.1-1
- Update to 4.1
- Modernize spec

* Fri Dec 5 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Drop requires python-simplejson

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Thomas Spura <tomspur@fedoraproject.org> - 3.2.1-1
- update to 3.2.1
- no noarch anymore
- remove defattr

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-5
- remove rhel conditional for with_python3:
  https://fedorahosted.org/fpc/ticket/200

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.1-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-1
- update to upstream release 2.2.1 (fixes CVE-2012-2374)
- fix typo for epel6 macro bug #822972 (Florian La Roche)

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.2-1
- upgrade to upstream release 2.2

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-4
- remove python3-simplejson dependency

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-3
- build python3 package

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-1
- new upstream version 2.1.1
- remove double word in description and rearrange it (#715272)
- fixed removal of shebangs
- added %%check section to run unittests during package build

* Tue Mar 29 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.2.1-1
- new upstream version 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep  8 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.1-1
- new upstream release 1.1

* Tue Aug 17 2010 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.1-1
- new upstream bugfix release: 1.0.1

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-2
- changed upstream source url

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-1
- new upstream release 1.0
- there's no longer a problem with spurious permissions, so remove that fix

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Oct 21 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-3
- changed -doc package group to Documentation
- use global instead of define

* Tue Oct 20 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-2
- create -doc package for examples
- altered description to not include references to FriendFeed
- rename to python-tornado

* Fri Sep 25 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.2-1
- New upstream version
- Fixed macro usage and directory ownership in spec

* Thu Sep 10 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.1-1
- Initial release

