Summary:	Music typesetter
Summary(pl):	Program do sk³adania nut
Name:		lilypond
Version:	2.0.0
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.lilypond.org/pub/LilyPond/v2.0/%{name}-%{version}.tar.gz
# Source0-md5:	80faf9f9abc4ecf72a71ba0036cdfee0
URL:		http://www.lilypond.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	guile-devel
BuildRequires:	kpathsea-devel
BuildRequires:	mftrace
BuildRequires:	autotrace >= 0.30
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel
BuildRequires:	texinfo
BuildRequires:	tetex-dvips
BuildRequires:	tetex-fonts-cm
BuildConflicts:	lilypond < 1.6.0
Requires:	tetex-format-latex
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

cp -f stepmake/aclocal.m4 .
cp -f /usr/share/automake/{config.*,install-sh} .

%build
%{__autoconf}
cd stepmake
%{__autoconf}
cd ..
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{texfontsdir}/{source,tfm,type1}
install -d $RPM_BUILD_ROOT/etc/profile.d

%{__make} install \
	local_lilypond_datadir=$RPM_BUILD_ROOT%{_datadir}/lilypond/%{version} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	localedir=$RPM_BUILD_ROOT%{_localedir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

install buildscripts/out/lilypond-profile \
	$RPM_BUILD_ROOT/etc/profile.d/lilypond.sh
install buildscripts/out/lilypond-login \
	$RPM_BUILD_ROOT/etc/profile.d/lilypond.csh

perl -pi -e "s#$RPM_BUILD_ROOT##" $RPM_BUILD_ROOT%{_bindir}/*

mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source \ 
	$RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/tfm \
	$RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/type1 \
	$RPM_BUILD_ROOT%{texfontsdir}/type1/lilypond

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.txt ChangeLog DEDICATION NEWS.txt README.txt THANKS

%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/lilypond
%dir %{_datadir}/lilypond/%{version}
%attr(755,root,root) /etc/profile.d/*
%{_datadir}/lilypond/%{version}/ly
%{_datadir}/lilypond/%{version}/ps
%dir %{_datadir}/lilypond/%{version}/python
%{_datadir}/lilypond/%{version}/python/*.py
%{_datadir}/lilypond/%{version}/python/*.pyc
%dir %{_libdir}/lilypond/%{version}/python
%attr(755,root,root) %{_libdir}/lilypond/%{version}/python/midi.so
%{_datadir}/lilypond/%{version}/scm
%{_datadir}/lilypond/%{version}/tex
%{texfontsdir}/*/lilypond
%{_infodir}/*.info*
%{_mandir}/man1/*

%dir %{_datadir}/lilypond/%{version}/dvips/
%{_datadir}/lilypond/%{version}/dvips/*
%dir %{_datadir}/lilypond/%{version}/fonts/type1/
%{_datadir}/lilypond/%{version}/fonts/type1/*
%dir %{_datadir}/lilypond/%{version}/make/
%{_datadir}/lilypond/%{version}/make/*

%dir %{_datadir}/omf/lilypond/%{version}/
%{_datadir}/omf/lilypond/%{version}/*
