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
\RequirePackage{pdflscape}
\RequirePackage{tikz}

%% Circled Korean 인 (seal mark)
\newcommand{\circledin}{%
  \tikz[baseline=(char.base)]{%
    \node[shape=circle, draw, inner sep=1pt, minimum size=1.2em] (char)
      {\koreanfont\fontsize{9pt}{9pt}\selectfont 인};%
  }%
}
\RequirePackage[titles]{tocloft}

%% Geometry: custom paper size 19cm x 26cm, reduced margins
\RequirePackage[
  paperwidth=19cm,
  paperheight=26cm,
  left=25mm,
  right=25mm,
  top=25mm,
  bottom=25mm,
  headheight=12mm,
  footskip=12mm
]{geometry}

%% ============================================================
%% Page number style: -- N -- (centered footer, no header)
%% ============================================================
\RequirePackage{fancyhdr}
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{-- \thepage\ --}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}
\pagestyle{plain}

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

%% Chapter title format (left-aligned, matching reference)
\makeatletter
\renewcommand{\@makechapterhead}[1]{%
  \vspace*{20pt}%
  {\parindent 0pt \raggedright
    \normalfont\fontsize{20pt}{24pt}\selectfont\bfseries
    \chaptername\ \thechapter\par
    \vskip 8pt
    \fontsize{22pt}{26pt}\selectfont\bfseries #1\par
    \nobreak
    \vskip 25pt
  }%
}
\renewcommand{\@makeschapterhead}[1]{%
  \vspace*{20pt}%
  {\parindent 0pt \centering
    \normalfont\fontsize{20pt}{24pt}\selectfont\bfseries #1\par
    \nobreak
    \vskip 25pt
  }%
}

%% ============================================================
%% Table of Contents formatting (matching reference dissertation)
%% ============================================================

%% TOC/LOT/LOF title vertical spacing
\setlength{\cftbeforetoctitleskip}{0pt}
\setlength{\cftaftertoctitleskip}{20pt}
\setlength{\cftbeforelottitleskip}{0pt}
\setlength{\cftafterlottitleskip}{20pt}
\setlength{\cftbeforeloftitleskip}{0pt}
\setlength{\cftafterloftitleskip}{20pt}

%% TOC title: "Contents", centered, 17pt bold
\renewcommand{\contentsname}{Contents}
\renewcommand{\cfttoctitlefont}{\hfil\fontsize{17pt}{20pt}\selectfont\bfseries}
\renewcommand{\cftaftertoctitle}{\hfil}

%% LOT title: "List of Tables", centered, 17pt bold
\renewcommand{\cftlottitlefont}{\hfil\fontsize{17pt}{20pt}\selectfont\bfseries}
\renewcommand{\cftafterlottitle}{\hfil}

%% LOF title: "List of Figures", centered, 17pt bold
\renewcommand{\cftloftitlefont}{\hfil\fontsize{17pt}{20pt}\selectfont\bfseries}
\renewcommand{\cftafterloftitle}{\hfil}

%% Chapter entries in TOC: bold, no "Chapter" prefix, just number + title
\renewcommand{\cftchapfont}{\bfseries}
\renewcommand{\cftchappagefont}{\bfseries}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}}
\renewcommand{\cftchappresnum}{}
\renewcommand{\cftchapaftersnum}{\hspace{0.5em}}
\setlength{\cftchapnumwidth}{1.5em}

%% Section entries: regular weight, indented
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsecpagefont}{\normalfont}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftsecindent}{1.5em}
\setlength{\cftsecnumwidth}{2.3em}

%% Subsection entries: regular weight, further indented
\renewcommand{\cftsubsecfont}{\normalfont}
\renewcommand{\cftsubsecpagefont}{\normalfont}
\renewcommand{\cftsubsecleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftsubsecindent}{3.8em}
\setlength{\cftsubsecnumwidth}{3.2em}

%% Spacing between TOC entries
\setlength{\cftbeforechapskip}{6pt}
\setlength{\cftbeforesecskip}{1pt}
\setlength{\cftbeforesubsecskip}{1pt}

%% LOT entries: no "Table" prefix, just number + caption
\renewcommand{\cfttabpresnum}{}
\renewcommand{\cfttabaftersnum}{\hspace{0.5em}}
\setlength{\cfttabnumwidth}{2.3em}
\setlength{\cfttabindent}{0em}
\renewcommand{\cfttableader}{\cftdotfill{\cftdotsep}}
\setlength{\cftbeforetabskip}{3pt}

%% LOF entries: no "Figure" prefix, just number + caption
\renewcommand{\cftfigpresnum}{}
\renewcommand{\cftfigaftersnum}{\hspace{0.5em}}
\setlength{\cftfignumwidth}{2.3em}
\setlength{\cftfigindent}{0em}
\renewcommand{\cftfigleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftbeforefigskip}{3pt}

%% Bibliography title
\renewcommand{\bibname}{References}

%% Dot leaders spacing (tighter dots)
\renewcommand{\cftdotsep}{2}

%% TOC depth: show only chapter and section (no subsection in TOC)
\setcounter{tocdepth}{1}

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
    {\fontsize{12pt}{14pt}\selectfont Thesis for the Degree of Ph.D.}\\
    \vspace{3cm}
    {\fontsize{20pt}{24pt}\selectfont \textbf{\@title}}\\
    \vspace{4cm}
    {\fontsize{12pt}{14pt}\selectfont \@major}\\
    {\fontsize{12pt}{14pt}\selectfont The Graduate School}\\
    \vspace{1.5cm}
    {\fontsize{14pt}{17pt}\selectfont \@author}\\
    \vspace{\fill}
    {\fontsize{12pt}{14pt}\selectfont August \@degreeyear}\\
    \vspace{1cm}
    {\fontsize{16pt}{19pt}\selectfont \textbf{The Graduate School}}\\[0.3cm]
    {\fontsize{16pt}{19pt}\selectfont \textbf{Kyungpook National University}}\\
  \end{center}
  \restoregeometry
  \clearpage
}

%% ============================================================
%% Spine page (landscape, for book binding)
%% ============================================================
\newcommand{\makespinepage}{%
  \thispagestyle{empty}
  \newgeometry{left=0.5cm,top=0.5cm,right=0.5cm,bottom=0.5cm}
  \begin{landscape}
    \vspace*{\fill}
    \noindent\resizebox{\linewidth}{!}{%
      \textbf{Systematic Benchmarking and Adaptive Clustering Frameworks for Multi-Scale Genomic Data Analysis%
        \hspace{2cm}%
        \@author%
        \hspace{2cm}%
        \@degreeyear}%
    }
    \vspace*{\fill}
  \end{landscape}
  \restoregeometry
  \clearpage
}

%% ============================================================
%% Inner title page (내표지, print version only)
%% ============================================================
\newcommand{\makeinnertitle}{%
  \thispagestyle{empty}
  \newgeometry{left=2cm,top=2.5cm,right=2cm,bottom=1.5cm}
  \setstretch{1.3}
  \begin{center}
    {\fontsize{20pt}{24pt}\selectfont \textbf{\@title}}\\
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
  \newgeometry{left=2cm,top=2.5cm,right=2cm,bottom=2cm}
  \setstretch{1.0}
  \begin{center}
    %% Title (use parbox to allow natural line wrapping)
    {\fontsize{16pt}{20pt}\selectfont \textbf{\@title}}\\
    \vspace{1.2cm}
    %% Author
    {\fontsize{14pt}{17pt}\selectfont \@author}\\
    \vspace{0.8cm}
    %% Department + Graduate School
    {\fontsize{11pt}{14pt}\selectfont \@major\\
    The Graduate School}\\
    \vspace{0.8cm}
    %% Supervisor
    {\fontsize{11pt}{14pt}\selectfont Supervised by Professor \@advisor}\\
    \vspace{0.8cm}
    %% Approval text
    {\fontsize{11pt}{14pt}\selectfont
      Approved as a qualified thesis of \@author\\
      for the degree of Ph.D.\\
      by the Evaluation Committee}\\
    \vspace{0.8cm}
    %% Date
    {\fontsize{11pt}{14pt}\selectfont August \@degreeyear}\\
    \vspace{1.2cm}
    %% Committee signatures — right-aligned block
  \end{center}
  \vspace{0.5cm}
  \vspace{0.5cm}
  \begin{flushright}
    {\fontsize{11pt}{14pt}\selectfont
      Chairman\hspace{0.2cm}\underline{\makebox[4.5cm]{\@committeechairman}}\hspace{0.3cm}\circledin\mbox{\hspace{1.0cm}}\\[0.7cm]
      \phantom{Chairman}\hspace{0.2cm}\underline{\makebox[4.5cm]{\@committeememberA}}\hspace{0.3cm}\circledin\mbox{\hspace{1.0cm}}\\[0.7cm]
      \phantom{Chairman}\hspace{0.2cm}\underline{\makebox[4.5cm]{\@committeememberB}}\hspace{0.3cm}\circledin\mbox{\hspace{1.0cm}}\\[0.7cm]
      \phantom{Chairman}\hspace{0.2cm}\underline{\makebox[4.5cm]{\@committeememberC}}\hspace{0.3cm}\circledin\mbox{\hspace{1.0cm}}\\[0.7cm]
      \phantom{Chairman}\hspace{0.2cm}\underline{\makebox[4.5cm]{\@committeememberD}}\hspace{0.3cm}\circledin\mbox{\hspace{1.0cm}}\\
    }
  \end{flushright}
  \begin{center}
    \vfill
    %% Institution
    {\fontsize{14pt}{17pt}\selectfont \textbf{The Graduate School Council}}\\[0.3cm]
    {\fontsize{14pt}{17pt}\selectfont \textbf{Kyungpook National University}}\\[1cm]
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
  \addcontentsline{toc}{chapter}{Abstract (Korean)}
  \thispagestyle{plain}
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
  \chapter*{Abstract}
  \setstretch{1.6}
  {\fontsize{11pt}{17pt}\selectfont #1}
  \clearpage
}

%% ============================================================
%% Acknowledgments page (kept for compatibility but not used)
%% ============================================================
\newcommand{\makeacknowledgments}[1]{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{Acknowledgments}
  \thispagestyle{plain}
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
