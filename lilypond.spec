Summary:	Music typesetter
Summary(pl):	Program do sk³adania nut
Name:		lilypond
Version:	2.2.6
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://lilypond.org/download/v2.2/%{name}-%{version}.tar.gz
# Source0-md5:	c379905b53973cc314415340dd017c77
Patch0:		%{name}-info.patch
Patch1:		%{name}-sh.patch
Patch2:		%{name}-po.patch
URL:		http://www.lilypond.org/
BuildRequires:	automake
BuildRequires:	bison >= 1.25
BuildRequires:	flex
BuildRequires:	fontforge
BuildRequires:	gettext-devel
BuildRequires:	guile-devel >= 1.6
BuildRequires:	kpathsea-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:3.0
BuildRequires:	mftrace >= 1.0.17
BuildRequires:	python-devel >= 2.1
BuildRequires:	tetex-dvips
BuildRequires:	tetex-fonts-cm
BuildRequires:	tetex-fonts-cmextra
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	texinfo >= 4.6
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

%package -n emacs-lilypond-mode-pkg
Summary:	LilyPond mode for Emacs
Summary(pl):	Tryb edycji plików LilyPond dla Emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}
Requires:	emacs

%description -n emacs-lilypond-mode-pkg
LilyPond mode for Emacs.

%description -n emacs-lilypond-mode-pkg -l pl
Tryb edycji plików LilyPond dla Emacsa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.* stepmake/bin
%configure \
	%{?debug:--disable-optimising}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{texfontsdir}/{source,tfm,type1}

%{__make} install \
	local_lilypond_datadir=$RPM_BUILD_ROOT%{_datadir}/lilypond/%{version} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	localedir=$RPM_BUILD_ROOT%{_localedir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

%{__perl} -pi -e "s#$RPM_BUILD_ROOT##" $RPM_BUILD_ROOT%{_bindir}/*

mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source \
      $RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/tfm \
      $RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/type1 \
      $RPM_BUILD_ROOT%{texfontsdir}/type1/lilypond

mv -f $RPM_BUILD_ROOT%{_infodir}/lilypond/*.info* $RPM_BUILD_ROOT%{_infodir}

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
%dir %{_libdir}/lilypond
%dir %{_libdir}/lilypond/%{version}
%dir %{_libdir}/lilypond/%{version}/python
%attr(755,root,root) %{_libdir}/lilypond/%{version}/python/midi.so
%dir %{_datadir}/lilypond
%dir %{_datadir}/lilypond/%{version}
%{_datadir}/lilypond/%{version}/ly
%{_datadir}/lilypond/%{version}/ps
%dir %{_datadir}/lilypond/%{version}/python
%{_datadir}/lilypond/%{version}/python/*.py
%{_datadir}/lilypond/%{version}/python/*.pyc
%{_datadir}/lilypond/%{version}/dvips
%{_datadir}/lilypond/%{version}/fonts
%{_datadir}/lilypond/%{version}/scm
%{_datadir}/lilypond/%{version}/tex
%{_infodir}/*.info*
%{_mandir}/man1/*

# lilypond/stepmake build system - not needed at runtime
#%{_datadir}/lilypond/%{version}/make

%{texfontsdir}/*/lilypond

# needed? subpackage? (could install in non-existing dir)
%{_datadir}/omf/lilypond

%files -n emacs-lilypond-mode-pkg
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/*.el
