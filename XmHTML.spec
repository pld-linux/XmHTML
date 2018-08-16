# Note: upstream automake stuff is outdated, imake stuff outdated even more,
# plain Makefiles not outdated but messy.
# Use automake with some patches.
#
# Conditional build:
%bcond_without	xft	# Xft support

Summary:	Motif HTML widget
Summary(pl.UTF-8):	Widget do HTML-a oparty o Motif
Name:		XmHTML
Version:	1.1.10
Release:	2
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://downloads.sourceforge.net/xmhtml/%{name}-%{version}.tgz
# Source0-md5:	fd339d59d020da2ccf6e92bf65b810e2
Patch0:		%{name}-am.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-xft.patch
URL:		https://sourceforge.net/projects/xmhtml/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	motif-devel >= 1.2
%{?with_xft:BuildRequires:	xorg-lib-libXft-devel}
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XmHTML provides a widget capable of displaying HTML 3.2 conforming
text.

%description -l pl.UTF-8
XmHTML zawiera widget wyświetlający HTML w wersji 3.2.

%package devel
Summary:	Development package of XmHTML
Summary(pl.UTF-8):	Pliki nagłówkowe XmHTML
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	libpng-devel
Requires:	motif-devel >= 1.2
%{?with_xft:Requires:	xorg-lib-libXft-devel}

%description devel
Headers needed to compile XmHTML programs.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do kompilowania programów korzystających z
XmHTML.

%package static
Summary:	Static version of XmHTML library
Summary(pl.UTF-8):	Statyczna biblioteka XmHTML
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of XmHTML library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki XmHTML.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%{!?debug:CPPFLAGS="%{rpmcppflags} -DNDEBUG -Dproduction"}
%configure \
	%{?with_xft:--with-xft}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} html/man/man.{map,tmpl}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc APPS BUG-REPORTING CHANGES Changelog.txt DEBUGGING FEEDBACK FIXES LICENSE README THANKS TODO docs/{QUOTES,README.*,REASONS,progressive.txt}
%attr(755,root,root) %{_libdir}/libXmHTML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libXmHTML.so.0

%files devel
%defattr(644,root,root,755)
%doc html/*
%attr(755,root,root) %{_libdir}/libXmHTML.so
%{_libdir}/libXmHTML.la
%{_includedir}/XmHTML

%files static
%defattr(644,root,root,755)
%{_libdir}/libXmHTML.a
