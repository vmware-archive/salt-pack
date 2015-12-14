%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 0
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:           PyYAML
Version:        3.11
Release:        1%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python-devel, python-setuptools, libyaml-devel
Provides:       python-yaml = %{version}-%{release}
Provides:       python-yaml%{?_isa} = %{version}-%{release}
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if 0%{?with_python3}
%package -n python3-PyYAML
Summary: YAML parser and emitter for Python
Group: Development/Libraries

%description -n python3-PyYAML
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif


%prep
%setup -q -n %{name}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="${RPM_OPT_FLAGS}" %{__python3} setup.py --with-libyaml build
popd
%endif


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-PyYAML
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python3_sitearch}/*
%endif


%changelog
* Fri Apr 27 2012 John Eckersberg <jeckersb@redhat.com> - 3.10-3
- Add Provides for python-yaml (BZ#740390)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 John Eckersberg <jeckersb@redhat.com> - 3.10-1
- New upstream release 3.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 John Eckersberg <jeckersb@redhat.com> - 3.09-7
- Add support to build for python 3

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.09-6
- Bump release number for upgrade path

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.09-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 3.09-1
- New upstream release 3.09

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 - John Eckersberg <jeckersb@redhat.com> - 3.08-5
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce inclusion of libyaml in build with --with-libyaml option to setup.py
- Deliver to %%{python_sitearch} instead of %%{python_sitelib} due to _yaml.so
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-4
- Correction, change libyaml to libyaml-devel in BuildRequires

* Mon Mar 2 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-3
- Add libyaml to BuildRequires

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.06-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 John Eckersberg <jeckersb@redhat.com> - 3.06-1
- New upstream release

* Wed Jan 02 2008 John Eckersberg <jeckersb@redhat.com> - 3.05-2
- Remove explicit dependency on python >= 2.3
- Remove executable on example script in docs

* Mon Dec 17 2007 John Eckersberg <jeckersb@redhat.com> - 3.05-1
- Initial packaging for Fedora
