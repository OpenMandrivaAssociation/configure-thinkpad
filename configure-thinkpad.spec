%define name	configure-thinkpad
%define ver 	0.9
%define rel	%mkrel 4

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
BuildRequires:	ImageMagick desktop-file-utils

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
