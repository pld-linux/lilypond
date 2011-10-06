# TODO:
#	- probably gui bcond is meaningless
#
# Conditional build:
%bcond_with	gui	# enable experimental GUI
%bcond_with	doc	# build docs
#
Summary:	Music typesetter
Summary(pl.UTF-8):	Program do składania nut
Name:		lilypond
Version:	2.12.2
Release:	7
License:	GPL
Group:		Applications/Sound
Source0:	http://lilypond.org/download/v2.12/%{name}-%{version}.tar.gz
# Source0-md5:	681dfbecf8a3710d1400cf9488be716b
Patch0:		%{name}-info.patch
Patch1:		%{name}-sh.patch
Patch3:		%{name}-afm.patch
Patch4:		%{name}-aclocal.patch
Patch5:		%{name}-bad_cast.patch
URL:		http://www.lilypond.org/
%{?with_doc:BuildRequires:	ImageMagick-coder-png}
%{?with_doc:BuildRequires:	ImageMagick}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison >= 1.29
BuildRequires:	flex >= 2.5.4a
BuildRequires:	fontconfig
BuildRequires:	fontconfig-devel >= 1:2.2.0
BuildRequires:	fontforge >= 20060125
BuildRequires:	fonts-Type1-urw
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	ghostscript >= 8.15
%{?with_doc:BuildRequires:	ghostscript >= 8.60}
BuildRequires:	ghostscript-fonts-std
%{?with_gui:BuildRequires:	gtk+2-devel >= 2:2.4.0}
BuildRequires:	guile-devel >= 5:1.8.2
BuildRequires:	kpathsea-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:3.4
#BuildRequires:	mftrace >= 1.1.19
%{?with_doc:BuildRequires:	netpbm-progs}
BuildRequires:	pango-devel >= 1.12.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python-devel >= 2.4
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
%{?with_doc:BuildRequires:	rsync}
BuildRequires:	texinfo >= 4.11
%{?with_doc:BuildRequires:	texinfo-texi2dvi}
%if "%{pld_release}" != "th"
%{?with_doc:BuildRequires:	tetex-latex-bibtex}
BuildRequires:	tetex-metapost
%else
#BuildRequires:	texlive-dvips
#BuildRequires:	texlive-fonts-cm
#BuildRequires:	texlive-fonts-cmextra
#BuildRequires:	texlive-fonts-jknappen
%{?with_doc:BuildRequires:	texlive-latex-bibtex}
BuildRequires:	texlive-metapost
%endif
BuildRequires:	t1utils
BuildConflicts:	lilypond < 1.6.0
Requires:	ghostscript >= 8.15
Requires:	guile >= 5:1.8.2
Requires:	python >= 2.4
%if "%{pld_release}" != "th"
Requires:	tetex-latex
%else
Requires:	texlive-latex
%endif
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
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
cp -f /usr/share/automake/config.* stepmake/bin
%{__autoconf}
%configure \
	%{?debug:--disable-optimising} \
	%{?with_gui:--enable-gui}
%{__make} -j1
%{?with_doc:%{__make} -j1 web}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{texmfdir}/{dvips,tex},%{texfontsdir}/{source,tfm,type1}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%if %{with doc}
%{__make} -j1 web-install \
	DESTDIR=$RPM_BUILD_ROOT
%endif
cp -aL out/share/lilypond/current/fonts/tfm \
	$RPM_BUILD_ROOT%{texfontsdir}/tfm/lilypond

find $RPM_BUILD_ROOT -name fonts.cache-1 | xargs rm -f

# ?
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source \
	$RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
# for latex and dvips
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/tex \
	$RPM_BUILD_ROOT%{texmfdir}/tex/lilypond
# both for lilypond and dvips
ln -sf %{_datadir}/lilypond/%{version}/fonts/type1 \
	$RPM_BUILD_ROOT%{texfontsdir}/type1/lilypond
ln -sf %{_datadir}/lilypond/%{version}/ps \
	$RPM_BUILD_ROOT%{texmfdir}/dvips/lilypond
rm -rf $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/dvips

# vim syntax/etc. files
install -d $RPM_BUILD_ROOT%{_datadir}/vim
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/vim \
	$RPM_BUILD_ROOT%{_datadir}/vim/vimfiles

# lilypond/stepmake build system - not needed at runtime
rm -rf $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/make

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -h %{texmfdir}/dvips/lilypond || rm -rf %{texmfdir}/dvips/lilypond

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2
[ ! -x /usr/bin/scrollkeeper-update ] || /usr/bin/scrollkeeper-update

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
[ ! -x /usr/bin/texhash ] || /usr/bin/texhash 1>&2
[ ! -x /usr/bin/scrollkeeper-update ] || /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.txt DEDICATION NEWS.txt README.txt THANKS
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
%dir %{_libdir}/lilypond
%dir %{_libdir}/lilypond/%{version}
%dir %{_libdir}/lilypond/%{version}/python
%attr(755,root,root) %{_libdir}/lilypond/%{version}/python/midi.so
%dir %{_datadir}/lilypond
%dir %{_datadir}/lilypond/%{version}
%{_datadir}/lilypond/%{version}/fonts
%{_datadir}/lilypond/%{version}/ly
%{_datadir}/lilypond/%{version}/ps
%dir %{_datadir}/lilypond/%{version}/python
%{_datadir}/lilypond/%{version}/python/*.py
%{_datadir}/lilypond/%{version}/python/*.pyc
%{_datadir}/lilypond/%{version}/scm
%{_infodir}/*.info*
%{_mandir}/man1/*

%{texfontsdir}/source/lilypond
%{texfontsdir}/tfm/lilypond
%{texfontsdir}/type1/lilypond
%{texmfdir}/dvips/lilypond
%{texmfdir}/tex/lilypond

%{_datadir}/omf/lilypond
%{?with_doc:/usr/share/doc/lilypond}

%files -n emacs-lilypond-mode-pkg
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/*.el

%files -n vim-syntax-lilypond
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/compiler/lilypond.vim
%{_datadir}/vim/vimfiles/ftdetect/lilypond.vim
%{_datadir}/vim/vimfiles/ftplugin/lilypond.vim
%{_datadir}/vim/vimfiles/indent/lilypond.vim
%{_datadir}/vim/vimfiles/syntax/lilypond*
