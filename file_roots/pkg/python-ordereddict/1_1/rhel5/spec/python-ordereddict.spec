# Python 2.4
%global __python python
%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")

# Python 2.6
%global __python26 /usr/bin/python2.6
%global python26_sitelib %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")

%global srcname ordereddict

Name:           python-%{srcname}
Version:        1.1
Release:        3%{?dist}
Summary:        Implementation of Python 2.7's OrderedDict

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/o/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Drop-in substitute for Py2.7's new collections.OrderedDict. 
Originally based on http://code.activestate.com/recipes/576693/

%package -n python26-%{srcname}
Summary:        Implementation of Python 2.7's OrderedDict
Group:          Development/Languages
BuildRequires:  python26-devel
BuildRequires:  python26-distribute
Requires:       python26

%description -n python26-%{srcname}
Drop-in substitute for Py2.7's new collections.OrderedDict. 
Originally based on http://code.activestate.com/recipes/576693/

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build
%{__python26} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__python26} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/*

%files -n python26-%{srcname}
%defattr(-,root,root,-)
%doc LICENSE
%{python26_sitelib}/*

%changelog
* Thu Jul 31 2014 Erik Johnson <jni@redhat.com> 1.1-3
- Added python26 package

* Thu Oct 28 2010 James Ni <jni@redhat.com> 1.1-2
- Modify the spec file and update to upstream source

* Wed Jul 14 2010 James Ni <jni@redhat.com> 1.1-1
- Initial RPM release
