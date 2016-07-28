-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Format: 1.0
Source: python2.7
Binary: python2.7, libpython2.7-stdlib, python2.7-minimal, libpython2.7-minimal, libpython2.7, python2.7-examples, python2.7-dev, libpython2.7-dev, libpython2.7-testsuite, idle-python2.7, python2.7-doc, python2.7-dbg, libpython2.7-dbg
Architecture: any all
Version: 2.7.12-1
Maintainer: Matthias Klose <doko@debian.org>
Standards-Version: 3.9.8
Vcs-Browser: https://code.launchpad.net/~doko/python/pkg2.7-debian
Vcs-Bzr: http://bazaar.launchpad.net/~doko/python/pkg2.7-debian
Testsuite: autopkgtest
Build-Depends: debhelper (>= 9), dpkg-dev (>= 1.17.11), quilt, autoconf, autotools-dev, lsb-release, sharutils, libreadline-dev, libtinfo-dev, libncursesw5-dev (>= 5.3), tk-dev, blt-dev (>= 2.4z), libssl-dev, zlib1g-dev, libbz2-dev, libexpat1-dev, libbluetooth-dev [linux-any], locales [!armel !avr32 !hppa !ia64 !mipsel], libsqlite3-dev, libffi-dev (>= 3.0.5) [!or1k !avr32], libgpm2 [linux-any], mime-support, netbase, net-tools, bzip2, time, libdb-dev (<< 1:6.0), libgdbm-dev, python:any, help2man, xvfb, xauth
Build-Depends-Indep: python-sphinx
Build-Conflicts: autoconf2.13, hardening-wrapper, python-cxx-dev, python-xml, python2.7-xml, tcl8.4-dev, tk8.4-dev
Package-List:
 idle-python2.7 deb python optional arch=all
 libpython2.7 deb libs standard arch=any
 libpython2.7-dbg deb debug extra arch=any
 libpython2.7-dev deb libdevel optional arch=any
 libpython2.7-minimal deb python standard arch=any
 libpython2.7-stdlib deb python standard arch=any
 libpython2.7-testsuite deb libdevel optional arch=all
 python2.7 deb python standard arch=any
 python2.7-dbg deb debug extra arch=any
 python2.7-dev deb python optional arch=any
 python2.7-doc deb doc optional arch=all
 python2.7-examples deb python optional arch=all
 python2.7-minimal deb python standard arch=any
Checksums-Sha1:
 1e80b781eacc6b7e243bd277e5002426aa56d0f1 16935960 python2.7_2.7.12.orig.tar.gz
 6cda98bbcbe04605c977b95b7f83abcad3b31173 274657 python2.7_2.7.12-1.diff.gz
Checksums-Sha256:
 3cb522d17463dfa69a155ab18cffa399b358c966c0363d6c8b5b3bf1384da4b6 16935960 python2.7_2.7.12.orig.tar.gz
 229438b402ddfce25b1c35e50d5110be5d9024724c2dad22950e9c9046635ab1 274657 python2.7_2.7.12-1.diff.gz
Files:
 88d61f82e3616a4be952828b3694109d 16935960 python2.7_2.7.12.orig.tar.gz
 0e8554e5ca3fc77fc1b1e2617099a77f 274657 python2.7_2.7.12-1.diff.gz

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iQIcBAEBCAAGBQJXc41TAAoJEL1+qmB3j6b1qacP/2EksToQqbzmgiH6bJeo5fya
OYpkWQRFa5DqIxnHMDZ2PJAVP7zklOrdWEvrtNLBT/UNoPUhwfeiqjAHCz4mtj8V
3CaSEQit/vy30SAmc52mTNV/7hg3OJqc1p0Fzb4iSVJtNDTbSV52b0veHVkRLxmH
jsYUfuEHav6XxsL54DY4HG5GepCVkdUePghNMQC1KNGHx3kws67mBa/h7Z0pgBz/
+46N7JIUrA7AyPDg1Xpevo7C8r/nxOeiExVOlYBlLPaU5vyEP6Ae9JDwCOPfOeB5
Nnj+nDeTCDFI6WZQLEHRqOErf6SEB/xl6OAnYgKrawnJygWaZRKq2hqB5XFTkINv
iY5owazB9+gVBG4Zjpmn8vpkPda33KKQphePfWC3dbkyqHTJn/azXkOIvF2DFgkM
8/eP3mKflnn3q60HUBP7YEINh/d6ANEkMhGoxb3yMdyyH/YQVOonTrukoUcn1ZYr
A/JSrOLiPH+S4yH2j1CQwSJWz3g19cIzMA9iODAibi93SpOVf//GhDC325Tr9+aB
o1jyxb2a6uthSAGo8gpaVurblwgr6XEBnOcfbfvWHyGksaphXPyB7T4pTZGAtdEI
DKpVXbR0P3QkU2xiBpI1sUJYIYmm4/otWkTktEbNdp3ihbI17B04RRIeBIkyG5aI
YiJYz90ym5V6jyxDFqoL
=PgWE
-----END PGP SIGNATURE-----
