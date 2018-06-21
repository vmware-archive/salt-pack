%if ( "0%{?dist}" == "0.amzn1" )
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

%global __inst_layout --install-layout=unix

%else

%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}


%if 0%{?rhel} == 6
%global with_python3 0

%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%endif

%global include_tests 0

# Release Candidate
%define __rc_ver %{nil}

%define fish_dir %{_datadir}/fish/vendor_functions.d

Name: salt
Version: 2018.3.2%{?__rc_ver}
Release: 1%{?dist}
Summary: A parallel remote execution system

Group:   System Environment/Daemons
License: ASL 2.0
URL:     http://saltstack.org/
Source0: https://pypi.io/packages/source/s/%{name}/%{name}-%{version}.tar.gz
Source1: %{name}-proxy@.service
Source2: %{name}-master
Source3: %{name}-syndic
Source4: %{name}-minion
Source5: %{name}-api
Source6: %{name}-master.service
Source7: %{name}-syndic.service
Source8: %{name}-minion.service
Source9: %{name}-api.service
Source10: README.fedora
Source11: %{name}-common.logrotate
Source12: salt.bash
Source13: salt.fish
Source14: salt_common.fish
Source15: salt-call.fish
Source16: salt-cp.fish
Source17: salt-key.fish
Source18: salt-master.fish
Source19: salt-minion.fish
Source20: salt-run.fish
Source21: salt-syndic.fish

## Patch0:  salt-%%{version}-tests.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%ifarch %{ix86} x86_64
Requires: dmidecode
%endif

Requires: pciutils
Requires: which

%if 0%{?fedora} >= 26
Requires: dnf-utils
%else
Requires: yum-utils
%endif

%if ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})
BuildRequires: python%{?__python_ver}-tornado >= 4.2.1
BuildRequires: python%{?__python_ver}-futures >= 2.0
BuildRequires: python%{?__python_ver}-crypto >= 2.6.1
BuildRequires: python%{?__python_ver}-jinja2
BuildRequires: python%{?__python_ver}-msgpack >= 0.4
BuildRequires: python%{?__python_ver}-pip
BuildRequires: python%{?__python_ver}-zmq >= 14.5

%if 0%{?with_explicit_python27}
BuildRequires: PyYAML%{?__python_ver}
%else
BuildRequires: PyYAML
%endif

BuildRequires: python%{?__python_ver}-requests
## BuildRequires: python%{?__python_ver}-unittest2

# this BR causes windows tests to happen
# clearly, that's not desired
# https://github.com/saltstack/salt/issues/3749
BuildRequires: python%{?__python_ver}-mock
BuildRequires: git
BuildRequires: python%{?__python_ver}-libcloud
BuildRequires: python%{?__python_ver}-six

%if ((0%{?rhel} == 6) && 0%{?include_tests})
# argparse now a salt-testing requirement
BuildRequires: python-argparse
%endif

%endif  ##  ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})

BuildRequires: python%{?__python_ver}-devel


Requires: python%{?__python_ver}-jinja2
Requires: python%{?__python_ver}-msgpack >= 0.4
Requires: python%{?__python_ver}-crypto >= 2.6.1

%if ( "0%{?dist}" == "0.amzn1" )
Requires: python27-PyYAML
Requires: python%{?__python_ver}
%else
%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
Requires: PyYAML%{?__python_ver}
%else
Requires: PyYAML
%endif

%endif

Requires: python%{?__python_ver}-requests >= 1.0.0
Requires: python%{?__python_ver}-zmq
Requires: python%{?__python_ver}-markupsafe
Requires: python%{?__python_ver}-tornado >= 4.2.1, python%{?__python_ver}-tornado < 5.0 
Requires: python%{?__python_ver}-futures >= 2.0
Requires: python%{?__python_ver}-six
Requires: python%{?__python_ver}-psutil


%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%else

%if 0%{?systemd_preun:1}

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%endif

BuildRequires: systemd-units
Requires:      systemd-python

%endif

%description
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.

%package master
Summary: Management component for salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%if (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires: systemd-python
%endif

%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name}-master = %{version}-%{release}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name}-master = %{version}-%{release}
Requires: python%{?__python_ver}-cherrypy


%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name}-master = %{version}-%{release}
Requires: python%{?__python_ver}-libcloud

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%prep
## %setup -q -c
## %setup -q -T -D -a 1
%setup -c

cd %{name}-%{version}
## %%patch0 -p1

%build


%install
rm -rf %{buildroot}
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
%{__python} setup.py install -O1 %{?__inst_layout } --root %{buildroot}

# Add some directories
install -d -m 0755 %{buildroot}%{_var}/log/salt
touch %{buildroot}%{_var}/log/salt/minion
touch %{buildroot}%{_var}/log/salt/master
install -d -m 0755 %{buildroot}%{_var}/cache/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/master.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/minion.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki/master
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki/minion
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.providers.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/proxy.d

# Add the config files
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/salt/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/salt/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/salt/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/salt/roster
install -p -m 0640 conf/proxy %{buildroot}%{_sysconfdir}/salt/proxy

%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
mkdir -p %{buildroot}%{_initrddir}
install -p %{SOURCE2} %{buildroot}%{_initrddir}/
install -p %{SOURCE3} %{buildroot}%{_initrddir}/
install -p %{SOURCE4} %{buildroot}%{_initrddir}/
install -p %{SOURCE5} %{buildroot}%{_initrddir}/
%else
# Add the unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE8} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
%endif

## # Force python2.7 on EPEL6
## # https://github.com/saltstack/salt/issues/22003
## %if 0%{?rhel} == 6
## sed -i 's#/usr/bin/python#/usr/bin/python2.7#g' %{buildroot}%{_bindir}/spm
## sed -i 's#/usr/bin/python#/usr/bin/python2.7#g' %{buildroot}%{_bindir}/salt*
## sed -i 's#/usr/bin/python#/usr/bin/python2.7#g' %{buildroot}%{_initrddir}/salt*
## %endif

# Logrotate
install -p %{SOURCE10} .
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/salt

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/bash_completion.d/salt.bash

# Fish completion (TBD remove -v)
mkdir -p %{buildroot}%{fish_dir}
install -p -m 0644  %{SOURCE13} %{buildroot}%{fish_dir}/salt.fish
install -p -m 0644  %{SOURCE14} %{buildroot}%{fish_dir}/salt_common.fish
install -p -m 0644  %{SOURCE15} %{buildroot}%{fish_dir}/salt-call.fish
install -p -m 0644  %{SOURCE16} %{buildroot}%{fish_dir}/salt-cp.fish
install -p -m 0644  %{SOURCE17} %{buildroot}%{fish_dir}/salt-key.fish
install -p -m 0644  %{SOURCE18} %{buildroot}%{fish_dir}/salt-master.fish
install -p -m 0644  %{SOURCE19} %{buildroot}%{fish_dir}/salt-minion.fish
install -p -m 0644  %{SOURCE20} %{buildroot}%{fish_dir}/salt-run.fish
install -p -m 0644  %{SOURCE21} %{buildroot}%{fish_dir}/salt-syndic.fish

%if ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})
%check
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
mkdir %{_tmppath}/salt-test-cache
PYTHONPATH=%{pythonpath} %{__python} setup.py test --runtests-opts=-u
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/LICENSE
%{python2_sitelib}/%{name}/*
#%%{python2_sitelib}/%%{name}-%%{version}-py?.?.egg-info

%if ( "0%{?dist}" == "0.amzn1" )
%{python2_sitelib}/%{name}-%{version}.egg-info
%else
%{python2_sitelib}/%{name}-*-py?.?.egg-info
%endif

%{_sysconfdir}/logrotate.d/salt
%{_sysconfdir}/bash_completion.d/salt.bash
%{_var}/cache/salt
%{_var}/log/salt
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/README.fedora
%{_bindir}/spm
%doc %{_mandir}/man1/spm.1*
%config(noreplace) %{_sysconfdir}/salt/
%config(noreplace) %{_sysconfdir}/salt/pki
%config(noreplace) %{fish_dir}/salt*.fish

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7*
%doc %{_mandir}/man1/salt.1*
%doc %{_mandir}/man1/salt-cp.1*
%doc %{_mandir}/man1/salt-key.1*
%doc %{_mandir}/man1/salt-master.1*
%doc %{_mandir}/man1/salt-run.1*
%doc %{_mandir}/man1/salt-unity.1*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_bindir}/salt-unity
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-master
%else
%{_unitdir}/salt-master.service
%endif
%config(noreplace) %{_sysconfdir}/salt/master
%config(noreplace) %{_sysconfdir}/salt/master.d
%config(noreplace) %{_sysconfdir}/salt/pki/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1*
%doc %{_mandir}/man1/salt-minion.1*
%doc %{_mandir}/man1/salt-proxy.1*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%{_bindir}/salt-proxy
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-minion
%else
%{_unitdir}/salt-minion.service
%{_unitdir}/salt-proxy@.service
%endif
%config(noreplace) %{_sysconfdir}/salt/minion
%config(noreplace) %{_sysconfdir}/salt/proxy
%config(noreplace) %{_sysconfdir}/salt/minion.d
%config(noreplace) %{_sysconfdir}/salt/pki/minion

%files syndic
%doc %{_mandir}/man1/salt-syndic.1*
%{_bindir}/salt-syndic
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-syndic
%else
%{_unitdir}/salt-syndic.service
%endif

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1*
%{_bindir}/salt-api
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/salt-api
%else
%{_unitdir}/salt-api.service
%endif

%files cloud
%doc %{_mandir}/man1/salt-cloud.1*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%doc %{_mandir}/man1/salt-ssh.1*
%{_bindir}/salt-ssh
%config(noreplace) %{_sysconfdir}/salt/roster


# less than RHEL 8 / Fedora 16
# not sure if RHEL 7 will use systemd yet
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

%preun master
  if [ $1 -eq 0 ] ; then
    /sbin/service salt-master stop >/dev/null 2>&1
  fi

%preun syndic
  if [ $1 -eq 0 ] ; then
      /sbin/service salt-syndic stop >/dev/null 2>&1
  fi

%preun minion
  if [ $1 -eq 0 ] ; then
      /sbin/service salt-minion stop >/dev/null 2>&1
  fi

%preun api
  if [ $1 -eq 0 ] ; then
      /sbin/service salt-api stop >/dev/null 2>&1
  fi

%post master
  if [ "$1" -ge "2" ] ; then
    /sbin/service salt-master condrestart >/dev/null 2>&1 || :
  fi

%post syndic
  if [ "$1" -ge "2" ] ; then
    /sbin/service salt-syndic condrestart >/dev/null 2>&1 || :
  fi

%post minion
  if [ "$1" -ge "2" ] ; then
    /sbin/service salt-minion condrestart >/dev/null 2>&1 || :
  fi

%post api
  if [ "$1" -ge "2" ] ; then
    /sbin/service salt-api condrestart >/dev/null 2>&1 || :
  fi

%postun master
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-master condrestart >/dev/null 2>&1 || :
  fi

%postun syndic
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-syndic condrestart >/dev/null 2>&1 || :
  fi

%postun minion
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-minion condrestart >/dev/null 2>&1 || :
  fi

%postun api
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-api condrestart >/dev/null 2>&1 || :
  fi

%else

%preun master
%if 0%{?systemd_preun:1}
  %systemd_preun salt-master.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-master.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-master.service > /dev/null 2>&1 || :
  fi
%endif

%preun syndic
%if 0%{?systemd_preun:1}
  %systemd_preun salt-syndic.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-syndic.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-syndic.service > /dev/null 2>&1 || :
  fi
%endif

%preun minion
%if 0%{?systemd_preun:1}
  %systemd_preun salt-minion.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
  fi
%endif

%preun api
%if 0%{?systemd_preun:1}
  %systemd_preun salt-api.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-api.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-api.service > /dev/null 2>&1 || :
  fi
%endif

%post master
%if 0%{?systemd_post:1}
  if [ $1 -gt 1 ] ; then
    /usr/bin/systemctl try-restart salt-master.service >/dev/null 2>&1 || :
  else
    %systemd_post salt-master.service
  fi
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post syndic
%if 0%{?systemd_post:1}
  if [ $1 -gt 1 ] ; then
    /usr/bin/systemctl try-restart salt-syndic.service >/dev/null 2>&1 || :
  else
    %systemd_post salt-syndic.service
  fi
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post minion
%if 0%{?systemd_post:1}
  if [ $1 -gt 1 ] ; then
    /usr/bin/systemctl try-restart salt-minion.service >/dev/null 2>&1 || :
  else
    %systemd_post salt-minion.service
  fi
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post api
%if 0%{?systemd_post:1}
  if [ $1 -gt 1 ] ; then
    /usr/bin/systemctl try-restart salt-api.service >/dev/null 2>&1 || :
  else
    %systemd_post salt-api.service
  fi
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%postun master
%if 0%{?systemd_post:1}
  %systemd_postun_with_restart salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-master.service &>/dev/null || :
%endif

%postun syndic
%if 0%{?systemd_post:1}
  %systemd_postun_with_restart salt-syndic.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-syndic.service &>/dev/null || :
%endif

%postun minion
%if 0%{?systemd_post:1}
  %systemd_postun_with_restart salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-minion.service &>/dev/null || :
%endif

%postun api
%if 0%{?systemd_post:1}
  %systemd_postun_with_restart salt-api.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-api.service &>/dev/null || :
%endif
%endif

%changelog
* Thu Jun 21 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2018.3.2-1
- Update to feature release 2018.3.2-1  for Python 2

* Fri Jun 08 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2018.3.1-1
- Update to feature release 2018.3.1-1  for Python 2
- Revised minimum msgpack version >= 0.4

* Fri Mar 30 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2018.3.0-1
- Update to feature release 2018.3.0-1

* Tue Mar 27 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.5-1
- Update to feature release 2017.7.5-1

* Fri Feb 16 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.4-1
- Update to feature release 2017.7.4-1
- Limit to Tornado use to between versions 4.2.1 and less than 5.0

* Tue Jan 30 2018 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.3-1
- Update to feature release 2017.7.3-1

* Mon Sep 18 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.2-1
- Update to feature release 2017.7.2

* Tue Aug 15 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.1-1
- Update to feature release 2017.7.1
- Altered dependency for dnf-utils instead of yum-utils if Fedora 26 or greater

* Wed Jul 12 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2017.7.0-1
- Update to feature release 2017.7.0
- Added python-psutil as a requirement, disabled auto enable for Redhat 6

* Thu Jun 22 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.6-1
- Update to feature release 2016.11.6

* Thu Apr 27 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.5-1
- Update to feature release 2016.11.5
- Altered to use pycryptodomex if 64 bit and Redhat 6 and greater otherwise pycrypto
- Addition of salt-proxy@.service

* Wed Apr 19 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.4-1
- Update to feature release 2016.11.4 and use of pycryptodomex

* Mon Mar 20 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.3-2
- Updated to allow for pre and post processing for salt-syndic and salt-api

* Wed Feb 22 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.3-1
- Update to feature release 2016.11.3

* Tue Jan 17 2017 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.2-1
- Update to feature release 2016.11.2

* Tue Dec 13 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.1-1
- Update to feature release 2016.11.1

* Wed Nov 30 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.0-2
- Adjust for single spec for Redhat family and fish-completions

* Tue Nov 22 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.0-1
- Update to feature release 2016.11.0

* Wed Nov  2 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.0-0.rc2
- Update to feature release 2016.11.0 Release Candidate 2

* Wed Oct 26 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.11.0-0.rc1
- Update to feature release 2016.11.0 Release Candidate 1

* Fri Oct 14 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.3-4
- Ported to build on Amazon Linux 2016.09 natively

* Mon Sep 12 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.3-3
- Adjust spec file for Fedora 24 support

* Tue Aug 30 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.3-2
- Fix systemd update of existing installation

* Fri Aug 26 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.3-1
- Update to feature release 2016.3.3

* Fri Jul 29 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.2-1
- Update to feature release 2016.3.2

* Fri Jun 10 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.1-1
- Update to feature release 2016.3.1

* Mon May 23 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.0-1
- Update to feature release 2016.3.0

* Wed Apr  6 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2016.3.0-rc2
- Update to bugfix release 2016.3.0 Release Candidate 2

* Fri Mar 25 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.8-2
- Patched fixes 32129, 32023, 32117

* Wed Mar 16 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.8-1
- Update to bugfix release 2015.8.8

* Tue Feb 16 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.7-1
- Update to bugfix release 2015.8.7

* Mon Jan 25 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.4-1
- Update to bugfix release 2015.8.4

* Thu Jan 14 2016 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.3-3
- Add systemd environment files

* Mon Dec  7 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.3-2
- Additional salt configuration directories on install

* Tue Dec  1 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.3-1
- Update to bugfix release 2015.8.3

* Fri Nov 13 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.2-1
- Update to bugfix release 2015.8.2

* Fri Oct 30 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.1-2
- Update for pre-install direcories

* Wed Oct  7 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.1-1
- Update to feature release 2015.8.1

* Wed Sep 30 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.0-3
- Update include python-uinttest2

* Wed Sep  9 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.0-2
- Update include testing

* Fri Sep  4 2015 SaltStack Packaging Team <packaging@saltstack.com> - 2015.8.0-1
- Update to feature release 2015.8.0

* Fri Jul 10 2015 Erik Johnson <erik@saltstack.com> - 2015.5.3-4
- Patch tests

* Fri Jul 10 2015 Erik Johnson <erik@saltstack.com> - 2015.5.3-3
- Patch init grain

* Fri Jul 10 2015 Erik Johnson <erik@saltstack.com> - 2015.5.3-2
- Update to bugfix release 2015.5.3, add bash completion

* Thu Jun  4 2015 Erik Johnson <erik@saltstack.com> - 2015.5.2-3
- Mark salt-ssh roster as a config file to prevent replacement

* Thu Jun  4 2015 Erik Johnson <erik@saltstack.com> - 2015.5.2-2
- Update skipped tests

* Thu Jun  4 2015 Erik Johnson <erik@saltstack.com> - 2015.5.2-1
- Update to bugfix release 2015.5.2

* Mon Jun  1 2015 Erik Johnson <erik@saltstack.com> - 2015.5.1-2
- Add missing dependency on which (RH #1226636)

* Wed May 27 2015 Erik Johnson <erik@saltstack.com> - 2015.5.1-1
- Update to bugfix release 2015.5.1

* Mon May 11 2015 Erik Johnson <erik@saltstack.com> - 2015.5.0-1
- Update to feature release 2015.5.0

* Fri Apr 17 2015 Erik Johnson <erik@saltstack.com> - 2014.7.5-1
- Update to bugfix release 2014.7.5

* Tue Apr  7 2015 Erik Johnson <erik@saltstack.com> - 2014.7.4-4
- Fix RH bug #1210316 and Salt bug #22003

* Tue Apr  7 2015 Erik Johnson <erik@saltstack.com> - 2014.7.4-2
- Update to bugfix release 2014.7.4

* Tue Feb 17 2015 Erik Johnson <erik@saltstack.com> - 2014.7.2-1
- Update to bugfix release 2014.7.2

* Mon Jan 19 2015 Erik Johnson <erik@saltstack.com> - 2014.7.1-1
- Update to bugfix release 2014.7.1

* Fri Nov  7 2014 Erik Johnson <erik@saltstack.com> - 2014.7.0-3
- Make salt-api its own package

* Thu Nov  6 2014 Erik Johnson <erik@saltstack.com> - 2014.7.0-2
- Fix changelog

* Thu Nov  6 2014 Erik Johnson <erik@saltstack.com> - 2014.7.0-1
- Update to feature release 2014.7.0

* Fri Oct 17 2014 Erik Johnson <erik@saltstack.com> - 2014.1.13-1
- Update to bugfix release 2014.1.13

* Mon Sep 29 2014 Erik Johnson <erik@saltstack.com> - 2014.1.11-1
- Update to bugfix release 2014.1.11

* Sun Aug 10 2014 Erik Johnson <erik@saltstack.com> - 2014.1.10-4
- Fix incorrect conditional

* Tue Aug  5 2014 Erik Johnson <erik@saltstack.com> - 2014.1.10-2
- Deploy cachedir with package

* Mon Aug  4 2014 Erik Johnson <erik@saltstack.com> - 2014.1.10-1
- Update to bugfix release 2014.1.10

* Thu Jul 10 2014 Erik Johnson <erik@saltstack.com> - 2014.1.7-3
- Add logrotate script

* Thu Jul 10 2014 Erik Johnson <erik@saltstack.com> - 2014.1.7-1
- Update to bugfix release 2014.1.7

* Wed Jun 11 2014 Erik Johnson <erik@saltstack.com> - 2014.1.5-1
- Update to bugfix release 2014.1.5

* Tue May  6 2014 Erik Johnson <erik@saltstack.com> - 2014.1.4-1
- Update to bugfix release 2014.1.4

* Thu Feb 20 2014 Erik Johnson <erik@saltstack.com> - 2014.1.0-1
- Update to feature release 2014.1.0

* Mon Jan 27 2014 Erik Johnson <erik@saltstack.com> - 0.17.5-1
- Update to bugfix release 0.17.5

* Thu Dec 19 2013 Erik Johnson <erik@saltstack.com> - 0.17.4-1
- Update to bugfix release 0.17.4

* Tue Nov 19 2013 Erik Johnson <erik@saltstack.com> - 0.17.2-2
- Patched to fix pkgrepo.managed regression

* Mon Nov 18 2013 Erik Johnson <erik@saltstack.com> - 0.17.2-1
- Update to bugfix release 0.17.2

* Thu Oct 17 2013 Erik Johnson <erik@saltstack.com> - 0.17.1-1
- Update to bugfix release 0.17.1

* Thu Sep 26 2013 Erik Johnson <erik@saltstack.com> - 0.17.0-1
- Update to feature release 0.17.0

* Wed Sep 11 2013 David Anderson <dave@dubkat.com>
- Change sourcing order of init functions and salt default file

* Sat Sep 07 2013 Erik Johnson <erik@saltstack.com> - 0.16.4-1
- Update to patch release 0.16.4

* Sun Aug 25 2013 Florian La Roche <Florian.LaRoche@gmx.net>
- fixed preun/postun scripts for salt-minion

* Thu Aug 15 2013 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 0.16.3-1
- Update to patch release 0.16.3

* Thu Aug 8 2013 Clint Savage <herlo1@gmail.com> - 0.16.2-1
- Update to patch release 0.16.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 9 2013 Clint Savage <herlo1@gmail.com> - 0.16.0-1
- Update to feature release 0.16.0

* Sat Jun 1 2013 Clint Savage <herlo1@gmail.com> - 0.15.3-1
- Update to patch release 0.15.3
- Removed OrderedDict patch

* Fri May 31 2013 Clint Savage <herlo1@gmail.com> - 0.15.2-1
- Update to patch release 0.15.2
- Patch OrderedDict for failed tests (SaltStack#4912)

* Wed May 8 2013 Clint Savage <herlo1@gmail.com> - 0.15.1-1
- Update to patch release 0.15.1

* Sat May 4 2013 Clint Savage <herlo1@gmail.com> - 0.15.0-1
- Update to upstream feature release 0.15.0

* Fri Apr 19 2013 Clint Savage <herlo1@gmail.com> - 0.14.1-1
- Update to upstream patch release 0.14.1

* Sat Mar 23 2013 Clint Savage <herlo1@gmail.com> - 0.14.0-1
- Update to upstream feature release 0.14.0

* Fri Mar 22 2013 Clint Savage <herlo1@gmail.com> - 0.13.3-1
- Update to upstream patch release 0.13.3

* Wed Mar 13 2013 Clint Savage <herlo1@gmail.com> - 0.13.2-1
- Update to upstream patch release 0.13.2

* Fri Feb 15 2013 Clint Savage <herlo1@gmail.com> - 0.13.1-1
- Update to upstream patch release 0.13.1
- Add unittest support

* Sat Feb 02 2013 Clint Savage <herlo1@gmail.com> - 0.12.1-1
- Remove patches and update to upstream patch release 0.12.1

* Thu Jan 17 2013 Wendall Cada <wendallc@83864.com> - 0.12.0-2
- Added unittest support

* Wed Jan 16 2013 Clint Savage <herlo1@gmail.com> - 0.12.0-1
- Upstream release 0.12.0

* Fri Dec 14 2012 Clint Savage <herlo1@gmail.com> - 0.11.1-1
- Upstream patch release 0.11.1
- Fixes security vulnerability (https://github.com/saltstack/salt/issues/2916)

* Fri Dec 14 2012 Clint Savage <herlo1@gmail.com> - 0.11.0-1
- Moved to upstream release 0.11.0

* Wed Dec 05 2012 Mike Chesnut <mchesnut@gmail.com> - 0.10.5-2
- moved to upstream release 0.10.5
- removing references to minion.template and master.template, as those files
  have been removed from the repo

* Sun Nov 18 2012 Clint Savage <herlo1@gmail.com> - 0.10.5-1
- Moved to upstream release 0.10.5
- Added pciutils as Requires

* Wed Oct 24 2012 Clint Savage <herlo1@gmail.com> - 0.10.4-1
- Moved to upstream release 0.10.4
- Patched jcollie/systemd-service-status (SALT@GH#2335) (RHBZ#869669)

* Tue Oct 2 2012 Clint Savage <herlo1@gmail.com> - 0.10.3-1
- Moved to upstream release 0.10.3
- Added systemd scriplets (RHBZ#850408)

* Thu Aug 2 2012 Clint Savage <herlo1@gmail.com> - 0.10.2-2
- Fix upstream bug #1730 per RHBZ#845295

* Tue Jul 31 2012 Clint Savage <herlo1@gmail.com> - 0.10.2-1
- Moved to upstream release 0.10.2
- Removed PyXML as a dependency

* Sat Jun 16 2012 Clint Savage <herlo1@gmail.com> - 0.10.1-1
- Moved to upstream release 0.10.1

* Sat Apr 28 2012 Clint Savage <herlo1@gmail.com> - 0.9.9.1-1
- Moved to upstream release 0.9.9.1

* Tue Apr 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.8-2
- dmidecode is x86 only

* Wed Mar 21 2012 Clint Savage <herlo1@gmail.com> - 0.9.8-1
- Moved to upstream release 0.9.8

* Thu Mar 8 2012 Clint Savage <herlo1@gmail.com> - 0.9.7-2
- Added dmidecode as a Requires

* Thu Feb 16 2012 Clint Savage <herlo1@gmail.com> - 0.9.7-1
- Moved to upstream release 0.9.7

* Tue Jan 24 2012 Clint Savage <herlo1@gmail.com> - 0.9.6-2
- Added README.fedora and removed deps for optional modules

* Sat Jan 21 2012 Clint Savage <herlo1@gmail.com> - 0.9.6-1
- New upstream release

* Sun Jan 8 2012 Clint Savage <herlo1@gmail.com> - 0.9.4-6
- Missed some critical elements for SysV and rpmlint cleanup

* Sun Jan 8 2012 Clint Savage <herlo1@gmail.com> - 0.9.4-5
- SysV clean up in post

* Sat Jan 7 2012 Clint Savage <herlo1@gmail.com> - 0.9.4-4
- Cleaning up perms, group and descriptions, adding post scripts for systemd

* Thu Jan 5 2012 Clint Savage <herlo1@gmail.com> - 0.9.4-3
- Updating for systemd on Fedora 15+

* Thu Dec 1 2011 Clint Savage <herlo1@gmail.com> - 0.9.4-2
- Removing requirement for Cython. Optional only for salt-minion

* Wed Nov 30 2011 Clint Savage <herlo1@gmail.com> - 0.9.4-1
- New upstream release with new features and bugfixes

* Thu Nov 17 2011 Clint Savage <herlo1@gmail.com> - 0.9.3-1
- New upstream release with new features and bugfixes

* Sat Sep 17 2011 Clint Savage <herlo1@gmail.com> - 0.9.2-1
- Bugfix release from upstream to fix python2.6 issues

* Fri Sep 09 2011 Clint Savage <herlo1@gmail.com> - 0.9.1-1
- Initial packages
