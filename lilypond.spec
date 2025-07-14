#
# Conditional build:
%bcond_without	doc	# build docs
#
Summary:	Music typesetter
Summary(pl.UTF-8):	Program do składania nut
Name:		lilypond
# note: 2.22.x is stable, 2.23.x devel
Version:	2.22.2
Release:	1
License:	GPL v3+ with font exception
Group:		Applications/Sound
Source0:	https://lilypond.org/download/sources/v2.22/%{name}-%{version}.tar.gz
# Source0-md5:	677e68e728b24f66be5d20072294f41c
Patch0:		%{name}-info.patch
Patch1:		%{name}-sh.patch
Patch2:		%{name}-aclocal.patch
Patch3:		%{name}-mf.patch
Patch4:		guile3.0.patch
URL:		https://lilypond.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison >= 2.4.1
BuildRequires:	flex >= 2.5.4a
BuildRequires:	fontconfig >= 1:2.4.0
BuildRequires:	fontconfig-devel >= 1:2.4.0
BuildRequires:	fontforge >= 20110222
BuildRequires:	fonts-TTF-DejaVu
BuildRequires:	fonts-Type1-urw
BuildRequires:	freetype >= 1:2.1.10
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	ghostscript-fonts-std
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	guile-devel >= 5:1.8.2
BuildRequires:	kpathsea-devel
BuildRequires:	libstdc++-devel >= 5:3.4
BuildRequires:	pango-devel >= 1:1.38.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	rpm-pythonprov
BuildRequires:	t1utils
BuildRequires:	texinfo >= 6.1
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-metapost
%if %{with doc}
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-png
BuildRequires:	dblatex >= 0.1.4
BuildRequires:	ghostscript >= 9.20
BuildRequires:	netpbm-progs
BuildRequires:	rsync
BuildRequires:	texi2html >= 1.82
BuildRequires:	texinfo-texi2dvi >= 6.1
# `kpsewhich tex epsf`
BuildRequires:	texlive
# `kpsewhich -format=mf fikparm`
BuildRequires:	texlive-fonts-lh
BuildRequires:	texlive-latex-bibtex
BuildRequires:	texlive-xetex
BuildRequires:	zip
%endif
BuildConflicts:	lilypond < 1.6.0
Requires:	fonts-TTF-DejaVu
Requires:	ghostscript >= 9.20
Requires:	glib2 >= 1:2.38
Requires:	pango >= 1:1.38.0
Requires:	python3-modules >= 1:3.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		texmfdir	%{_datadir}/texmf
%define		texmfdistdir	%{texmfdir}-dist
%if "%{pld_release}" != "th"
%define		texfontsdir	%{texmfdir}/fonts
%else
%define		texfontsdir	%{texmfdistdir}/fonts
%endif

%description
LilyPond is a music typesetter. It produces beautiful sheet music
using a high level description file as input. It excels at typesetting
classical music, but you can also print pop-songs. With LilyPond we
hope to make music publication software available to anyone on the
internet.

%description -l pl.UTF-8
LilyPond jest programem do składu muzycznego. Produkuje piękne
partytury używając języka wysokiego poziomu jako wejście. Służy przede
wszystkim do składania nut muzyki klasycznej, ale można drukować także
piosenki pop. Autorzy udostępniają LilyPond z nadzieją dostarczenia
wszystkim oprogramowania do publikacji muzycznych.

%package -n emacs-lilypond-mode-pkg
Summary:	LilyPond mode for Emacs
Summary(pl.UTF-8):	Tryb edycji plików LilyPond dla Emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}
Requires:	emacs

%description -n emacs-lilypond-mode-pkg
LilyPond mode for Emacs.

%description -n emacs-lilypond-mode-pkg -l pl.UTF-8
Tryb edycji plików LilyPond dla Emacsa.

%package -n vim-syntax-lilypond
Summary:	LilyPond files support for Vim
Summary(pl.UTF-8):	Obsługa plików LilyPonda dla Vima
Group:		Applications/Editors/Vim
Requires:	%{name} = %{version}-%{release}
Requires:	vim-rt >= 4:6.4.001-2

%description -n vim-syntax-lilypond
LilyPond files support for Vim.

%description -n vim-syntax-lilypond -l pl.UTF-8
Obsługa plików LilyPonda dla Vima.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__autoconf}
%configure \
	PYTHON=%{__python3} \
	%{?debug:--disable-optimising} \
	--with-texgyre-dir=%{texfontsdir}/opentype/public/tex-gyre/ \
	%{__enable_disable doc documentation}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{texmfdir}/{dvips,tex},%{texfontsdir}/{source,tfm/lilypond,type1/lilypond}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p mf/out/*.tfm $RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond
cp -p mf/out/*.pfb $RPM_BUILD_ROOT%{texfontsdir}/type1/lilypond

find $RPM_BUILD_ROOT -name fonts.cache-1 | xargs rm -f

# ?
%{__mv} $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source \
	$RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
# for latex and dvips
%{__mv} $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/tex \
	$RPM_BUILD_ROOT%{texmfdir}/tex/lilypond
# both for lilypond and dvips
ln -sf %{_datadir}/lilypond/%{version}/ps \
	$RPM_BUILD_ROOT%{texmfdir}/dvips/lilypond

# vim syntax/etc. files
install -d $RPM_BUILD_ROOT%{_datadir}/vim
%{__mv} $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/vim \
	$RPM_BUILD_ROOT%{_datadir}/vim/vimfiles

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -h %{texmfdir}/dvips/lilypond || rm -rf %{texmfdir}/dvips/lilypond

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2
[ ! -x %{_bindir}/scrollkeeper-update ] || %{_bindir}/scrollkeeper-update

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2
[ ! -x %{_bindir}/scrollkeeper-update ] || %{_bindir}/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.txt DEDICATION LICENSE* NEWS.txt README.md ROADMAP
%attr(755,root,root) %{_bindir}/abc2ly
%attr(755,root,root) %{_bindir}/convert-ly
%attr(755,root,root) %{_bindir}/etf2ly
%attr(755,root,root) %{_bindir}/lilymidi
%attr(755,root,root) %{_bindir}/lilypond
%attr(755,root,root) %{_bindir}/lilypond-book
%attr(755,root,root) %{_bindir}/lilypond-invoke-editor
%attr(755,root,root) %{_bindir}/lilysong
%attr(755,root,root) %{_bindir}/midi2ly
%attr(755,root,root) %{_bindir}/musicxml2ly
%dir %{_datadir}/lilypond
%dir %{_datadir}/lilypond/%{version}
%{_datadir}/lilypond/%{version}/fonts
%{_datadir}/lilypond/%{version}/ly
%{_datadir}/lilypond/%{version}/ps
%{_datadir}/lilypond/%{version}/python
%{_datadir}/lilypond/%{version}/scm

%{texfontsdir}/source/lilypond
%{texfontsdir}/tfm/lilypond
%{texfontsdir}/type1/lilypond
%{texmfdir}/dvips/lilypond
%{texmfdir}/tex/lilypond

%if %{with doc}
%{_infodir}/lilypond-*.info*
%{_infodir}/music-glossary.info*
%{_mandir}/man1/abc2ly.1*
%{_mandir}/man1/convert-ly.1*
%{_mandir}/man1/etf2ly.1*
%{_mandir}/man1/lilymidi.1*
%{_mandir}/man1/lilypond.1*
%{_mandir}/man1/lilypond-book.1*
%{_mandir}/man1/lilypond-invoke-editor.1*
%{_mandir}/man1/lilysong.1*
%{_mandir}/man1/midi2ly.1*
%{_mandir}/man1/musicxml2ly.1*
%endif

%files -n emacs-lilypond-mode-pkg
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/lilypond-*.el

%files -n vim-syntax-lilypond
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/compiler/lilypond.vim
%{_datadir}/vim/vimfiles/ftdetect/lilypond.vim
%{_datadir}/vim/vimfiles/ftplugin/lilypond.vim
%{_datadir}/vim/vimfiles/indent/lilypond.vim
%{_datadir}/vim/vimfiles/syntax/lilypond*
