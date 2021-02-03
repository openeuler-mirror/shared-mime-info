Name:	    shared-mime-info	
Version:	2.1
Release:	1
Summary:	Shared MIME information database
License:	GPLv2+
URL:		https://freedesktop.org/wiki/Software/shared-mime-info/

Source0:	https://gitlab.freedesktop.org/xdg/shared-mime-info/uploads/0ee50652091363ab0d17e335e5e74fbe/shared-mime-info-2.1.tar.xz
Source1:    mimeapps.list

Patch0:     0001-Remove-sub-classing-from-OO.o-mime-types.patch

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
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/applications/mimeapps.list



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
* Mon Feb 1 2021 jinzhimin <jinzhimin2@huawei.com> - 2.1-1
- Upgrade to 2.1

* Thu Sep 10 2020 hanhui <hanhui15@huawei.com> - 2.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify source url

* Thu Jul 31 2020 chxssg<chxssg@qq.com> - 2.0-1
- Update to 2.0

* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.10-4
- Package init
