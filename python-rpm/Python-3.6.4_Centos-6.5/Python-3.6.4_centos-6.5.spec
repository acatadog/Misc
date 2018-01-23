%define pyname Python
%define pybasever 3.6
%define version %{pybasever}.4
%define release 1

%global with_gdbm 1



Summary: A high-level object-oriented programming language
Name: Python3
Version: %{version}
Release: %{release}
#Source: https://www.python.org/ftp/python/%{version}/%{pyname}-%{version}.tgz
Source0: %{pyname}-%{version}.tgz
License: PSF license
Group: Development/Languages
BuildRoot: %{_tmppath}/%{pyname}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: phw
Url: http://www.python.org/
Packager: phw

Provides: python(abi) = %{pybasever}
Provides: python-abi = %{pybasever}
Provides: /usr/local/bin/python
Provides: libpython3.6m.so.debug()(64bit)

BuildRequires: autoconf
#BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: expat-devel >= 2.0.1
BuildRequires: findutils
BuildRequires: gcc-c++

%if %{with_gdbm}
BuildRequires: gdbm-devel
%endif

BuildRequires: glibc-devel
BuildRequires: gmp-devel
#BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel

BuildRequires: tar
BuildRequires: tcl-devel
#BuildRequires: tix-devel
BuildRequires: tk-devel

BuildRequires: zlib-devel


Patch1: 00001-lib64.patch

%description
Python3 for CentOS release 6.5

%prep
%setup -n %{pyname}-%{version}
%patch1 -p0

%build
%configure \
  --enable-shared \
  --enable-loadable-sqlite-extensions \
  --enable-ipv6 \
  --with-computed-gotos=yes \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --with-ensurepip \
  --enable-optimizations \
  %{nil}

make
#make test

%install
make DESTDIR=$RPM_BUILD_ROOT install
export QA_SKIP_BUILD_ROOT=1


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/include/*
%{_prefix}/lib/*
%{_prefix}/lib64/*
%{_prefix}/share/man/man1/*
