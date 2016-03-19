%define major	1
%define libname	%mklibname paper %{major}
%define devname	%mklibname paper -d

Summary:	Library for handling paper characteristics
Name:		libpaper
Version:	1.1.24
Release:	18
License:	LGPLv2
Group:		System/Libraries
Url:		http://packages.debian.org/unstable/source/libpaper
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}.tar.gz
# consult also LC_PAPER env var before bluntly falling back to "letter" (#45804)
# https://bugzilla.redhat.com/show_bug.cgi?id=458833
Patch0:		libpaper-useglibcfallback.patch
Patch1:		libpaper-1.1.23-debianbug475683.patch
%ifarch x86_64
BuildRequires:	chrpath
%endif

%description
This package contains a simple library for use by programs needing
to handle papers. It lets program automatically recognize a lot of
different papers with their properties (actually their size).

%package -n	%{libname}
Summary:	Library for handling paper characteristics
Group:		System/Libraries

%description -n	%{libname}
Libraries for paper.

%package -n	%{devname}
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%package -n	paper-utils
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C

%description  -n paper-utils
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%prep
%setup -q
%apply_patches
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
touch NEWS AUTHORS
autoreconf -fi

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

# (tpg) this should close bug #31988
mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/papersize << EOF
# Simply write the paper name. See papersize(5) for possible values.
EOF

%ifarch x86_64
chrpath -d %{buildroot}%{_bindir}/paperconf
%endif

%files -n %{libname}
%{_libdir}/libpaper.so.%{major}*

%files -n %{devname}
%doc ChangeLog COPYING debian/changelog
%{_includedir}/*
%{_libdir}/*.so

%files -n paper-utils
%doc README
%config(noreplace) %{_sysconfdir}/papersize
%{_bindir}/paperconf
%{_sbindir}/paperconfig
%{_mandir}/man*/*

