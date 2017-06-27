%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __inst_layout --install_layout=unix
 
%else

%if 0%{?fedora} > 12 || 0%{?rhel} > 8
%global with_python3 1
%else
%if 0%{?rhel} < 7
%global pybasever 2.6
%endif

%{!?__python2: %global __python2 /usr/bin/python%{?pybasever}}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?rhel} == 6
%global with_python3 0

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __os_install_post %{__python27_os_install_post}
%endif

%endif  # amzn


%define debug_package %{nil}

%global pypi_name impacket

Name:           python%{?__python_ver}-%{pypi_name}
Version:        0.9.14
Release:        4%{?dist}
Summary:        Network protocols Constructors and Dissectors

License:        Apache modified
URL:            https://github.com/CoreSecurity/impacket
Source0:        https://pypi.python.org/packages/source/i/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
Requires: python%{?__python_ver}-crypto >= 2.6.1

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%endif 

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires: python3-crypto >= 2.6.1
%endif

%description
Impacket is a collection of Python classes focused on providing access to
network packets. Impacket allows Python developers to craft and decode network
packets in simple and consistent manner.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Network protocols Constructors and Dissectors
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Impacket is a collection of Python classes focused on providing access to
network packets. Impacket allows Python developers to craft and decode network
packets in simple and consistent manner.
%endif


%prep
%setup -q -n %{pypi_name}-%{version}

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}

%if 0%{?with_python3}
%files -n python3-%{pypi_name} 
%doc README.md LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python%{?__python_ver}-%{pypi_name} 
%defattr(-,root,root)
%docdir /usr/share/doc/%{pypi_name} 
/usr/share/doc/%{pypi_name} 
%{python2_sitelib}/*
%{_bindir}/atexec.py
%{_bindir}/esentutl.py
%{_bindir}/goldenPac.py
%{_bindir}/ifmap.py
%{_bindir}/karmaSMB.py
%{_bindir}/lookupsid.py
%{_bindir}/loopchain.py
%{_bindir}/mssqlclient.py
%{_bindir}/mssqlinstance.py
%{_bindir}/netview.py
%{_bindir}/nmapAnswerMachine.py
%{_bindir}/ntfs-read.py
%{_bindir}/opdump.py
%{_bindir}/os_ident.py
%{_bindir}/ping.py
%{_bindir}/ping6.py
%{_bindir}/psexec.py
%{_bindir}/raiseChild.py
%{_bindir}/rdp_check.py
%{_bindir}/registry-read.py
%{_bindir}/rpcdump.py
%{_bindir}/samrdump.py
%{_bindir}/secretsdump.py
%{_bindir}/services.py
%{_bindir}/smbclient.py
%{_bindir}/smbexec.py
%{_bindir}/smbrelayx.py
%{_bindir}/smbserver.py
%{_bindir}/smbtorture.py
%{_bindir}/sniff.py
%{_bindir}/sniffer.py
%{_bindir}/split.py
%{_bindir}/tracer.py
%{_bindir}/uncrc32.py
%{_bindir}/wmiexec.py
%{_bindir}/wmipersist.py
%{_bindir}/wmiquery.py


%changelog
* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 0.9.14-4
- Updated to use Python 2.7 on Redhat 6

* Thu Apr 27 2017 SaltStack Packaging Team <packaging@saltstack.com> - 0.9.14-3
- Added requirement for python-crypto

* Fri Oct 21 2016 SaltStack Packaging Team <packaging@saltstack.com> - 0.9.14-2
- Ported to build on Amazon Linux 2016.09 natively

* Thu Jan 14 2016 SaltStack Packaging Team <packaging@saltstack.com> - 0.9.14-1
- Initial package.
