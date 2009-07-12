Summary:	Motif HTML widget
Summary(pl.UTF-8):	Widget do HTML-a oparty o Motif
Name:		XmHTML
Version:	1.1.7
Release:	8
License:	LGPL
Group:		X11/Libraries
Source0:	http://www.xs4all.nl/~ripley/XmHTML/dist/%{name}-%{version}.tar.gz
# Source0-md5:	6d079435fb954bb7878f4dd0d3f7b8d8
Patch0:		%{name}-am.patch
Patch1:		%{name}-macro.patch
URL:		http://www.xs4all.nl/~ripley/XmHTML/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	motif-devel >= 1.2
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

%build
# Argh! automake stuff outdated, imake stuff outdated even more,
# makefiles not outdated but don't support shared libraries :/
# Use automake with some patches/workarounds/etc
cd lib
mv -f common/*.c .
mv -f Motif/*.c .
cd ..

%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CFLAGS="%{rpmcflags} \
	-I`pwd`/include/XmHTML -I`pwd`/include/common \
	%{!?debug:-DNDEBUG -Dproduction} -DVERSION=1107"
%configure

cd lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/XmHTML

%{__make} install -C lib \
	DESTDIR=$RPM_BUILD_ROOT

install include/XmHTML/{Balloon,HTML,HTMLStrings,XCC,XmHTML}.h \
	include/common/LZWStream.h \
	$RPM_BUILD_ROOT%{_includedir}/XmHTML

rm -f html/man/man.{map,tmpl}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc APPS BUG-REPORTING CHANGES DEBUGGING FEEDBACK FIXES
%doc README THANKS TODO docs/{QUOTES,README.*,REASONS,progressive.txt}
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc html/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/XmHTML

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
