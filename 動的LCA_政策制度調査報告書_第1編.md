# 動的LCA 政策・制度調査報告書
## 第1編：政策および制度調査
### なぜ動的LCAがフランスで始まったのか — 政治的・科学的背景と国際動向

* **調査主体:** 林野庁委託調査 / 2025年度
* **作成機関:** 一般社団法人サステナブル経営推進機構（SuMPO）
* **作成日:** 2025年6月（第1版）

---

## 目次

* [エグゼクティブサマリー](#エグゼクティブサマリー)
* [第1章 調査の背景と目的](#第1章-調査の背景と目的)
    * 1.1 静的 LCA の限界と「時間問題」
    * 1.2 動的 LCA の登場： Levasseur et al. （ 2010 ）の貢献
    * 1.3 本調査の目的と構成
* [第2章 気候変動政策と国際動向](#第2章-気候変動政策と国際動向)
    * 2.1 EU の建築環境政策フレームワーク
    * 2.2 フランスの政策的文脈：グルネルから RE2020 へ
    * 2.3 フランスにおける動的 LCA 採用の政治経済的背景
    * 2.4 欧州・北米の国際動向
* [第3章 フランス RE2020 の制度構造](#第3章-フランス-re2020-の制度構造)
    * 3.1 3 つの性能指標と法的位置づけ
    * 3.2 ライフサイクルモジュール構造（ EN 15978 準拠）
    * 3.3 動的 LCA 補正係数の定義と実務計算
    * 3.4 RE2020 法制化の経緯：政治的・科学的連携の詳細
    * 3.5 RE2020 の科学的課題と批判的考察
* [第4章 動的 LCA の技術的・数理的基礎](#第4章-動的-lca-の技術的数理的基礎)
    * 4.1 静的 LCA と動的 LCA の数式比較
    * 4.2 動的特性化係数（ DCF ）の定義
    * 4.3 IPCC AR4 Bern2.5CC ： CO₂ 大気中応答モデル
    * 4.4 DCF の数値計算手順
    * 4.5 RE2020 線形近似係数（ 1−0.00842·t ）の導出
    * 4.6 バイオジェニック炭素と動的 LCA の関係
    * 4.7 CLT と一般建材の比較：静的 LCA vs 動的 LCA
* [第5章 日本の LCA 制度との整合性課題](#第5章-日本の-lca-制度との整合性課題)
    * 5.1 日本の現行建築 LCA 制度の概況
    * 5.2 国際標準との整合課題
    * 5.3 日本における動的 LCA 導入に向けた課題と提言
* [第6章 まとめと今後の課題](#第6章-まとめと今後の課題)
    * 6.1 本調査の総括
    * 6.2 今後の調査課題（ SuMPO Tasks 2 〜 4 ）
* [参考文献](#参考文献)

---

## エグゼクティブサマリー

本報告書は、林野庁委託調査（2025年度）の第1編として、動的ライフサイクルアセスメント（動的LCA）が政策・規制の場でどのように導入・普及したか、その政治的・科学的背景を調査・分析したものである。特に、世界初の動的LCA規制として2022年に施行されたフランスのRE2020（Réglementation Environnementale 2020）を中心に据えた。

従来の静的LCAは全排出を評価開始時点 $t=0$ に集中させ、IPCC GWP100を指標とする手法であり（EN 15804、ISO 14067等が準拠）、木材の炭素貯蔵が数十年にわたって継続するという物理的事実を反映できない構造的な限界を持つ。動的LCA（Dynamic LCA）はこの限界を克服し、排出タイミング $t_i$ に応じて動的特性化係数（DCF; Dynamic Characterization Factor）を乗じることで時間軸を明示的に評価に組み込む。

本調査の主要な知見は以下の5点に集約される。

1. **フランスRE2020の実現背景:** Benoist（2009）、Levasseur et al.（2010）、Solinnen（2018）の科学的蓄積と、フランス木材産業（FCBA等）のアドボカシー活動、EU気候政策（European Green Deal）という三位一体の連携によるものである。
2. **核心技術と実務化:** 動的LCAの核心技術は、IPCC AR4 Bern2.5CCモデルに基づく累積放射強制力（CRF）からDCFを導出する数値積分法であり、RE2020はこれを $DCF(t) pprox 1 - 0.00842 \cdot t$ （ $t \le 50$ 年）という線形近似で実務化した。
3. **CLT（直交集成板）の事例:** 静的LCA評価の $+98\text{ kgCO}_2\text{eq/m}^3$ が動的LCAでは $-171\text{ kgCO}_2\text{eq/m}^3$ へと逆転する。この $269\text{ kgCO}_2\text{eq/m}^3$ の差異が木材利用促進政策の定量的根拠となっている。
4. **学術的批判と国際規格:** Ventura & Feraille（2021）は、RE2020の固定DO（時間地平線100年）が遅延ベネフィットを35〜53%過大評価すると批判しており、ISO 21391-1:2025はより厳密な非線形DCFを採用した。
5. **日本の現状:** 日本の建築LCA制度は静的LCAに留まり、動的手法・バイオジェニック炭素の時間評価は未対応である。ISO 21391-1:2025の国内対応とLCAデータベースの整備が急務である。

---

## 第1章　調査の背景と目的

### 1.1　静的LCAの限界と「時間問題」
気候変動対策における建築分野の役割が増大するなか、建築物のライフサイクル全体でのGHG排出量を定量化するLCA（ライフサイクルアセスメント）の重要性は増している。しかし、現行の主要LCA規格（EN 15804、ISO 14067、JIS Q 14025）が準拠する「静的LCA」には根本的な限界がある。

静的LCAにおける気候変動影響（ $PRG_{\text{static}}$ ）は、次の式で定義される：

$$PRG_{\text{static}} = \sum_i prg(x_i) \cdot m_i$$

* $prg(x_i)$ ：物質 $x_i$ の100年統合温暖化係数（GWP100） $[\text{kgCO}_2\text{eq/kg}]$
* $m_i$ ：物質量 $[\text{kg}]$

この式のきわめて重要な特性は、全ての排出・吸収フローが評価開始時点（ $t=0$ ）に一括して発生するとみなしている点である。つまり、今日の化石燃料燃焼による $\text{CO}_2$ 排出も、50年後の木材燃焼による $\text{CO}_2$ 排出も、この式では等価に扱われる。

この「時間の平板化」が木材評価において重大な問題を引き起こす。木材製品は製造段階（A1-A3モジュール）においてバイオジェニック炭素を大気から固定するが、建物の使用終了後（50年〜100年後）に解体・焼却される際に初めてその炭素を放出する。静的LCAはこの時間差を無視するため、木材の「今は固定し、数十年後に放出する」という気候的優位性が正当に評価されない。

### 1.2　動的LCAの登場：Levasseur et al.（2010）の貢献
動的LCAという概念は2000年代後半から学術的に提唱され始め、Levasseur et al.（2010）がカナダ・CIRAIG（産業LCA研究センター）において発表した論文が、現代的な動的LCAの理論的基盤を確立したとされる。この論文はDCF（Dynamic Characterization Factor；動的特性化係数）という概念を導入し、次の動的GHG評価式を提示した：

$$\Delta PRG_{\text{dyn}} = \sum_i DCF(t_i, DO) \cdot prg(x_i) \cdot m_i$$

ここで $DCF(t_i, DO)$ は、時刻 $t_i$ に放出された単位量のGHGが、時間地平線 $DO$ までの間に生じる累積放射強制力（CRF）を、即時排出（ $t_i=0$ ）の場合のCRFで正規化したものである。DCFは $0 \le DCF \le 1$ の値をとり、早期排出ほど1に近く、後年の排出ほど0に近い。

DCFの導入により、木材の炭素貯蔵が持つ「時間적価値」が初めて定量的に評価可能になった。同時期にCherubini et al.（2011）、Zetterberg & Chen（2015）なども動的LCAの方法論を発展させ、2010年代を通じて学術的な標準化が進んだ。

### 1.3　本調査の目的と構成
本調査（SuMPO・林野庁委託、2025年度）は、動的LCAの政策的・科学的背景を体系的に整理することを第一の目的とする。特に以下の問いに答えることを目標とする。

* なぜ動的LCAはフランスで最初に規制化されたのか（第2〜3章）。
* 動的LCAの数理的・技術的基礎は何か（第4章）。
* 日本の現行LCA制度との整合性課題はどこにあるか（第5章）。

本報告書は、SuMPO企画書（2025年）に基づく4つの調査タスクのうち「Task 1：政策および制度調査」の成果として位置づけられる。

---

## 第2章　気候変動政策と国際動向

### 2.1　EUの建築環境政策フレームワーク
欧州連合は、2019年の「European Green Deal（欧州グリーンディール）」において2050年気候中立を目標として掲げ、2021年の「Fit for 55」パッケージでは2030年までに1990年比55%のGHG削減を法的義務とした。この枠組みの下で建築分野は特に重要な削減対象として位置づけられ、以下の政策群が整備された。

* **建築物エネルギー性能指令（EPBD）の変遷:** 2002年に初版が制定されたEPBDは、2010年改正でゼロエネルギー建築（nZEB）の概念を導入し、2018年改正でライフサイクルGHG評価の検討を加速させた。2024年の改正では建物のGHG排出に関するライフサイクル性能（Whole Life Carbon; WLC）の開示義務を段階的に導入することが決定され、動的LCAが評価手法の主要な選択肢として浮上している。
* **Level(s)フレームワーク:** 欧州委員会が開発した建築の持続可能性評価枠組みで、指標6としてライフサイクルGHG排出量の評価を規定している。EN 15978（建物ライフサイクル評価）およびEN 15804+A2（建材EPD）との整合が図られている。

### 2.2　フランスの政策的文脈：グルネルからRE2020へ
フランスにおける動的LCA規制の実現は、一夜にして生まれたものではない。2007年のニコラ・サルコジ大統領政権下で開催されたグルネル環境ラウンドテーブル（Grenelle de l'environnement）において、建築分野の環境規制強化が政策課題として確立した。その後の経緯を年表として整理する。

* **2007年 グルネル環境RTT:** 建築分野の環境規制の政策的枠組みを確立。エネルギーと炭素の両面から建物を評価する方向性が決定される。
* **2009年 Benoist博士論文（Paris Est大学）:** 動的LCAの補正係数の数理的基礎を確立。 $1 - 0.00842 \cdot t$ という線形近似式の原型がここで提示される。
* **2012年 RT2012施行:** エネルギー消費規制（Cep指標）を法制化。炭素評価は未導入。
* **2015年 パリ協定採択:** フランスが締約国として2050年炭素中立を目標に設定。建物全体LCAの法制化を加速させる政策的文脈が形成される。
* **2016〜2019年 E+C-実験プログラム:** RE2020の前身として2,200棟超の建物で実証実験を実施。動的LCAを含む炭素評価手法の実務的検証を行う。
* **2018年 Solinnnen（現Elodie Consulting）報告書:** DCFの線形近似係数を実務算定のために最終確定。RE2020の動的補正係数（ $1 - 0.00842 \cdot t$ 、下限0.58）の根拠となる。
* **2021年7月** RE2020法令（デクレ2021-1004号）公布。
* **2022年1月1日** 住宅向けRE2020 第1フェーズ正式施行。世界初の動的LCA法規制が実現。

### 2.3　フランスにおける動的LCA採用の政治経済的背景
RE2020が世界に先駆けて動的LCAを規制化できた要因は、科学的・政策的・産業的の三要素が同時に揃ったことにある。
* **科学的側面:** 2009年のBenoist論文以降、フランス国内の研究者・コンサルタントが継続的に手法を発展させた。
* **政策的側面:** グルネル以降の建築環境政策の蓄積とEUのグリーンディールとの整合性が重要であった。
* **産業的側面:** フランス木材・建設木材センター（FCBA）を中心とする木材産業界が積極的なロビー活動を展開した。木材産業にとって動的LCAはコンクリート・鉄鋼に対する競争上の優位性を定量的に示す手段であり、業界一体となってRE2020の動的LCA条項の採用を支持した。

さらに、フランスが2022年上半期にEU議長国を務めたことも、RE2020の手法を欧州標準として国際発信する好機として活用された。ISO 21391（後の21391-1:2025）の策定においてフランスが主導的役割を果たした背景にも、この政策的文脈がある。

### 2.4　欧州・北米の国際動向

#### 2.4.1　ノルウェー：FutureBuilt ZEROプログラム
ノルウェーは、NS 3720規格（建物のGHG算定）に基づくFutureBuilt ZEROプログラムにおいて、動的LCAの時間重み付けを建築物認証の要件に組み込んでいる。RE2020とは係数の設定が一部異なるが、「後の排出ほど気候影響が小さい」という原理は共通している。

#### 2.4.2　スウェーデン・ドイツ：動的評価の検討段階
スウェーデンは2022年に住宅建設に対する国家LCA指針（Boverket）を施行したが、現時点では静的LCAが主体である。ドイツの連邦持続可能建築認証（BNB）も同様に静的LCAベースであり、動的評価は研究・検討段階にある。

#### 2.4.3　米国：ARPA-E HESTIAプログラム
米国ではARPA-E（先端エネルギー研究機構）の「HESTIA（Harnessing Emissions into Structures Taking Inputs from the Atmosphere）」プログラム（2022〜2026年）が、建物を炭素固定の場として定量化する研究を支援しており、動的LCAが主要な評価ツールとして使用されている。

#### 2.4.4　国際標準化：ISO 21391-1:2025
ISO 21391-1:2025（旧ISO 13391）は「建材におけるバイオジェニック炭素の動的評価方法」に関する最初の国際規格として2025年に策定された。本規格は非線形DCFを採用しており、RE2020の線形近似よりも物理的に精密な評価が可能である。また、CEN/TC 350委員会ではEN 15804の次期改訂（2025年〜）において動的バイオジェニック炭素評価の組み込みが検討されている。

---

## 第3章　フランスRE2020の制度構造

### 3.1　3つの性能指標と法的位置づけ
RE2020は建物性能を下記の3指標で評価する。

| 指標記号 | 日本語名 | 評価対象・算定内容 |
| :--- | :--- | :--- |
| **Bbio** | 気候要求係数 | 建物の断熱・通気設計から生じる暖冷房需要。高い値ほど気候負荷が大きい。従来のRT2012から継続。 |
| **Cep,nr** | 非再生一次エネルギー消費量 | 運用段階における非再生可能一次エネルギー（化石燃料等）の年間消費量 $[\text{kWh/m}^2/\text{yr}]$ 。RE2020ではRT2012より基準値を強化。 |
| **Ic** | 炭素影響指標（新設） | 建材・施工・運用・解体の全ライフサイクルGHG排出量を動的LCAで算定 $[\text{kgCO}_2\text{eq/m}^2]$ 。フランスが世界で初めて法規制に採用した指標。 |

これらのうち炭素指標 $Ic$ は次の式で定義される：

$$Ic = Ic_{\text{construction}} + Ic_{\text{énergie}} - StockC$$

* $Ic_{\text{construction}}$ ：建設段階（材料・施工）の炭素排出量
* $Ic_{\text{énergie}}$ ：運用段階（エネルギー使用）の炭素排出量
* $StockC$ ：炭素貯蔵クレジット（動的LCAの時間補正を含む）

### 3.2　ライフサイクルモジュール構造（EN 15978準拠）
RE2020のライフサイクル評価はEN 15978に準拠し、建物のライフサイクルを下表のモジュールに分類する。

| モジュール | ライフサイクル段階 | 主な算定対象 |
| :--- | :--- | :--- |
| **A1–A3** | 製品段階 | 原材料採取・輸送・製造（製材、集成材加工を含む） |
| **A4–A5** | 建設段階 | 現場への輸送・建設施工・仮設材廃棄 |
| **B1–B7** | 使用段階 | 運用エネルギー（B6）・保守（B2）・修繕（B3）・部品交換（B4）・改修（B5） |
| **C1–C4** | 廃棄段階 | 解体（C1）・廃棄物輸送（C2）・廃棄物処理（C3）・最終処分（C4） |
| **D** | システム境界外便益 | 再利用・リサイクル・エネルギー回収（正味便益または負荷として報告） |
| **StockC** | 炭素貯蔵クレジット（RE2020独自） | バイオジェニック炭素の一時貯蔵に対するクレジット。動的LCA時間補正と組み合わせて算定。 |

特に重要なのは $StockC$ の扱いである。EN 15804+A2（2019）は「 $-1/+1$ アプローチ」を採用しており、A1-A3段階でバイオジェニック炭素の固定を $-1\text{ kgCO}_2/\text{kgC}$ （負値）として計上し、C段階（解体・廃棄）での放出を $+1\text{ kgCO}_2/\text{kgC}$ （正値）として計上する。RE2020はこれに加えて、C段階の放出に動的LCA時間補正係数を乗じることで、将来の炭素放出を現在価値に換算する。

### 3.3　動的LCA補正係数の定義と実務計算

#### 3.3.1　RE2020線形補正係数
RE2020において動的LCAの時間補正は、Solinnen（2018）の報告書で最終化された次の線形近似式で実施される：

$$\text{coefficient}(t) = 1 - 0.00842 \cdot t \quad (t \le 50\text{年})$$
$$\text{coefficient}(t) = 0.580 \quad (t > 50\text{年、下限固定})$$

この係数は、時刻 $t_i$ （年）に排出された単位量のGHGの「気候影響の時間割引」を表す。 $t=0$ では係数1.0（即時排出は割引なし）、 $t=50$ 年では係数 $\approx 0.58$ （42%割引）、 $t>50$ 年では0.58に固定される。

#### 3.3.2　動的LCAとStockCの算定フロー
RE2020の $StockC$ 算定は、各建材の炭素フロー（吸収・放出）とそのタイミング $t_i$ を特定し、補正係数を乗じて正味の炭素クレジットを計算する。フランスのBIM・LCAツールである「Elodie（CSTB提供）」がこの計算を自動化しており、登録された建材データベース（FICES）のデータを参照して評価が行われる。

### 3.4　RE2020法制化の経緯：政治的・科学的連携の詳細
RE2020の立案・施行は、フランス環境・エネルギー省（DHUP：住宅都市計画局、DGALN：自然・建築・土地整備総局）が主論した。省内の専門家グループが2016〜2021年にかけてE+C-実験データを分析し、炭素指標（ $Ic$ ）の設定値・動的LCA係数を決定した。

科学的根拠の中心となったのは、2018年のSolinnen報告書と2009年のBenoist博士論文である。Benoist（2009）は動的LCAの補正係数を累積放射強制力の比率から導出し、その線形近似として $1 - 0.00842 \cdot t$ を提案した。Solinnen（2018）はこれを実務的規制に適用可能な形で再整理し、 $DO=100$ 年の固定と下限値0.58の設定を提案した。フランス行政はこれらの科学的成果を踏まえてRE2020条文に組み込んだ。

### 3.5　RE2020の科学的課題と批判적考察

#### 3.5.1　Ventura & Feraille（2021）の批判
RE2020の動的LCA手法は世界初の規制化として高く評価される一方、Ventura & Feraille（2021）は以下の根本的な批判を展開している。

* **DO（時間地平線）の固定問題:** RE2020は全ての炭素フローに対して $DO=100$ 年を固定しているが、物理的に妥当なDOは各排出イベントのタイミング $t_i$ に依存する。正確には $\text{DO} = t_i + \text{HTI}$ （熱時間積分）として各フローのDOを可変とすべきである。
* **過大評価の定量:** 固定 $DO=100$ 年の使用により、遅延ベネフィット（後に排出されることの気候的有利さ）が35〜53%過大評価される。
* **数値例:** $t=50$ 年の排出に対し、RE2020は係数0.58を適用するが、物理的に正確なDCF（ $\text{DO}=t_i+\text{HTI}$ ）は約0.72となる（約24%の差）。

この批判は学術的に重要であり、RE2020の次期改正（2028年フェーズ3）でも係数の見直しが議論されている。しかし、規制実務においては簡便性も重要であり、線形近似の採用には政策的合理性もある。

#### 3.5.2　バイオジェニック炭素の会計方法論的課題
EN 15804+A2の $-1/+1$ アプローチは、持続可能な森林管理（SFM）が前提であれば、A1-A3での固定量とC段階での放出量が概ね等しいとみなせる。しかし実際には、伐採した木材量に対して同等量の植林が保証されない場合の扱いや、森林炭素ストックの長期的変動の考慮が課題として残る。

#### 3.5.3　RE2020係数の比較（表3）
下表は、RE2020の線形近似係数、IPCC AR4モデルからの数値積分による真のDCF、およびVentura & Feraille（2021）の提案する物理的に妥当なDCFを比較したものである。

| 排出時点 $t_i$ （年） | RE2020線形近似 | 真のDCF<br> (DO=100yr, 数値積分) | Ventura提案<br> (DO= $t_i$ +HTI) | 差異※ |
| :--- | :--- | :--- | :--- | :--- |
| **$t = 0$ （建設時）** | 1.000 | 1.000 | 1.000 | 0% |
| **$t = 10$ 年** | 0.916 | 0.915 | 0.951 | +3.9% |
| **$t = 25$ 年** | 0.790 | 0.792 | 0.858 | +8.3% |
| **$t = 50$ 年（設計寿命）** | 0.579 | 0.606 | 0.720 | +24% |
| **$t > 50$ 年（RE2020上限）** | 0.580（固定） | 0.427（ $t=75\text{yr}$ ）<br>0.283（ $t=100\text{yr}$ ） | 0.617（ $t=75\text{yr}$ ） | 〜53% |

<blockquote>
※差異はRE2020とVentura提案の比較（正値はRE2020が木材に対して有利（楽観的）である割合）（Ventura & Feraille, 2021より整理）。
</blockquote>

---

## 第4章　動的LCAの技術的・数理的基礎

### 4.1　静的LCAと動的LCAの数式比較
第1章で概観した数式を、より詳細に比較する。

* **【静的LCA】** 全排出フローを $t=0$ に集約し、IPCC GWP100係数で重み付けする：
  $$PRG_{\text{static}} = \sum_i prg(x_i) \cdot m_i$$
* **【動的LCA】** 各排出フローの時刻 $t_i$ に応じたDCF係数を乗じる：
  $$\Delta PRG_{\text{dyn}} = \sum_i DCF(t_i, DO) \cdot prg(x_i) \cdot m_i$$

両式の唯一の相違は $DCF(t_i, DO)$ の有無である。 $DCF=1$ （全フローが $t_i=0$ ）のとき、動的LCAは静的LCAに一致する。 $DCF<1$ （ $t_i>0$ ）のとき、後の排出は静的LCAよりも小さく評価される。

### 4.2　動的特性化係数（DCF）の定義
DCF（Dynamic Characterization Factor）は次のように定義される：

$$DCF(t_i, DO) = \frac{CRF(t_i, DO)}{CRF(0, DO)} = \frac{\int_{t_i}^{DO} a_x(t) \cdot [x(t-t_i)] dt}{\int_{0}^{DO} a_x(t) \cdot [x(t)] dt}$$

* $CRF(t_i, DO)$ ：時刻 $t_i$ に放出されたGHGが、 $[t_i, DO]$ の期間に生じる累積放射強制力（Cumulative Radiative Forcing）
* $CRF(0, DO)$ ：即時排出（ $t_i=0$ ）の場合の $[0, DO]$ における累積放射強制力（正規化の分母）
* $a_x(t)$ ：物質 $x$ の放射強制力係数（ $\text{CO}_2$ の場合 $a_x = 1.55 \times 10^{-15} \text{ W}\cdot\text{m}^{-2}\cdot(\text{kgCO}_2)^{-1}$ ）
* $[x(t)]$ ：大気中のGHG濃度インパルス応答関数（ $=r(t)$ ）
* $DO$ ：時間地平線（Time Horizon）。RE2020では100年を採用。

すなわちDCFは、「 $t_i$ 時点での排出が気候に与える累積影響」の「即時排出の場合との比率」であり、DCFが小さいほど気候への影響が小さいことを意味する。

### 4.3　IPCC AR4 Bern2.5CC：CO₂大気中応答モデル
DCFの計算には、大気中に放出された $\text{CO}_2$ の経時的な残存割合を表す「濃度インパルス応答関数 $r(t)$ 」が必要となる。RE2020（および多くの動的LCA研究）は、IPCC第4次評価報告書（AR4）で採用されたBern2.5CCモデルの4指数関数近似を使用する：

$$r(t) = c_0 + c_1 \cdot e^{-t/\tau_1} + c_2 \cdot e^{-t/\tau_2} + c_3 \cdot e^{-t/\tau_3}$$

| パラメータ | 数値 | 物理的意味 |
| :--- | :--- | :--- |
| **$c_0$** | 0.217 | 大気中に永続的に残存する成分（数千年スケール）。炭酸塩平衡により長期的に大気に留まる割合。 |
| **$c_1$** | 0.259 | 深層海洋炭素循環で吸収される成分（時定数 $\tau_1=172.9$ 年）。 |
| **$c_2$** | 0.338 | 海洋上層・中層で吸収される成分（時定数 $\tau_2=18.51$ 年）。最も速い海洋炭素吸収。 |
| **$c_3$** | 0.186 | 生物圏・土壌による短期吸収成分（時定数 $\tau_3=1.186$ 年）。 |
| **$a_x$** | $1.55 \times 10^{-15}$ | $\text{CO}_2$ の放射強制力係数 $[\text{W}\cdot\text{m}^{-2}\cdot(\text{kgCO}_2)^{-1}]$ 。大気中 $\text{CO}_2$ 濃度1kgの増加が引き起こす放射強制力。 |

この式の物理的解釈は以下の通りである。定数項 $c_0=0.217$ は、大気中に永続的に残存する成分（超長期）を表す。 $t=1000$ 年での残存割合は $r(1000) \approx 0.217 + 0.259 \cdot e^{-5.79} \approx 22.4\%$ となり、IPCCの「約22%が大気に永続残存」という記述と一致する。この検証により、フランス語文献で「 $\tau_1=1729$ 」と記載されている場合（フランス語の千位区切り表記）は正確には $\tau_1=172.9$ 年であることが確認できる。

### 4.4　DCFの数値計算手順
DCFは以下の手順で数値積分により計算される。

* **手順①:** $r(t)$ を0から $DO-t_i$ まで数値積分し、各時刻の放射強制力 $RF(t)=a_x \cdot r(t)$ を計算する。
* **手順②:** $\int_{0}^{DO-t_i} a_x \cdot r(t) dt$ を数値積分して $CRF(t_i, DO)$ を求める。
* **手順③:** $CRF(0, DO) = \int_{0}^{DO} a_x \cdot r(t) dt$ を計算する（正規化の分母）。
* **手順④:** $DCF(t_i, DO) = CRF(t_i, DO) / CRF(0, DO)$ を計算する。

 $DO=100$ 年の場合、 $CRF(0,100)$ の典型値はおよそ $0.0192 \text{ W}\cdot\text{m}^{-2}\cdot\text{yr}\cdot(\text{kgCO}_2)^{-1}$ となる。各 $t_i$ に対する代表的なDCF値は第3.5.3節の表3に示した。

### 4.5　RE2020線形近似係数（1−0.00842·t）の導出
RE2020において実務的に使用される線形近似係数は、Benoist（2009）がIPCC AR4 Bern2.5CCモデルに基づいて導出し、Solinnen（2018）が実規制向けに最終化したものである。

導出のロジックは次の通りである。数値積分から得られたDCF曲線（ $t_i: 0 \to 50$ 年）を最小二乗法で線形近似すると、傾きは約 $-0.00842/\text{年}$ （つまり1年あたり約0.842%の割引率）となる。この線形近似は0〜50年の範囲で真のDCFに対しておおむね $\pm 3\%$ 以内の精度を持つ。

$$DCF_{\text{RE2020}}(t) \approx 1 - 0.00842 \cdot t \quad (0 \le t \le 50\text{年})$$
$$DCF_{\text{RE2020}}(t) = 0.580 \quad (t > 50\text{年})$$

 $t>50$ 年での0.580固定は、①50年超の炭素フローは建物ライフサイクルで稀であること、②規制の透明性・予測可能性を高めること、という実務的理由による。ただしこの固定化がVentura & Feraille（2021）の批判の一因でもある。

### 4.6　バイオジェニック炭素と動的LCAの関係
木材のバイオジェニック炭素（biogenic carbon）の扱いは動的LCAの核心的テーマである。EN 15804+A2（2019）の「 $-1/+1$ アプローチ」と動的LCAの時間補正を組み合わせると次のようになる：

* **A1-A3段階（製品製造時）:** バイオジェニック炭素固定 $\to$ 即時クレジット（ $DCF=1.0$ で計上）
* **C段階（解体・焼却時、 $t \approx 50 \sim 100$ 年後）:** バイオジェニック炭素放出 $	o$ $DCF \approx 0.58$ で割引計上

この非対称性（吸収は $DCF=1$ 、放出は $DCF \ll 1$ ）が、木材のバイオジェニック炭素貯蔵をきわめて有利に評価する仕組みの本質である。固定されたバイオジェニック炭素は即座に全額クレジットされ、将来の放出は大幅に割り引かれるため、正味の $StockC$ が大きくなる。

### 4.7　CLTと一般建材の比較：静的LCA vs 動的LCA
下表は、代表的建材の静的LCA評価値と動的LCA評価値を比較したものである。

| 建材カテゴリ | 代表例 | 静的LCA (GWP100) $[\text{kgCO}_2\text{eq/m}^3]$ | 動的LCA (RE2020準拠) $[\text{kgCO}_2\text{eq/m}^3]$ |
| :--- | :--- | :--- | :--- |
| 木質系 | **CLT（直交集成板）** | +98（排出） | **−171（吸収） ★** |
| 木質系 | **製材（sawn timber）** | +65（排出） | **−115（吸収） ★** |
| コンクリート系 | RC造（鉄筋コンクリート） | +300前後（排出） | +295前後（ほぼ不変） |
| 金属系 | 構造用鋼材（steel） | +550前後（排出） | +548前後（ほぼ不変） |

<blockquote>
★印の木質系建材は、動的LCAで「排出→吸収」へと評価が逆転する。CLTの場合、 $269\text{ kgCO}_2\text{eq/m}^3$ の評価差が生じる。コンクリート・鉄鋼は炭素貯蔵を持たないため静的・動的でほぼ同値となる。この大きな評価差こそが、フランスの建材産業（特に木材産業）が動的LCA의 導入を強く支持した経済的根拠である。
</blockquote>

---

## 第5章　日本のLCA制度との整合性課題

### 5.1　日本の現行建築LCA制度の概況
日本では現在、建築物のLCA評価は自主的な認証制度（CASBEE；建築環境総合性能評価システム、ZEB/ZEH認証等）を通じて行われているが、いずれも静的LCA（GWP100）を基本とする。バイオジェニック炭素の計上については統一的なルールがなく、EN 15804+A2が規定する $-1/+1$ アプローチも導入されていない。

国内のLCAデータベースとしてIDEA（産業連関表を利用した産業環境データブック）などが存在するが、建材の排出フローについて時系列情報は含まれておらず、動的LCAへの対応は実質的に不可能な状況である。

### 5.2　国際標準との整合課題
日本が対応すべき主要な国際標準と現状のギャップを下表に整理する。

| 規格・制度 | バイオジェニック炭素の扱い | 動的LCA採用状況 | 備考・適用範囲 |
| :--- | :--- | :--- | :--- |
| **EN 15804+A2（2019）** | 別途開示（GWP-biogenic）、−1/+1アプローチ | 任意；別途GWP-dyn推奨 | 欧州建材EPD基準。改訂でバイオジェニックを前面に |
| **ISO 14067（2018）** | 別途報告、合算禁止 | 未採用（静的GWP100） | 製品のCFP算定規格 |
| **ISO 21391-1（2025）** | 動的バイオジェニック炭素評価 | **★採用（国際初）** | 建材の動的バイオジェニック炭素評価の最初の国際規格 |
| **PEF Method（EU）** | Annex Cで任意推奨 | 代替手段として任意 | 製品環境フットプリント法。製品カテゴリ規則で変動 |
| **RE2020（フランス、2022）** | 時間補正付きバイオジェニック炭素計上（StockC） | **★★世界初規制義務化** | 建設分野での動的LCA法規制。2022年施行。2028年第3フェーズで係数見直し予定 |
| **NS 3720（ノルウェー）** | 動的重み付け評価 | FutureBuilt ZEROで採用 | 建築認証プログラムとして実装。RE2020と並ぶ先進事例 |
| **日本（CASBEE/ZEB等）** | 未対応（静的GWP100） | **✗ 未導入** | 国内標準整備・データベース拡充・法制度化が急務 |

### 5.3　日本における動的LCA導入に向けた課題と提言

#### 5.3.1　短期的課題（〜2027年）
* ISO 21391-1:2025の国内JIS化と建材・木材産業への普及啓発。
* フランスRE2020の動的補正手法を国産建材に試験的適用し、CLT・製材等の評価差を定量化（SuMPO Task 2の一環）。
* 国内LCAデータベース（IDEA等）への時系列排出フローデータの追加整備。

#### 5.3.2　中期的課題（2027〜2030年）
* 国土交通省・林野庁との連携による「建築物ライフサイクル炭素評価指針」への動的LCAオプション追加。
* ZEB/ZEH認証における木材炭素貯蔵クレジット制度の検討（RE2020の $StockC$ に相当する国内制度の設計）。
* フランスFICES（建材環境データベース）に相当する国内データベースの整備。

#### 5.3.3　長期的展望
中長期的には、日本版「動的LCAに基づく建築物炭素評価制度」の構築が目標となる。林業再生・国産木材利用促進（Forest Agency Wood Miles方針等）の定量的根拠として動的LCAを活用することで、木材産業の経済的優位性と気候政策目標を両立させる制度設計が可能となる。

---

## 第6章　まとめと今後の課題

### 6.1　本調査の総括
本報告書では、動的LCAの政策적・科学的背景を3つの視点から分析した。

* **政策的視点:** フランスRE2020の実現は、15年以上の政策議論（グルネル2007〜施行2022）、科学的蓄積、産業アドボカシーの三位一体によるものであった。EUの気候政策との整合性が政治的正当性を与え、フランスが議長国を務めたタイミングが国際標準化（ISO 21391-1）へとつながった。
* **技術的視点:** 動的LCAの核心はDCFであり、IPCC AR4 Bern2.5CCモデルに基づく累積放射強制力（CRF）の比として数値積分で算出される。RE2020は $1 - 0.00842 \cdot t$ という線形近似を採用し実務化したが、Ventura & Feraille（2021）はDO固定による35〜53%の過大評価を指摘している。ISO 21391-1:2025は非線形DCFを採用して精度を改善した。
* **制度的視点:** 日本の建築LCA制度は静的LCAに留まり、動的手法・バイオジェニック炭素の時間評価は未対応である。国際標準への対応と国産LCAデータベースの整備が急務である。

### 6.2　今後の調査課題（SuMPO Tasks 2〜4）
* **Task 2（技術・手法調査）:** DCF算出の完全再現計算；国内木材製品（CLT・製材・集成材等）への動的LCA試験適用；EN 15804+A2とISO 21391-1の詳細技術比較。
* **Task 3（情報基盤調査）:** フランスFICES・ADEMEデータベースの詳細分析；日本IDEA・建材LCAデータベースとの比較；動的LCA対応データ形式の要件定義。
* **Task 4（専門家調査）:** ADEME・DHUP・FCBA（フランス）、FutureBuilt（ノルウェー）、Boverket（スウェーデン）へのヒアリング；国内の関係省庁・木材業界・学識者へのインタビュー。

---

## 参考文献

* ARPA-E (2022). HESTIA: Harnessing Emissions into Structures Taking Inputs from the Atmosphere. U.S. Department of Energy, Advanced Research Projects Agency-Energy. https://arpa-e.energy.gov/technologies/programs/hestia
* Benoist, A. (2009). Intégration des émissions de CO₂ biogénique dans les analyses de cycle de vie — Proposition d'une méthode dynamique. Thèse de doctorat, Université Paris Est. [動的補正係数1−0.00842·tの原型を提示した博士論文。]
* BMWK (2023). BNB — Bewertungssystem Nachhaltiges Bauen: Steckbriefe. Bundesministerium für Wirtschaft und Klimaschutz. Berlin.
* Boverket (2022). Klimatdeklaration — En ny lag om klimatdeklaration för byggnader. Boverket, Karlskrona, Sweden.
* Cherubini, F., Bright, R.M., & Strømman, A.H. (2011). Site-specific global warming potentials of biogenic CO₂ for bioenergy: contributions from carbon fluxes and albedo dynamics. Environmental Research Letters, 7(4), 045902.
* CSTB (2022). Outil Elodie: Logiciel d'aide à l'Analyse du Cycle de Vie des bâtiments. Centre Scientifique et Technique du Bâtiment. Paris.
* Décret RE2020 (2021). Décret n°2021-1004 du 29 juillet 2021 relatif aux exigences de performance énergétique et environnementale des constructions de bâtiments en France métropolitaine. Journal officiel de la République française.
* DHUP (2021). Guide d'utilisation de la RE2020: Exigences environnementales. Direction de l'Habitat, de l'Urbanisme et des Paysages, Ministère de la Transition Écologique. Paris.
* EN 15804+A2 (2019). EN 15804:2012+A2:2019 — Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products. European Committee for Standardization (CEN).
* EN 15978 (2011). Sustainability of construction works — Assessment of environmental performance of buildings — Calculation method. CEN, Brussels.
* European Commission (2019). The European Green Deal. COM(2019) 640 final. European Commission, Brussels.
* European Commission (2020). Level(s) — A common EU framework of core sustainability indicators for office and residential buildings. European Commission, Brussels.
* European Parliament (2024). Directive (EU) 2024/1275 on the Energy Performance of Buildings (recast). Official Journal of the European Union.
* FutureBuilt (2022). FutureBuilt ZERO — Standard for Zero Emission Buildings and Districts. FutureBuilt, Oslo, Norway.
* Guest, G., Cherubini, F., & Strømman, A.H. (2013). Global warming potential of carbon dioxide emissions from biomass stored in the anthroposphere and used for bioenergy at end of life. Journal of Industrial Ecology, 17(1), 20–30.
* Hoxha, E., Passer, A., Saade, M.R.M., Trigaux, D., Shuttleworth, A., Pittau, F., ... & Habert, G. (2020). Biogenic carbon in buildings: a critical overview of LCA methods. Buildings and Cities, 1(1), 504–524.
* IPCC (2007). Climate Change 2007: The Physical Science Basis. Contribution of Working Group I to the Fourth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press, Cambridge.
* ISO 14067 (2018). ISO 14067:2018 — Greenhouse gases — Carbon footprint of products — Requirements and guidelines for quantification. International Organization for Standardization. Geneva.
* ISO 21391-1 (2025). ISO 21391-1:2025 — Sustainability in buildings and civil engineering works — A framework for assessment of sustainability performance of buildings using dynamic life cycle assessment — Part 1: General principles and requirements. ISO, Geneva.
* Levasseur, A., Lesage, P., Margni, M., Deschênes, L., & Samson, R. (2010). Considering time in LCA: Dynamic LCA and its application to global warming impact assessments. Environmental Science & Technology, 44(8), 3169–3174. [動的LCA・DCFの理論的基礎を確立した先駆的論文。]
* Peñaloza, D., Erlandsson, M., & Falk, A. (2016). Exploring the climate impact effects of increased use of bio-based materials in buildings. Construction and Building Materials, 125, 219–226.
* Perez, E., Borrion, A., & Xu, Z. (2021). Life cycle assessment of cross-laminated timber: a systematic literature review. Sustainability, 13(22), 12570.
* Solinnen [Elodie Consulting] (2018). Rapport sur les méthodes de calcul des impacts environnementaux — Coefficient dynamique du bilan carbone. Rapport technique pour la DHUP. Paris. [RE2020の動的補正係数（1−0.00842·t）を最終化した実務報告書。]
* Temporiti, M., Brunetti, A., Battistoni, P., & Viola, F. (2021). Dynamic LCA of wood in construction: comparing static and dynamic approaches. Journal of Cleaner Production, 318, 128400.
* Ventura, A., & Feraille, A. (2021). Temporal sensitivity of the global warming impact of a building. Journal of Industrial Ecology, 25(4), 999–1010. [RE2020のDO固定問題を指摘し代替DCFを提案した重要論文。]
* 産業環境管理協会 (2023). IDEA（産業連関表による環境負荷原単位データブック）ver.3.3. 一般社団法人産業環境管理協会. 東京.
* 林野庁 (2023). 木材利用促進基本計画. 農林水産省林野庁. 東京.
