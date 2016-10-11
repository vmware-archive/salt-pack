%if 0%{?fedora} > 12
%global with_python3 0
%endif

# Fix lack of rhel macro on COPR
# (https://bugzilla.redhat.com/show_bug.cgi?id=1213482)
%if 0%{?rhel} == 5 || (0%{?rhel} == 0 && 0%{?fedora} == 0)
%global rhel5 1
%endif

# el5 has python-2.4, but 2.5 is minimum, so build with python2.6:
# http://lists.zeromq.org/pipermail/zeromq-dev/2010-November/007597.html
%if 0%{?rhel5}
%global pybasever 2.6
%global __python_ver 26
%global __python %{_bindir}/python%{?pybasever}
%global python python26
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%else
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
%filter_setup
}
%endif

%global checkout 18f5d061558a176f5496aa8e049182c1a7da64f6

%global srcname pyzmq

%global run_tests 0

Name:           python-zmq
Version:        14.5.0
Release:        2%{?dist}
Summary:        Software library for fast, message-based applications

Group:          Development/Libraries
License:        LGPLv3+ and ASL 2.0
URL:            http://www.zeromq.org/bindings:python
# VCS:          git:http://github.com/zeromq/pyzmq.git
# git checkout with the commands:
# git clone http://github.com/zeromq/pyzmq.git pyzmq.git
# cd pyzmq.git
# git archive --format=tar --prefix=pyzmq-%%{version}/ %%{checkout} | xz -z --force - > pyzmq-%%{version}.tar.xz
Source0:        http://cloud.github.com/downloads/zeromq/pyzmq/pyzmq-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel5}
BuildRequires:  python26-devel
BuildRequires:  python26-distribute
%else
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%endif

BuildRequires:  zeromq-devel >= 4.0.5

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
%endif


%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%if 0%{?rhel5}
%package -n python26-zmq
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%description -n python26-zmq
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings for python26.
%endif


%if 0%{?rhel5}
%package -n python26-zmq-tests
%else
%package tests
%endif
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%if 0%{?rhel5}
Requires:       python26-zmq = %{version}-%{release}
%description -n python26-zmq-tests
%else
Requires:       python-zmq = %{version}-%{release}
%description tests
%endif
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the testsuite for the python bindings.


%if 0%{?with_python3}
%package -n python3-zmq
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%description -n python3-zmq
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%package -n python3-zmq-tests
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
Requires:       python3-zmq = %{version}-%{release}
%description -n python3-zmq-tests
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


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
rm -r %{py3dir}/examples

%endif


%build
CFLAGS="%{optflags}" %{__python} setupegg.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3



%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# remove tests doesn't work here, do that after running the tests

popd
%endif # with_python3


%{__python} setupegg.py install -O1 --skip-build --root %{buildroot}

# remove tests doesn't work here, do that after running the tests



%check
%if 0%{?run_tests}
    rm zmq/__*
    PYTHONPATH=%{buildroot}%{python_sitearch} \
        %{__python} setup.py test

    %if 0%{?with_python3}
    # there is no python3-nose yet
    pushd %{py3dir}
    rm zmq/__*
    PYTHONPATH=%{buildroot}%{python3_sitearch} \
        %{__python3} setup.py test
    popd
    %endif
%endif


%if 0%{?rhel5}
%files -n python26-zmq
%else
%files
%endif
%defattr(-,root,root,-)
%doc COPYING.LESSER examples/
%{python_sitearch}/%{srcname}-*.egg-info
%{python_sitearch}/zmq
%exclude %{python_sitearch}/zmq/tests

%if 0%{?rhel5}
%files -n python26-zmq-tests
%else
%files tests
%endif
%defattr(-,root,root,-)
%{python_sitearch}/zmq/tests

%if 0%{?with_python3}
%files -n python3-zmq
%defattr(-,root,root,-)
%doc COPYING.LESSER
# examples/
%{python3_sitearch}/%{srcname}-*.egg-info
%{python3_sitearch}/zmq
%exclude %{python3_sitearch}/zmq/tests

%files -n python3-zmq-tests
%defattr(-,root,root,-)
%{python3_sitearch}/zmq/tests
%endif


%changelog
* Fri Apr 10 2015 Erik Johnson <erik@saltstack.com> - 14.5.0-1
- Updated for version 14.5.0

* Wed Oct  8 2014 Erik Johnson <erik@saltstack.com> - 14.3.1-3
- Update minimum supported zeromq-devel version

* Thu Sep  4 2014 Erik Johnson <erik@saltstack.com> - 14.3.1-2
- Added minimum supported zeromq-devel version

* Thu Sep  4 2014 Erik Johnson <erik@saltstack.com> - 14.3.1-1
- Updated for version 14.3.1

* Wed Dec 14 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-3
- tests package requires main package
- filter python3

* Thu Dec  8 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.9-2
- use proper buildroot macro
- use python2.6 on el5 and below (only build intended for el5)
- build python26-zmq and ignore python-zmq packages on el5
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
