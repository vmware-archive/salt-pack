%global __python2 /usr/bin/python2.6
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global srcname python2-chardet
%global realname chardet

Name:           python-%{realname}
Version:        2.0.1
Release:        2%{?dist}
Summary:        Character encoding auto-detection in Python

Group:          Development/Languages
License:        LGPLv2
URL:            http://chardet.feedparser.org
Source0:        http://chardet.feedparser.org/download/%{srcname}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python26-devel
BuildRequires:  python26-distribute
Requires:       python26

%description
Character encoding auto-detection in Python. As smart as your browser. Open
source.

%package -n python26-%{realname}
Summary:        Character encoding auto-detection in Python
Group:          Development/Languages
Requires:       python26

%description -n python26-%{realname}
Character encoding auto-detection in Python. As smart as your browser. Open
source.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python2} setup.py build

%install
rm -rf %{buildroot}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
chmod -x COPYING
 
%clean
rm -rf %{buildroot}

%files -n python26-%{realname}
%defattr(-,root,root,-)
%doc COPYING
%{python2_sitelib}/*

%changelog
* Wed Jan 13 2010 Erik Johnson <kushal@fedoraproject.org> 2.0.1-2
- Initial EL5 build

* Wed Jan 13 2010 Kushal Das <kushal@fedoraproject.org> 2.0.1-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Aug 04 2008 Kushal Das <kushal@fedoraproject.org> 1.0.1-1
- Initial release

