# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
%define soversion 10
%define __fipspath /usr/local/ssl/fips-2.0
%define __fips_standalone_sha1 %{__fipspath}/bin/fips_standalone_sha1

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

Summary: A general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.0.2t
Release: 58%{?dist}
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: openssl-%{version}-phw.tar.gz
Source2: Makefile.certificate
Source5: README.legacy-settings
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source8: openssl-thread-test.c
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source11: README.FIPS

# Build changes
Patch2: openssl-1.0.1t-defaults.patch

# Functionality changes
Patch33: openssl-1.0.0-beta4-ca-dir.patch


License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: coreutils, krb5-devel, perl, sed, zlib-devel, /usr/bin/cmp
BuildRequires: /usr/bin/rename
Requires: coreutils, make
Requires: ca-certificates >= 2008-5

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, krb5-devel, zlib-devel
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n %{name}-%{version}

%patch2 -p1 -b .defaults

sed -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64
sslarch=linux-ppc64
%endif

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
	enable-cms enable-md2 no-mdc2 no-rc5 no-ec2m no-gost no-srp \
	--with-krb5-flavor=MIT --enginesdir=%{_libdir}/openssl/engines \
	--with-krb5-dir=/usr shared  ${sslarch} %{?!nofips:fips}

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
make depend
make all

# Generate hashes for the included certs.
make rehash

# Overwrite FIPS README and copy README.legacy-settings
cp -f %{SOURCE5} %{SOURCE11} .

%check
# Verify that what was compiled actually works.

# We must revert patch33 before tests otherwise they will fail
#patch -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
make -C test apps tests
%{__cc} -o openssl-thread-test \
	`krb5-config --cflags` \
	-I./include \
	$RPM_OPT_FLAGS \
	%{SOURCE8} \
	-L. \
	-lssl -lcrypto \
	`krb5-config --libs` \
	-lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of sha1 checksum of the final stripped library
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    %{__fips_standalone_sha1} $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{version}.sha1 \
    ln -sf .libcrypto.so.%{version}.sha1 $RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{soversion}.sha1 \
    %{__fips_standalone_sha1} $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.sha1 \
    ln -sf .libssl.so.%{version}.sha1 $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.sha1 \
%{nil}

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
mkdir $RPM_BUILD_ROOT/%{_lib}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/renew-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{_includedir}/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{_mandir}
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
done
popd

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc
mv CA.sh CA
popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h
%endif

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ LICENSE CHANGES NEWS INSTALL README
%doc doc/c-indentation.el doc/openssl.txt
#%doc doc/openssl_button.html doc/openssl_button.gif
%doc doc/ssleay.txt
%doc README.FIPS
%doc README.legacy-settings
%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{_sysconfdir}/pki/tls/certs/renew-dummy-cert
%{_sysconfdir}/pki/tls/certs/Makefile
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%attr(0755,root,root) %{_bindir}/openssl
%attr(0644,root,root) %{_mandir}/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{_mandir}/man5*/*
%attr(0644,root,root) %{_mandir}/man7*/*
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.sha1
%attr(0644,root,root) %{_libdir}/.libssl.so.*.sha1
%attr(0755,root,root) %{_libdir}/openssl

%files devel
%defattr(-,root,root)
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*.a

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0644,root,root) %{_mandir}/man1*/*.pl*
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Wed Sep 18 2019 phw <13935045@qq.com> 1.0.2t-58
- build openssl 1.0.2t-fips

