export type CollectibleQuality = '傳奇' | '史詩' | '優秀' | '精良' | '普通';

export type Collectible = {
  id: number;
  name: string;
  quality: CollectibleQuality;
  edition: number;
  imageUrl: string;
  detailUrl: string;
};

const qualityByCode: Record<number, CollectibleQuality> = {
  11: '傳奇',
  7: '史詩',
  4: '優秀',
  3: '精良',
  2: '普通',
};

function editionForId(id: number) {
  if (id <= 30) return 1;
  if (id <= 47) return 2;
  if (id <= 78) return 3;
  if (id <= 110) return 4;
  if (id <= 140) return 5;
  if (id <= 170) return 6;
  if (id <= 200) return 7;
  if (id <= 230) return 8;
  if (id <= 260) return 9;
  return 10;
}

const rawCatalog = `
1|11|renleijiyintupu|人類基因圖譜
2|11|yuanguzhihuizhishu|遠古智慧之書
31|11|buxiudexingyunyingbi|不朽的幸運硬幣
32|11|xingjiyueqianjuzhentuzhi|星際躍遷矩陣圖紙
51|11|tianshizhileishuijing|天使之淚水晶
52|11|dujiaoshoudejiao|獨角獸的角
75|11|yijieqiyao|異界奇鑰
76|11|xinghebaozuan|星核寶鑽
79|11|gaoweidunengliangmofang|高緯度能量魔術方塊
80|11|xukongzhihua|虛空之花
81|11|zhenshizhiyan|真實之眼
82|11|shengmingshalou|生命沙漏
111|11|naminitaimianju|奈米擬態面具
112|11|mingyunduomiantou|命運多面骰
113|11|weidubo|維度箔
114|11|yishitongbutoukui|意識同步頭盔
141|11|yuanzijiqiren|原子機器人
142|11|shiguangqixiping|時光氣息瓶
143|11|longya|龍牙
144|11|chaonengshenjingyuan|超能神經元
171|11|saibotutengzhu|賽博圖騰柱
172|11|fuzhibaojing|複製寶鏡
173|11|mengjingpintu|夢境拼圖
174|11|jiyinbianjiqi|基因編輯器
201|11|jiyibianjiqi|記憶編輯器
202|11|shijianhuisuchilun|時間回溯齒輪
203|11|kongjianhuisuchilun|空間回溯齒輪
204|11|mengjingxianyingye|夢境顯影液
231|11|anwuzhikuilei|暗物質傀儡
232|11|shijianxianmofang|時間線魔術方塊
233|11|baibiangongshengti|百變共生體
234|11|yuyantaluopai|預言塔羅牌
261|11|shuipingzuoxinghui|水瓶座星徽
262|11|shuangyuzuoxinghui|雙魚座星徽
263|11|baiyangzuoxinghui|白羊座星徽
264|11|jinniuzuoxinghui|金牛座星徽
3|7|huangjincanju|黃金餐具
4|7|gulaodeyixueshuji|古老的醫學書籍
5|7|jiushizhudeyiwu|救世主的遺物
6|7|cangshenzhisuodeditu|藏身之所的地圖
33|7|xingyunhushenfu|幸運護身符
34|7|shenmixing|神秘星
35|7|dingjiankexuejiadebiji|頂尖科學家的筆記
36|7|chaojidianluban|超級電路板
48|7|shenmiguanghuan|神秘光環
49|7|shengshiyanhuo|盛世煙火
50|7|qingxinzuanjie|清心鑽戒
53|7|shishiniban|史詩泥板
54|7|honghuangzhangu|洪荒戰鼓
55|7|lieyanhongyu|烈焰紅羽
56|7|xianjingyulu|仙境雨露
70|7|menghuanzhixindangao|夢幻之心蛋糕
71|7|xianliangkuancaidan|限量款彩蛋
72|7|huolizhongzi|活力種子
73|7|duyiwuerdeyezi|獨一無二的葉子
74|7|qiyidejingshi|奇異晶石
77|7|kongqijiaoshuihu|空氣膠水壺
78|7|mohuanyuer|魔幻魚餌
83|7|henengdianchi|核能電池
84|7|denglizijian|等離子劍
85|7|huangjinhaojiao|黃金號角
86|7|yuansuzhihuan|元素之環
103|7|zidongdaqitong|自動打氣筒
104|7|yundonghuijiangpai|運動會獎牌
105|7|shijieshushuyebiaoben|世界樹樹葉標本
106|7|daxiangwanou|大象玩偶
107|7|shengrihuangguan|生日皇冠
108|7|shuiguozhazhiji|水果榨汁機
109|7|mofashuijingqiu|魔法水晶球
110|7|touziyaokongqi|投資遙控器
115|7|fanzhonglizhuangzhi|反重力裝置
116|7|shuidongtuilijiaopu|水動推力腳蹼
117|7|chaorenleiyaopian|超人類藥片
118|7|tongxunhailuo|通訊海螺
135|7|zhencangkapai|珍藏卡牌
136|7|wushi|巫師
137|7|xinxinglazhu|心形蠟燭
138|7|xiyouyuekuang|稀有樂框
139|7|jixiangjie|吉祥結
140|7|jinbotiantianquan|金箔甜甜圈
145|7|minidaisenqiu|迷你戴森球
146|7|weixingrenzaotaiyang|微型人造太陽
147|7|kelaiyinping|克萊因瓶
148|7|fanlizihulu|反粒子葫蘆
165|7|tuzibaijian|兔子擺件
166|7|zhenxianhe|針線盒
167|7|zhanxindeyuangui|嶄新的圓規
168|7|fenyuanmofamao|次元魔法帽
169|7|fangshengjixieyu|仿生機械魚
170|7|yinghuochongzhiye|螢火蟲之夜
175|7|shouhuozhilu|收穫之鹿
176|7|wuxianyinfu|無限音符
177|7|yuzhouluopan|宇宙羅盤
178|7|chongdongtanceqi|蟲洞探測器
195|7|diancizhilong|電磁之龍
196|7|yuansuzhixin|元素之心
197|7|tongxinsuo|同心鎖
198|7|moliduorou|魔力多肉
199|7|xiaohuangya|小黃鴨
200|7|lifaqi|理髮器
205|7|feixingqijiaonang|飛行器膠囊
206|7|naojixinpian|腦機芯片
207|7|xingguichegnkeka|星軌乘客卡
208|7|bianxieshijijiaxiang|便攜式機甲箱
225|7|tianshiguoshi|天使果實
226|7|dianyingjiaopian|電影膠片
227|7|yuhangyuantoukui|宇航員頭盔
228|7|tongqupintu|童趣拼圖
229|7|bingfengzhiyan|冰封之眼
230|7|xiezhenji|寫真機
235|7|diyuansuzhizhu|地元素之珠
236|7|shuiyuansuzhizhu|水元素之珠
237|7|huoyuansuzhizhu|火元素之珠
238|7|fengyuansuzhizhu|風元素之珠
255|7|jishengpugongying|寄生蒲公英
256|7|jijiaqudonglu|機甲驅動爐
257|7|taiyangguoshi|太陽果實
258|7|feituwangguan|廢土王冠
259|7|wushuguanjunjiangbei|武術冠軍獎盃
260|7|feixueyizhiji|飛雪意志機
265|7|shuangzizuoxinghui|雙子座星徽
266|7|juxiezuoxinghui|巨蟹座星徽
267|7|shizizuoxinghui|獅子座星徽
268|7|chinvzuoxinghui|處女座星徽
285|7|liuhaohuahewu|六號化合物
286|7|huixiangtishen|回響替身
287|7|guokeyuzhou|果殼宇宙
288|7|huanjingzhitong|幻境之瞳
289|7|wannengmiyao|萬能密鑰
290|7|wenxuejiangzhang|文學獎章
7|4|juebanmanhua|絕版漫畫
8|4|guantoushipin|罐頭食品
9|4|huifuhuanjingdezhongzi|恢復環境的種子
10|4|yishidehuwaiyongpin|遺失的戶外用品
11|4|qiangguangshoudiantong|強光手電筒
12|4|shijiemoribaozhi|世界末日報紙
13|4|beikunxingcunzhedexinjian|被困倖存者的信件
14|4|yichuanmiyaoka|遺傳密鑰卡
15|4|xingcunzhexiaoshuo|倖存者小說
16|4|yinliaopinggai|飲料瓶蓋
17|4|fangdumianju|防毒面具
18|4|moriyuyanluyin|末日預言錄音
37|4|xingyunsiyecaoshouchuan|幸運四葉草手串
38|4|shixiaodeweixinglingjian|失效的衛星零件
39|4|laoshixiangji|老式相機
40|4|yiliuderijiben|遺留的日記本
41|4|shijiudejindan|獅鷲的金蛋
42|4|jiebaideyuyi|潔白的羽翼
43|4|jiatingheyingzhaopian|家庭合影照片
44|4|pojiudemaikefeng|破舊的麥克風
45|4|banguanshenshangxiansu|半管腎上腺素
46|4|gulaodelaiyaqin|古老的萊雅琴
57|4|dahongdenglong|大紅燈籠
58|4|xueshuqikan|學術期刊
59|4|zhuangshixinglinpian|裝飾性鱗片
60|4|xuancaihuachemoxing|炫彩花車模型
61|4|hanjiandemogu|罕見的蘑菇
62|4|lingmindeshouhuiban|靈敏的手繪板
63|4|quanxidiqiuyi|全息地球儀
64|4|fushezhiliaoyi|輻射治療儀
87|4|zenqiangxianshidoupeng|增強現實斗篷
88|4|kuangbaomianju|狂暴面具
89|4|jisuchangxue|疾速長靴
90|4|zhuiyinggongjian|追影弓箭
91|4|wuzhichangbaotu|霧之藏寶圖
92|4|chiyanjita|赤焰吉他
93|4|jininabanmenpiao|紀念版門票
94|4|cinengshoutao|磁能手套
95|4|sandiyanjing|三維眼鏡
96|4|shiyanshigongpai|實驗室工牌
119|4|naojizhiruqi|腦機植入器
120|4|jinjiyuezhang|禁忌樂章
121|4|shenhaiyangqiping|深海氧氣瓶
122|4|haigoutanzhaodeng|海溝探照燈
123|4|fangshuidahuoji|防水打火機
124|4|haidibaoxianxiang|海底保險箱
125|4|fangshengjiqihaitun|仿生機器海豚
126|4|jiaozhu|鮫珠
127|4|jixiefeixingyi|機械飛行翼
128|4|chenchuandingweiqi|沉船定位器
149|4|nengliangyasuoguan|能量壓縮罐
150|4|yinguolvxiangshui|因果律香水
151|4|leitingzhichui|雷霆之錘
152|4|liangzipeiyangmin|量子培養皿
153|4|huixuanjiasuqi|迴旋加速器
154|4|jueduihesetuliao|絕對黑色塗料
155|4|henengyizhibang|核能抑制棒
156|4|yuanziguangpu|原子光譜
157|4|rechengxiangyi|熱成像儀
158|4|shuijingdiaoxiang|水晶雕像
179|4|anwuzhiyuanquan|暗物質源泉
180|4|xukongzhisuo|虛空之鎖
181|4|jufengzhizhong|颶風之鐘
182|4|taiyangxidingweiqi|太陽系定位器
183|4|zhaohuangudi|召喚骨笛
184|4|anyingfengchao|暗影蜂巢
185|4|xingjifubiao|星際浮標
186|4|shiluozhimen|失落之門
187|4|jixiemifeng|機械蜜蜂
188|4|fangshengrenou|仿生人偶
209|4|oumijianenglianghexin|歐米伽能量核心
210|4|shiwangmotouyingmeitong|視網膜投影美瞳
211|4|chaoxingxituanlaoyin|超星系團烙印
212|4|jingjiwangguan|荊棘王冠
213|4|jueduijingzhizhimao|絕對靜止之錨
214|4|wuxianfangyulichang|無限防禦立場
215|4|wenmingshachaqi|文明沙查器
216|4|yongdongji|永動機
217|4|jueduilingduzhibing|絕對零度之冰
218|4|zuizhongrongyuxunzhang|最終榮譽勳章
239|4|mengjingtuoluo|夢境陀螺
240|4|xingyunmatitie|幸運馬蹄鐵
241|4|renshengchangjiban|人生唱機版
242|4|wangzhequantao|王者拳套
243|4|shanheshan|山河扇
244|4|jiedujing|解讀鏡
245|4|xunzongfeibiao|尋蹤飛鏢
246|4|zhikujinnang|智庫錦囊
247|4|minglingzhibian|命令之鞭
248|4|lianjindun|煉金盾
269|4|tianchengzuoxinghui|天秤座星徽
270|4|tianxiezuoxinghui|天蠍座星徽
271|4|sheshouzuoxinghui|射手座星徽
272|4|mojiezuoxinghui|摩羯座星徽
273|4|lingbai|靈擺
274|4|xingxiangkapai|星象卡牌
275|4|zhanxingshouzha|占星手札
276|4|yunshicanpian|隕石殘片
277|4|renzaoweixing|人造衛星
278|4|zhenkongbiaobenxiang|真空標本箱
19|3|shouyinji|收音機
20|3|shouyinjidianchi|收音機電池
21|3|gangbiyumoshuiping|鋼筆與墨水瓶
22|3|shuijinghuashebei|水淨化設備
23|3|qianglixinhaoqiang|強力信號槍
24|3|yiliaoxiang|醫療箱
47|3|toujiangcaipiao|頭獎彩票
65|3|youhuayiji|油畫遺跡
66|3|nihongdengzhaopai|霓虹燈招牌
97|3|hongwaiwangyuanjing|紅外望遠鏡
98|3|qiaokelibaomihua|巧克力爆米花
99|3|laoshihumujing|老式護目鏡
129|3|wufaximiedehuochai|無法熄滅的火柴
130|3|haidixunzhang|海底勳章
131|3|shuitong|水桶
159|3|chaorenleiyaopianhe|超人類藥片盒
160|3|heiyaobaoshi|黑曜寶石
161|3|laoshibaoxianxiang|老式保險箱
189|3|shiqianhuozhong|史前火種
190|3|jueduimingzhongfuwen|絕對命中符文
191|3|qiheifadian|漆黑髮簪
219|3|qulvyinqing|曲率引擎
220|3|fuzhirenpeiyangcang|複製人培養艙
221|3|kemengdehuiyilu|可夢的回憶錄
249|3|shuixiongchongbiaoben|水熊蟲標本
250|3|shuangshengling|雙生鈴
251|3|lingnengfengche|靈能風車
279|3|tianwenwangyuanjing|天文望遠鏡
280|3|tianwentaimoxing|天文台模型
281|3|yuhangyuanshouban|宇航員手辦
25|2|bianyishengwubiaoben|變異生物標本
26|2|fushejishuqi|輻射計數器
27|2|gudongzhinanzhen|古董指南針
28|2|shengmingtanceyi|生命探測儀
29|2|shouhuirili|手繪日曆
30|2|binanzhemingdan|避難者名單
67|2|mofaguoshi|魔法果實
68|2|laiziwaixingdetenglei|來自外星的藤類
69|2|hanbingsongta|寒冰松塔
100|2|wuxianheika|無限黑卡
101|2|shijianzantingqi|時間暫停器
102|2|mengxiangchengzhenbiji|夢想成真筆記
132|2|heijiaochangpian|黑膠唱片
133|2|suishenting|隨身聽
134|2|jieshideluxiangji|結實的錄像機
162|2|jiniankuandahuoji|紀念款打火機
163|2|jixiexinzang|機械心臟
164|2|beiyiqidefadongji|被遺棄的發動機
192|2|zhaomingtoudeng|照明頭燈
193|2|kaisuogongju|開鎖工具
194|2|suojiangdeziwoxiuyang|鎖匠的自我修養
222|2|jingdiandianyingyingpan|經典電影硬盤
223|2|zhumingyouxikadai|著名遊戲卡帶
224|2|zhencangdeyingji|珍藏的影集
252|2|weixingqianshuiting|微型潛水艇
253|2|juhetishanhu|聚合體珊瑚
254|2|jixieshuihudie|機械水蝴蝶
282|2|tiaosepan|調色盤
283|2|youhuayanliao|油畫顏料
284|2|huabu|畫布
`;

export const COLLECTIBLES: Collectible[] = rawCatalog
  .trim()
  .split('\n')
  .map((row) => {
    const [rawId, rawQuality, slug, name] = row.split('|');
    const id = Number(rawId);
    const quality = qualityByCode[Number(rawQuality)];

    return {
      id,
      name,
      quality,
      edition: editionForId(id),
      imageUrl: `https://wsrv.nl/?output=webp&url=https://garrytools.com/assets/img/survivor/UITexture/CollectionIcon/${id}_${slug}.png&hash=511`,
      detailUrl: `https://garrytools.com/collections/info?collectionId=${id}`,
    };
  })
  .sort((a, b) => a.edition - b.edition || a.id - b.id);

export const PRIORITY_COLLECTIBLES = [
  {
    id: 32,
    priority: '最優先',
    target: '無人機',
    reason: '終局主力技能，黃3、黃5、紅3、紅5每個斷點都有效。',
    milestones: ['黃3：飛彈數量＋5％', '黃5：單發傷害＋5％', '紅3：暴擊率＋10％', '紅5：飛彈數量與單發傷害各＋10％'],
  },
  {
    id: 116,
    priority: '最優先',
    target: '無人機',
    reason: '史詩收藏品成本比傳奇低，卻同時補無人機與暴擊率。',
    milestones: ['黃3：單發傷害＋3％', '黃5：飛彈數量＋3％', '紅3：暴擊率＋5％', '紅5：飛彈數量與單發傷害各＋5％'],
  },
  {
    id: 231,
    priority: '終局核心',
    target: '雙生無人機',
    reason: '同時強化一般無人機與雙生無人機，是合成科技後的長期核心。',
    milestones: ['黃3：兩種無人機單發傷害各＋5％', '黃5：兩種無人機單發傷害各＋10％', '紅3：暴擊傷害＋10％', '紅5：兩種無人機單發傷害各＋15％'],
  },
  {
    id: 75,
    priority: '高優先',
    target: '足球',
    reason: '量子球是高階單體與清場常用技能，且紅3提供暴擊率。',
    milestones: ['黃3：足球與量子球傷害＋20％', '黃5：量子球持續時間＋1秒', '紅3：暴擊率＋10％', '紅5：足球與量子球傷害＋25％'],
  },
  {
    id: 76,
    priority: '高優先',
    target: '雷電',
    reason: '適合雷電共振與相關套組，紅3同樣提供暴擊率。',
    milestones: ['黃3：雷電與狂雷電池傷害＋20％', '黃5：擴散電波傷害＋20％', '紅3：暴擊率＋10％', '紅5：雷電與狂雷電池傷害＋40％'],
  },
  {
    id: 2,
    priority: '暴擊補齊',
    target: '破壞之力',
    reason: '武器本體未必常駐，但紅3的全域暴擊率仍有價值。',
    milestones: ['黃3：投射物範圍再增加10％', '黃5：黑洞爆炸傷害＋60％', '紅3：暴擊率＋10％', '紅5：能量罩破裂爆炸傷害＋60％'],
  },
  {
    id: 79,
    priority: '模式需求',
    target: '永恆戰衣',
    reason: '用永恆戰衣打王或復活流時價值高；不用就延後。',
    milestones: ['黃3：復活額外恢復30％能量護盾', '黃5：第2次復活技能選擇＋1', '紅3：暴擊傷害＋10％', '紅5：技能傷害＋20％'],
  },
  {
    id: 147,
    priority: '暴擊補齊',
    target: '永恆戰衣',
    reason: '史詩成本較低，紅3能補5％暴擊率，適合暴擊斷點。',
    milestones: ['黃3：復活額外恢復15％護盾', '黃5：復活額外恢復20％護盾', '紅3：暴擊率＋5％', '紅5：技能傷害＋10％'],
  },
  {
    id: 171,
    priority: '流派需求',
    target: '燃油桶',
    reason: '燃燒與易傷流才投資；一般終局帳號排在無人機、暴擊之後。',
    milestones: ['黃3：火焰傷害＋20％', '黃5：燃油桶重傷使敵人額外承傷10％', '紅3：暴擊傷害＋10％', '紅5：火焰傷害＋40％'],
  },
  {
    id: 1,
    priority: '武器專精',
    target: '混亂之劍',
    reason: '只在混亂之劍仍是主武器時優先，否則主要取紅3暴擊傷害。',
    milestones: ['黃3：所有技能傷害再＋10％', '黃5：禁錮傷害上限再＋20％', '紅3：暴擊傷害＋10％', '紅5：靈魂潰散觸發全屏傷害'],
  },
  {
    id: 31,
    priority: '武器專精',
    target: '追光者',
    reason: '追光者專用收藏；終局已換武器時不要為技能效果追滿。',
    milestones: ['黃3：迴旋斬觸發更快、傷害＋10％', '黃5：劍陣觸發更快、傷害＋10％', '紅3：暴擊傷害＋10％', '紅5：迴旋斬與劍陣傷害＋20％'],
  },
  {
    id: 145,
    priority: '套組需求',
    target: '雷電',
    reason: '用來補雷電套組與暴擊傷害，非雷電主力可以排後。',
    milestones: ['黃3：雷電與狂雷電池傷害＋8％', '黃5：擴散電波傷害＋8％', '紅3：暴擊傷害＋5％', '紅5：雷電與狂雷電池傷害＋12％'],
  },
] as const;

export const COLLECTION_SET_GUIDE = [
  {
    title: '先完成自訂收藏',
    label: '全帳號收益',
    detail: '先解鎖足夠欄位，再把高星傳奇收藏品放入；對已成形帳號通常比硬追單一舊套組更划算。',
  },
  {
    title: '雙生無人機套組',
    label: '終局輸出',
    detail: '合成科技零件後，以暗物質傀儡等雙生無人機增幅收藏為核心，不要只看舊無人機收藏。',
  },
  {
    title: '暴擊率收藏群',
    label: '先到紅3',
    detail: '先把能提供暴擊率的史詩收藏推到紅3，再補暴擊傷害；成本與全域收益通常最好。',
  },
  {
    title: '模式專用套組',
    label: '按需求投資',
    detail: '永恆戰衣、燃燒、雷電與足球套組只在你的主力模式與技能輪替中投資，避免平均升星。',
  },
] as const;

export const COLLECTIBLE_SOURCES = {
  database: 'https://garrytools.com/collections/info',
  sets: 'https://garrytools.com/guide/collectionsets',
  chineseEffects: 'https://notalknote.xyz/survivorio-collection-hall/',
  official: 'https://apps.apple.com/us/app/survivor-io/id1528941310',
};
