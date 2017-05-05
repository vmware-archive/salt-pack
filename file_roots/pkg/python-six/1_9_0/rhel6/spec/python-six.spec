%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora} > 12 || 0%{?rhel} > 7
%global with_python3 0

%global __python3 python3

%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global __os_install_post %{__python27_os_install_post}
%endif


Name:           python%{?__python_ver}-six
Version:        1.9.0
Release:        3%{?dist}
Summary:        Python 2 and 3 compatibility utilities

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/six/
Source0:        http://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?with_explicit_python27}
BuildRequires:  python%{?__python_ver}-devel
%else
BuildRequires:  python2-devel
%endif
Requires:       python%{?__python_ver}

# For use by selftests:
#BuildRequires:  pytest
#BuildRequires:  tkinter
%if 0%{?with_python3}
BuildRequires:  python3-devel
# For use by selftests:
BuildRequires:  python3-pytest
BuildRequires:  python3-tkinter
%endif

%description
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 2 build of the module.

%if 0%{?with_python3}
%package -n python3-six
Summary:        Python 2 and 3 compatibility utilities
Group:          Development/Languages

%description -n python3-six
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 3 build of the module.
%endif

%prep
%setup -q -n six-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


#%check
#py.test -rfsxX test_six.py
#%if 0%{?with_python3}
#pushd %{py3dir}
#py.test-%{python3_version} -rfsxX test_six.py
#popd
#%endif


%files -n python%{?__python_ver}-six
%doc LICENSE README documentation/index.rst
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-six
%doc LICENSE README documentation/index.rst
%{python3_sitelib}/*
%endif


%changelog
* Fri May  5 2017 SaltStack Packaging Team <packaging@saltstack.com> - 1.9.0-3
- Updated to use Python 2.7 on Redhat 6 and disabled Python 3

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.9.0-2
- Rebuild for RHEL 6.7
Resolves: rhbz#1183146

* Tue Mar 10 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.9.0-1
- upgrade to 1.9.0

* Tue Apr 29 2014 Matthias Runge <mrugne@redhat.com> - 1.6.1-1
- upgrade to 1.6.1 (rhbz#1076578)

* Fri Mar 07 2014 Matthias Runge <mrunge@redhat.com> - 1.5.2-1
- upgrade to 1.5.2 (rhbz#1048819)

* Mon Sep 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-1
- 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 David Malcolm <dmalcolm@redhat.com> - 1.3.0-1
- 1.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 David Malcolm <dmalcolm@redhat.com> - 1.2.0-1
- 1.2.0 (rhbz#852658)
- add %%check section

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.0-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Ralph Bean <rbean@redhat.com> - 1.1.0-2
- Conditionalized python3-six, allowing an el6 build.

* Tue Feb  7 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.0-1
- 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.0-1
- initial packaging


