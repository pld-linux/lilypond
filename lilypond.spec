Summary:	Music typesetter
Summary(pl):	Program do sk³adania nut
Name:		lilypond
Version:	1.4.13
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.gnu.org/gnu/lilypond/%{name}-%{version}.tar.gz
Patch0:		%{name}-pythonhack.patch
URL:		http://www.cs.uu.nl/people/hanwen/lilypond/index.html
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	guile-devel
BuildRequires:	kpathsea-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/lilypond
%define		_localedir	%{_prefix}/share/locale

%description
LilyPond is a music typesetter. It produces beautiful sheet music
using a high level description file as input. It excels at typesetting
classical music, but you can also print pop-songs. With LilyPond we
hope to make music publication software available to anyone on the
internet.

%description -l pl
LilyPond jest programem do sk³adu muzycznego. Produkuje piêkne
partytury u¿ywaj±c jêzyka wysokiego poziomu jako wej¶cie. S³u¿y przede
wszystkim do sk³adania nut muzyki klasycznej, ale mo¿na drukowaæ tak¿e
piosenki pop. Autorzy udostêpniaj± LilyPond z nadziej± dostarczenia
wszystkim oprogramowania do publikacji muzycznych.

%prep
%setup -q
%patch -p1

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	localedir=$RPM_BUILD_ROOT%{_localedir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES DEDICATION FAQ.txt NEWS README.txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}
%{_infodir}/*
%{_mandir}/man1/*
