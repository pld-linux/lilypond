#
# Conditional build:
%bcond_with	gui	# enable experimental GUI
#
Summary:	Music typesetter
Summary(pl.UTF-8):	Program do składania nut
Name:		lilypond
Version:	2.10.33
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://lilypond.org/download/v2.10/%{name}-%{version}.tar.gz
# Source0-md5:	86a67fcc404e942be723f8a72988b286
Patch0:		%{name}-info.patch
Patch1:		%{name}-sh.patch
Patch2:		%{name}-po.patch
Patch3:		%{name}-afm.patch
URL:		http://www.lilypond.org/
BuildRequires:	automake
BuildRequires:	bison >= 1.29
BuildRequires:	flex >= 2.5.4a
BuildRequires:	fontconfig-devel >= 1:2.2.0
BuildRequires:	fontforge >= 20050624
BuildRequires:	gettext-devel
BuildRequires:	ghostscript >= 8.15
BuildRequires:	ghostscript-fonts-std
%{?with_gui:BuildRequires:	gtk+2-devel >= 2:2.4.0}
BuildRequires:	guile-devel >= 5:1.6.7
BuildRequires:	kpathsea-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	mftrace >= 1.1.19
BuildRequires:	pango-devel >= 1.6.0
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python-devel >= 2.1
BuildRequires:	tetex-dvips
BuildRequires:	tetex-fonts-cm
BuildRequires:	tetex-fonts-cmextra
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	texinfo >= 4.7
BuildConflicts:	lilypond < 1.6.0
Requires:	ghostscript >= 8.15
Requires:	guile >= 5:1.6.5
Requires:	python >= 2.1
Requires:	tetex-format-latex >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		texmfdir	/usr/share/texmf
%define		texfontsdir	%{texmfdir}/fonts

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
Requires:	vim >= 4:6.4.001-2

%description -n vim-syntax-lilypond
LilyPond files support for Vim.

%description -n vim-syntax-lilypond -l pl.UTF-8
Obsługa plików LilyPonda dla Vima.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp -f /usr/share/automake/config.* stepmake/bin
%{__autoconf}
%configure \
	%{?debug:--disable-optimising} \
	%{?with_gui:--enable-gui}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{texmfdir}/{dvips/misc,tex},%{texfontsdir}/{source,tfm,type1}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name fonts.cache-1 | xargs rm -f

# for dvips
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/dvips \
	$RPM_BUILD_ROOT%{texmfdir}/dvips/lilypond
# ?
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/fonts/source \
	$RPM_BUILD_ROOT%{texfontsdir}/source/lilypond
# for latex and dvips
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/tex \
	$RPM_BUILD_ROOT%{texmfdir}/tex/lilypond
# both for lilypond and dvips
ln -sf %{_datadir}/lilypond/%{version}/fonts/type1 \
	$RPM_BUILD_ROOT%{texfontsdir}/type1/lilypond
ln -sf %{_datadir}/lilypond/%{version}/ps/music-drawing-routines.ps \
	$RPM_BUILD_ROOT%{texmfdir}/dvips/misc

# no need for subdir
mv -f $RPM_BUILD_ROOT%{_infodir}/lilypond/*.info* $RPM_BUILD_ROOT%{_infodir}

# vim syntax/etc. files
install -d $RPM_BUILD_ROOT%{_datadir}/vim
mv -f $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/vim \
	$RPM_BUILD_ROOT%{_datadir}/vim/vimfiles

# lilypond/stepmake build system - not needed at runtime
rm -rf $RPM_BUILD_ROOT%{_datadir}/lilypond/%{version}/make

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc AUTHORS.txt ChangeLog DEDICATION NEWS.txt README.txt THANKS
%attr(755,root,root) %{_bindir}/*
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
%{texfontsdir}/type1/lilypond
%{texmfdir}/dvips/lilypond
%{texmfdir}/dvips/misc/*.ps
%{texmfdir}/tex/lilypond

%{_datadir}/omf/lilypond

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
