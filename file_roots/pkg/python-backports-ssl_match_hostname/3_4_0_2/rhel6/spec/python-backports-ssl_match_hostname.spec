
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif


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

%global module_name backports.ssl_match_hostname

Name:           python%{?__python_ver}-backports-ssl_match_hostname
Version:        3.4.0.2
Release:        3%{?dist}
Summary:        The ssl.match_hostname() function from Python 3

License:        Python
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname
Source0:        http://pypi.python.org/packages/source/b/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
%else
BuildRequires:  python2-devel
%endif

BuildRequires:  python%{?__python_ver}-setuptools

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%endif

Requires:       python%{?__python_ver}-backports

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code inside comes verbatim from Python 3.2.


%prep
## %setup -qn %{module_name}-%{version}
%setup -n %{module_name}-%{version}
mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./


%build
## python setup.py build
%{__python2} setup.py build


%install
## python setup.py install --skip-build --root %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{python2_sitelib}/backports/__init__.py*

 
%files
%doc README.txt LICENSE.txt
%{python2_sitelib}/*


%changelog
* Fri Sep 22 2017 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.0.2-3
- Update to use Python 2.7 on Redhat 6

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0.2-2
- Rebuild for RHEL 6.7
Resolves: rhbz#1176258

* Sun Oct 27 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.4.0.2-1
- Update to upstream 3.4.0.2 for a security fix
- http://bugs.python.org/issue17997

* Mon Sep 02 2013 Ian Weller <iweller@redhat.com> - 3.4.0.1-1
- Update to upstream 3.4.0.1

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 3.2-0.5.a3
- Use python-backports instead of providing backports/__init__.py

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.4.a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-0.3.a3
- Add patch for CVE 2013-2099 https://bugzilla.redhat.com/show_bug.cgi?id=963260

* Tue Feb 05 2013 Ian Weller <iweller@redhat.com> - 3.2-0.2.a3
- Fix Python issue 12000

* Fri Dec 07 2012 Ian Weller <iweller@redhat.com> - 3.2-0.1.a3
- Initial package build
