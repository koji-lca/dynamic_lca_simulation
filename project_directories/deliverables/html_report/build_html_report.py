"""
build_html_report.py
調査ブロック①② MD報告書 → SuMPO ブランド マルチページ HTML 変換スクリプト
"""
import os
import re
import markdown
from datetime import datetime

# ─── Paths ─────────────────────────────────────────────────────────────────────
HERE    = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.abspath(os.path.join(HERE, '..', '..'))
S1_OUT  = os.path.join(ROOT, 'blocks', '01_政策及び制度調査', 'outputs')
S2_OUT  = os.path.join(ROOT, 'blocks', '02_技術及び手法調査', 'outputs')
PMO_DIR = os.path.join(ROOT, 'pmo', 'integration')

OUT       = HERE
ASSETS    = os.path.join(OUT, 'assets')
S1_HTML   = os.path.join(OUT, 'survey1')
S2_HTML   = os.path.join(OUT, 'survey2')
PMO_HTML  = os.path.join(OUT, 'pmo')

for d in [ASSETS, S1_HTML, S2_HTML, PMO_HTML]:
    os.makedirs(d, exist_ok=True)

GENERATED = datetime.now().strftime('%Y年%m月%d日 %H:%M')

# ─── Navigation definition ─────────────────────────────────────────────────────
NAV = [
    {
        'label': '調査ブロック①  政策及び制度調査',
        'prefix': '../survey1/',
        'items': [
            ('ch01.html', 'No.1-3・8　RE2020全体構造'),
            ('ch02.html', 'No.9-11　動的LCA要件整理'),
            ('ch03.html', 'No.12-14　生物由来炭素・炭素貯蔵'),
            ('ch04.html', 'No.4-7　制度導入背景（v4統合）'),
        ]
    },
    {
        'label': '調査ブロック②  技術及び手法調査',
        'prefix': '../survey2/',
        'items': [
            ('tech01.html', 'No.15-17　動的LCAの理論的枠組み'),
            ('tech02.html', 'No.18-20　評価指標・算定方法'),
            ('tech03.html', 'No.21-23　建築物LCA位置付け'),
        ]
    },
    {
        'label': 'PMO評価',
        'prefix': '../pmo/',
        'items': [
            ('evaluation_survey1.html', '調査ブロック①　PMO評価'),
            ('evaluation_survey2.html', '調査ブロック②　PMO評価'),
        ]
    },
]

# ─── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
:root {
  --nav-w: 260px;
  --hdr-h: 56px;
  --blue:  #0057BA;
  --dblue: #125486;
  --navy:  #193950;
  --silver:#C5C9CD;
  --gray:  #f4f6f8;
  --text:  #1a1a2e;
  --muted: #555;
  --code-bg: #f0f3f6;
  --border: #dde2e8;
  --radius: 6px;
  --shadow: 0 2px 8px rgba(0,0,0,.12);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', sans-serif;
       color: var(--text); background: #fff; font-size: 15px; line-height: 1.7; }

/* ── Header ── */
#hdr { position: fixed; top: 0; left: 0; right: 0; height: var(--hdr-h);
       background: var(--navy); color: #fff;
       display: flex; align-items: center; padding: 0 24px;
       z-index: 200; box-shadow: var(--shadow); gap: 16px; }
#hdr .org { font-size: 13px; opacity: .7; white-space: nowrap; }
#hdr .title { font-size: 16px; font-weight: 700; letter-spacing: .03em; }
#hdr a { color: #fff; text-decoration: none; }
#hdr a:hover { text-decoration: underline; }

/* ── Sidebar ── */
#sidebar { position: fixed; top: var(--hdr-h); left: 0; bottom: 0;
           width: var(--nav-w); background: var(--gray);
           border-right: 1px solid var(--border);
           overflow-y: auto; padding: 16px 0; z-index: 100; }
.nav-group { margin-bottom: 8px; }
.nav-group-label { font-size: 11px; font-weight: 700; color: var(--navy);
                   letter-spacing: .08em; text-transform: uppercase;
                   padding: 12px 16px 4px; }
.nav-group a { display: block; font-size: 13px; color: var(--text);
               padding: 6px 16px 6px 20px; text-decoration: none;
               border-left: 3px solid transparent;
               transition: background .15s, border-color .15s; }
.nav-group a:hover { background: #e8ecf0; border-left-color: var(--blue); }
.nav-group a.active { background: #dce8f5; border-left-color: var(--blue);
                      color: var(--dblue); font-weight: 600; }
.nav-home { display: block; font-size: 13px; font-weight: 700; color: var(--navy);
            padding: 8px 16px 12px; text-decoration: none;
            border-bottom: 1px solid var(--border); margin-bottom: 8px; }
.nav-home:hover { color: var(--blue); }

/* ── Main ── */
#main { margin-left: var(--nav-w); padding-top: var(--hdr-h); min-height: 100vh; }
#content { max-width: 880px; margin: 0 auto; padding: 36px 40px 80px; }

/* ── Breadcrumb ── */
.breadcrumb { font-size: 12px; color: var(--muted); margin-bottom: 20px; }
.breadcrumb a { color: var(--blue); text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb span { margin: 0 6px; }

/* ── Typography ── */
h1 { font-size: 1.8rem; color: var(--navy); border-bottom: 3px solid var(--blue);
     padding-bottom: 10px; margin: 0 0 28px; line-height: 1.3; }
h2 { font-size: 1.25rem; color: var(--dblue); border-left: 4px solid var(--blue);
     padding-left: 12px; margin: 36px 0 14px; }
h3 { font-size: 1.05rem; color: var(--navy); margin: 28px 0 10px; }
h4 { font-size: .95rem; color: var(--dblue); margin: 20px 0 8px; }
p  { margin: 0 0 14px; }
ul, ol { margin: 0 0 14px 22px; }
li { margin-bottom: 4px; }
a  { color: var(--blue); }

/* ── Code ── */
code { background: var(--code-bg); border-radius: 3px; padding: 1px 5px;
       font-size: .88em; font-family: 'Fira Code', 'Courier New', monospace; }
pre  { background: var(--code-bg); border: 1px solid var(--border);
       border-radius: var(--radius); padding: 16px; overflow-x: auto;
       margin: 0 0 18px; line-height: 1.5; }
pre code { background: none; padding: 0; font-size: .87em; }

/* ── Tables ── */
table { border-collapse: collapse; width: 100%; margin: 0 0 20px;
        font-size: .9em; box-shadow: var(--shadow); border-radius: var(--radius);
        overflow: hidden; }
thead tr { background: var(--navy); color: #fff; }
thead th { padding: 10px 14px; text-align: left; font-weight: 600; }
tbody tr:nth-child(even) { background: var(--gray); }
tbody tr:hover { background: #dce8f5; }
td, th { padding: 9px 14px; border-bottom: 1px solid var(--border); }

/* ── Blockquote ── */
blockquote { border-left: 4px solid var(--blue); background: #eef4fb;
             padding: 12px 16px; margin: 0 0 16px; border-radius: 0 var(--radius) var(--radius) 0; }
blockquote p { margin: 0; color: var(--dblue); }

/* ── Score card (PMO) ── */
.score-card { display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }
.score-item { background: var(--gray); border: 1px solid var(--border);
              border-radius: var(--radius); padding: 16px 20px; text-align: center;
              min-width: 140px; flex: 1; }
.score-item .num { font-size: 2.4rem; font-weight: 800; color: var(--blue); line-height: 1; }
.score-item .lbl { font-size: 12px; color: var(--muted); margin-top: 4px; }
.score-item.pass .num { color: #1a8a3a; }

/* ── Section badge ── */
.section-badge { display: inline-block; background: var(--blue); color: #fff;
                 font-size: 11px; font-weight: 700; padding: 2px 8px;
                 border-radius: 3px; margin-right: 8px; letter-spacing: .05em; }

/* ── Footer ── */
#footer { text-align: center; font-size: 12px; color: var(--muted);
          padding: 20px; border-top: 1px solid var(--border);
          background: var(--gray); margin-left: var(--nav-w); }

/* ── Math (KaTeX) ── */
.math-block { overflow-x: auto; margin: 16px 0; padding: 12px; background: var(--code-bg);
              border-radius: var(--radius); border: 1px solid var(--border); }
.katex-display { overflow: auto hidden; }

/* ── Figures ── */
.fig-block { margin: 28px 0; }
.fig-block img { width: 100%; height: auto; border: 1px solid var(--border);
                 border-radius: var(--radius); box-shadow: var(--shadow);
                 cursor: zoom-in; transition: opacity .15s; }
.fig-block img:hover { opacity: .88; }
.fig-caption { font-size: .85em; color: var(--muted); margin-top: 8px;
               text-align: center; font-style: italic; }
.fig-caption strong { color: var(--navy); font-style: normal; }
.fig-section-title { font-size: 1.1rem; font-weight: 700; color: var(--navy);
                     border-left: 4px solid var(--blue); padding-left: 12px;
                     margin: 40px 0 18px; }

/* ── Lightbox ── */
#lb-overlay { display: none; position: fixed; inset: 0; z-index: 9000;
              background: rgba(0,0,0,.82); align-items: center;
              justify-content: center; cursor: zoom-out; padding: 24px; }
#lb-overlay.open { display: flex; }
#lb-overlay img { max-width: 92vw; max-height: 90vh; object-fit: contain;
                  border-radius: var(--radius); box-shadow: 0 4px 32px rgba(0,0,0,.5);
                  cursor: default; }
#lb-caption { position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
              background: rgba(0,0,0,.65); color: #eee; font-size: .82em;
              padding: 6px 16px; border-radius: 20px; max-width: 80vw;
              text-align: center; pointer-events: none; }
#lb-close { position: fixed; top: 16px; right: 20px; color: #fff; font-size: 2rem;
            line-height: 1; cursor: pointer; user-select: none;
            text-shadow: 0 1px 4px rgba(0,0,0,.6); }

/* ── Responsive ── */
@media (max-width: 720px) {
  #sidebar { display: none; }
  #main, #footer { margin-left: 0; }
  #content { padding: 24px 16px 60px; }
}
"""

# ─── HTML template ─────────────────────────────────────────────────────────────

def make_sidebar(current_file: str, depth: int = 1) -> str:
    prefix = '../' * depth
    lines = [f'<a class="nav-home" href="{prefix}index.html">🏠 トップページ</a>']
    for group in NAV:
        lines.append('<div class="nav-group">')
        lines.append(f'  <div class="nav-group-label">{group["label"]}</div>')
        for fname, label in group['items']:
            full = group['prefix'].lstrip('../') + fname
            href = prefix + full
            active = 'active' if fname == current_file else ''
            lines.append(f'  <a href="{href}" class="{active}">{label}</a>')
        lines.append('</div>')
    return '\n'.join(lines)


def page(title: str, breadcrumb_html: str, body_html: str,
         current_file: str, depth: int = 1) -> str:
    sidebar = make_sidebar(current_file, depth)
    prefix  = '../' * depth
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | SuMPO 動的LCA調査報告</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body,{{delimiters:[
      {{left:'$$',right:'$$',display:true}},
      {{left:'$',right:'$',display:false}}
    ]}})"></script>
</head>
<body>
<header id="hdr">
  <span class="title"><a href="{prefix}index.html">SuMPO 動的LCA調査報告書</a></span>
  <span class="org">一般社団法人サステナブル経営推進機構</span>
</header>
<nav id="sidebar">
{sidebar}
</nav>
<main id="main">
  <div id="content">
    <div class="breadcrumb">{breadcrumb_html}</div>
    {body_html}
  </div>
</main>
<footer id="footer">
  一般社団法人サステナブル経営推進機構（SuMPO）&emsp;|&emsp;生成日時: {GENERATED}
</footer>

<!-- Lightbox overlay -->
<div id="lb-overlay" role="dialog" aria-modal="true">
  <span id="lb-close" title="閉じる" aria-label="閉じる">&times;</span>
  <img id="lb-img" src="" alt="">
  <div id="lb-caption"></div>
</div>

<script>
(function(){{
  var overlay = document.getElementById('lb-overlay');
  var lbImg   = document.getElementById('lb-img');
  var lbCap   = document.getElementById('lb-caption');
  var lbClose = document.getElementById('lb-close');
  function open(src, alt) {{
    lbImg.src = src; lbImg.alt = alt;
    lbCap.textContent = alt;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }}
  function close() {{
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    lbImg.src = '';
  }}
  document.querySelectorAll('.fig-block img').forEach(function(img) {{
    img.addEventListener('click', function() {{
      var cap = '';
      var capEl = img.closest('.fig-block').querySelector('.fig-caption');
      if (capEl) cap = capEl.textContent.trim();
      open(img.src, cap);
    }});
  }});
  overlay.addEventListener('click', function(e) {{
    if (e.target === overlay || e.target === lbClose) close();
  }});
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') close();
  }});
}})();
</script>
</body>
</html>"""


# ─── MD preprocessing ─────────────────────────────────────────────────────────

MD_EXT = ['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br', 'sane_lists']


def md_to_html(text: str, depth: int = 1) -> str:
    """Convert markdown text to HTML body."""
    # Protect display math $$...$$ from markdown parser
    placeholders = {}
    def protect_math(m):
        key = f'MATHBLOCK{len(placeholders)}MATHBLOCK'
        inner = m.group(1).strip()
        placeholders[key] = f'<div class="math-block">$$\n{inner}\n$$</div>'
        return key
    text = re.sub(r'\$\$(.+?)\$\$', protect_math, text, flags=re.DOTALL)

    html = markdown.markdown(text, extensions=MD_EXT)

    # Restore math placeholders
    for key, val in placeholders.items():
        html = html.replace(key, val)

    # Replace <!-- FIG:filename.png|caption --> markers with inline figure blocks
    def replace_fig_marker(m):
        fname = m.group(1).strip()
        caption = m.group(2).strip()
        return fig_html(fname, caption, depth)
    html = re.sub(r'<!--\s*FIG:([^|]+)\|([^-]+)-->', replace_fig_marker, html)

    return html


def read_md(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


# ─── Figure helpers ─────────────────────────────────────────────────────────────

def fig_html(fname: str, caption: str, depth: int = 1) -> str:
    prefix = '../' * depth
    src = f'{prefix}assets/charts/{fname}'
    fig_id = fname.replace('.png', '')
    return f'''
<div class="fig-block" id="{fig_id}">
  <img src="{src}" alt="{caption}" loading="lazy">
  <p class="fig-caption"><strong>[{fig_id.upper()}]</strong> {caption}</p>
</div>'''


def figs_section(figures: list, label: str = '関連図表', depth: int = 1) -> str:
    if not figures:
        return ''
    inner = ''.join(fig_html(f, c, depth) for f, c in figures)
    return f'\n<h2 class="fig-section-title">📊 {label}</h2>\n{inner}'


# ─── Build each chapter ────────────────────────────────────────────────────────

def build_chapter(out_path: str, title: str, badge: str,
                  breadcrumb: str, md_text: str,
                  current_file: str, depth: int = 1):
    body = f'<span class="section-badge">{badge}</span>\n' + md_to_html(md_text, depth=depth)
    html = page(title, breadcrumb, body, current_file, depth)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ {out_path}')


CRUMB = lambda p, c: f'<a href="{p}index.html">トップ</a><span>›</span>{c}'

def s1_crumb(label):
    return f'<a href="../index.html">トップ</a><span>›</span><a href="../survey1/ch01.html">調査ブロック①</a><span>›</span>{label}'

def s2_crumb(label):
    return f'<a href="../index.html">トップ</a><span>›</span><a href="../survey2/tech01.html">調査ブロック②</a><span>›</span>{label}'

def pmo_crumb(label):
    return f'<a href="../index.html">トップ</a><span>›</span>PMO評価<span>›</span>{label}'


def build_all():
    print('📄 SuMPO HTML Report Builder')
    print(f'   出力先: {OUT}\n')

    # ── CSS ──────────────────────────────────────────────────────────────────
    with open(os.path.join(ASSETS, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(CSS)
    print('  ✅ assets/style.css')

    # ── Survey 1 ─────────────────────────────────────────────────────────────
    print('\n[調査ブロック①]')

    build_chapter(
        os.path.join(S1_HTML, 'ch01.html'),
        'RE2020全体構造', '調査ブロック① No.1-3・8',
        s1_crumb('No.1-3・8　RE2020全体構造'),
        read_md(os.path.join(S1_OUT, 'ch01_re2020_overview.md')),
        'ch01.html')

    build_chapter(
        os.path.join(S1_HTML, 'ch02.html'),
        '動的LCA要件整理', '調査ブロック① No.9-11',
        s1_crumb('No.9-11　動的LCA要件整理'),
        read_md(os.path.join(S1_OUT, 'ch02_dynamic_lca_requirements.md')),
        'ch02.html')

    build_chapter(
        os.path.join(S1_HTML, 'ch03.html'),
        '生物由来炭素・炭素貯蔵', '調査ブロック① No.12-14',
        s1_crumb('No.12-14　生物由来炭素・炭素貯蔵'),
        read_md(os.path.join(S1_OUT, 'ch03_biogenic_carbon_storage.md')),
        'ch03.html')

    # ch04: v3 + v4 additions を結合
    ch04_text = (read_md(os.path.join(S1_OUT, 'ch04_policy_background_v3.md'))
                 + '\n\n---\n\n'
                 + read_md(os.path.join(S1_OUT, 'ch04_policy_background_v4_additions.md')))
    build_chapter(
        os.path.join(S1_HTML, 'ch04.html'),
        '制度導入背景（v4統合）', '調査ブロック① No.4-7',
        s1_crumb('No.4-7　制度導入背景（v4統合）'),
        ch04_text, 'ch04.html')

    # ── Survey 2 ─────────────────────────────────────────────────────────────
    print('\n[調査ブロック②]')

    build_chapter(
        os.path.join(S2_HTML, 'tech01.html'),
        '動的LCAの理論的枠組み', '調査ブロック② No.15-17',
        s2_crumb('No.15-17　動的LCAの理論的枠組み'),
        read_md(os.path.join(S2_OUT, 'tech01_dynamic_lca_concepts_v2.md')),
        'tech01.html')

    build_chapter(
        os.path.join(S2_HTML, 'tech02.html'),
        '評価指標及び算定方法', '調査ブロック② No.18-20',
        s2_crumb('No.18-20　評価指標及び算定方法'),
        read_md(os.path.join(S2_OUT, 'tech02_indicators_calculation_v2.md')),
        'tech02.html')

    build_chapter(
        os.path.join(S2_HTML, 'tech03.html'),
        '建築物LCA算定における位置付け', '調査ブロック② No.21-23',
        s2_crumb('No.21-23　建築物LCA算定における位置付け'),
        read_md(os.path.join(S2_OUT, 'tech03_building_lca_positioning_v2.md')),
        'tech03.html')

    # ── PMO evaluations ───────────────────────────────────────────────────────
    print('\n[PMO評価]')

    pmo1_text = (read_md(os.path.join(PMO_DIR, 'evaluation_ch01_v3_final.md'))
                 + '\n\n---\n\n'
                 + read_md(os.path.join(PMO_DIR, 'evaluation_ch02_ch03_ch04_v2.md'))
                 + '\n\n---\n\n'
                 + read_md(os.path.join(PMO_DIR, 'evaluation_ch04_v4.md')))
    build_chapter(
        os.path.join(PMO_HTML, 'evaluation_survey1.html'),
        '調査ブロック① PMO評価', 'PMO',
        pmo_crumb('調査ブロック① PMO評価'),
        pmo1_text, 'evaluation_survey1.html')

    build_chapter(
        os.path.join(PMO_HTML, 'evaluation_survey2.html'),
        '調査ブロック② PMO評価', 'PMO',
        pmo_crumb('調査ブロック② PMO評価'),
        read_md(os.path.join(PMO_DIR, 'evaluation_tech_v1.md')),
        'evaluation_survey2.html')

    # ── index.html ────────────────────────────────────────────────────────────
    print('\n[index.html]')
    _build_index()


def _build_index():
    cards_s1 = [
        ('survey1/ch01.html', 'No.1-3・8', 'RE2020全体構造',
         'RE2020の3評価指標・seuil値・Level(s)・EN15978との関係。',
         '94.0'),
        ('survey1/ch02.html', 'No.9-11', '動的LCA要件整理',
         'FRE2020(t)=1-0.00842tの制度要件・対象建物・段階施行。',
         '92.0'),
        ('survey1/ch03.html', 'No.12-14', '生物由来炭素・炭素貯蔵',
         'StockC算定・評価期間DO=100年の根拠・解体シナリオ。',
         '92.0'),
        ('survey1/ch04.html', 'No.4-7', '制度導入背景（v4統合）',
         '4条件収束・Loi Climat・産業調停・Rivaton 12勧告。',
         '93.0'),
    ]
    cards_s2 = [
        ('survey2/tech01.html', 'No.15-17', '動的LCAの理論的枠組み',
         'DCF導出・100年評価期間の科学的根拠・ISO 21391-1との比較。',
         '92.8'),
        ('survey2/tech02.html', 'No.18-20', '評価指標及び算定方法',
         '係数0.00842の導出・炭素循環・放射強制力との関係。',
         '93.0'),
        ('survey2/tech03.html', 'No.21-23', '建築物LCA位置付け',
         'Elodieエコシステム・静的LCAのハイブリッド設計・Ic開示制度。',
         '91.2'),
    ]

    def card_html(href, badge, title, desc, score):
        return f"""
<a class="card" href="{href}">
  <div class="card-badge">{badge}</div>
  <div class="card-title">{title}</div>
  <div class="card-desc">{desc}</div>
  <div class="card-score">PMO <strong>{score}</strong> / 100</div>
</a>"""

    s1_cards = ''.join(card_html(*c) for c in cards_s1)
    s2_cards = ''.join(card_html(*c) for c in cards_s2)

    body = f"""
<h1>SuMPO 動的LCA調査報告書</h1>
<p>フランスRE2020における動的LCAの政策的背景・技術的枠組みに関する調査。
   調査ブロック①（政策及び制度調査）と調査ブロック②（技術及び手法調査）の
   全成果物をHTML形式で参照できます。</p>

<div class="score-card" style="margin:28px 0">
  <div class="score-item pass"><div class="num">92.8</div><div class="lbl">調査ブロック①<br>PMO平均スコア</div></div>
  <div class="score-item pass"><div class="num">92.3</div><div class="lbl">調査ブロック②<br>PMO平均スコア</div></div>
  <div class="score-item pass"><div class="num">92.6</div><div class="lbl">両ブロック<br>統合スコア</div></div>
  <div class="score-item"><div class="num">7</div><div class="lbl">成果物数<br>（MD報告書）</div></div>
</div>

<h2>調査ブロック①　政策及び制度調査（No.1〜14）</h2>
<div class="card-grid">{s1_cards}</div>

<h2>調査ブロック②　技術及び手法調査（No.15〜23）</h2>
<div class="card-grid">{s2_cards}</div>

<h2>PMO評価</h2>
<div class="card-grid">
  <a class="card" href="pmo/evaluation_survey1.html">
    <div class="card-badge">PMO</div>
    <div class="card-title">調査ブロック① PMO評価</div>
    <div class="card-desc">ch01〜ch04 各版のスコア履歴・v4最終判定。統合スコア 92.8点。</div>
  </a>
  <a class="card" href="pmo/evaluation_survey2.html">
    <div class="card-badge">PMO</div>
    <div class="card-title">調査ブロック② PMO評価</div>
    <div class="card-desc">tech01〜03 v2 初回評価。全No.15-23カバー確認。統合スコア 92.3点。</div>
  </a>
</div>

<h2 class="fig-section-title">📊 グラフギャラリー（全12図）</h2>
<p style="color:var(--muted);font-size:.9em;margin-bottom:20px">
  Jupyter Notebook（<code>dynamic_lca_visualization.ipynb</code>）および追加分析から生成。
  各図をクリックすると拡大表示できます。
</p>
<div class="gallery-grid">
  <a class="gal-item" href="survey2/tech01.html#fig01_bern_impulse">
    <img src="assets/charts/fig01_bern_impulse.png" loading="lazy">
    <div class="gal-cap">Fig.01 Bern CO₂インパルス応答</div>
  </a>
  <a class="gal-item" href="survey2/tech01.html#fig02_crf_dcf_relationship">
    <img src="assets/charts/fig02_crf_dcf_relationship.png" loading="lazy">
    <div class="gal-cap">Fig.02 CRF/DCF関係（3パネル）</div>
  </a>
  <a class="gal-item" href="survey2/tech02.html#fig03_dcf_re2020_vs_bern">
    <img src="assets/charts/fig03_dcf_re2020_vs_bern.png" loading="lazy">
    <div class="gal-cap">Fig.03 RE2020近似精度比較</div>
  </a>
  <a class="gal-item" href="survey1/ch03.html#fig04_wood_gwp_comparison">
    <img src="assets/charts/fig04_wood_gwp_comparison.png" loading="lazy">
    <div class="gal-cap">Fig.04 木材GWP比較（DO別）</div>
  </a>
  <a class="gal-item" href="survey2/tech03.html#fig05_bern_sensitivity">
    <img src="assets/charts/fig05_bern_sensitivity.png" loading="lazy">
    <div class="gal-cap">Fig.05 Bern感度シミュレーション</div>
  </a>
  <a class="gal-item" href="survey2/tech02.html#fig06_gas_dcf_comparison">
    <img src="assets/charts/fig06_gas_dcf_comparison.png" loading="lazy">
    <div class="gal-cap">Fig.06 CO₂/CH₄/N₂O DCF比較</div>
  </a>
  <a class="gal-item" href="survey2/tech02.html#fig07_module_dcf_impact">
    <img src="assets/charts/fig07_module_dcf_impact.png" loading="lazy">
    <div class="gal-cap">Fig.07 モジュール別DCF・CLT vs RC</div>
  </a>
  <a class="gal-item" href="survey1/ch01.html#fig08_seuil_timeline">
    <img src="assets/charts/fig08_seuil_timeline.png" loading="lazy">
    <div class="gal-cap">Fig.08 RE2020 seuil値タイムライン</div>
  </a>
  <a class="gal-item" href="survey2/tech01.html#fig09_time_horizon_comparison">
    <img src="assets/charts/fig09_time_horizon_comparison.png" loading="lazy">
    <div class="gal-cap">Fig.09 時間地平（HTI）の影響</div>
  </a>
  <a class="gal-item" href="survey1/ch03.html#fig10_biogenic_carbon_cycle">
    <img src="assets/charts/fig10_biogenic_carbon_cycle.png" loading="lazy">
    <div class="gal-cap">Fig.10 バイオジェニック炭素サイクル</div>
  </a>
  <a class="gal-item" href="survey2/tech01.html#fig11_ar4_vs_ar6">
    <img src="assets/charts/fig11_ar4_vs_ar6.png" loading="lazy">
    <div class="gal-cap">Fig.11 AR4 vs AR6 パラメータ比較</div>
  </a>
  <a class="gal-item" href="survey1/ch04.html#fig12_policy_timeline">
    <img src="assets/charts/fig12_policy_timeline.png" loading="lazy">
    <div class="gal-cap">Fig.12 制度化タイムライン</div>
  </a>
</div>
"""

    idx_css = """
.card-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(260px,1fr));
             gap: 16px; margin: 16px 0 32px; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
                gap: 16px; margin: 16px 0 40px; }
.gal-item { display: block; border: 1px solid var(--border); border-radius: var(--radius);
            overflow: hidden; text-decoration: none; color: var(--text);
            box-shadow: var(--shadow); transition: box-shadow .2s, transform .15s; background:#fff; }
.gal-item:hover { box-shadow: 0 6px 20px rgba(0,87,186,.2); transform: translateY(-2px); }
.gal-item img { width: 100%; display: block; height: 180px; object-fit: cover; object-position: top; }
.gal-cap { font-size: .82em; color: var(--navy); padding: 8px 12px; font-weight: 600; }
.card { display: block; background: #fff; border: 1px solid var(--border);
        border-radius: var(--radius); padding: 20px;
        text-decoration: none; color: var(--text);
        box-shadow: var(--shadow); transition: box-shadow .2s, transform .15s; }
.card:hover { box-shadow: 0 6px 20px rgba(0,87,186,.18); transform: translateY(-2px); }
.card-badge { font-size: 11px; font-weight: 700; color: var(--blue);
              text-transform: uppercase; letter-spacing: .08em; margin-bottom: 6px; }
.card-title { font-size: 1rem; font-weight: 700; color: var(--navy); margin-bottom: 6px; }
.card-desc  { font-size: .88em; color: var(--muted); line-height: 1.5; margin-bottom: 10px; }
.card-score { font-size: .82em; color: var(--muted); }
.card-score strong { color: #1a8a3a; font-size: 1.1em; }
"""

    sidebar = make_sidebar('index.html', depth=0)
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SuMPO 動的LCA調査報告書 | トップ</title>
  <link rel="stylesheet" href="assets/style.css">
  <style>{idx_css}</style>
</head>
<body>
<header id="hdr">
  <span class="title">SuMPO 動的LCA調査報告書</span>
  <span class="org">一般社団法人サステナブル経営推進機構</span>
</header>
<nav id="sidebar">{sidebar}</nav>
<main id="main">
  <div id="content">
    <div class="breadcrumb">トップページ</div>
    {body}
  </div>
</main>
<footer id="footer">
  一般社団法人サステナブル経営推進機構（SuMPO）&emsp;|&emsp;生成日時: {GENERATED}
</footer>

<!-- Lightbox overlay -->
<div id="lb-overlay" role="dialog" aria-modal="true">
  <span id="lb-close" title="閉じる" aria-label="閉じる">&times;</span>
  <img id="lb-img" src="" alt="">
  <div id="lb-caption"></div>
</div>

<script>
(function(){{
  var overlay = document.getElementById('lb-overlay');
  var lbImg   = document.getElementById('lb-img');
  var lbCap   = document.getElementById('lb-caption');
  var lbClose = document.getElementById('lb-close');
  function open(src, alt) {{
    lbImg.src = src; lbImg.alt = alt;
    lbCap.textContent = alt;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }}
  function close() {{
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    lbImg.src = '';
  }}
  document.querySelectorAll('.fig-block img, .gallery-item img').forEach(function(img) {{
    img.addEventListener('click', function() {{
      var cap = img.alt || '';
      var capEl = img.closest('.fig-block, .gallery-item');
      if (capEl) {{
        var c = capEl.querySelector('.fig-caption, .gallery-caption');
        if (c) cap = c.textContent.trim();
      }}
      open(img.src, cap);
    }});
  }});
  overlay.addEventListener('click', function(e) {{
    if (e.target === overlay || e.target === lbClose) close();
  }});
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') close();
  }});
}})();
</script>
</body>
</html>"""

    out_path = os.path.join(OUT, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ {out_path}')
    print(f'\n🎉 完了！  open {out_path}')


if __name__ == '__main__':
    build_all()
