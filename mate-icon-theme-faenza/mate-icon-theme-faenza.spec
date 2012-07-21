Name:           mate-icon-theme-faenza
Version:        1.4.0
Release:        1%{?dist}
Summary:        faenza-theme for MATE

Group:          User Interface/Desktops
License:        GPL
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: 		noarch

BuildRequires:  mate-common

%description
This icon theme uses Faenza and Faience icon themes by ~Tiheum and
some icons customized for MATE by Rowen Stipe.


%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/matefaenza &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/matefaenza &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/matefaenza &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/matefaenza &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/icons/matefaenza
%{_datadir}/icons/matefaenzadark

%changelog
* Tue Jul 18 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0
- add rpm scriplet commands

* Fri Jun 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.3.1-1
- update to 1.3.1

* Mon May 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.3.0-1
- Initial package


