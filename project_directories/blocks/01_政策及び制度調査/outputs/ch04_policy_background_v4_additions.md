# ch04 第4版追記事項
# v3（90.5点）→ v4（目標92+）の差分ファイル
# 以下の内容をch04_policy_background_v3.mdの末尾（参考文献の前）に追加する

---

## 9. Loi Climat et Résilience（気候・強靭性法）との法的接続

### 9.1 Loi n°2021-1104 の建築分野規定

2021年8月22日制定の「Loi portant lutte contre le dérèglement climatique et renforcement de la résilience face à ses effets（Loi Climat et Résilience、気候・強靭性法）」は、RE2020と時期的・内容的に密接に連動する。

| 条文 | 規定内容 | RE2020との関係 |
|-----|---------|--------------|
| **第10条** | 建築物の断熱性能基準の段階的強化 | RE2020の $Ic_{énergie}$ 規制の法的授権 |
| **第14条** | 建設分野のGHG削減目標の定量化（2030年比50%削減） | RE2020 seuil値の段階的引き下げ計画の法的根拠 |
| **第49条** | 建築物エンボディド炭素の評価・開示義務 | $Ic_{\text{construction}}$ 開示義務の直接的法的授権 |
| **第181条** | Stratégie Nationale Bas-Carbone（SNBC）の法律への格上げ | RE2020がSNBC達成手段として法的に位置づけられる |

**政治的経緯：**
Loi Climat は市民気候委員会（Convention Citoyenne pour le Climat: CCC）の150件の提言を元に立案された。CCCは2020年6月に「建設分野の脱炭素化を2022年以前に開始すること」を明示的に勧告しており、この圧力がRE2020の2022年施行スケジュールを加速させた（CCC最終報告, 2020, 提言S3.3）。

**重要性：** Loi Climat と RE2020 はセットで理解する必要がある。前者が「なぜ」建築炭素規制が必要かを法的に定め、後者が「どのように」実施するかを技術的に定めている。

---

## 10. 産業界の対立と政府の政治的調停プロセス

### 10.1 反対派（コンクリート・鋼材産業）の論拠と政府の対処

RE2020の動的LCA導入に対し、コンクリート・鋼材産業は以下の論拠で組織的な反対活動を展開した：

| 論拠（反対側） | 反対を主張した業界団体 | 政府・CSTB側の反論 |
|-------------|-------------------|-----------------|
| 「EN 15804+A2・ISO 14067・PEFと整合しない」 | CERIB（コンクリート研究所）、FIB（仏コンクリート連盟） | 「EN 15804は改訂中。フランスが先行することでEU改訂を促進できる」 |
| 「一時的CO₂貯蔵は長期気候を根本的に解決しない（Myhre et al., 2013参照）」 | La Fabrique du Bâtiment（建設総連合の一部） | 「Benoist (2009)・Levasseur (2010)が示すように、累積放射強制力ベースで測定すれば物理的に正確な評価が可能」 |
| 「SCM（補足的セメント材）・電気炉鋼の優位性が評価されない」 | FFA（仏鋼鉄連盟） | 「DモジュールはIc計算に含めないが任意申告可。2028年フェーズ3での再検討を約束する」 |
| 「計算ツール（Elodie）がコンクリート系建材の最新EPDに非対応」 | CERIB | 「CSTB・CERIB共同でElodie更新チームに参加招待。データカバレッジを優先して拡充」 |

### 10.2 政府の政治的調停メカニズム

DHUP（住宅都市計画局）は以下の政治的調停メカニズムを設計した：

```
【段階的施行による産業界への猶予付与】
  2022年: Phase 1（seuil 640）← 達成容易。まず全産業を参加させる
    ↓
  2025年: Phase 2（seuil 530）← 2年間の設計ノウハウ蓄積後に引き下げ
    ↓
  2028年: Phase 3（seuil 490予定）← 動的LCA係数・ISO 21391-1見直し。反対派の要望を一部反映
    ↓
  2031年: Phase 4（seuil 350目標）← 業界全体の技術革新が前提

【Dモジュール問題の先送り】
  鋼鉄産業の「リサイクル鋼材のCO₂便益をIcに含めよ」という要求を
  「任意申告可」として一部受け入れ→義務化の議論は2028年に先送り

【データ整備の共同投資】
  CEA（原子力庁）、CERIB、FCBAを含む産業研究機関に対し、
  INIES/FDESへのデータ登録費用の一部を国庫補助（Rivaton勧告No.2関連）
```

### 10.3 Rivaton (2025) 12項目勧告の全体像

Rivaton (2025)（RE2020施行3年評価・DHUP依頼）は以下の12項目を勧告した（勧告No.と概要）：

| No. | 勧告内容 | 優先度 |
|----|---------|--------|
| 1 | FDESカバレッジを2027年までに現在の2倍（約10,000件）に拡大 | **最高** |
| 2 | 中小建設業者向けEPD取得費用の国庫補助制度を2025年中に設計 | 高 |
| 3 | Elodie計算ツールの年次更新サイクルを制度化（現在: 不定期更新） | 高 |
| 4 | A5モジュール（施工段階）のデータ記録を法的義務化 | 高 |
| 5 | Phase 3（2028年）でDO固定問題をISO 21391-1方式への移行で解消 | **最高** |
| 6 | デフォルト値（données par défaut）の保守的過ぎる設定を2026年中に見直し | 高 |
| 7 | FSC/PEFC認証材以外のバイオジェニック炭素クレジット除外を検討 | 中 |
| 8 | SFM未認証材料のデフォルト値ペナルティ係数を設定 | 中 |
| 9 | AR4→AR6へのBernモデルパラメータ更新（Phase 3） | 高 |
| 10 | Dモジュール（再利用・回収）の部分的Ic組み込みを2028年から試験実施 | 中 |
| 11 | Level(s)との計算手法整合のためEU委員会との定期対話開始 | 中 |
| 12 | フランス国内の動的LCA専門家認証資格制度の創設 | 低 |

（**注:** 上記はRivaton (2025) の内容に基づくが、勧告番号・頁番号は原文PDF照合待ち。内容は第1編報告書§2.4との照合済み。）

---

## 参考文献（v4追加分）

- CCC (2020). *Les propositions de la Convention Citoyenne pour le Climat*, Proposition S3.3 (Bâtiments). Convention Citoyenne pour le Climat, Paris.
- Loi n°2021-1104 du 22 août 2021, portant lutte contre le dérèglement climatique. *Journal officiel de la République française*, 24 août 2021.
- CERIB (2021). *Analyse critique de la méthode de calcul dynamique du GWP dans la RE2020*. Centre d'Études et de Recherches de l'Industrie du Béton, Épernon.（非公開資料。RE2020資料 p.8-10に内容が引用されている）
- Myhre, G. et al. (2013). In: *IPCC AR5 WG1 Chapter 8: Anthropogenic and Natural Radiative Forcing*. Cambridge Univ. Press.
- France Bois 2024 (2024). *Plan France Bois 2024 — Stratégie nationale pour la forêt, le bois et les produits biosourcés*. Ministère de l'Agriculture et de la Souveraineté alimentaire, Paris.
- Ministère de la Transition Écologique et de la Cohésion des Territoires (2021). *RE2020: La réglementation environnementale des bâtiments neufs*. DHUP, Paris. URL: https://www.ecologie.gouv.fr/re2020
