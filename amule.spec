%define subver rc2
%define name amule
%define version 2.3.1
%define release %mkrel 0.%{subver}
%define oname aMule

Summary: File sharing client compatible with eDonkey
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2+
Group: Networking/File transfer

Source:	http://ovh.dl.sourceforge.net/sourceforge/amule/%{oname}-%{version}%{subver}.tar.bz2
Source10: %{name}-16.png
Source11: %{name}-32.png
Source12: %{name}-48.png
#gw in 2011.0, the segv handler is disabled. Add the missing preprocessor
# stuff to fix the build
#Patch0: aMule-2.2.6-fix-build-without-wx-segv-handler.patch
URL: http://amule.org
BuildRoot: %{_tmppath}/%{name}-buildroot
Patch0: aMule-2.3.1rc2-wxversion.patch
BuildRequires: gd-devel >= 2.0
BuildRequires: curl-devel
Buildrequires: ncurses-devel
Buildrequires: readline-devel
BuildRequires: gettext-devel
Buildrequires: desktop-file-utils
BuildRequires: libwxgtku-devel >= 2.8
BuildRequires: libcryptopp-devel
BuildRequires: libupnp-devel
BuildRequires: libgeoip-devel
BuildRequires: binutils-devel

Conflicts: xmule < 1.6.0-2plf

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package commandline
Summary: File sharing client compatible with eDonkey
Group: Networking/File transfer
Requires: amule

%description commandline
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the command line tool to control aMule remotely (or locally:).

%package webserver
Summary: File sharing client compatible with eDonkey
Group: Networking/File transfer
Requires: amule

%description webserver
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the webserver to control aMule remotely (or locally:).

%prep
%setup -q -n %{oname}-%{version}%{subver}
%patch0 -p1
#apply_patches

%build
./autogen.sh
%configure2_5x \
--with-wx-config=%{_bindir}/wx-config-unicode\
               --enable-amulecmd \
               --enable-amulecmdgui\
	       --enable-amule-gui \
               --enable-webserver\
               --enable-webservergui\
               --disable-gsocket\
               --disable-xas\
	       --enable-cas\
	       --enable-wxcas\
 	       --enable-alc\
               --enable-alcc \
               --enable-embedded_crypto\
               --disable-debug\
               --enable-utf8-systray\
	       --enable-amule-daemon \
	       --enable-optimize \
	       --enable-geoip
%make

%install
rm -rf %{buildroot}

%makeinstall_std
rm -rf %{buildroot}%{_datadir}/locale/ee/LC_MESSAGES/amule.mo
%find_lang %{name}
%find_lang %{name}gui
install -m 644 -D %{SOURCE10} %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 -D %{SOURCE11} %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 -D %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.png
mkdir -p %{buildroot}%{_menudir}

# Fix wrong-script-end-of-line-encoding
perl -pi -e 's/\015$//' %{buildroot}%{_datadir}/doc/amule-%{version}/amule-win32.HOWTO.txt


rm -f %{buildroot}%{_datadir}/doc/amule-%{version}/man/.cvsignore

mv %{buildroot}%{_bindir}/ed2k %{buildroot}%{_bindir}/ed2k-%{name}
rm -rf %{buildroot}%{_datadir}/doc/%{oname}-%{version}
rm -f %{buildroot}%{_libdir}/xchat/plugins/xas.pl

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*


%clean
rm -rf %{buildroot}

%post
%{update_menus}
update-alternatives --install %{_bindir}/ed2k ed2k %{_bindir}/ed2k-%{name} 5

%postun
%{clean_menus}
update-alternatives --remove ed2k %{_bindir}/ed2k-%{name}
%files -f %{name}.lang
%defattr(-,root,root)
%doc docs/* 
%{_datadir}/applications/alc.desktop
%{_datadir}/applications/wxcas.desktop
%{_datadir}/pixmaps/alc.xpm
%{_datadir}/pixmaps/wxcas.xpm
%{_bindir}/amule
#{_bindir}/autostart-xas
%{_bindir}/amulegui
%{_bindir}/wxcas
%{_bindir}/cas
%{_bindir}/ed2k-amule
%{_bindir}/alc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/skins
%{_datadir}/applications/amule.desktop
%{_datadir}/applications/amulegui.desktop
%{_datadir}/pixmaps/amule.xpm
%{_datadir}/pixmaps/amulegui.xpm
%{_datadir}/cas
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%lang(de) %{_mandir}/de/man1/alc.1*
%lang(es) %{_mandir}/es/man1/alc.1*
#lang(eu) %{_mandir}/eu/man1/alc.1*
%lang(fr) %{_mandir}/fr/man1/alc.1*
%lang(hu) %{_mandir}/hu/man1/alc.1*
%lang(it) %{_mandir}/it/man1/alc.1*
%lang(ru) %{_mandir}/ru/man1/alc.1*
%{_mandir}/man1/alc.1*
%lang(de) %{_mandir}/de/man1/amule.1*
%lang(es) %{_mandir}/es/man1/amule.1*
#lang(eu) %{_mandir}/eu/man1/amule.1*
%lang(fr) %{_mandir}/fr/man1/amule.1*
%lang(hu) %{_mandir}/hu/man1/amule.1*
%lang(it) %{_mandir}/it/man1/amule.1*
%lang(ru) %{_mandir}/ru/man1/amule.1*
%lang(de) %{_mandir}/de/man1/amulegui.1*
%lang(es) %{_mandir}/es/man1/amulegui.1*
%lang(fr) %{_mandir}/fr/man1/amulegui.1*
%lang(hu) %{_mandir}/hu/man1/amulegui.1*
%lang(it) %{_mandir}/it/man1/amulegui.1*
%lang(ru) %{_mandir}/ru/man1/amulegui.1*
%{_mandir}/de/man1/cas.1*
%lang(es) %{_mandir}/es/man1/cas.1*
%lang(fr) %{_mandir}/fr/man1/cas.1*
#lang(eu) %{_mandir}/eu/man1/cas.1*
%lang(hu) %{_mandir}/hu/man1/cas.1*
%lang(it) %{_mandir}/it/man1/cas.1*
%lang(ru) %{_mandir}/ru/man1/cas.1*
%lang(de) %{_mandir}/de/man1/ed2k.1*
%lang(es) %{_mandir}/es/man1/ed2k.1*
#lang(eu) %{_mandir}/eu/man1/ed2k.1*
%lang(fr) %{_mandir}/fr/man1/ed2k.1*
%lang(hu) %{_mandir}/hu/man1/ed2k.1*
%lang(it) %{_mandir}/it/man1/ed2k.1*
%lang(ru) %{_mandir}/ru/man1/ed2k.1*
%lang(de) %{_mandir}/de/man1/wxcas.1*
%lang(es) %{_mandir}/es/man1/wxcas.1*
#lang(eu) %{_mandir}/eu/man1/wxcas.1*
%lang(fr) %{_mandir}/fr/man1/wxcas.1*
%lang(hu) %{_mandir}/hu/man1/wxcas.1*
%lang(it) %{_mandir}/it/man1/wxcas.1*
%lang(ru) %{_mandir}/ru/man1/wxcas.1*
#lang(de) %{_mandir}/de/man1/xas.1*
#lang(es) %{_mandir}/es/man1/xas.1*
#lang(hu) %{_mandir}/hu/man1/xas.1*
#lang(eu) %{_mandir}/eu/man1/xas.1*
%{_mandir}/man1/amule.1*
%{_mandir}/man1/amulegui.1*
%{_mandir}/man1/cas.1*
%{_mandir}/man1/ed2k.1*
%{_mandir}/man1/wxcas.1*
#{_mandir}/man1/xas.1*

%files commandline
%defattr(-,root,root)
%doc docs/README
%{_bindir}/%{name}cmd
%{_bindir}/alcc
%{_bindir}/amuled
%lang(de) %{_mandir}/de/man1/alcc.1*
%lang(es) %{_mandir}/es/man1/alcc.1*
#lang(eu) %{_mandir}/eu/man1/alcc.1*
%lang(fr) %{_mandir}/fr/man1/alcc.1*
%lang(it) %{_mandir}/it/man1/alcc.1*
%lang(ru) %{_mandir}/ru/man1/alcc.1*
%{_mandir}/man1/alcc.1*
%lang(hu) %{_mandir}/hu/man1/alcc.1*
%lang(de) %{_mandir}/de/man1/amulecmd.1*
%lang(es) %{_mandir}/es/man1/amulecmd.1*
#lang(eu) %{_mandir}/eu/man1/amulecmd.1*
%lang(fr) %{_mandir}/fr/man1/amulecmd.1*
%lang(hu) %{_mandir}/hu/man1/amulecmd.1*
%lang(it) %{_mandir}/it/man1/amulecmd.1*
%lang(ru) %{_mandir}/ru/man1/amulecmd.1*
%{_mandir}/man1/amulecmd.1*
%lang(de) %{_mandir}/de/man1/amuled.1*
%lang(es) %{_mandir}/es/man1/amuled.1*
#lang(eu) %{_mandir}/eu/man1/amuled.1*
%lang(fr) %{_mandir}/fr/man1/amuled.1*
%lang(hu) %{_mandir}/hu/man1/amuled.1*
%lang(it) %{_mandir}/it/man1/amuled.1*
%lang(ru) %{_mandir}/ru/man1/amuled.1*
%{_mandir}/man1/amuled.1*

%files webserver
%defattr(-,root,root)
%doc docs/README
%{_bindir}/%{name}web
%{_datadir}/amule/webserver/*
%lang(de) %{_mandir}/de/man1/amuleweb.1*
%lang(es) %{_mandir}/es/man1/amuleweb.1*
#lang(eu) %{_mandir}/eu/man1/amuleweb.1*
%lang(fr) %{_mandir}/fr/man1/amuleweb.1*
%lang(hu) %{_mandir}/hu/man1/amuleweb.1*
%lang(it) %{_mandir}/it/man1/amuleweb.1*
%lang(ru) %{_mandir}/ru/man1/amuleweb.1*
%{_mandir}/man1/amuleweb.1*

