%define name	configure-thinkpad
%define ver 	0.9
%define rel	%mkrel 6

Name:		%{name}
Version:	%{ver}
Release:	%{rel}
Summary:	Utility to configure IBM Thinkpad behaviour
URL:		http://tpctl.sourceforge.net/configure-thinkpad.html
License:	GPL
Group:		System/Configuration/Hardware
Source:		http://prdownloads.sourceforge.net/tpctl/%{name}-%{version}.tar.bz2
Patch0:		configure-thinkpad-fix-desktop-entry.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	imagemagick desktop-file-utils

%description
Utility to configure IBM Thinkpad behaviour.

Currently, mainly power management features are supported.

%prep
%setup -q
%patch0 -p0

%build
%configure
%make

%install
rm -Rf %{buildroot}
%makeinstall_std


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Settings;HardwareSettings" \
  --add-category="X-MandrivaLinux-System-Configuration-Hardware" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -resize 48x48 pixmaps/gnome-laptop.png %{buildroot}/%{_liconsdir}/%{name}.png
convert -resize 32x32 pixmaps/gnome-laptop.png %{buildroot}/%{_iconsdir}/%{name}.png
convert -resize 16x16 pixmaps/gnome-laptop.png %{buildroot}/%{_miconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%update_menus
%endif

modulesconf=/etc/modules.conf
if ! `grep -q "/dev/thinkpad" $modulesconf` ; then
        echo "adding entry for /dev/thinkpad/* to your $modulesconf"
        cat >> $modulesconf << EOF
#Added by %{name} to autoload thinkpad drivers
#path[thinkpad]=/lib/modules/`uname -r`/thinkpad
#options thinkpad enable_smapi=1 enable_superio=1 enable_rtcmosram=1 enable_thinkpadpm=1
alias char-major-10-170 thinkpad
alias /dev/thinkpad thinkpad
alias /dev/thinkpad/thinkpad thinkpad
alias /dev/thinkpad/smapi smapi
alias /dev/thinkpad/superio superio
alias /dev/thinkpad/rtcmosram rtcmosram
alias /dev/thinkpad/thinkpadpm thinkpadpm

EOF
fi

consoleperms=/etc/security/console.perms
if ! `grep -q "/dev/thinkpad" $consoleperms` ; then
        echo "adding entry for /dev/thinkpad/* to your $consoleperms"
        cat >> $consoleperms << EOF

# Added by %{name} to allow user access to thinkpad devices
<console>  0600 /dev/thinkpad/*   0600 root

EOF
fi

# We don't remove the additions to modules.conf and console.perms since
# some other package (ie tpctl) may want them ...

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop

%doc AUTHORS


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9-6mdv2011.0
+ Revision: 617411
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.9-5mdv2010.0
+ Revision: 424940
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.9-4mdv2009.0
+ Revision: 222018
- patch 0: fix 'error: value "configure-thinkpad/gnome-laptop.png" for key
  "Icon" in group "Desktop Entry" looks like a relative path, instead of being
  an absolute path to an icon or an icon name'
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - cleanup %%postun

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Gustavo De Nardin <gustavodn@mandriva.com>
    - Import configure-thinkpad



* Tue Sep 12 2006 Emmanuel Andry <eandry@mandriva.org> 0.9-3mdv2007.0
- add buildrequires desktop-file-utils

* Tue Sep 12 2006 Emmanuel Andry <eandry@mandriva.org> 0.9-2mdv2007.0
- %%mkrel
- xdg menu

* Mon Mar 21 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.9-1mdk
- from Emmanuel Andry <eandry@free.fr> : 
	- 0.9
* Tue Aug 24 2004 Erwan Velu <erwan@mandrakesoft.com> 0.3-1mdk
- 0.3
* Tue Dec 23 2003 Buchan Milne <bgmilne@linux-mandrake.com> 0.1-1mdk
- First Mandrake package
- We need a better solution for the thinkpad device files ...
