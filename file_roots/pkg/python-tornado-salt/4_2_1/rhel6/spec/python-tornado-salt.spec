%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?rhel} > 6 || 0%{?fedora} > 12
%global __python2 /usr/bin/python
%else
%global __python2 /usr/bin/python2.6
%endif

# Fix lack of rhel macro on COPR
# (https://bugzilla.redhat.com/show_bug.cgi?id=1213482)
%if (0%{?rhel} == 0 && 0%{?fedora} == 0) || 0%{?rhel} == 5
%global rhel5 1
%endif

%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global _srcname tornado
%global _modname_old tornado
%global _modname_new tornado_salt
%global _pkgname tornado-salt

Name:           python-%{_pkgname}
Version:        4.2.1
Release:        1%{?dist}
Summary:        Scalable, non-blocking web server and tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://pypi.python.org/packages/source/t/tornado/tornado-%{version}.tar.gz
# Patch to use system CA certs instead of certifi
Patch0:         python-tornado-cert.patch
Patch1:         python-tornado-netutil-cert.patch
Patch2:         %{_modname_new}_rename.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel5}

BuildRequires:  python26-devel
BuildRequires:  python26-distribute
BuildRequires:  python26-backports-ssl_match_hostname
Requires:       python26-backports-ssl_match_hostname
Requires:       python26-pycurl

%else

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-backports-ssl_match_hostname
BuildRequires:  python-unittest2
Requires:       python-backports-ssl_match_hostname
Requires:       python-pycurl

%if 0%{?with_python3}
BuildRequires:  python2-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%endif

%endif

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package doc
Summary:        Examples for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%if 0%{?rhel5}
%package -n python26-%{_pkgname}
Summary:        Scalable, non-blocking web server and tools
Group:          Development/Libraries
Requires:       python26-backports-ssl_match_hostname
Requires:       python26-pycurl

%description -n python26-%{_pkgname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package -n python26-%{_pkgname}-doc
Summary:        Examples for python-%{_pkgname}
Group:          Documentation
Requires:       python26-%{_pkgname} = %{version}-%{release}

%description -n python26-%{_pkgname}-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%endif # rhel5


%if 0%{?with_python3}
%package -n python3-%{_pkgname}
Summary:        Scalable, non-blocking web server and tools
Group:          Development/Libraries
%description -n python3-%{_pkgname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package -n python3-%{_pkgname}-doc
Summary:        Examples for python3-%{_pkgname}
Group:          Documentation
Requires:       python3-%{_pkgname} = %{version}-%{release}

%description -n python3-%{_pkgname}-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%endif # with_python3


%prep
%setup -qc
mv %{_srcname}-%{version} python2
pushd python2
%patch0 -p1 -b .cert
%patch1 -p1 -b .cert

# Rename usage of "tornado" to "tornado_salt"
%patch2 -p1

# remove shebang from files
%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
%endif # with_python3

%build
%if 0%{?with_python3}
pushd python3
    # Rename directory in source to "tornado_salt"
    mv %{_modname_old} %{_modname_new}
    mv %{_modname_old}.egg-info %{_modname_new}.egg-info
    %{__python3} setup.py build
popd
%endif # with_python3

pushd python2
    # Rename directory in source to "tornado_salt"
    mv %{_modname_old} %{_modname_new}
    mv %{_modname_old}.egg-info %{_modname_new}.egg-info
    %{__python2} setup.py build
popd


%install
%if 0%{?with_python3}
pushd python3
    PATH=$PATH:%{buildroot}%{python3_sitearch}/%{_srcname}
    %{__python3} setup.py install --root=%{buildroot}
popd
%endif # with_python3

pushd python2
    PATH=$PATH:%{buildroot}%{python2_sitearch}/%{_srcname}
    %{__python2} setup.py install --root=%{buildroot}
popd


%check
%if ! 0%{?rhel5} || 0%{?rhel} > 6 || 0%{?fedora} > 12
    %if 0%{?with_python3}
    pushd python3
        PYTHONPATH=%{python3_sitearch} \
        %{__python3} -m %{_modname_new}.test.runtests --verbose
    popd
    %endif # with_python3
    pushd python2
        PYTHONPATH=%{python2_sitearch} \
        %{__python2} -m %{_modname_new}.test.runtests --verbose
    popd
%endif

%if 0%{?rhel5}

%files -n python26-%{_pkgname}
%doc python2/README.rst python2/PKG-INFO

%{python2_sitearch}/%{_modname_new}/
%{python2_sitearch}/%{_modname_new}-%{version}-*.egg-info

%files -n python26-%{_pkgname}-doc
%doc python2/demos

%else

%files
%doc python2/README.rst python2/PKG-INFO

%{python2_sitearch}/%{_modname_new}/
%{python2_sitearch}/%{_modname_new}-%{version}-*.egg-info

%files doc
%doc python2/demos

%endif

%if 0%{?with_python3}
%files -n python3-%{_pkgname}
%doc python3/README.rst python3/PKG-INFO

%{python3_sitearch}/%{_modname_new}/
%{python3_sitearch}/%{_modname_new}-%{version}-*.egg-info

%files -n python3-%{_pkgname}-doc
%doc python3/demos
%endif


%changelog
* Thu Dec 24 2015 SaltStack Packaging Team <packaging@saltstack.com> 4.2.1-1
- Initial build
