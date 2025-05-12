%define oname aMule
%global optflags %{optflags} -Wno-register

Summary:	File sharing client compatible with eDonkey
Name:		amule
Version:	2.4.0
Release:	8.git.20231116-1
License:	GPLv2+
Group:		Networking/File transfer
Url:		https://amule.org
#Source0:	https://sourceforge.net/projects/amule/files/aMule/%{version}/%{oname}-%{version}.tar.gz
# Use latest git, last release was done years ago and is broken and terrible to compile.
# Git from 2023-11-16, commit: e26d06a6eeaf37c716a88a47890cb85b931a0538
Source0:	https://github.com/amule-project/amule/archive/refs/heads/master.tar.gz
Source10:	%{name}-16.png
Source11:	%{name}-32.png
Source12:	%{name}-48.png
#Patch1:		125.patch
#Patch2:		amule-2.3.2-c++11.patch

BuildRequires:	bison
BuildRequires:  cmake
BuildRequires:	flex
BuildRequires:	desktop-file-utils
#BuildRequires:	boost-devel
BuildRequires:	binutils-devel
BuildRequires:	gd-devel >= 2.0
BuildRequires:	gettext-devel
BuildRequires:	readline-devel
# At some point we can switch to new wxgtk 3.1.X/3.2
BuildRequires:	wxgtku3.0-devel
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libupnp)
BuildRequires:	pkgconfig(ncurses)

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network. It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%files -f %{name}.lang
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
%{_bindir}/autostart-xas
%{_bindir}/fileview
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
%{_mandir}/*/man1/amuled.1.*
%{_mandir}/*/man1/xas.1.*
%{_mandir}/man1/xas.1.*

%post
update-alternatives --install %{_bindir}/ed2k ed2k %{_bindir}/ed2k-%{name} 5

%postun
update-alternatives --remove ed2k %{_bindir}/ed2k-%{name}

#----------------------------------------------------------------------------

%package commandline
Summary:	File sharing client compatible with eDonkey
Group:		Networking/File transfer
Requires:	amule = %{version}-%{release}

%description commandline
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the command line tool to control aMule remotely (or locally:).

%files commandline -f commandline.lang
%doc docs/README
%{_bindir}/%{name}cmd
%{_bindir}/alcc
%{_bindir}/amuled
%{_mandir}/man1/alcc.1*
%{_mandir}/man1/amulecmd.1*
%{_mandir}/man1/amuled.1*

#----------------------------------------------------------------------------

%package webserver
Summary:	File sharing client compatible with eDonkey
Group:		Networking/File transfer
Requires:	amule = %{version}-%{release}

%description webserver
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network.  It is a fork of xMule, whis was based on emule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

This is the webserver to control aMule remotely (or locally:).

%files webserver -f %{name}web.lang
%doc docs/README
%{_bindir}/%{name}web
%{_datadir}/amule/webserver/*
%{_mandir}/man1/amuleweb.1*

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-master

# fix SVN version tag name
sed -i -e 's|VERSION "GIT"|VERSION "%{version} GIT"|' CMakeLists.txt

sed -i 's|unset (\${CMAKE_REQUIRED_LIBRARIES})|#unset (\${CMAKE_REQUIRED_LIBRARIES})|' cmake/bfd.cmake

#find . -name "*.cpp" -o -name "*.c" |xargs sed -i -e 's,register ,,g'

%build
%cmake \
        	-DENABLE_BOOST=ON      \
	        -DBUILD_AMULECMD=ON    \
	        -DBUILD_REMOTEGUI=ON   \
	        -DBUILD_WEBSERVER=ON   \
	        -DBUILD_CAS=ON         \
	        -DBUILD_WXCAS=ON       \
	        -DBUILD_ALC=ON         \
	        -DBUILD_ALCC=ON        \
	        -DBUILD_DAEMON=ON      \
	        -DENABLE_IP2COUNTRY=ON \
	        -DBUILD_FILEVIEW=ON    \
	        -DBUILD_XAS=ON         
%make_build

%install
%make_install -C build
install -m 644 -D %{SOURCE10} %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 -D %{SOURCE11} %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 -D %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.png

# Fix wrong-script-end-of-line-encoding
perl -pi -e 's/\015$//' %{buildroot}%{_datadir}/doc/amule-%{version}/amule-win32.HOWTO.txt

mv %{buildroot}%{_bindir}/ed2k %{buildroot}%{_bindir}/ed2k-%{name}
rm -rf %{buildroot}%{_datadir}/doc/%{oname}-%{version}
rm -f %{buildroot}%{_libdir}/xchat/plugins/xas.pl

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# find_lang macro is different since 2012
%find_lang %{name} %{name}gui alc cas wxcas ed2k %{name}.lang --with-man
%find_lang alcc %{name}cmd commandline.lang --with-man
%find_lang %{name}web --with-man
