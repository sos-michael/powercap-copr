%global commit  REPLACED_BY_CRON
     %global cdate   REPLACED_BY_CRON
     %global shortc  %(c=%{commit}; echo ${c:0:7})

     Name:    powercap
     Version: 0.7.0
     Release: 0.%{cdate}git%{shortc}%{?dist}
     Summary: C bindings to the Linux Power Capping Framework
     License: BSD-3-Clause
     URL:     https://github.com/powercap/powercap
     Source0: %{url}/archive/%{commit}/powercap-%{shortc}.tar.gz
     BuildRequires: gcc cmake make

     %description ...
     %prep
     %autosetup -n powercap-%{commit}
     %build
     %cmake -DBUILD_SHARED_LIBS=On -DCMAKE_BUILD_TYPE=Release
     %cmake_build
     %install
     %cmake_install
     %files
     %license LICENSE
     %{_bindir}/powercap-*
     %{_libdir}/libpowercap.so.*
     %{_mandir}/man1/*
     %{_mandir}/man3/*
     %package devel
     Summary: Headers for %{name}
     Requires: %{name}%{?_isa} = %{version}-%{release}
     %description devel ...
     %files devel
     %{_includedir}/powercap/
     %{_libdir}/libpowercap.so
     %{_libdir}/pkgconfig/powercap.pc
     %{_libdir}/cmake/Powercap/
