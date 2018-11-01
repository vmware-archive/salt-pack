%global with_python3 0

# we don't want to provide private python extension libs in either the python2 or python3 dirs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%global checkout 18f5d061558a176f5496aa8e049182c1a7da64f6

%global srcname pyzmq
%global modname zmq

%global run_tests 0

Name:           python-zmq
Version:        15.3.0
Release:        3%{?dist}
Summary:        Software library for fast, message-based applications

Group:          Development/Libraries
License:        LGPLv3+ and ASL 2.0 and BSD
URL:            http://www.zeromq.org/bindings:python
# VCS:          git:http://github.com/zeromq/pyzmq.git
# git checkout with the commands:
# git clone http://github.com/zeromq/pyzmq.git pyzmq.git
# cd pyzmq.git
# git archive --format=tar --prefix=pyzmq-%%{version}/ %%{checkout} | xz -z --force - > pyzmq-%%{version}.tar.xz
#Source0:        https://pypi.python.org/packages/source/p/pyzmq/pyzmq-%{version}.tar.gz
Source0:        https://github.com/zeromq/pyzmq/archive/v%{version}.tar.gz#/pyzmq-%{version}.tar.gz

BuildRequires:  chrpath

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  zeromq-devel
BuildRequires:  Cython
%if 0%{?run_tests}
BuildRequires:  pytest
BuildRequires:  python-tornado
%endif

# For some tests
# czmq currently FTBFS, so enable it some time later
#BuildRequires:  czmq-devel

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# needed for 2to3
BuildRequires:  python-tools
%if 0%{?run_tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-tornado
%endif
%endif

Requires:   zeromq >= 4

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%package -n python-zmq-tests
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
Requires:       python-zmq = %{version}-%{release}
%{?python_provide:%python_provide python-%{modname}-tests}
%description -n python-zmq-tests
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the testsuite for the python bindings.


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-zmq
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}
%description -n python%{python3_pkgversion}-zmq
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%package -n python%{python3_pkgversion}-zmq-tests
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
Requires:       python%{python3_pkgversion}-zmq = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}-tests}
%description -n python%{python3_pkgversion}-zmq-tests
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the testsuite for the python bindings.

%endif


%prep
%setup -q -n %{srcname}-%{version}

# remove bundled libraries
rm -rf bundled

# forcibly regenerate the Cython-generated .c files:
#find zmq -name "*.c" -delete
#%%{__python} setup.py cython

# remove shebangs
for lib in zmq/eventloop/*.py; do
    sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done

# remove excecutable bits
chmod -x examples/pubsub/topics_pub.py
chmod -x examples/pubsub/topics_sub.py

# delete hidden files
#find examples -name '.*' | xargs rm -v



%build
%global py_setup setupegg.py
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3



%install
%global RPATH /zmq/{backend/cython,devices}
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
%py3_install

chrpath --delete %{buildroot}%{python3_sitearch}%{RPATH}/*.so
%endif # with_python3


%py2_install

chrpath --delete %{buildroot}%{python_sitearch}%{RPATH}/*.so

# Remove Python 3 only code from python2 package
rm  %{buildroot}%{python2_sitearch}/zmq/asyncio.py \
    %{buildroot}%{python2_sitearch}/zmq/auth/asyncio.py \
    %{buildroot}%{python2_sitearch}/zmq/tests/*test_asyncio.py \
    %{buildroot}%{python2_sitearch}/zmq/tests/test_future.py


%check
%if 0%{?run_tests}
    # Make sure we import from the install directory
    rm zmq/__*.py
    PYTHONPATH=%{buildroot}%{python3_sitearch} \
        %{__python3} setup.py test

    # Remove Python 3 only tests
    rm  zmq/asyncio.py zmq/auth/asyncio.py \
        zmq/tests/*test_asyncio.py zmq/tests/test_future.py
    PYTHONPATH=%{buildroot}%{python2_sitearch} \
        %{__python2} setup.py test
%endif


%files -n python-%{modname}
%license COPYING.*
%doc README.md examples/
%{python2_sitearch}/%{srcname}-*.egg-info
%{python2_sitearch}/zmq
%exclude %{python2_sitearch}/zmq/tests

%files -n python-%{modname}-tests
%{python2_sitearch}/zmq/tests

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-zmq
%license COPYING.*
%doc README.md
# examples/
%{python3_sitearch}/%{srcname}-*.egg-info
%{python3_sitearch}/zmq
%exclude %{python3_sitearch}/zmq/tests

%files -n python%{python3_pkgversion}-zmq-tests
%{python3_sitearch}/zmq/tests
%endif


%changelog
* Fri Aug 03 2018 SaltStack Packaging Team <packagin@saltstack.com> - 15.3.0-3
- Added dependency on zeromq >= 4, zeromq provided by Salt

* Tue Jul 19 2016 SaltStack Packaging Team <packagin@saltstack.com> - 15.3.0-2
- Disabled python3, tests and reverted output python2-* to python-*

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 15.3.0-1
- Update to 15.3.0

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 14.7.0-7
- Use modern provides filtering

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Thomas Spura <tomspur@fedoraproject.org> - 14.7.0-5
- Use setupegg.py for building/installing to have an unzip'ed egg

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Thomas Spura <tomspur@fedoraproject.org> - 14.7.0-3
- rebuilt to pick up new obsoletes/provides

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 14.7.0-2
- Use python_provide and py_build macros
- Cleanup spec

* Mon Jun 29 2015 Ralph Bean <rbean@redhat.com> - 14.7.0-2
- Support python34 on EPEL7.

* Tue Jun 23 2015 Thomas Spura <tomspur@fedoraproject.org> - 14.7.0-1
- update to 14.7.0
- temporarily disable python3 testsuite as it hangs on koji

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Thomas Spura <tomspur@fedoraproject.org> - 14.4.1-1
- update to 14.4.1
- build against zeromq-4

* Wed Aug 27 2014 Thomas Spura <tomspur@fedoraproject.org> - 14.3.1-1
- update to 14.3.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 13.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug  5 2013 Thomas Spura <tomspur@fedoraproject.org> - 13.0.2-1
- update to new version (fixes FTBFS)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Thomas Spura <tomspur@fedoraproject.org> - 13.0.0-1
- update to 13.0.0
- add BSD to license list

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0.1-1
- update to 2.2.0.1
- move to BR zeromq3
- not all *.c files may be deleted, when receneration of .c files by Cython
- remove bundled folder explicitely

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-4
- force regeneration of .c files by Cython (needed for python 3.3 support)

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.0-1
- update to 2.2.0

* Wed Mar  7 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.11-1
- update to new version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-3
- tests package requires main package
- filter python3 libs

* Thu Dec  8 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-2
- use proper buildroot macro
- don't include tests twice

* Wed Sep 21 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-1
- update to new version
- run testsuite on python3

* Sun Jul 31 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-2
- don't delete the tests, needed by ipython-tests on runtime
- don't use _sourcedir macro

* Wed Apr  6 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-1
- update to new version (#690199)

* Wed Mar 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-1
- update to new version (#682201)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10.1-1
- update to new version (fixes memory leak)
- no need to run 2to3 on python3 subpackage

* Thu Jan 13 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10-1
- update to new version
- remove patch (is upstream)
- run tests differently

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.8-2
- rebuild for newer python3

* Thu Sep 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-1
- update to new version to be comply with zeromp

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Aug  5 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-3
- add missing BR for 2to3

* Tue Aug  3 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-2
- build python3 subpackage
- rename to from pyzmq to python-zmq
- change license

* Sun Jul 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-1
- renew git snapshot
- start from version 0.1 like upstream (not the version from zeromq)
- remove buildroot / %%clean

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org - 2.0.7-1
- initial package (based on upstreams example one)
