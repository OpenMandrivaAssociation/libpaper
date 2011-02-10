%define major 1
%define libname %mklibname paper %{major}
%define develname %mklibname paper -d
%define staticdevelname %mklibname paper -d -s

Summary:	Library for handling paper characteristics
Name:		libpaper
Version:	1.1.24
Release:	%mkrel 1
License:	LGPL
Group:		System/Libraries
URL:		http://packages.debian.org/unstable/source/libpaper
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}.tar.gz
# consult also LC_PAPER env var before bluntly falling back to "letter" (#45804)
# https://bugzilla.redhat.com/show_bug.cgi?id=458833
Patch0:		libpaper-useglibcfallback.patch
Patch1:		libpaper-1.1.23-debianbug475683.patch
%ifarch x86_64
BuildRequires:	chrpath
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package contains a simple library for use by programs needing
to handle papers. It lets program automatically recognize a lot of
different papers with their properties (actually their size).

%package -n	%{libname}
Summary:	Library for handling paper characteristics
Group:		System/Libraries

%description -n	%{libname}
Libraries for paper.

%package -n	%{develname}
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Provides:	libpaper-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname paper 1 -d
Provides:	%mklibname paper 1 -d

%description -n	%{develname}
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%package -n	%{staticdevelname}
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Obsoletes:	%mklibname paper 1 -d -s

%description -n %{staticdevelname}
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%package -n	paper-utils
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description  -n paper-utils
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%prep
%setup -q -n libpaper-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure2_5x
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# (tpg) this should close bug #31988
mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/papersize << EOF
# Simply write the paper name. See papersize(5) for possible values.
EOF

%ifarch x86_64
chrpath -d %{buildroot}%{_bindir}/paperconf
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog COPYING debian/changelog
%_includedir/*
%{_libdir}/*.so
%{_libdir}/*.la

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/*.a

%files -n paper-utils
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/papersize
%{_bindir}/paperconf
%{_sbindir}/paperconfig
%{_mandir}/man*/*
