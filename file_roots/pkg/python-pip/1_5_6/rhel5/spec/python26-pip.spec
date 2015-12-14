%global __python python26
%global python_sitelib /usr/lib/python2.6/site-packages

%global srcname pip

Name:           python26-%{srcname}
Version:        1.5.6
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz

Patch0:         pip-1.5rc1-allow-stripping-prefix-from-wheel-RECORD-files.patch
# patch by dstufft, more at http://seclists.org/oss-sec/2014/q4/655
Patch1:         local-dos.patch
#Patch2:         skip-network-tests.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python26-devel
BuildRequires:  python26-distribute

Requires:       python26
Requires:       python26-distribute

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%prep
%setup -q -n %{srcname}-%{version}

%patch0 -p1
%patch1 -p1
#%patch2 -p1

%{__sed} -i '1d' pip/__init__.py


%build

%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst docs
%attr(755,root,root) %{_bindir}/pip*
%{python_sitelib}/pip*

%changelog
* Mon Apr  6 2015 Erik Johnson <erik@saltstack.com> - 1.5.6-1
- Initial EL5 build
