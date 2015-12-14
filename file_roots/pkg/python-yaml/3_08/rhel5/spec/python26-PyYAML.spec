%global __python26 /usr/bin/python2.6
%define python26_sitelib %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
#%{!?python26_sitelib: %global python26_sitearch %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global __os_install_post %{__python26_os_install_post}

Name:           python26-PyYAML
Version:        3.08
Release:        4%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/PyYAML-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python26-devel, python26-setuptools, libyaml-devel

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that allow
to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%prep
%setup -q -n PyYAML-%{version}


%build
%{__python26} setup.py build
chmod a-x examples/yaml-highlight/yaml_hl.py


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
%{__python26} setup.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc PKG-INFO README LICENSE examples
%{python26_sitelib}/*


