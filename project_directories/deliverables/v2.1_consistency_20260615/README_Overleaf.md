# Overleaf 読み込み手順（日本語LaTeX → PDF）

本フォルダの `.tex` は、最新版調査報告書をOverleafでPDF表示するための自己完結ファイルです。

## ファイル
- `ブロック1_政策制度調査_v2.tex`
- `ブロック2_技術手法調査_v2.tex`

（外部画像なし。各ファイル単体で完結します。）

## 手順
1. Overleafで **New Project → Upload Project**（または既存プロジェクトに **Upload**）から `.tex` をアップロード。
2. **Menu → Settings → Compiler** を **「LuaLaTeX」** に変更（**重要**：既定のpdfLaTeXでは日本語が表示されません）。
3. **Recompile** を押すとPDFが表示されます。

## 技術メモ
- 文書クラス: `ltjsarticle`（LuaTeX-ja）。Overleaf標準のTeX Liveに含まれ、原ノ味（Haranoaji）日本語フォントで自動組版されます。
- 表は `longtable` ＋ `booktabs`、下付き・上付き・記号（CO₂、10⁻¹⁴、→、≈ 等）は `newunicodechar` でフォールバック設定済み。
- ローカルでLuaLaTeXの構造コンパイルを実施し、致命的エラー・未定義コマンドが無いことを確認済み（和文フォントはサンドボックスに無いためレンダリングはOverleaf上で確認してください）。

## 代替（XeLaTeXを使う場合）
`ltjsarticle` の代わりに XeLaTeX ＋ `xeCJK` でも組版可能ですが、Overleafでは **LuaLaTeX ＋ `ltjsarticle`** が最も簡単で安定です。
