Summary:	Music typesetter
Summary(pl):	Program do sk³adania nut
Name:		lilypond
Version:	1.6.11
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.gnu.org/gnu/lilypond/%{name}-%{version}.tar.gz
# Source0-md5:	e06e05046c0741cdce090c9eaae5102a
Patch0:		%{name}-info.patch
Patch1:		%{name}-gcc33.patch
Patch2:		%{name}-python23.patch
Patch3:		%{name}-acfix.patch
URL:		http://www.cs.uu.nl/people/hanwen/lilypond/index.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	guile-devel
BuildRequires:	kpathsea-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	python
BuildRequires:	texinfo
BuildConflicts:	lilypond < 1.6.0
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -f stepmake/aclocal.m4 .
cp -f /usr/share/automake/{config.*,install-sh} .

%build
%{__autoconf}
cd stepmake
%{__autoconf}
cd ..
%configure
%{__make} \
	builddir="`pwd`"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{texfontsdir}/{afm,source,tfm}

%{__make} install \
	builddir="`pwd`" \
	local_lilypond_datadir=$RPM_BUILD_ROOT%{_datadir}/lilypond/%{version} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	localedir=$RPM_BUILD_ROOT%{_localedir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/afm $RPM_BUILD_ROOT%{texfontsdir}/afm/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source $RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/tfm $RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond

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
%doc AUTHORS.txt ChangeLog DEDICATION NEWS README.txt THANKS
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/lilypond
%dir %{_datadir}/lilypond/%{version}
%{_datadir}/lilypond/%{version}/ly
%{_datadir}/lilypond/%{version}/ps
%dir %{_datadir}/lilypond/%{version}/python
%attr(755,root,root) %{_datadir}/lilypond/%{version}/python/midi.so
%{_datadir}/lilypond/%{version}/scm
%{_datadir}/lilypond/%{version}/tex
%{texfontsdir}/*/lilypond
%{_infodir}/*.info*
%{_mandir}/man1/*
