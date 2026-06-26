# -*- coding: utf-8 -*-
preamble = r"""% !TEX program = lualatex
% Overleaf: メニューの Menu > Compiler を「LuaLaTeX」に設定してコンパイルしてください。
\documentclass[11pt]{ltjsarticle}
\usepackage{luatexja-fontspec}
\usepackage{amsmath,amssymb}
\usepackage{longtable,booktabs,array}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fancyvrb}
\usepackage[margin=20mm]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{newunicodechar}

% pandoc 互換マクロ
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\passthrough}[1]{#1}

% Unicode 下付き・上付き・記号のフォールバック（フォント欠落対策）
\newunicodechar{₀}{\textsubscript{0}}
\newunicodechar{₁}{\textsubscript{1}}
\newunicodechar{₂}{\textsubscript{2}}
\newunicodechar{₃}{\textsubscript{3}}
\newunicodechar{₄}{\textsubscript{4}}
\newunicodechar{₅}{\textsubscript{5}}
\newunicodechar{₆}{\textsubscript{6}}
\newunicodechar{₇}{\textsubscript{7}}
\newunicodechar{₈}{\textsubscript{8}}
\newunicodechar{₉}{\textsubscript{9}}
\newunicodechar{⁰}{\textsuperscript{0}}
\newunicodechar{¹}{\textsuperscript{1}}
\newunicodechar{²}{\textsuperscript{2}}
\newunicodechar{³}{\textsuperscript{3}}
\newunicodechar{⁴}{\textsuperscript{4}}
\newunicodechar{⁵}{\textsuperscript{5}}
\newunicodechar{⁶}{\textsuperscript{6}}
\newunicodechar{⁷}{\textsuperscript{7}}
\newunicodechar{⁸}{\textsuperscript{8}}
\newunicodechar{⁹}{\textsuperscript{9}}
\newunicodechar{⁻}{\textsuperscript{-}}
\newunicodechar{→}{\ensuremath{\rightarrow}}
\newunicodechar{×}{\ensuremath{\times}}
\newunicodechar{−}{\ensuremath{-}}
\newunicodechar{≈}{\ensuremath{\approx}}
\newunicodechar{≤}{\ensuremath{\leq}}
\newunicodechar{≥}{\ensuremath{\geq}}
\newunicodechar{·}{\ensuremath{\cdot}}
\newunicodechar{≒}{\ensuremath{\fallingdotseq}}

\title{TITLEPLACEHOLDER}
\author{一般社団法人サステナブル経営推進機構（SuMPO）}
\date{2026年6月15日（PMO整合性レビュー反映版 v2）}

\begin{document}
\maketitle
"""

import sys
bodyfile, outfile, title = sys.argv[1], sys.argv[2], sys.argv[3]
body = open(bodyfile, encoding='utf-8').read()
pre = preamble.replace('TITLEPLACEHOLDER', title)
open(outfile,'w',encoding='utf-8').write(pre + "\n" + body + "\n\\end{document}\n")
print("wrote", outfile)
