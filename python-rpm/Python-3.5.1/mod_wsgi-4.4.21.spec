%define g_name mod_wsgi
%define g_basever 4.4
%define g_version %{g_basever}.21
%define g_release 1

Summary: A WSGI interface for Python web applications in Apache
Name: %{g_name}
Version: %{g_version}
Release: %{g_release}
#Source: https://github.com/GrahamDumpleton/mod_wsgi
Source0: %{g_name}-%{g_version}.zip
License: PSF license
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{g_name}-%{g_version}-%{g_release}-buildroot
Prefix: %{_prefix}
Vendor: phw
Url: https://github.com/GrahamDumpleton/mod_wsgi
Packager: phw

#Provides: mod_wsgi = %{g_basever}

BuildRequires: httpd-devel >= 2.2
BuildRequires: Python3 >= 3.5
BuildRequires: unzip

Requires: httpd >= 2.2

%description
mod_wsgi with Python3 for httpd-2.2.15-29 in CentOS release 6.5

%prep
%setup -n %{g_name}-%{g_version}

%build
%configure --with-python=/usr/bin/python3

make

%install
make DESTDIR=$RPM_BUILD_ROOT install
echo "LoadModule wsgi_module modules/mod_wsgi.so" >wsgi.conf
install -p -D -m 0644 wsgi.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/wsgi.conf

%clean
rm -rf $RPM_BUILD_ROOT
rm -f wsgi.conf

%files
%defattr(-,root,root)
%{_prefix}/lib64/httpd/modules/*
%config /etc/httpd/conf.d/wsgi.conf

