Name:		libffi
Version:	3.0.5
Release:	1%{?dist}
Summary:	A portable foreign function interface library

Group:		System Environment/Libraries
License:	BSD
URL:		http://sourceware.org/libffi
Source0:	http://sourceware.org/libffi/libffi-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.  A
calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.  The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.  


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:       pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%post devel
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/libffi.info.gz

%preun devel
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/libffi.info.gz
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}-%{version}
%{_libdir}/*.so
%{_mandir}/man3/*.gz
%{_infodir}/libffi.info.gz

%changelog
* Tue Jul 08 2008 Anthony Green <green@redhat.com> 3.0.5-1
- Upgrade to 3.0.5

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 3.0.1-1
- Upgrade to 3.0.1

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.9-1
- Upgrade to 2.99.9
- Require pkgconfig for the devel package.
- Update summary.

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.8-1
- Upgrade to 2.99.8

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.7-1
- Upgrade to 2.99.7

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.6-1
- Upgrade to 2.99.6

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.4-1
- Upgrade to 2.99.4

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.3-1
- Upgrade to 2.99.3

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.2-1
- Created.
