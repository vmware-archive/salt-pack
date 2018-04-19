%global srcname pycryptodome
%global nsname %{srcname}x
# For now we don't want to replace PyCrypto as it requires patching of
# libraries/applications (in some cases).
%global eggname %{nsname}
%global modname Cryptodome


%global with_python3 0

%{!?python3_pkgversion:%global python3_pkgversion 3}

## %global python2_pkgversion 2
%global python2_pkgversion %{nil}


Name:           python-%{srcname}
Version:        3.4.11
Release:        2%{?dist}
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

%package -n python2-%{eggname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{eggname}}
BuildRequires:  python%{python2_pkgversion}-devel
BuildRequires:  python%{python2_pkgversion}-setuptools

%description -n python2-%{eggname} %{_description}

Python 2 version.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{eggname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%{eggname} %{_description}

Python 3 version.
%endif

%prep
## %%autosetup -n %%{srcname}-%%{version} -p1
%setup -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1

# Bundled libtomcrypt
rm -vrf src/libtom/
# Use separate namespace
touch .separate_namespace

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

## %check
## %{__python2} setup.py test -v
## %if 0%{?with_python3}
## %{__python3} setup.py test -v
## %endif

%files -n python2-%{eggname}
%license Doc/LEGAL/
%{python2_sitearch}/%{eggname}-*.egg-info/
%{python2_sitearch}/%{modname}/

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{eggname}
%license Doc/LEGAL/
%{python3_sitearch}/%{eggname}-*.egg-info/
%{python3_sitearch}/%{modname}/
%endif

%changelog
* Thu Apr 19 2018 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.11-2
- Update to v3.4.11, and update Python 3 version produced

* Wed Apr 26 2017 SaltStack Packaging Team <packaging@saltstack.com> - 3.4.3-2
- Patched to allow for MD5 handling on Redhat 6 using  hashlib causing errors

* Sun Jan 01 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.4.3-1
- Update to 3.4.3

* Sun Aug 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.4.2-1
- Initial package

