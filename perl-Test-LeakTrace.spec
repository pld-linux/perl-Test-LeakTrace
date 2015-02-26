#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Test
%define		pnam	LeakTrace
%include	/usr/lib/rpm/macros.perl
Summary:	Test::LeakTrace - tracing memory leaks
Summary(pl.UTF-8):	Test::LeakTrace - śledzenie wycieków pamięci
Name:		perl-Test-LeakTrace
Version:	0.14
Release:	5
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Test/GFUJI/Test-LeakTrace-%{version}.tar.gz
# Source0-md5:	d53953f442cf782c30f843df677db210
URL:		http://search.cpan.org/dist/Test-LeakTrace/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-Simple >= 0.62
%endif
Requires:	perl-dirs >= 4-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Test::LeakTrace provides several functions that trace memory leaks.
This module scans arenas, the memory allocation system, so it can
detect any leaked SVs in given blocks.

%description -l pl.UTF-8
Test::LeakTrace udostępnia kilka funkcji do śledzenia wycieków
pamięci. Moduł skanuje areny systemu przydzielania pamięci, przez co
może wykryć wycieki SV w podanych blokach.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as man
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/Test/LeakTrace/JA.pod

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorarch}/Test/LeakTrace.pm
%{perl_vendorarch}/Test/LeakTrace
%dir %{perl_vendorarch}/auto/Test/LeakTrace
%attr(755,root,root) %{perl_vendorarch}/auto/Test/LeakTrace/LeakTrace.so
%{_mandir}/man3/Test::LeakTrace*.3pm*
%{_examplesdir}/%{name}-%{version}
