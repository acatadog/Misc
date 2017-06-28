%define g_name pysvn
%define g_basever 1.8
%define g_version %{g_basever}.0
%define g_release 1

Summary: The pysvn project's goal is to enable Tools to be written in Python that use Subversion.
Name: %{g_name}
Version: %{g_version}
Release: %{g_release}
#Source: http://pysvn.barrys-emacs.org/
Source0: %{g_name}-%{g_version}.tar.gz
License: The Apache Software License, Version 1.1
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{g_name}-%{g_version}-%{g_release}-buildroot
Prefix: %{_prefix}
Vendor: phw
Url: http://pysvn.tigris.org/
Packager: phw

#Provides: pysvn = %{g_basever}

BuildRequires: gcc-c++
BuildRequires: subversion-devel >= 1.7
BuildRequires: python-devel >= 2.7

Requires: subversion >= 1.7
Requires: python >= 2.7

%description
pysvn with python2.7 for subversion-1.7 in CentOS release 7.3

%prep
%setup -n %{g_name}-%{g_version}

%build
cd Source
/usr/bin/python setup.py configure
make

%install
cd Source
install -p -D -m 0755 pysvn/__init__.py $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/pysvn/__init__.py
install -p -D -m 0755 pysvn/_pysvn*.so $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/pysvn/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/lib64/python2.7/site-packages/pysvn/*

