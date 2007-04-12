%define major 1
%define raw_name paper
%define fname lib%{raw_name}
%define libname %mklibname %{raw_name} %{major}

Summary:	Library for handling paper characteristics
Name:		%{fname}
Version:	1.1.21
Release:	%mkrel 1
License:	LGPL
Group:		System/Libraries
URL:		http://packages.debian.org/unstable/source/libpaper
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{fname}_%{version}.tar.gz
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

%package -n	%{libname}-devel
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Provides:	libpaper-devel = %{version}-%{release}
Obsoletes:	libpaper-devel
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%package -n	%{libname}-static-devel
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
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

%build
%configure2_5x
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%ifarch x86_64
chrpath -d %{buildroot}%{_bindir}/paperconf
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{libname}-devel
%defattr(644,root,root,755)
%doc ChangeLog debian/changelog
%_includedir/*
%{_libdir}/*.so
%{_libdir}/*.la

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
%{_libdir}/*.a

%files -n paper-utils
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/paperconf
%attr(755,root,root) %{_sbindir}/paperconfig
%{_mandir}/man*/*


