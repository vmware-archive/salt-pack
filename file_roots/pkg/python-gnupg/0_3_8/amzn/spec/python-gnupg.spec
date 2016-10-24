%if ( "0%{?dist}" == "0.amzn1" )
%global with_python3 0
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --install-layout=unix --root %{buildroot}}}

%else

%if 0%{?rhel}
%global with_python3 0
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}
%else
%global with_python3 1
%endif
%endif

Name:           python-gnupg
Version:        0.3.8
Release:        4%{?dist}
Summary:        A wrapper for the Gnu Privacy Guard (GPG or GnuPG)
Group:          Development/Languages

License:        BSD
URL:            http://pythonhosted.org/python-gnupg
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
%else
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with_python3

%description
GnuPG bindings for python. This uses the gpg command.

%if 0%{?with_explicit_python27}
%package -n     python%{?__python_ver}-gnupg
%else
%package -n     python2-gnupg
%endif
Summary:        A wrapper for the Gnu Privacy Guard (GPG or GnuPG)
Requires:       gnupg

%if ( "0%{?dist}" == "0.amzn1" )
%{?python_provide:%python_provide python%{?__python_ver}-gnupg}
%{?el6:Provides: python-gnupg}
%{?el6:Obsoletes: python-gnupg < 0.3.8}
%{?amzn1:Provides: python-gnupg}
%{?amzn1:Obsoletes: python-gnupg < 0.3.8}

%description -n python%{?__python_ver}-gnupg
GnuPG bindings for python. This uses the gpg command.
%else
%{?python_provide:%python_provide python2-gnupg}
%{?el6:Provides: python-gnupg}
%{?el6:Obsoletes: python-gnupg < 0.3.8}

%description -n python2-gnupg
GnuPG bindings for python. This uses the gpg command.
%endif

%if 0%{?with_python3}
%package -n     python3-gnupg
Summary:        A wrapper for the Gnu Privacy Guard (GPG or GnuPG)
Requires:       gnupg
%{?python_provide:%python_provide python3-gnupg}

%description -n python3-gnupg
GnuPG bindings for python. This uses the gpg command.
%endif # with_python3

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%py2_install 
%if 0%{?with_python3}
%py3_install
%endif # with_python3

%if ( "0%{?dist}" == "0.amzn1" )
%files -n python%{?__python_ver}-gnupg
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE.txt
## %{python2_sitelib}/gnupg.py*
## %{python2_sitelib}/python_gnupg-%{version}.egg-info
/usr/lib/python2.7/dist-packages/gnupg.py*
/usr/lib/python2.7/dist-packages/python_gnupg-%{version}.egg-info
%else
%files -n python2-gnupg
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE.txt
%{python2_sitelib}/gnupg.py*
%{python2_sitelib}/python_gnupg-%{version}-py?.?.egg-info
%endif

%if 0%{?with_python3}
%files -n python3-gnupg
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/gnupg.py
%{python3_sitelib}/python_gnupg-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Mon Oct 17 2016 SaltStack Packaging Team <packaging@saltstack.com> - 0.3.8-4
- Ported to build on Amazon Linux 2016.09 natively

* Thu Jun 02 2016 Fabio Alessandro Locati <fabio@locati.cc> - 0.3.8-3
- Put the gnupg dependence for both py2 and py3 packages

* Wed May 04 2016 Fabio Alessandro Locati <fabio@locati.cc> - 0.3.8-2
- Fix provides and obsoletes

* Sun Feb 07 2016 Fabio Alessandro Locati <fabio@locati.cc> - 0.3.8-1
- Enable python3 compilation
- Move to current python standard
- Update 0.3.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 06 2015 Paul Wouters <pwouters@redhat.com> - 0.3.7-1
- Updated to 0.3.7 Merged in export-minimal and armor options, many encoding fixes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Paul Wouters <pwouters@redhat.com> - 0.3.6-3
- Removed patch as gpg.decode_errors=ignore works well

* Thu Apr 17 2014 Paul Wouters <pwouters@redhat.com> - 0.3.6-2
- Re-instate part of export patch that fixed encoding bug

* Thu Feb 06 2014 Paul Wouters <pwouters@redhat.com> - 0.3.6-1
- Updated to 0.3.6 which includes Security fix (CVE-2014-XXXX)
- Upstream including our export patch and converted README file
- Upstream switched to new download site

* Mon Jan 06 2014 Paul Wouters <pwouters@redhat.com> - 0.3.5-4
- Require gnupg (duh)
- Remove cleaning in install target
- Fix license to BSD
- Link to upstream bug tracker for included patch

* Sat Jan 04 2014 Paul Wouters <pwouters@redhat.com> - 0.3.5-3
- Remove unused global, fix python macro, buildroot macro
- Converted README from DOS to unix (and reported upstream)

* Tue Dec 31 2013 Paul Wouters <pwouters@redhat.com> - 0.3.5-2
- Added minimal= and armor= options to export_keys()

* Sun Dec 22 2013 Paul Wouters <pwouters@redhat.com> - 0.3.5-1
- Initial package
