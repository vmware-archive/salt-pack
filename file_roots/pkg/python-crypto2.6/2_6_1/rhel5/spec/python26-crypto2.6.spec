%global __python python26
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}

%global _modname_old Crypto
%global _modname_new Crypto26
%global _eggname pycrypto26

Summary:        Cryptography library for Python
Name:           python26-crypto2.6
Version:        2.6.1
Release:        4%{?dist}
# Mostly Public Domain apart from parts of HMAC.py and setup.py, which are Python
License:        Public Domain and Python
Group:          Development/Libraries
URL:            http://www.pycrypto.org/
Source0:        http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Patch0:         python-crypto-2.4-optflags.patch
Patch1:         python-crypto-2.4-fix-pubkey-size-divisions.patch
Patch2:         %{_modname_new}_rename.patch
Provides:       %{_eggname} = %{version}-%{release}
BuildRequires:  python26-devel >= 2.2, gmp-devel >= 4.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot-%(id -nu)

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/%{_modname_new}/.*\.so}
%{?filter_setup}

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This package provides version 2.6.1 under an alternate name ("Crypto26"), so
that it can be installed side-by-side with the default version available in
EPEL.

%prep
%setup -n pycrypto-%{version} -q

# Use distribution compiler flags rather than upstream's
%patch0 -p1

# Fix divisions within benchmarking suite:
%patch1 -p1

# Rename usage of "Crypto" to "Crypto26"
%patch2 -p1

%build
# Rename directory in source to "Crypto26"
mv lib/%{_modname_old} lib/%{_modname_new}
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python_sitearch} -name '*.so' -exec chmod -c g-w {} \;

# See if there's any egg-info
if [ -f %{buildroot}%{python_sitearch}/%{_eggname}-%{version}-py?.?.egg-info ]; then
        echo %{python_sitearch}/%{_eggname}-%{version}-py?.?.egg-info
fi > egg-info

# Remove the _fastmath extension module for now.  Timing vulnerability when
# this is used with libgmp<5 which is what RHEL6 provides
# Remove this if RHEL6 updates gmp or backports mpz_powm_sec() to their gmp
find %{buildroot} -name '_fastmath.*' -exec rm -f {} \;

%check
%{__python} setup.py test

# Benchmark uses os.urandom(), which is available from python 2.4
%if %(%{__python} -c "import sys; print sys.hexversion >= 0x02040000 and 1 or 0" 2>/dev/null || echo 0)
PYTHONPATH=%{buildroot}%{python_sitearch} %{__python} pct-speedtest.py
%endif

%clean
rm -rf %{buildroot}

%files -f egg-info
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LEGAL/ COPYRIGHT Doc/
%{python_sitearch}/%{_modname_new}/

%changelog
* Thu Dec 24 2015 SaltStack Packaging Team <packaging@saltstack.com> 2.6.1-4
- Initial build
