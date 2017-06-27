%global srcname pycryptodome
%global nsname %{srcname}x
# For now we don't want to replace PyCrypto as it requires patching of
# libraries/applications (in some cases).
%global eggname %{nsname}
%global modname Cryptodome


%{!?python3_pkgversion:%global python3_pkgversion 3}

## %global python2_pkgversion 2
%global python2_pkgversion %{nil}

%if 0%{?rhel} == 6
%global with_explicit_python27 1
%global pybasever 2.7
%global __python_ver 27
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __os_install_post %{__python27_os_install_post}
%endif

Name:           python%{?__python_ver}-%{srcname}
Version:        3.4.3
Release:        3%{?dist}
Summary:        Self-contained Python package of low-level cryptographic primitives

# Only OCB blockcipher mode is patented, but according to
# http://web.cs.ucdavis.edu/~rogaway/ocb/license1.pdf
# BSD 2-claus ("Simplified") has been approved in 2009 so
# it means license for OSS Implementations applies here.
License:        Public Domain and BSD
URL:            https://pycryptodome.readthedocs.io
Source0:        https://github.com/Legrandin/pycryptodome/archive/v%{version}/%{srcname}-%{version}.tar.gz

# Unbundle libtomcrypt
Patch0:         0001-use-system-libtomcrypt.patch
Patch1:         0002-handle-MD5.patch

BuildRequires:  gcc
BuildRequires:  libtomcrypt-devel
BuildRequires:  gmp-devel

%if 0%{?with_explicit_python27}
Requires: python%{?__python_ver}  >= 2.7.9-1
%endif 

%global _description \
PyCryptodome is a fork of PyCrypto. It brings the following enhancements with\
respect to the last official version of PyCrypto (2.6.1):\
\
* Authenticated encryption modes (GCM, CCM, EAX, SIV, OCB)\
* Accelerated AES on Intel platforms via AES-NI\
* First class support for PyPy\
* Elliptic curves cryptography (NIST P-256 curve only)\
* Better and more compact API (nonce and iv attributes for ciphers, automatic\
  generation of random nonces and IVs, simplified CTR cipher mode, and more)\
* SHA-3 (including SHAKE XOFs) and BLAKE2 hash algorithms\
* Salsa20 and ChaCha20 stream ciphers\
* scrypt and HKDF\
* Deterministic (EC)DSA\
* Password-protected PKCS#8 key containers\
* Shamir’s Secret Sharing scheme\
* Random numbers get sourced directly from the OS (and not from a CSPRNG in\
  userspace)\
* Cleaner RSA and DSA key generation (largely based on FIPS 186-4)\
* Major clean ups and simplification of the code base\
\
PyCryptodome is not a wrapper to a separate C library like OpenSSL. To the\
largest possible extent, algorithms are implemented in pure Python. Only the\
pieces that are extremely critical to performance (e.g. block ciphers) are\
implemented as C extensions.

%description %{_description}

## DGM %package -n python2-%{eggname}
## DGM %package -n python%{python2_pkgversion}-%{eggname}
## DGM Summary:        %{summary}
## DGM %{?python_provide:%python_provide python2-%{eggname}}
## DGM BuildRequires:  python2-devel
## DGM BuildRequires:  python2-setuptools
## DGM 
## DGM %description -n python2-%{eggname} %{_description}
## DGM 

%if 0%{?with_explicit_python27}
%package -n python%{?__python_ver}-%{eggname}
Summary:        %{summary}
%{?python_provide:%python_provide python-%{eggname}}
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools

%description -n python%{?__python_ver}-%{eggname} %{_description}

Python %{?__python_ver} version.

%else

%package -n python2-%{eggname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{eggname}}
BuildRequires:  python%{python2_pkgversion}-devel
BuildRequires:  python%{python2_pkgversion}-setuptools

%description -n python2-%{eggname} %{_description}

Python 2 version.
%endif

%package -n python3-%{eggname}
Summary:        %{summary}
## DGM %{?python_provide:%python_provide python3-%{eggname}}
## DGM BuildRequires:  python3-devel
## DGM BuildRequires:  python3-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description -n python3-%{eggname} %{_description}

Python 3 version.

%prep
%setup -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1

# Bundled libtomcrypt
rm -vrf src/libtom/
# Use separate namespace
touch .separate_namespace

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
%{__python2} setup.py test -v
%{__python3} setup.py test -v

%if 0%{?with_explicit_python27}
%files -n python%{?__python_ver}-%{eggname}
%else
%files -n python2-%{eggname}
%endif
%license Doc/LEGAL/
%{python2_sitearch}/%{eggname}-*.egg-info/
%{python2_sitearch}/%{modname}/

%files -n python3-%{eggname}
%license Doc/LEGAL/
%{python3_sitearch}/%{eggname}-*.egg-info/
%{python3_sitearch}/%{modname}/

%changelog
* Tue May 09 2017 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.3-3
- Updated to use Python 2.7 on Redhat 6

* Wed Apr 26 2017 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.3-2
- Patched to allow for MD5 handling on Redhat 6 using  hashlib causing errors

* Sun Jan 01 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.4.3-1
- Update to 3.4.3

* Sun Aug 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.4.2-1
- Initial package
## %autosetup -n %{srcname}-%{version} -p1
