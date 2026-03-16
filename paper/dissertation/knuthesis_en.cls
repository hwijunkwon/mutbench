%% knuthesis_en.cls — Kyungpook National University Ph.D. Thesis Class (English)
%% Based on knuthesis.cls, adapted for English-only version (no kotex)
%% Custom paper size: 19cm x 26cm
%% XeLaTeX environment

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{knuthesis_en}[2026/03/12 KNU PhD Thesis Class (English)]

%% Pass options to report class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

%% Load base class
\LoadClass[11pt,oneside,openany]{report}

%% ============================================================
%% Required packages
%% ============================================================
\RequirePackage{ifthen}
\RequirePackage{setspace}

%% Geometry: custom paper size 19cm x 26cm, 35mm margins
\RequirePackage[
  paperwidth=19cm,
  paperheight=26cm,
  left=35mm,
  right=35mm,
  top=35mm,
  bottom=35mm,
  headheight=15mm,
  footskip=15mm
]{geometry}

%% ============================================================
%% Chapter/section formatting
%% ============================================================
\renewcommand{\chaptername}{Chapter}
\renewcommand{\thechapter}{\arabic{chapter}}
\renewcommand{\thesection}{\thechapter.\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}

%% Figure/Table/Equation numbering by chapter
\@addtoreset{figure}{chapter}
\@addtoreset{table}{chapter}
\@addtoreset{equation}{chapter}
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\renewcommand{\theequation}{\thechapter.\arabic{equation}}

%% Chapter title format
\makeatletter
\renewcommand{\@makechapterhead}[1]{%
  \vspace*{30pt}%
  {\parindent 0pt \centering
    \normalfont\LARGE\bfseries
    \chaptername\ \thechapter\par
    \vskip 10pt
    \Huge\bfseries #1\par
    \nobreak
    \vskip 30pt
  }%
}
\renewcommand{\@makeschapterhead}[1]{%
  \vspace*{30pt}%
  {\parindent 0pt \centering
    \normalfont\Huge\bfseries #1\par
    \nobreak
    \vskip 30pt
  }%
}

%% ============================================================
%% Metadata commands
%% ============================================================
\newcommand{\@ktitle}{}
\newcommand{\ktitle}[1]{\renewcommand{\@ktitle}{#1}}

\newcommand{\@kauthor}{}
\newcommand{\kauthor}[1]{\renewcommand{\@kauthor}{#1}}

\newcommand{\@advisor}{}
\newcommand{\advisor}[1]{\renewcommand{\@advisor}{#1}}

\newcommand{\@kadvisor}{}
\newcommand{\kadvisor}[1]{\renewcommand{\@kadvisor}{#1}}

\newcommand{\@major}{}
\newcommand{\major}[1]{\renewcommand{\@major}{#1}}

\newcommand{\@kmajor}{}
\newcommand{\kmajor}[1]{\renewcommand{\@kmajor}{#1}}

\newcommand{\@degreeyear}{}
\newcommand{\@degreemonth}{}
\newcommand{\degreedate}[2]{%
  \renewcommand{\@degreeyear}{#1}%
  \renewcommand{\@degreemonth}{#2}%
}

%% Committee members
\newcommand{\@committeechairman}{}
\newcommand{\committeechairman}[1]{\renewcommand{\@committeechairman}{#1}}

\newcommand{\@committeememberA}{}
\newcommand{\committeememberA}[1]{\renewcommand{\@committeememberA}{#1}}

\newcommand{\@committeememberB}{}
\newcommand{\committeememberB}[1]{\renewcommand{\@committeememberB}{#1}}

\newcommand{\@committeememberC}{}
\newcommand{\committeememberC}[1]{\renewcommand{\@committeememberC}{#1}}

\newcommand{\@committeememberD}{}
\newcommand{\committeememberD}[1]{\renewcommand{\@committeememberD}{#1}}

%% ============================================================
%% Cover page
%% ============================================================
\newcommand{\makecoverpage}{%
  \thispagestyle{empty}
  \newgeometry{left=2cm,top=2.5cm,right=2cm,bottom=1.5cm}
  \setstretch{1.3}
  \begin{center}
    {\fontsize{11pt}{13pt}\selectfont \textbf{Thesis for the Degree of Ph.D.}}\\
    \vspace{3cm}
    {\fontsize{21pt}{25pt}\selectfont \textbf{\@title}}\\
    \vspace{4cm}
    {\fontsize{12pt}{14pt}\selectfont \textbf{The Graduate School}}\\[0.3cm]
    {\fontsize{12pt}{14pt}\selectfont \textbf{Kyungpook National University}}\\[0.3cm]
    {\fontsize{12pt}{14pt}\selectfont \textbf{\@major}}\\
    \vspace{2cm}
    {\fontsize{14pt}{17pt}\selectfont \textbf{\@author}}\\
    \vspace{\fill}
    {\fontsize{12pt}{14pt}\selectfont \textbf{August \@degreeyear}}\\
    \vspace{1cm}
    {\fontsize{16pt}{19pt}\selectfont \textbf{Kyungpook National University}}\\
  \end{center}
  \restoregeometry
  \clearpage
}

%% ============================================================
%% Inner title page
%% ============================================================
\newcommand{\makeinnertitle}{%
  \thispagestyle{empty}
  \newgeometry{left=2cm,top=2.5cm,right=2cm,bottom=1.5cm}
  \setstretch{1.3}
  \begin{center}
    {\fontsize{21pt}{25pt}\selectfont \textbf{\@title}}\\
    \vspace{3cm}
    {\fontsize{12pt}{14pt}\selectfont
      Advisor: Professor \@advisor}\\
    \vspace{2cm}
    {\fontsize{12pt}{14pt}\selectfont
      Submitted as a Doctoral Dissertation}\\
    \vspace{2cm}
    {\fontsize{12pt}{14pt}\selectfont August \@degreeyear}\\
    \vspace{2cm}
    {\fontsize{14pt}{17pt}\selectfont \textbf{The Graduate School}}\\[0.3cm]
    {\fontsize{14pt}{17pt}\selectfont \textbf{Kyungpook National University}}\\[0.3cm]
    {\fontsize{12pt}{14pt}\selectfont \@major}\\
    \vspace{1.5cm}
    {\fontsize{14pt}{17pt}\selectfont \textbf{\@author}}\\
  \end{center}
  \restoregeometry
  \clearpage
}

%% ============================================================
%% Approval page
%% ============================================================
\newcommand{\makeapprovalpage}{%
  \thispagestyle{empty}
  \newgeometry{left=2cm,top=2.5cm,right=2cm,bottom=1.5cm}
  \setstretch{1.3}
  \begin{center}
    {\fontsize{14pt}{17pt}\selectfont \textbf{Approved as a Doctoral Dissertation}}\\[0.5cm]
    {\fontsize{14pt}{17pt}\selectfont \textbf{for \@author}}\\
    \vspace{2cm}
    {\fontsize{18pt}{22pt}\selectfont \textbf{\@title}}\\
    \vspace{3cm}
    {\fontsize{12pt}{14pt}\selectfont
      \begin{tabular}{r@{\hspace{1cm}}l}
        Committee Chair & \underline{\hspace{5cm}} \\[1cm]
        Committee Member & \underline{\hspace{5cm}} \\[1cm]
        Committee Member & \underline{\hspace{5cm}} \\[1cm]
        Committee Member & \underline{\hspace{5cm}} \\[1cm]
        Committee Member & \underline{\hspace{5cm}} \\
      \end{tabular}
    }\\
    \vspace{\fill}
    {\fontsize{12pt}{14pt}\selectfont August \@degreeyear}\\[0.5cm]
    {\fontsize{14pt}{17pt}\selectfont \textbf{The Graduate School, Kyungpook National University}}\\
  \end{center}
  \restoregeometry
  \clearpage
}

%% ============================================================
%% Korean abstract page (국문초록) — for back matter of English thesis
%% ============================================================
\newcommand{\makekorabstract}[1]{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{국문초록}
  \thispagestyle{empty}
  \begin{center}
    \setstretch{1.5}
    {\koreanfont\fontsize{14pt}{17pt}\selectfont \textbf{\@ktitle}}\\
    \vspace{1cm}
    {\koreanfont\fontsize{11pt}{13pt}\selectfont \textbf{\@kauthor}}\\
    \vspace{0.5cm}
    {\koreanfont\fontsize{10pt}{12pt}\selectfont 경북대학교 대학원 \@kmajor\\(지도교수 \@kadvisor)}\\
  \end{center}
  \vspace{1.5cm}
  \setstretch{1.6}
  {\koreanfont\fontsize{14pt}{17pt}\selectfont \textbf{(초\hspace{1em}록)}}\\[0.5cm]
  {\koreanfont\fontsize{11pt}{17pt}\selectfont #1}
  \clearpage
}

%% ============================================================
%% Abstract page
%% ============================================================
\newcommand{\makeengabstract}[1]{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{Abstract}
  \thispagestyle{empty}
  \begin{center}
    \setstretch{1.5}
    {\fontsize{14pt}{17pt}\selectfont \textbf{\@title}}\\
    \vspace{1cm}
    {\fontsize{11pt}{13pt}\selectfont \textbf{\@author}}\\
    \vspace{0.5cm}
    {\fontsize{10pt}{12pt}\selectfont \@major\\The Graduate School\\Kyungpook National University\\(Supervised by Professor \@advisor)}\\
  \end{center}
  \vspace{1.5cm}
  \setstretch{1.6}
  {\fontsize{14pt}{17pt}\selectfont \textbf{Abstract}}\\[0.5cm]
  {\fontsize{11pt}{17pt}\selectfont #1}
  \clearpage
}

%% ============================================================
%% Acknowledgments page
%% ============================================================
\newcommand{\makeacknowledgments}[1]{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{Acknowledgments}
  \thispagestyle{empty}
  \vspace*{2cm}
  \begin{center}
    {\fontsize{16pt}{19pt}\selectfont \textbf{Acknowledgments}}\\
  \end{center}
  \vspace{1.5cm}
  \setstretch{1.6}
  {\fontsize{11pt}{17pt}\selectfont #1}
  \clearpage
}

\makeatother
\endinput
