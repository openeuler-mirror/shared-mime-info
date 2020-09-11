Name:	    shared-mime-info	
Version:	2.0
Release:	2
Summary:	Shared MIME information database
License:	GPLv2+
URL:		https://freedesktop.org/wiki/Software/shared-mime-info/

Source0:	http://gitlab.freedesktop.org/xdg/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Source1:        gnome-mimeapps.list
Source2:        totem-defaults.list
Source3:        file-roller-defaults.list
Source4:        eog-defaults.list

Patch0:     0001-Fix-pkg-config-installation-path.patch
Patch1:     0002-Update-compilation-instructions.patch

BuildRequires:	gcc libxml2-devel glib2-devel gettext intltool perl-XML-Parser meson itstool xmlto

%global __requires_exclude ^/usr/bin/pkg-config$

%description
The shared-mime-info package contains the core database of common types 
and the update-mime-database command used to extend it. It requires 
glib2 to be installed for building the update command. Additionally, it 
uses intltool for translations, though this is only a dependency for 
the maintainers.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1 

%build
#%%configure  --disable-silent-rules  --disable-update-mimedb
#make
%meson
%meson_build

%install
#PKGSYSTEM_ENABLE_FSYNC=0 \
#%%make_install
%meson_install

find $RPM_BUILD_ROOT%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find $RPM_BUILD_ROOT%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

install -d  $RPM_BUILD_ROOT%{_datadir}/applications
install -p -m 644 %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE2 >> $RPM_BUILD_ROOT%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE3 >> $RPM_BUILD_ROOT%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE4 >> $RPM_BUILD_ROOT%{_datadir}/applications/gnome-mimeapps.list

pushd $RPM_BUILD_ROOT%{_datadir}/applications
install -p -m 644 gnome-mimeapps.list mimeapps.list
popd

%check
%meson_test

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%transfiletriggerin -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%transfiletriggerpostun -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/update-mime-database
%{_datadir}/applications/*.list
%{_datadir}/mime/packages/*.org.xml
%{_datadir}/pkgconfig/shared-mime-info.pc
%{_datadir}/gettext/*
%exclude %{_datadir}/locale/*

%files help
%doc README.md  NEWS HACKING.md data/shared-mime-info-spec.xml
%{_mandir}/man1/*.gz

%changelog
* Thu Sep 10 2020 hanhui <hanhui15@huawei.com> - 2.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify source url

* Thu Jul 31 2020 chxssg<chxssg@qq.com> - 2.0-1
- Update to 2.0

* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.10-4
- Package init
