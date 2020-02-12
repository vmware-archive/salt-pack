## Backport of python-ipaddress explicitly for Amazon Linux 1

%bcond_with tests

%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so)$

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
# work-around Amazon Linux get_python_lib returning  /usr/lib64/python2.7/dist-packages
## %global python2_sitelib  %{_libdir}/python2.7/site-packages 
## %global python2_sitearch  /usr/lib64/python2.7/site-packages 
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global __inst_layout --install-layout=unix

%global pyname ipaddress

Name:           python-%{pyname}
Version:        1.0.18
Release:        7%{?dist}
Summary:        Port of the python 3.3+ ipaddress module to 2.6+

License:        Python
URL:            https://pypi.python.org/pypi/ipaddress/
Source0:        https://pypi.python.org/packages/source/i/%{pyname}/%{pyname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27  >= 2.7.9-1

%global _description\
ipaddress provides the capabilities to create, manipulate and operate\
on IPv4 and IPv6 addresses and networks.\
\
The functions and classes in this module make it straightforward to\
handle various tasks related to IP addresses, including checking\
whether or not two hosts are on the same subnet, iterating over all\
hosts in a particular subnet, checking whether or not a string\
represents a valid IP address or network definition, and so on.

%description %_description

%package -n python27-%{pyname}
Summary: %summary

Provides:   python-%{pyname}
Provides:   python27-%{pyname}
Provides:   python2-%{pyname}

%description -n python27-%{pyname} %_description

%prep
%setup -q -n %{pyname}-%{version}


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build %{?__inst_layout } --root %{buildroot}


%files -n python27-%{pyname}
%doc README.md
%{python2_sitelib}/*


%changelog
* Mon Feb 03 2020 SaltStack Packaging Team <packaging@saltstack.com> - 1.0.18-7
- Support for Python 2.7, backport to Amazon Linux 1

* Tue Nov 13 2018 SaltStack Packaging Team >packaging@saltstack.com> - 1.0.18-6
- Backport to support RHEL 6 for Python 2.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.18-3
- Python 2 binary package renamed to python2-ipaddress
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Paul Wouters <pwouters@redhat.com> - 1.0.18-1
- Updated to 1.0.18, fixup URL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.16-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Matěj Cepl <mcepl@redhat.com> - 1.0.16-1
- Update to the latest upstream (#1242475)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-3
- Remove Conflicts: python-ipaddr

* Mon Jun  8 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-2
- Add Conflicts: python-ipaddr

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Wed Mar 20 2013 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.3-1
- initial release
