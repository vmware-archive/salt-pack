%if (! 0%{?rhel}) || 0%{?rhel} > 7
%global with_python3 1
%global build_wheel 1
%global with_tests 0
%endif
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname pip
%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%endif
%endif

%global bashcompdir %(b=$(pkg-config --variable=completionsdir bash-completion 2>/dev/null); echo ${b:-%{_sysconfdir}/bash_completion.d})
%if "%{bashcompdir}" != "%{_sysconfdir}/bash_completion.d"
%global bashcomp2 1
%endif

Name:           python-%{srcname}
Version:        7.1.0
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz

# to get tests:
# git clone https://github.com/pypa/pip && cd fig
# git checkout 1.5.6 && tar -czvf pip-1.5.6-tests.tar.gz tests/
%if 0%{?with_tests}
Source1:        pip-6.0.8-tests.tar.gz
%endif

Patch0:         pip-1.5rc1-allow-stripping-prefix-from-wheel-RECORD-files.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-mock
BuildRequires:  pytest
BuildRequires:  python-pretend
BuildRequires:  python-freezegun
BuildRequires:  python-scripttest
BuildRequires:  python-virtualenv
%endif
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
Requires:       python-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%if 0%{?with_python3}
%package -n python3-pip
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Libraries

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  bash-completion
%if 0%{?with_tests}
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-pretend
BuildRequires:  python3-freezegun
BuildRequires:  python3-scripttest
BuildRequires:  python3-virtualenv
%endif
%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif
Requires:  python3-setuptools

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_tests}
tar -xf %{SOURCE1}
%endif

%patch0 -p1

%{__sed} -i '1d' pip/__init__.py

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%if 0%{?build_wheel}
%{__python} setup.py bdist_wheel
%else
%{__python} setup.py build
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
%{__python3} setup.py bdist_wheel
%else
%{__python3} setup.py build
%endif
popd
%endif # with_python3


%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
pip3 install -I dist/%{python3_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/pip
%else
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif
%endif # with_python3

%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%endif

mkdir -p %{buildroot}%{bashcompdir}
PYTHONPATH=%{buildroot}%{python_sitelib} \
    %{buildroot}%{_bindir}/pip completion --bash \
    > %{buildroot}%{bashcompdir}/pip
%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip3 completion --bash \
    > %{buildroot}%{bashcompdir}/pip3
%endif
pips2=pip
pips3=pip3
for pip in %{buildroot}%{_bindir}/pip*; do
    pip=$(basename $pip)
    case $pip in
        pip2*)
            pips2="$pips2 $pip"
%if 0%{?bashcomp2}
            ln -s pip %{buildroot}%{bashcompdir}/$pip
%endif
            ;;
%if 0%{?with_python3}
        pip3?*)
            pips3="$pips3 $pip"
%if 0%{?bashcomp2}
            ln -s pip3 %{buildroot}%{bashcompdir}/$pip
%endif
            ;;
%endif
    esac
done
%if 0%{?with_python3}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 $pips3/" \
    -e s/_pip_completion/_pip3_completion/ \
    %{buildroot}%{bashcompdir}/pip3
%endif
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 $pips2/" \
    %{buildroot}%{bashcompdir}/pip

%if 0%{?with_tests}
%check
py.test -m 'not network'
pushd %{py3dir}
py.test-3.4 -m 'not network'
popd
%endif


%clean
%{__rm} -rf %{buildroot}

# unfortunately, pip's test suite requires virtualenv >= 1.6 which isn't in
# fedora yet. Once it is, check can be implemented

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc README.rst docs
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip2*
%{python_sitelib}/pip*
%{bashcompdir}
%if 0%{?with_python3}
%exclude %{bashcompdir}/pip3*
%endif
%if 0%{?bashcomp2}
%dir %(dirname %{bashcompdir})
%endif

%if 0%{?with_python3}
%files -n python3-pip
%defattr(-,root,root,-)
%license LICENSE.txt
%doc README.rst docs
%attr(755,root,root) %{_bindir}/pip3*
%{python3_sitelib}/pip*
%dir %{bashcompdir}
%{bashcompdir}/pip3*
%if 0%{?bashcomp2}
%dir %(dirname %{bashcompdir})
%endif
%endif # with_python3

%changelog
* Wed Jul 01 2015 Slavek Kabrda <bkabrda@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Tue Jun 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 7.0.3-3
- Install bash completion
- Ship LICENSE.txt as %%license where available

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 7.0.3-1
- Update to 7.0.3

* Fri Mar 06 2015 Matej Stuchlik <mstuchli@redhat.com> - 6.0.8-1
- Update to 6.0.8

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

