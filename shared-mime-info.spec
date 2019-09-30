Name:	        shared-mime-info	
Version:	1.10
Release:	4
Summary:	Shared MIME information database
License:	GPLv2+
URL:		https://freedesktop.org/wiki/Software/shared-mime-info/

Source0:	http://freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Source1:        gnome-mimeapps.list
Source2:        totem-defaults.list
Source3:        file-roller-defaults.list
Source4:        eog-defaults.list

Patch0:         0001-Remove-sub-classing-from-OO.o-mime-types.patch
Patch6001:      Fix-potential-fd-leak-on-error-in-sync_file.patch
Patch6002:      Fix-potential-memleak-in-parse_string_mask.patch
Patch6003:      Fix-memleak-in-write_data.patch

BuildRequires:	gcc libxml2-devel glib2-devel gettext intltool perl-XML-Parser

%global __requires_exclude ^/usr/bin/pkg-config$

%description
The shared-mime-info package contains the core database of common types 
and the update-mime-database command used to extend it. It requires 
glib2 to be installed for building the update command. Additionally, it 
uses intltool for translations, though this is only a dependency for 
the maintainers.

%package_help

%prep
%autosetup -n %{name}-%{version} 

%build
%configure  --disable-silent-rules  --disable-update-mimedb
make

%install
PKGSYSTEM_ENABLE_FSYNC=0 \
%make_install

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
%exclude %{_datadir}/locale/*

%files help
%doc README NEWS HACKING shared-mime-info-spec.xml
%{_mandir}/man1/*.gz

%changelog
* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.10-4
- Package init
