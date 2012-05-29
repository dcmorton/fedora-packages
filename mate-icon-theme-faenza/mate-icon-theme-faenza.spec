Name:           mate-icon-theme-faenza
Version:        1.3.0
Release:        1%{?dist}
Summary:        faenza-theme for MATE

Group:          User Interface/Desktops
License:        GPL
URL:            https://github.com/mate-desktop/mate-icon-theme-faenza
Source0:        %{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: 		noarch

%description
This icon theme uses Faenza and Faience icon themes by ~Tiheum and
some icons customized for MATE by Rowen Stipe.


%prep
%setup -q

%build
# there is no build necessary

%install
rm -rf $RPM_BUILD_ROOT
install -d -p %{buildroot}%{_datadir}/icons
cp -rf $RPM_BUILD* %{buildroot}%{_datadir}/icons
mv %{buildroot}%{_datadir}/icons/AUTHORS %{buildroot}%{_datadir}/icons/matefaenza/AUTHORS
mv %{buildroot}%{_datadir}/icons/README %{buildroot}%{_datadir}/icons/matefaenza/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/icons/matefaenza

%changelog
* Mon May 28 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.3.0-1
- Initial package


