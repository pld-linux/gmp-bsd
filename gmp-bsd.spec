#
# Conditional build:
%bcond_without	tests	# don't perform tests
#
Summary:	GNU arbitrary precision library - BSD-compatible MP library
Summary(pl.UTF-8):	Biblioteka arytmetyczna GNU - biblioteka MP kompatybilna z BSD
Name:		gmp-bsd
Version:	5.0.5
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/gmp/gmp-%{version}.tar.xz
# Source0-md5:	8aef50959acec2a1ad41d144ffe0f3b5
Patch0:		gmp-info.patch
Patch1:		gmp-multilib.patch
Patch2:		gmp-cpu.patch
Patch3:		gmp-tinfo.patch
Patch4:		gmp-am.patch
URL:		http://gmplib.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains BSD-compatible MP library based on GNU MP.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę MP kompatybilną z BSD opartą na GNU MP.

%package devel
Summary:	GNU arbitrary precision library - BSD-compatible MP API
Summary(pl.UTF-8):	Biblioteka arytmetyczna GNU - API MP kompatybilne z BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains BSD-compatible MP library header file.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy biblioteki MP kompatybilnej z BSD.

%package static
Summary:	GNU arbitrary precision library - BSD-compatible static MP library
Summary(pl.UTF-8):	Biblioteka arytmetyczna GNU - biblioteka statyczna MP kompatybilna z BSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains BSD-compatible MP static library based on GNU
MP.

%description static -l pl.UTF-8
Ten pakiet zawiera bibliotekę statyczną MP kompatybilną z BSD opartą
na GNU MP.

%prep
%setup -q -n gmp-%{version}
%patch -P0 -p1
%ifarch %{ix86} %{x8664} ppc ppc64 s390 s390x sparc sparcv9 sparc64
# ugly hack, don't apply on other archs (also recheck sizes on each upgrade)
%patch -P1 -p1
%endif
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-cpu=%{_target_cpu} \
	--enable-fft \
	--enable-mpbsd

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgmp.* \
	$RPM_BUILD_ROOT%{_includedir}/gmp.h \
	$RPM_BUILD_ROOT%{_infodir}/gmp.info*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmp.so
%{_libdir}/libmp.la
%{_includedir}/mp.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmp.a
