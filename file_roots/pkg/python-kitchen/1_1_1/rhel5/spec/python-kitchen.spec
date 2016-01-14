%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python-kitchen
Version:        1.1.1
Release:        1%{?dist}
Summary:        Small, useful pieces of code to make python coding easier

Group:          Development/Languages
License:        LGPLv2+
URL:            https://pypi.python.org/pypi/kitchen/
Source0:        https://fedorahosted.org/releases/k/i/kitchen/kitchen-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
%if 0%{?fedora} || 0%{?rhel} >=  6
# sphinx needs to be more recent to build the html docs
BuildRequires: python-sphinx
%endif
%if 0%{?fedora} || 0%{?rhel} >  6
# At present, chardet isn't present in epel but it's a soft dep
BuildRequires: python-chardet
Requires: python-chardet
%endif

%description
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes), and compatibility modules for writing code that uses
python-2.7 modules but needs to run on python-2.3 

%prep
%setup -q -n kitchen-%{version}


%build
%{__python} setup.py build
# Build docs
%if 0%{?fedora} || 0%{?rhel} >= 6
%{__python} setup.py build_sphinx
cp -pr build/sphinx/html .
rm -rf html/.buildinfo

%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
# In current mock, the PATH isn't being reset.  This causes failures in some
# subprocess tests as a check tests /root/bin/PROGRAM and fails with Permission
# Denied instead of File Not Found.  reseting the PATH works around this.
PATH=/bin:/usr/bin
nosetests
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README NEWS COPYING.LESSER docs/
%if 0%{?fedora} || 0%{?rhel} >= 6
%doc html
%endif
%{python_sitelib}/*


%changelog
* Tue Feb 14 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.1-1
- Bugfix for using easy_gettext_setup or get_translation_object with the
  default localedirs

* Thu Jan 12 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 final

* Thu Apr 14 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.0-1
- Upstream update to 1.0 final

* Sun Feb 20 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.4-1
- Upstream update 0.2.4
  - Changes i18n.easy_gettext_setup() to return lgettext functions when
    byte strings are requested.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.3-2
- Upstream respin of the tarball

* Wed Jan 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.3-1
- Upstream update to 0.2.3
- Fixes https://bugzilla.redhat.com/show_bug.cgi?id=667433

* Mon Jan 3 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.2-1
- Upstream update 0.2.2
  - Adds exception to message functions
- Build html docs

* Thu Sep 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2.1-0.1.a1
- Update to upstream 0.2.1a1 release.
- Fixes build on python-2.7, adds iterutils module, optimizes some functions,
  increases documentation

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2-0.1.a2
- propoerlly version accrding to pre-release guidelines
- run tests
- update to 0.2a2
- include COPYING.LESSER and docs dir

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2a1-2
- rename to python-kitchen

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.2a1-1
- update to 0.2a1

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-3
- fix spelling mistake in description

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-2
- add documentaion
- fix description

* Thu Jul 15 2010 Dennis Gilmore <dennis@ausil.us> - 0.1a3-1
- initial package
