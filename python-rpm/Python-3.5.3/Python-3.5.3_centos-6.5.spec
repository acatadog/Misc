%define pyname Python
%define pybasever 3.5
%define version %{pybasever}.3
%define release 1

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
Url: http://www.python.org/3.5
Packager: phw

Provides: python(abi) = %{pybasever}
Provides: python-abi = %{pybasever}
Provides: /usr/local/bin/python

# yum -y install openssl-devel readline-devel bzip2-devel sqlite-devel zlib-devel ncurses-devel db4-devel expat-devel tk-devel xz-devel

BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: db4-devel >= 4.7
BuildRequires: expat-devel
BuildRequires: findutils
BuildRequires: gcc-c++
BuildRequires: gdbm-devel
BuildRequires: glibc-devel
#BuildRequires: libGL-devel
#BuildRequires: gmp-devel
#BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: tar
BuildRequires: tcl-devel
#BuildRequires: tix-devel
BuildRequires: tk-devel
BuildRequires: xz-devel
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
  --enable-profiling \
  --enable-loadable-sqlite-extensions \
  --enable-ipv6 \
  --with-computed-gotos=yes \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --enable-optimizations \
#  --without-ensurepip \
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
