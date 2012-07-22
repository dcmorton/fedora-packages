%define pygtk2_version 2.24.0

Summary: 		Dropbox extension for caja
Name: 			caja-dropbox
Version: 		0.7.1
Release: 		4%{?dist}
License: 		GNU
Group: 			User Interface/Desktops
URL: 			http://pub.mate-desktop.org
Source: 		http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires: 	gtk2-devel
BuildRequires: 	glib2-devel
BuildRequires: 	caja-devel
BuildRequires: 	caja-extensions
BuildRequires: 	mate-vfs-devel
BuildRequires: 	pygtk2-devel >= %{pygtk2_version}
BuildRequires: 	pygtk2 >= %{pygtk2_version}
BuildRequires: 	python-docutils
BuildRequires: 	ImageMagick
BuildRequires: 	libmatenotify-devel
BuildRequires:  mate-common
BuildRequires:  xorg-x11-server-utils
BuildRequires:  python-docutils
BuildRequires:  python-devel 

Requires: 		caja
Requires: 		glib2
Requires: 		gtk2
Requires: 		libmatenotify
Requires: 		mate-vfs
Requires: 		pygtk2
Requires: 		python-docutils

%description
Dropbox extension for caja
Dropbox allows you to sync your files online and across your computers automatically.

%prep
%setup -q -n %{name}-%{version}
NOCONFIGURE=1 ./autogen.sh

%build
export DISPLAY=:0.0
xhost +
%configure


make %{?_smp_mflags}
# resize icons
for icon in emblem-dropbox-syncing.png emblem-dropbox-unsyncable.png emblem-dropbox-uptodate.png
do
	convert data/emblems/$icon -resize 16x data/emblems/$icon
done

%install
DESTDIR=$RPM_BUILD_ROOT make install
libtool --finish %{_libdir}/caja/extensions-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README 
%{_bindir}/dropbox
%{_datadir}/caja-dropbox
%{_datadir}/icons
%{_mandir}/man1/dropbox.*
%{_datadir}/applications/dropbox.desktop
%{_libdir}/caja/extensions-2.0/libcaja-dropbox.*

%changelog
* Thu Jul 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.7.1-4
- switch to Mate-Desktop source

* Thu Feb 23 2012 Wolfgang Ulbrich <info@raveit.de> - 0.7.1-3
- fixed build error for i686

* Mon Feb 13 2012 Wolfgang Ulbrich <info@raveit.de> - 0.7.1-2
-- rebuild for enable builds for .i686

* Thu Jan 19 2012 Wolfgang Ulbrich <info@raveit.de> - 0.7.1-1
- start building for caja   

* Fri Oct 8 2010 Thomas Uphill <uphill@ias.edu> 0.6.3-3
- wrapper to download appropriate binary

