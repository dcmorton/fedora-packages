%define glib2_version 2.25.0
%define gtk2_version 2.20.0
%define dbus_version 1.0
%define gcrypt_version 1.2.2
%define libtasn1_version 0.3.4

Summary: 	Framework for managing passwords and other secrets
Name: 		mate-keyring
Version: 	1.3.0
Release: 	1%{?dist}
License: 	GPLv2+ and LGPLv2+
Group: 		System Environment/Libraries
Source: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
URL: 		http://pub.mate-desktop.org

# why is gnome-keyring-daemon setuid root?
# https://bugzilla.redhat.com/show_bug.cgi?id=668831
Patch4: file-caps.patch

# gnome keyring pam module is starting gnome-keyring with the wrong SELinux context.
# https://bugzilla.redhat.com/show_bug.cgi?id=684225
Patch5: gnome-keyring-2.91.93-pam-selinux.patch


BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: libgcrypt-devel >= %{gcrypt_version}
BuildRequires: libtasn1-devel >= %{libtasn1_version}
BuildRequires: pam-devel
BuildRequires: libtool
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libtasn1-tools
BuildRequires: libmatekeyring-devel
BuildRequires: gtk-doc
BuildRequires: mate-common
BuildRequires: libcap-ng-devel
BuildRequires: libselinux-devel

# for smooth transition since the core was split
Requires: libmatekeyring

%description
The mate-keyring session daemon manages passwords and other types of
secrets for the user, storing them encrypted with a main password.
Applications can use the mate-keyring library to integrate with the keyring.

%package devel
Summary: Development files for mate-keyring
License: LGPLv2+
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: glib2-devel
# for smooth transition since the core was split
Requires: libmatekeyring-devel

%description devel
The mate-keyring-devel package contains the libraries and
header files needed to develop applications that use mate-keyring.

%package pam
Summary: Pam module for unlocking keyrings
License: LGPLv2+
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# for /lib64/security
Requires: pam

%description pam
The mate-keyring-pam package contains a pam module that can
automatically unlock the "login" keyring when the user logs in.


%prep
%setup -q -n mate-keyring-%{version}
%patch4 -p1 -b .file-caps
%patch5 -p1 -b .pam-selinux
NOCONFIGURE=1 ./autogen.sh

%build
autoreconf -i -f

%configure --disable-gtk-doc \
           --with-pam-dir=/%{_lib}/security \
           --enable-pam \
           --with-gtk=2.0 \

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_lib}/security/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
rm $RPM_BUILD_ROOT%{_libdir}/mate-keyring/devel/*.la
rm $RPM_BUILD_ROOT%{_libdir}/mate-keyring/standalone/*.la

%find_lang mate-keyring

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas


%files -f mate-keyring.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README COPYING COPYING.LIB
# LGPL
%{_libdir}/lib*.so.*
%dir %{_libdir}/mate-keyring
%dir %{_libdir}/mate-keyring/devel
%{_libdir}/mate-keyring/devel/*.so
%{_libdir}/mate-keyring/standalone/gkm-secret-store-standalone.so
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/*.so
# GPL
%attr(0755,root,root) %caps(cap_ipc_lock=ep) %{_bindir}/mate-keyring-daemon
%{_bindir}/mate-keyring
%{_libexecdir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/mategcr
%{_datadir}/mate-keyring
%{_sysconfdir}/xdg/autostart/*
%{_datadir}/MateConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%files devel
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%doc %{_datadir}/gtk-doc

%files pam
%defattr(-, root, root)
/%{_lib}/security/pam_mate_keyring.so


%changelog
* Fri May 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.3.0-1
- update to version 1.3.0

* Thu Mar 15 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to version 1.2.1

* Tue Feb 28 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2.0

* Thu Feb 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- fixed build error for i686

* Mon Jan 30 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- fixed rpmbuild directory error

* Mon Jan 30 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct pam path

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on gnome-keyring-2.32.0-1.fc14 spec

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

