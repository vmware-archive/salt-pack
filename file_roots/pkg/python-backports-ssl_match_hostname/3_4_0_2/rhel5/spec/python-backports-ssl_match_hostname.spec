%global __python2 /usr/bin/python2.6
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global srcname backports.ssl_match_hostname
%global realname backports-ssl_match_hostname

Name:           python-%{realname}
Version:        3.4.0.2
Release:        2%{?dist}
Summary:        The ssl.match_hostname() function from Python 3

Group:          Development/Languages
License:        Python
URL:            https://bitbucket.org/brandon/%{srcname}
Source0:        http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python26-devel
BuildRequires:  python26-distribute
Requires:       python26
Requires:       python26-backports

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

%package -n python26-%{realname}
Summary:        The ssl.match_hostname() function from Python 3
Group:          Development/Languages
BuildRequires:  python26-devel
BuildRequires:  python26-distribute
Requires:       python26
Requires:       python26-backports

%description -n python26-%{realname}
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
%setup -qn %{srcname}-%{version}
mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{python2_sitelib}/backports/__init__.py*

%clean
rm -rf %{buildroot}
 
%files -n python26-%{realname}
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python2_sitelib}/*


%changelog
* Fri Jul 25 2014 Erik Johnson <erik@saltstack.com> - 3.4.0.2-2
- Initial EL5 build

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
