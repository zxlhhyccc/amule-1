%define		oname aMule

Name:		amule
Version:	2.3.1
Release:	%mkrel 1
Summary:	File sharing client compatible with eDonkey
License:	GPLv2+
Group:		Networking/File transfer
Source:		http://ovh.dl.sourceforge.net/sourceforge/amule/%{oname}-%{version}.tar.bz2
Source10:	%{name}-16.png
Source11:	%{name}-32.png
Source12:	%{name}-48.png
URL:		http://amule.org
Patch0:		aMule-2.3.1rc2-wxversion.patch
BuildRequires:	gd-devel >= 2.0
BuildRequires:	curl-devel
Buildrequires:	ncurses-devel
Buildrequires:	readline-devel
BuildRequires:	gettext-devel
Buildrequires:	desktop-file-utils
BuildRequires:	wxgtku-devel >= 2.8
BuildRequires:	libcryptopp-devel
BuildRequires:	libupnp-devel
BuildRequires:	libgeoip-devel
BuildRequires:	binutils-devel

Conflicts:	xmule < 1.6.0-2plf

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package	commandline
Summary:	File sharing client compatible with eDonkey
Group:		Networking/File transfer
Requires:	amule

%description	commandline
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the command line tool to control aMule remotely (or locally:).

%package	webserver
Summary:	File sharing client compatible with eDonkey
Group:		Networking/File transfer
Requires:	amule

%description	webserver
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the webserver to control aMule remotely (or locally:).

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1

%build
./autogen.sh
%configure2_5x \
--with-wx-config=%{_bindir}/wx-config-unicode\
		--enable-amulecmd \
		--enable-amule-gui \
		--enable-webserver\
		--disable-xas\
		--enable-cas\
		--enable-wxcas\
		--enable-alc\
		--enable-alcc \
		--disable-debug\
		--enable-amule-daemon \
		--enable-optimize \
		--enable-geoip
%make

%install
%__rm -rf %{buildroot}

%makeinstall_std
%__install -m 644 -D %{SOURCE10} %{buildroot}%{_miconsdir}/%{name}.png
%__install -m 644 -D %{SOURCE11} %{buildroot}%{_iconsdir}/%{name}.png
%__install -m 644 -D %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.png

# Fix wrong-script-end-of-line-encoding
perl -pi -e 's/\015$//' %{buildroot}%{_datadir}/doc/amule-%{version}/amule-win32.HOWTO.txt

%__mv %{buildroot}%{_bindir}/ed2k %{buildroot}%{_bindir}/ed2k-%{name}
%__rm -rf %{buildroot}%{_datadir}/doc/%{oname}-%{version}
%__rm -f %{buildroot}%{_libdir}/xchat/plugins/xas.pl

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# find_lang macro is different since 2012
%if %{mdvver} <= 201100
%find_lang %{name} %{name} %{name}gui alc cas wxcas ed2k --with-man
%find_lang commandline alcc %{name}cmd %{name}d --with-man
%else
%find_lang %{name} %{name}gui alc cas wxcas ed2k %{name}.lang --with-man
%find_lang alcc %{name}cmd %{name}d commandline.lang --with-man
%endif
%find_lang %{name}web --with-man


%clean
%__rm -rf %{buildroot}

%post
update-alternatives --install %{_bindir}/ed2k ed2k %{_bindir}/ed2k-%{name} 5

%postun
update-alternatives --remove ed2k %{_bindir}/ed2k-%{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc docs/*
%{_datadir}/applications/alc.desktop
%{_datadir}/applications/wxcas.desktop
%{_datadir}/pixmaps/alc.xpm
%{_datadir}/pixmaps/wxcas.xpm
%{_bindir}/amule
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
%{_mandir}/man1/alc.1*
%{_mandir}/man1/amule.1*
%{_mandir}/man1/amulegui.1*
%{_mandir}/man1/cas.1*
%{_mandir}/man1/ed2k.1*
%{_mandir}/man1/wxcas.1*

%files commandline -f commandline.lang
%defattr(-,root,root)
%doc docs/README
%{_bindir}/%{name}cmd
%{_bindir}/alcc
%{_bindir}/amuled
%{_mandir}/man1/alcc.1*
%{_mandir}/man1/amulecmd.1*
%{_mandir}/man1/amuled.1*

%files webserver -f %{name}web.lang
%defattr(-,root,root)
%doc docs/README
%{_bindir}/%{name}web
%{_datadir}/amule/webserver/*
%{_mandir}/man1/amuleweb.1*

