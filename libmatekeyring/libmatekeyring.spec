%define glib2_version 2.16.0
%define dbus_version 1.0
%define gcrypt_version 1.2.2

Summary: 		Framework for managing passwords and other secrets
Name:    		libmatekeyring
Version: 		1.4.0
Release: 		1%{?dist}
License: 		GPLv2+ and LGPLv2+
Group:   		System Environment/Libraries
Source:  		http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
URL:     		http://pub.mate-desktop.org

BuildRequires: 	glib2-devel >= %{glib2_version}
BuildRequires: 	dbus-devel >= %{dbus_version}
BuildRequires: 	libgcrypt-devel >= %{gcrypt_version}
BuildRequires: 	intltool
BuildRequires:  mate-common
BuildRequires:  gtk-doc

%description
libmatekeyring is a program that keep password and other secrets for
users. The library libmatekeyring is used by applications to integrate
with the libmatekeyring system.

%package devel
Summary: 	Development files for libmate-keyring
License: 	LGPLv2+
Group: 		Development/Libraries
Requires: 	%name = %{version}-%{release}
Requires: 	glib2-devel

%description devel
The libmatekeyring-devel package contains the libraries and
header files needed to develop applications that use libmate-keyring.


%prep
%setup -q -n libmatekeyring-%{version}
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-gtk-doc
	
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libmatekeyring


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libmatekeyring.lang
%defattr(-, root, root, -)
%doc AUTHORS NEWS README COPYING
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root, -)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%doc %{_datadir}/gtk-doc/

%changelog
* Thu Jul 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0

* Fri May 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.3.0-1
- update to version 1.3.0

* Tue Feb 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-1
- update to version 1.2.0

* Thu Feb 23 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-3
- fixed build error for  libmateui i686

* Thu Feb 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686
- enable fedora patch

* Wed Jan 04 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - libmatekbd-1.1.0-1
- libmate-keyring.spec based on libgnome-keyring-2.32.0-2.fc14 spec

* Fri Mar 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.32.0-2
- Fix an invalid assert checking pending calls (#660407, #665761)

