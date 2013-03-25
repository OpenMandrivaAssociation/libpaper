%define major 1
%define libname %mklibname paper %{major}
%define develname %mklibname paper -d
%define staticdevelname %mklibname paper -d -s

Summary:	Library for handling paper characteristics
Name:		libpaper
Version:	1.1.24
Release:	4
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

%description -n	%{develname}
This package contains the development files for a simple library for use
by programs needing to handle papers. It lets program automatically
recognize a lot of different papers with their properties (actually their
size).

%package -n	%{staticdevelname}
Summary:	Library for handling paper characteristics (development files)
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}

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
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
touch NEWS AUTHORS
libtoolize --copy --force
autoreconf -fi
%configure2_5x
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
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc ChangeLog COPYING debian/changelog
%{_includedir}/*
%{_libdir}/*.so

%files -n %{staticdevelname}
%{_libdir}/*.a

%files -n paper-utils
%doc README
%config(noreplace) %{_sysconfdir}/papersize
%{_bindir}/paperconf
%{_sbindir}/paperconfig
%{_mandir}/man*/*

%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.24-2mdv2011.0
+ Revision: 662393
- mass rebuild

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 1.1.24-1
+ Revision: 637177
- new version 1.1.24
- sync with fedora's patches

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.23-6mdv2011.0
+ Revision: 602595
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.23-5mdv2010.1
+ Revision: 520897
- rebuilt for 2010.1

* Tue Oct 20 2009 Gustavo De Nardin <gustavodn@mandriva.com> 1.1.23-4mdv2010.0
+ Revision: 458482
- consult also LC_PAPER env var before bluntly falling back to "letter" (#45804)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.1.23-3mdv2010.0
+ Revision: 425687
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.1.23-2mdv2009.0
+ Revision: 222960
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 27 2008 Funda Wang <fwang@mandriva.org> 1.1.23-1mdv2008.1
+ Revision: 158853
- update to new version 1.1.23

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Aug 15 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.22-1mdv2008.0
+ Revision: 63691
- fix bug #31988
- new devel library policy
- spec file clean
- new version


* Thu Feb 15 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.21-1mdv2007.0
+ Revision: 121263
- bump version
- fix url
- make use of %%{major} and ldconfig for libraries
- add clean routines in %%install
- Import libpaper

* Tue Mar 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.1.8-8mdk
- fix summary (#21690)

* Wed Jan 18 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.1.8-7mdk
- fix libification

* Mon Jan 16 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.1.8-6mdk
- fix build on x86_64

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.1.8-5mdk
- Rebuild

