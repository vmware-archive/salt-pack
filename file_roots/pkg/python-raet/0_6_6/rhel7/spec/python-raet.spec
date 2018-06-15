%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%else
%global with_python3 1
%endif

%{!?__python2: %global __python2 /usr/bin/python%{?pybasever}}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

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
A high level, stack based communication protocol for network and IPC communication

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname raet

Name:       python-%{srcname}
Version:    0.6.6
Release:    5%{?dist}
Summary:    Reliable Asynchronous Event Transport Protocol

License:    ASL 2.0
URL:        https://github.com/RaetProtocol/raet
Source0:    http://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz
## Patch0:     raet-0.6.6.patch

BuildArch:  noarch

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  python%{?__python_ver}-six
Requires:  python%{?__python_ver}-six

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-libnacl >= 1.4.3-1
BuildRequires:  python%{?__python_ver}-ioflo >= 1.3.8-1
Requires:  python%{?__python_ver}-ioflo >= 1.3.8-1
Requires:  python%{?__python_ver}-ioflo >= 1.3.8-1
%else
BuildRequires:  python-libnacl >= 1.4.3-1
BuildRequires:  python2-ioflo >= 1.3.8-1
Requires:  python2-ioflo >= 1.3.8-1
Requires:  python2-ioflo >= 1.3.8-1
%endif

%if (0%{?rhel} == 6) && (! 0%{?with_explicit_python27})
Requires:  python%{?__python_ver}-simplejson
%endif 

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
Provides: python-%{srcname}
%endif

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_setup
}

%description    %{_description}

%package    -n  python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python-%{srcname}}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}
Python 2 version.


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-ioflo >= 1.3.8-1
BuildRequires:  python%{python3_pkgversion}-libnacl >= 1.4.3-1
Requires:  python%{python3_pkgversion}-six
Requires:  python%{python3_pkgversion}-ioflo >= 1.3.8-1
Requires:  python%{python3_pkgversion}-libnacl >= 1.4.3-1
##%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Provides: python%{python3_pkgversion}-%{srcname}

%description -n python%{python3_pkgversion}-%{srcname} %{_description}
Python 3 version.
%endif


%prep
## %setup -q -n %{srcname}-%{version}
%autosetup -n %{srcname}-%{version}
## %patch0 -p1 

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


## %if 0%{?with_python3}
## rm -rf %{py3dir}
## cp -a . %{py3dir}
## %endif

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif


%install
## rm -rf %{buildroot}
## %py2_install
## 
## %if 0%{?with_python3}
## ## sed -i '1s|^#!%{__python3}|#!%{__python2}|' %{buildroot}/usr/bin/raetflo
## %py3_install
## %endif
## 
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
rm -rf %{buildroot}%{_bindir}/*
%py3_install


## %check
## %{__python2} setup.py test
## %{__python3} setup.py test


%files -n python2-%{srcname}
%{_bindir}/raetflo
## %%{_bindir}/raetflo2
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py*.egg-info
%exclude %{python2_sitelib}/systest*


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
## %%{_bindir}/raetflo3
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py*.egg-info
%exclude %{python3_sitelib}/systest*
%endif


%changelog
* Tue Apr 24 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.6-5
- Updated build requires for libnacl

* Wed Feb 07 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.6-4
- Add support for Python 3

* Tue Jan 16 2018 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.6-3
- Support for Python 3 on RHEL 7 & 6
- Removed support for RHEL 5

* Mon Jul 17 2017 SaltStack Packaging Team <packaging@saltstack.com> - 0.6.6-2
- Updated to use Python 2.7 on Redhat 6

* Tue Jan 17 2017 Packaging <packaging@saltstack.com> - 0.6.6-1
- Patched fix to overcome lack of kwargs support with decode in python2.6

* Wed Dec  7 2016 Packaging <packaging@saltstack.com> - 0.6.5-1
- Build 0.6.5 for Salt implementation on various versions Redhat

* Thu Aug  6 2015 Packaging <packaging@saltstack.com> - 0.6.3-2
- Build 0.6.3 for Salt implementati
on on various versions Redhat


