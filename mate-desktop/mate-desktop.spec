%define po_package mate-desktop-2.0

Summary: 	Shared code among gnome-panel, gnome-session, nautilus, etc
Name: 		mate-desktop
Version: 	1.4.1
Release: 	2%{?dist}
URL: 		http://pub.mate-desktop.org
Source0: 	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

License: 	GPLv2+ and LGPLv2+
Group: 		System Environment/Libraries

Requires: 	redhat-menus
Requires: 	pycairo
Requires: 	pygtk2

BuildRequires: mate-common
BuildRequires: libxml2-devel
BuildRequires: gtk2-devel
BuildRequires: glib2-devel
BuildRequires: libmateui-devel
BuildRequires: libmatecanvas-devel
BuildRequires: startup-notification-devel
BuildRequires: mate-doc-utils
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: libtool

# Upstream fixes
Patch0: 0001-bgo-629168-Don-t-read-past-the-end-of-a-string-mate.patch
Patch1: 0001-Fix-possible-double-free-when-destroying-private-win.patch
Patch2: mate-desktop_remove_mate-bg-crossfade.patch

%description
The mate-desktop package contains an internal library
(libmatedesktop) used to implement some portions of the MATE
desktop, and also some data files and other shared components of the
MATE user environment.

%package devel
Summary: Libraries and headers for libmate-desktop
License: LGPLv2+
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.

%prep
%setup -q
%patch0 -p1 -b .pnp
%patch1 -p1 -b .double-free
%patch2 -p1 -b .mate-desktop_remove_mate-bg-crossfade
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-libtool-lock	\
	--disable-scrollkeeper    \
	--disable-static          \
	--with-pnp-ids-path="/usr/share/hwdata/pnp.ids" \

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# stuff we don't want
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper


mkdir $RPM_BUILD_ROOT%{_datadir}/omf/mate
mv -f $RPM_BUILD_ROOT%{_datadir}/omf/fdl $RPM_BUILD_ROOT%{_datadir}/omf/mate
mv -f $RPM_BUILD_ROOT%{_datadir}/omf/gpl $RPM_BUILD_ROOT%{_datadir}/omf/mate
mv -f $RPM_BUILD_ROOT%{_datadir}/omf/lgpl $RPM_BUILD_ROOT%{_datadir}/omf/mate

%find_lang %{po_package} --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_datadir}/applications/mate-about.desktop
%doc %{_mandir}/man*/*
# GPL
%{_bindir}/mate-about
# LGPL
%{_libdir}/lib*.so.*
%{_datadir}/mate/help/*/*/*.xml
%{_datadir}/omf/mate/*
%{_datadir}/mate-about/mate-version.xml

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%doc %{_datadir}/gtk-doc


%changelog
* Tue Sep 11 2012 Derek Morton <dmorton@hostgator.com> - 1.4.1.-2
- remove reference to mate-desktop_remove_nyan-cat.patch in Patch lines

* Thu Jul 20 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-1
- remove mate-desktop_remove_nyan-cat.patch, nyan-cat is removed from source

* Thu Jul 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0
- disable nyan cat

* Sun May 27 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-4
- add mate-desktop_remove_mate-bg-crossfade.patch

* Mon Apr 30 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-3
- switch back to mate original source

* Thu Apr 24 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-2
- fix black background in mdm
- change source to https://github.com/NiceandGently/mate-desktop

* Thu Mar 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-1
- update to 1.2.0

* Sat Feb 18 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-3
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-2
- added fedora patches 

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-desktop.spec based on gnome-desktop-2.32.0-9.fc16 spec

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-9
- Rebuilt for glibc bug#747377

