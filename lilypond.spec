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
%define		texfontsdir	/usr/share/texmf/fonts

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
install -d $RPM_BUILD_ROOT%{texfontsdir}/{afm,source,tfm}

%{__make} install \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	localedir=$RPM_BUILD_ROOT%{_localedir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

mv -f $RPM_BUILD_ROOT%{_datadir}/afm $RPM_BUILD_ROOT%{texfontsdir}/afm/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/mf $RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/tfm $RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond

%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES DEDICATION FAQ.txt NEWS README.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}
%{_datadir}/ly
%{_datadir}/ps
%{_datadir}/scm
%{_datadir}/tex
%{texfontsdir}/*/lilypond
%{_infodir}/*
%{_mandir}/man1/*
