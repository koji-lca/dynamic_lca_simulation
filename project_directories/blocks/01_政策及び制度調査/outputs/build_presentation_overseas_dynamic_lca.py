#!/usr/bin/env python3
"""Generate 20-min presentation PPTX for overseas dynamic LCA trends."""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

OUTPUT = Path(__file__).parent / "presentation_海外動的LCA動向_20min.pptx"

SLIDES = [
    {
        "title": "海外における動的LCAの動きとその意味",
        "bullets": [
            "なぜ導入され、導入後に何が変わったのか",
            "調査項目(1) 政策・制度調査｜第1係",
            "2026年5月（ドラフト）｜想定20分・14枚",
        ],
        "notes": "本日はフランスを中心に、米国・EUの文脈も含め海外動向を整理します。",
    },
    {
        "title": "本日のゴール",
        "bullets": [
            "① なぜ海外（特にフランス）で動的LCAが政策の中心になったか",
            "② どう制度化されたか（RE2020の要点）",
            "③ 導入後、産業・設計・数値にどんな影響が出ているか",
            "※算定式の詳細・INIESは他係で扱う",
        ],
        "notes": "聴き取りの軸を3点に絞ります。",
    },
    {
        "title": "世界の流れ：建築の炭素を「見える化」",
        "bullets": [
            "運用エネルギー効率化は各国で進展 → 残る大きな論点はエンボディド炭素",
            "ネットゼロ整合：建物はライフサイクル全体で説明責任",
            "フランス：RE2020で建築物LCA義務化＋簡易動的LCA",
            "EU：Level(s)・EN15978で共通枠組み",
            "米国：Buy Clean・LEED v5・EPA低炭素建材ラベル",
        ],
        "notes": "入り口は違うが、材料・時間・データが共通課題です。",
    },
    {
        "title": "静的LCAだけでは足りない理由",
        "bullets": [
            "GWP100：全排出を同時に集約 → 比較しやすいが時間構造を失う",
            "建築・木材の論点：一時的炭素貯蔵／遅延排出／生物由来CO₂",
            "学術：Levasseur et al.(2010,2013) 動的LCI＋動的LCIA（累積放射強制力）",
            "フランスはこれを規制向けに「簡略化」して採用",
        ],
        "notes": "静的は国際標準の強み。動的は時間の論点に応える試みです。",
    },
    {
        "title": "海外マップ：どこまで「動的」か",
        "bullets": [
            "規制で動的採用 → フランス RE2020（簡易動的LCA・義務）",
            "LCA枠組み → EU Level(s) / EN15978",
            "調達・認証 → 米国 Buy Clean / LEED v5 / 州条例",
            "研究・ツール → カナダ CIRAIG DynCO₂ 等",
        ],
        "notes": "動的LCA＝学術概念と、規制の簡易版を分けて見ることが重要です。",
    },
    {
        "title": "フランス RE2020：何が変わったか",
        "bullets": [
            "RT2012 → RE2020：環境性能が第3の柱（ライフサイクルACV）",
            "規制指標：GES（kgCO₂eq/m²）— 2025 -15% / 2028 -25% / 2031 -30〜40%",
            "2022年〜段階適用（住宅→事務所・学校→小規模等）",
            "データ基盤：INIES・FDES（フランスEPD）",
        ],
        "notes": "Cerema Guide 2024に基づく制度概要です。",
    },
    {
        "title": "なぜ「簡易動的LCA」か",
        "bullets": [
            "狙い：排出タイミングを反映しつつ、既存静的LCA・EPDを活用",
            "混合：建設前＝静的／建設以降（原則50年）＝簡易動的",
            "時間原点 t=0：建物引渡し｜観測：建設から100年",
            "算式：GWPdyn(t) = FRE2020(t) × GWPstat100",
            "2021年：標準化手続き表明／大学勧告は係数・期間の修正を提案",
        ],
        "notes": "Ventura & Feraille 2021、RE2020 Dynamic LCA資料が根拠です。",
    },
    {
        "title": "数値で見る「時間地平」の威力",
        "bullets": [
            "1kg CO₂を50年貯蔵：100年地平→0.42kg相当／150年→0.27kg（約35%減）",
            "制度が選ぶ年数＝政策メッセージ（木材優位の度合いが変わる）",
            "Ventura(2022)：50年時点で係数が最大約25%過大になり得る",
            "木材団体＝支持｜セメント・金属等＝国際標準との不整合を主張",
        ],
        "notes": "ステークホルダー対立の核心は「一時貯蔵を緩和とみなすか」です。",
    },
    {
        "title": "RE2020導入後の影響",
        "bullets": [
            "設計：部材炭素が規制値と直結 → 木造CLT vs コンクリートの順位が変化",
            "産業：FDES/INIES需要増・各素材団体の反対運動",
            "政策：段階目標を動的GESでモニタリング",
            "2025 Rivaton報告：ACVルール・データ品質・コストを評価し12項目勧告",
            "国際：EN15804/PEF/ISO14067（一時貯蔵除外）との緊張が継続",
        ],
        "notes": "木造化義務そのものではなく、評価手法が設計インセンティブになり得ます。",
    },
    {
        "title": "アメリカ：同じ課題、異なる答え",
        "bullets": [
            "建築法での動的LCA全国義務は未整備",
            "Buy Clean：連邦調達で低炭素建材・EPD優先",
            "EPA低炭素建材ラベル(2024)：PCR・バイオジェニック開示要件",
            "LEED v5(2025〜)：エンボディド炭素LCAを前提化",
            "州・都市条例は分断的 → 静的GWP＋開示から開始",
        ],
        "notes": "米国は調達・認証で押し上げ。バイオジェニック論点は避けられません。",
    },
    {
        "title": "フランス vs 米国",
        "bullets": [
            "義務の形：規制(RE2020) vs 調達・認証・州法",
            "時間軸：簡易動的LCA vs 原則静的GWP",
            "木材：制度クレジット vs 開示・事例依存",
            "産業政治：セメントvs木材の公開論戦 vs 鋼・コンクリート中心",
            "日本示唆：年数・起点の合意と、段階導入・国DBをセット設計",
        ],
        "notes": "比較表で「同じ論点・違う制度化の入り口」を示します。",
    },
    {
        "title": "EU・研究（補足）",
        "bullets": [
            "EU Level(s)/EN15978：建築LCAの共通フレーム",
            "動的LCAの統一義務はフランスが先行",
            "CIRAIG DynCO₂：RE2020係数の理論的源流",
            "参照時は「学術の完全版」と「規制の簡易版」を意図的に分離",
        ],
        "notes": "1分で補足。詳細はNo.3（Level(s)）で深掘り予定。",
    },
    {
        "title": "日本の建築物LCA制度化への示唆",
        "bullets": [
            "時間の設計が本体（THI/TOD・起点）→ 導入前の合意が必要",
            "段階導入：静的＋簡易動的（仏）／開示・調達先行（米）",
            "林野・木材：評価方法は木造インセンティブになり得るが、起源証明とセット",
            "第3係：国DB・炭素フローとの接続が前提",
        ],
        "notes": "日本は両国の「中間」も可能。まず地平の合意を推奨します。",
    },
    {
        "title": "まとめ・次ステップ",
        "bullets": [
            "海外＝エンボディド炭素をLCAで制度・市場に載せるフェーズ",
            "フランス＝簡易動的LCAを建築規制の中心に置いた先進事例",
            "米国＝EPD・調達・LEEDで押上げ、動的統一は未整備",
            "第1係次：政令照合・導入背景・Level(s)対照・ヒアリング論点",
        ],
        "notes": "質疑：日本導入は時間地平とデータ基盤の合意が先。",
    },
]


def add_slide(prs: Presentation, data: dict) -> None:
    layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = data["title"]
    body = slide.placeholders[1].text_frame
    body.clear()
    for i, bullet in enumerate(data["bullets"]):
        p = body.paragraphs[0] if i == 0 else body.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(20)
    if data.get("notes"):
        slide.notes_slide.notes_text_frame.text = data["notes"]


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    for slide_data in SLIDES:
        add_slide(prs, slide_data)
    prs.save(OUTPUT)
    print(f"Wrote {OUTPUT} ({len(SLIDES)} slides)")


if __name__ == "__main__":
    main()
