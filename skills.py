#!/usr/bin/env python3
# -*- encoding=utf-8 -*-


import sys
import os
import json
import random
from dueros.Bot import Bot

from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1

from dueros.card.ImageCard import ImageCard
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem
from dueros.card.StandardCard import StandardCard
from dueros.card.TextCard import TextCard

class PuGongYing(Bot):

    def __init__(self, data):

        super().__init__(data)
        self.data = data
        # idiom modle
        self.addLaunchHandler(self.launchRequest)
        self.addIntentHandler('start_IdiomC', self.start_IdiomC)
        self.addIntentHandler('tell_idiom_story', self.tell_idiom_story)
        self.addIntentHandler('start_IdiomGuess', self.start_IdiomGuess)
        # english modle
        self.addIntentHandler('study_word', self.study_word)
        self.addIntentHandler('tell_joke', self.tell_joke)
        self.addIntentHandler('tell_english_story', self.tell_english_story)
        self.addIntentHandler('translate', self.translate)
        # else
        self.addIntentHandler('welcome', self.welcome)
        self.addIntentHandler('ai.dueros.common.default_intent', self.quesheng)
        self.idiom_story = {
            '滥竽充数': ['滥竽充数这则成语的滥是失实，与真实不符，引申为蒙混的意思；竽是一种簧管乐器；充数是凑数。指没有真才实学的人混在行家里充数，或是以次充好，有时也用作自谦之辞。这个成语来源于《韩非子.内储说上》，齐宣王使人吹竿，必三百人。南郭处士请为王吹竽，宣王说之，廪食以数百人。宣王死，潜王立，好一一听之，处士逃。战国时期，齐宣王非常喜欢听人吹竽，而且喜欢许多人一起合奏给他听，所以齐宣王派人到处搜罗能吹善奏的乐工，组成了一支三百人的吹竽乐队。而那些被挑选入宫的乐师，受到了特别优厚的待遇。当时，有一个游手好闲、不务正业的浪荡子弟，名叫南郭。他听说齐宣王有这种嗜好，就一心想混进那个乐队，便设法求见宣王，向他吹嘘自己是一名了不起的乐师，博得了宣王的欢心，把他编入了吹竽的乐师班里。可笑的是，这位南郭先生根本不会吹竽。每当乐队给齐宣王吹奏的时候，他就混在队伍里，学着别的乐工的样子，摇头晃脑，东摇西摆，装模做样地在那儿吹奏。因为他学得维妙维肖，又由于是几百人在一起吹奏，齐宣王也听不出谁会谁不会。就这样，南郭混了好几年，不但没有露出一丝破绽，而且还和别的乐工一样领到一份优厚的赏赐，过着舒适的生活。后来，齐宣王死了，他儿子齐潜王继位，潜王同样爱听吹竽。只有一点不同，他不喜欢合奏，而喜欢乐师门一个个单独吹给他听。南郭先生听到这个消息后，吓得浑身冒汗，整天提心吊胆的。心想，这回要露出马脚来了，丢饭碗是小事，要是落个欺君犯上的罪名，连脑袋也保不住了。所以，趁潜王还没叫他演奏，就赶紧溜走了。 ', ''],
            '画蛇添足': ['战国时楚国有位管祠堂的人，在祭祀后把酒分给底下办事的人，但酒不够分，于是他们想出一个办法来：大家在地上画蛇，画得最快的人就可以喝酒。其中一人画得最快，正打算拿酒来喝，因见其它人还未画好，他就再为蛇添上脚，此时另一人刚好画好了，便从他的手上把酒抢过来，并说：“蛇本来没有脚，你为甚么要为它添上脚呢？”说完就把酒喝掉了。', ''],
            '守株待兔': ['春秋时代有位宋国的农夫，他每天早上很早就到田里工作，一直到太阳下山才收拾农具准备回家。有一天，农夫正在田里辛苦的工作，突然却远远跑来一只兔子。这只兔子跑得又急又快，一个不小心，兔子撞上稻田旁边的大树，这一撞，撞断了兔子的颈部，兔子当场倒地死亡。一旁的农夫看到之后，急忙跑上前将死了的兔子一手抓起，然后很开心的收拾农具准备回家把这只兔子煮来吃。农夫心想，天底下既然有这么好的事，自己又何必每天辛苦的耕田？从此以后，他整天守在大树旁，希望能再等到不小心撞死的兔子。可是许多天过去了，他都没等到撞死在大树下的兔子，反而因为他不处理农田的事，因此田里长满了杂草，一天比一天更荒芜。', ''],
            '刻舟求剑': ['这个成语来源于《吕氏春秋.察今》，楚人有涉江者，其剑自舟中坠于水，遽契其舟曰：是吾剑之所从坠。舟止，从其所契者入水求之。战国时，楚国有个人坐船渡江。船到江心，他一不小心，把随身携带的一把宝剑掉落江中。他赶紧去抓，已经来不及了。船上的人对此感到非常惋惜，但那楚人似乎胸有成竹，马上掏出一把小刀，在船舷上刻上一个记号，并向大家说：这是我宝剑落水的地方，所以我要刻上一个记号。大家都不理解他为什么这样做，也不再去问他。船靠岸后那楚人立即在船上刻记号的地方下水，去捞取掉落的宝剑。捞了半天，不见宝剑的影子。他觉得很奇怪，自言自语说：我的宝剑不就是在这里掉下去吗？我还在这里刻了记号呢，怎么会找不到的呢？至此，船上的人纷纷大笑起来，说：船一直在行进，而你的宝剑却沉入了水底不动，你怎么找得到你的剑呢？其实，剑掉落在江中后，船继续行驶，而宝剑却不会再移动。像他这样去找剑，真是太愚蠢可笑了。《吕氏春秋》的作者也在写完这个故事后评论说这个，刻舟求剑的人是太愚蠢可笑了！', ''],
            '掩耳盗铃': ['从前有一个人，看见人家门口有一口大钟，就想把它偷去。可这钟太重，没法背走，他就取来一个铁锤，想敲碎后一块块偷走。可是还有一个问题，用铁椎砸钟会发出很大的声音，肯定会被人抓做的。他转念一想：钟一响耳朵就能听见，可是如果把耳朵蒙起来，就什么都听不到了！掩耳盗铃：比喻蠢人自己欺骗自己。《吕氏春秋·自知》：有得钟者，欲负而走，则钟大不可负。以椎毁之，钟况然有音。恐人闻之而夺已也，遽掩其耳。', ''],
            '买椟还珠': ['春秋时代，楚国有一个商人，专门卖珠宝的，有一次他到齐国去兜售珠宝，为了生意好，珠宝畅销起见，特地用名贵的木料，造成许多小盒子，把盒子雕刻装饰得非常精致美观，使盒子会发出一种香味，然后把珠宝装在盒子里面。有一个郑国人，看见装宝珠的盒子既精致又美观，问明了价钱后，就买了一个，打开盒子，把里面的宝物拿出来，退还给珠宝商。', ''],
            '自相矛盾': ['战国时楚国有一个卖盾和矛的人，他夸说自己所卖的盾坚固无比，没有东西能把它刺穿；又夸说自己所卖的矛十分锋利，没有东西不被它刺穿。路上有人听见后，忍不住说：“如果用你的矛去刺你的盾，结果会如何？”楚国人立刻瞠目结舌，无法回答他的问题。', ''],
            '拔苗助长': ['拔苗助长这则成语的意思是将苗拔起，帮助它生长。比喻不顾事物发展的规律，强求速成，结果反而把事情弄糟。这个成语来源于《孟子.公孙丑上》，宋人有闵其苗之不长而揠之者，芒芒然归，谓其人曰：今日病矣！予助苗长矣！其子趋而往视之，苗则槁矣。《孟子》是一部儒家经典，记载了战国时期著名思想家孟轲的政治活动、政治学说和哲学伦理教育思想。这部书中有个故事十分有名：宋国有一个农夫，他担心自己田里的禾苗长不高，就天天到田边去看。可是，一天、两天、三天，禾苗好象一点儿也没有往上长。他在田边焦急地转来转去，自言自语地说：我得想办法帮助它们生长。一天，他终于想出了办法，急忙奔到田里，把禾苗一棵棵地拔，从早上一直忙到太阳落山，弄得精疲力尽。他回到家里，十分疲劳，气喘吁吁地说：今天可把我累坏了，力气总算没白费，我帮禾苗都长高了一大截。他的儿子听了，急忙跑到田里一看，禾苗全都枯死了。孟轲借用这个故事向他的学生们说明违反事物发展的客观规律而主观地急躁冒进，就会把事情弄糟。', ''],
            '亡羊补牢': ['战国七雄之一的楚国，国土比较大，国势比较强，可是传至襄王，宠信佞臣，一意贪图享受，朝政一天比一天紊乱。有一位大臣庄辛，忠心耿耿，看到这种情形，知道楚国已经伏下了严重的危机，十分担忧。有一天就向襄王说：“大王的四周有州侯、夏侯、鄢陵君和寿陵君这四个人，大王一味宠信他们，受了他们包围，整天陶醉在酒里，浪费国帑，不管国家大事，这样下去，恐怕楚国难保了。”襄王听了，很不高兴，就用责备的口吻说：“你喝醉了吧？要不然就是你老糊涂了！你看国跟国之间互不侵扰，国内又太平无事，不知道你为什么说这些不吉祥的话？也许你要变成楚 ', ''],
            '杯弓蛇影': ['有一天，乐广请他的朋友在家里大厅中喝酒。那个朋友在喝酒的时候，突然看见自己的酒杯里，有一条小蛇的影子在晃动，他心里很厌恶，可还是把酒喝了下去。喝了之后，心里到底不自在，放心不下。回到家中就生起病来。隔了几天，乐广听到那个朋友生病的消息，了解了他得病的原因。乐广心里想：酒杯里绝对不会有蛇的！于是，他就跑到那天喝酒的地方去察看。原来，在大厅墙上，挂有一把漆了彩色的弓。那把弓的影子，恰巧映落在那朋友放过酒杯的地方，乐广就跑到那个朋友那里去，把这事解释给他听。这人明白了原因以后，病就立刻好了。后来人们就用杯弓蛇影比喻疑神疑鬼，自相惊扰。', ''],
            '背水一战': ['这个成语来源于《史记.淮阴侯列传》，信乃使万人先行，出，背水陈。...军皆殊死战，不可败。韩信，淮阴（今江苏清江西南）人。他是汉王刘邦手下的大将。为了打败项羽，夺取天下，他为刘邦定计，先攻取了关中，然后东渡黄河，打败并俘虏了背叛刘邦、听命于项羽的魏王豹，接着往东攻打赵王歇。韩信的部队要通过一道极狭的山口，叫井陉口。赵王手下的谋士李左军主张一面堵住井陉口，一面派兵抄小路切断汉军的辎重粮草，韩信的远征部队没有后援，就一定会败走；但大将陈余不听，仗着兵力优势，坚持要与汉军正面作战。韩信了解到这一情况，非常高兴。他命令部队在离井陉三十里的地方安营，到了半夜，让将士们吃些点心，告诉他们打了胜仗再吃饱饭。随后，他派出两千轻骑从小路隐蔽前进，要他们在赵军离开营地后迅速冲入赵军营地，换上汉军旗号；又派一万军队故意背靠河水排列阵势来引诱赵军。到了天明，韩信率军发动进攻，双方展开激战。不一会，汉军假意败回水边阵地，赵军全部离开营地，前来追击。这时，韩信命令主力部队出击，背水结阵的士兵因为没有退路，也回身猛扑敌军。赵军无法取胜，正要回营，忽然营中已插遍了汉军旗帜，于是四散奔逃。汉军乘胜追击，打了一个大胜仗。在庆祝胜利的时候，将领们问韩信：兵法上说，列阵可以背靠山，前面可以临水泽，现在您让我们背靠水排阵，还说打败赵军再饱饱地吃一顿，我们当时不相信，然而竟然取胜了，这是一种什么策略呢？韩信笑着说：这也是兵法上有的，只是你们没有注意到罢了。兵法上不是说‘陷之死地而后生，置之亡地而后存’吗？如果是有退路的地方，士兵都逃散了，怎么能让他们拼命呢！这个故事演化出成语背水一战，多用于军事行动，也可用于比哺有决战性质的行动。', ''],
            '望梅止渴': ['南朝？宋？刘义庆《世说新语？假谲》：有一次曹操带兵在外行军，一时找不到取水的地方，士兵都渴极了，曹操就骗他们说：“前面有个大梅林，梅子又甜又酸，可以解渴。”士兵听了，一个个都流出了口水，暂时止住了口渴。', ''],
            '纸上谈兵': ['赵括从小学习兵法，自以为天下没有人能够与其匹敌。他的父亲赵奢曾经评论说：“打仗是非常危险的事情，而赵括把它说得太容易了，假使将来赵国不任命他为将军，那也就算了，如果一定要拜他为将军，导致赵军大败的人必定是赵括无疑。”后来赵括果然代替廉颇做了大将军，长平一战被秦将白起打败，四十万赵军全部被消灭，赵括自己也战死了。', ''],
            '三顾茅庐': ['东汉末年，诸葛亮居住在隆中的茅庐里。谋士徐庶向刘备推荐说：诸葛亮是个奇才。刘备为了请诸亮帮助自己打天下，就同关羽、张飞一起去请他出山。可是诸葛亮不在家，刘备只好留下姓名，怏怏不乐地回去。隔了几天，刘备打听到诸葛亮回来了，又带着关羽、张飞冒着风雪前去。哪知诸葛亮又出门出去了，刘备他们又空走一趟。刘备第三次去隆中，终于见到了诸葛亮。在交谈中，诸葛亮对天下形势作了非常精辟的分析，刘备十分叹服。刘备三顾茅庐，使诸葛亮非常感动，答应出山相助。刘备尊诸葛亮为军师，对关羽、张飞说：我之有孔明，犹鱼之有水也！诸葛亮初出茅庐，就帮刘备打了不少胜仗，为刘备奠定了蜀汉的国基。成语三顾茅庐由此而来，', ''],
            '卧薪尝胆': ['春秋时期，吴王夫差凭着自己国力强大，领兵攻打越国。结果越国战败，越王勾践于是被抓到吴国。吴王为了羞辱越王，因此派他看墓与喂马这些奴仆才做的工作。越王心里虽然很不服气，但仍然极力装出忠心顺从的样子。吴王出门时，他走在前面牵着马；吴王生病时，他在床前尽力照顾，吴王看他这样尽心伺候自己，觉得他对自己非常忠心，最后就允许他返回越国。越王回国后，决心洗刷自己在吴国当囚徒的耻辱。为了告诫自己不要忘记复仇雪恨，他每天睡在坚硬的木柴上，还在门上吊一颗苦胆，吃饭和睡觉前都要品尝一下，为的就是要让自己记住教训。除此之外，他还经常到民间视察民情，替百姓解决问题，让人民安居乐业，同时加强军队的训练。经过十年的艰苦奋斗，越国变得国富兵强，于是越王亲自率领军队进攻吴国，也成功取得胜利，吴王夫差羞愧得在战败后自杀。后来，越国又趁胜进军中原，成为春秋末期的一大强国。 ', ''],
            '四面楚歌': ['项羽和刘邦原来约定以鸿沟（在今河南荣县境贾鲁河）东西边作为界限，互不侵犯。后来刘邦听从张良和陈平的规劝，觉得应该趁项羽衰弱的时候消灭他，就又和韩信、彭越、刘贾会合兵力追击正在向东开往彭城（即今江苏徐州）的项羽部队。终于布置了几层兵力，把项羽紧紧围在垓下（在今安徽灵璧县东南）。这时，项羽手下的兵士已经很少，粮食又没有了。夜里听见四面围住他的军队都唱起楚地的民歌，不禁非常吃惊地说：刘邦已经得到了楚地了吗？为什么他的部队里面楚人这么多呢？说看，心里已丧失了斗志，便从床上爬起来，在营帐里面喝酒，并和他最宠爱的妃子虞姬一同唱歌。唱完，直掉眼泪，在一旁的人也非常难过，都觉得抬不起头来。虞姬自刎于项羽的马前，项羽英雄末路，带了仅剩兵卒至乌江，最终自刎于江边。以后人们就用四面楚歌这个词，形容人们遭受各方面攻击或逼迫，而陷于孤立窘迫的境地。凡是陷于此种境地者，其命运往往是很悲惨的。例如某人因经常与坏人为伍，不事生产，游手好闲，但后来却被那些坏人逼迫得无以为生，而求助于别人时，别人又因他平日行为太坏，绝不同情理睬，这人所处的境地便是四面楚歌。', ''],
            '指鹿为马': ['秦朝二世的时候，宰相赵高掌握了朝政大权。他因为害怕群臣中有人不服，就想了一个主意。有一天上朝时，他牵着一只梅花鹿对二世说：陛下，这是我献的名马，它一天能走一千里，一夜能走八百里。二世听了，大笑说：承相啊，这明明是一只鹿，你却说是马，真是错得太离谱了！赵高说：这确实是一匹马，陛下怎么说是鹿呢？二世觉得纳闷，就让群臣百官来评判。大家心想，说实话会得罪承相，说假话又怕欺骗陛下，就都不出声。这时赵高盯着群臣，指着鹿大声问：大家看，这样身圆腿瘦，耳尖尾粗，不是马是甚么？大家都害怕赵高的势力，知道不说不行，就都说是马，赵高非常得意，二世被弄胡涂了，明明是鹿，怎么大家都说是马呢？他以为自己疯了，从此越来越胡涂，朝政上的事都完全由赵高来操纵。赵高暗中把那些说实话的人杀掉，又派人杀死二世，霸占整个朝廷，最后终于导致秦朝灭亡。', ''],
            '画龙点睛': ['传说古时候有个画家叫张僧繇，他画龙画得特别好。有一次，他在金陵（现在南京）安乐寺的墙壁上画了四条巨龙，那龙画得活灵活现，非常逼真，只是都没有眼睛。人们问张僧繇：“为什么不把眼睛画出来。”他说：“眼睛可不能轻易画呀！一画了，龙就会腾空飞走的！”大家听了，谁也不信，都认为他在说大话。后来，经不起人们一再请求，张僧繇只好答应把龙的眼睛画出来。奇怪的事情果然发生了，他刚刚点出第二条龙的眼睛，突然刮起了大风，顷刻间电闪雷鸣。两条巨龙转动着光芒四射的眼睛冲天而起，腾空而去。围观的人，个个看得目瞪口呆，对张僧繇更佩服了。成语“画龙点睛”就是从这个传说中来的。现在一般用来比喻写作、讲话时，在关键性的地方用上一两句精辟的语言来点明含义，使内容更加生动有力。这种手法也称为“点睛”之笔。', ''],
            '攀龙附凤': ['“攀龙附凤”这则成语的“龙、凤”是形容有权势的人。比喻巴结或投靠有权势的人。这个成语来源于《汉书.叙转下》，午阳鼓刀，滕公厩驺，颖阴商贩，曲周庸夫，攀龙附凤，并乘天衢。西汉的开国皇帝刘邦，出身于一个农民家庭，他的父母连名字都没有。刘邦原名季，意思是“老三”，直到做了皇帝，才改名为邦。刘邦三十岁时，当了秦朝沛县的一个乡村小吏——亭长。他为人豁达大度，胸怀开朗，做事很有气魄，很多人都和他合得来。当地的萧何、樊哙、夏侯婴等，都是他的好朋友。这些人后来都为刘邦建立汉朝出了大力。樊哙是刘邦的同乡，是个杀狗卖狗的。陈胜、吴广发动起义后，沛县县令惊恐万分，打算投起义之机响应陈胜，就派樊哙去召刘邦来相助。不料刘邦带了几百人来时，县令又反悔起来。于是，刘邦说服城里人杀了县令，带领二三千人马誓师起兵。夏侯婴与刘邦也早就有了交情。他原来是县衙里的马夫，每次奉命为过往使者赶车，回来时经过刘邦那里，总要与刘邦闲谈很长时间，直到日落西山才走。后来夏侯婴当了县吏，与刘邦交往更密切了。一天刘邦与他闹着玩，一不小心打伤了他。有人告刘邦身为亭长，动手打人，应当严惩，夏侯婴赶紧为他解释。不料，后来夏侯婴反以伪证罪被捕下狱，坐了一年多班房。后来刘邦在沛县起兵，他和樊哙主动参加，并担任部将。刘邦的势力逐渐发展后，有个名叫灌婴的人又来投奔他。灌婴是睢阳人，本为贩卖丝绸的小商人。此人后来也成为刘邦的心腹，领兵转战各地，立了不少战功。公元前208年，刘邦根据各路起义军开会的决定，带领人马西攻秦都咸阳。第二年初，刘邦大军兵临陈留，把营扎在城郊，当地有个名叫郦食其的小吏前来献计。郦食其对刘邦说，现在您兵不满万人，又缺乏训练，要西攻强秦，如进虎口。不如先攻取陈留，招兵买马，等兵强马壮后再打天下。郦食其还表示，他和陈留县令相好，愿意前去劝降；如县令不降，就把他杀了。刘邦采纳了郦食其的计谋。郦食其连夜进陈留城劝说县令，但那县令不肯起义。于是郦食其半夜割下他的头颅来见刘邦。第二天刘邦攻城时，把那县令的头颅高悬在竹竿上，结果守军开城门投降。在陈留，刘邦补充了大量粮食、武器和兵员。接着郦食其又推荐了他颇有智勇的弟弟郦商，郦商又给刘邦带来了四千人。刘邦就任命他为副将，带领这支队伍西攻开封。后来，刘邦又战胜项羽，在公元前202年即皇帝位，建立了西汉王朝。刘邦当皇帝后大封功臣，樊哙、夏侯婴、灌婴、郦商等人也先后被封为舞阳侯、当汝阴侯、颖阴侯和曲周侯。', ''],
            '屠龙之技': ['有个人叫朱泙漫，他想学一种出奇的本领，听说支离益会宰龙，就去拜支离益做老师，向他学宰龙的本领。朱泙漫在支离益那儿学了三年，家产都花光了，才把宰龙的本领学到了手。可是天下本来没有龙，他到哪儿去施展他那绝妙的本领呢？“屠龙之技”就是从这个故事来的，比喻毫不实用的所谓不平凡的本领。“屠”是“宰杀”，“技”是“技巧”，“本领”。', ''],
            '叶公好龙': ['春秋时，有位叫叶公的人非常喜欢龙。他家的屋梁上、柱子上和门窗上都雕刻着龙的图案，墙上也绘着龙。传说天上的真龙知道此事后很受感动，专程到叶公家里来，把头从窗口伸进屋子里，把尾巴横在客堂上。叶公看到后，吓得面无血色，魂不附体，抱头就跑。原来他并不是真正喜欢龙。他爱的是假龙，怕的是真龙。这个成语比喻表面上爱好某一事物，实际上并不是真正爱好它，甚至是畏惧它。', ''],
            '精卫填海': ['传说，很久以前，炎帝有个女儿叫女娃，炎帝很喜欢她，经常带她到东海去游泳。女娃非常勇敢，大风大浪从不畏惧。女娃长大后，每天都要自己到东海去游泳。有一天，她不幸被大海淹死了。女娃死后变成了一只鸟，每天从山上衔来石头和草木，投入东海，然后发出“精卫”“精卫”的叫声，好像在呼唤着自己。精卫鸟日复一日，年复一年，顽强不息，坚持不懈，决心要把东海填平。这句成语比喻矢志不移，努力不懈。后人常以“精卫填海”这个成语比喻深仇大恨，立志必报。或比喻不畏艰难险阻，矢志不移的坚毅决心。', ''],
            '八仙过海': ['传说吕洞宾等八位神仙去赴西王母的的蟠桃会，途经东海，只见巨浪汹涌。吕洞宾提议各自投一样东西到海里，然后各显神通过海。于是铁拐李把拐杖投到水里，自己立在水面过海；韩湘子以花蓝技水而渡；吕洞宾、蓝采和、张果老、汉钟离、曹国舅。何仙姑也分别把自己的萧、拍板、纸驴、鼓、玉版、竹罩投到海里，站在上面逐浪而过。八位神仙都靠自己的神通渡过了东海。八仙过海根据这个传说而来。八仙过海比喻各自有一套办法或本领去完成任务。', ''],
            '开天辟地': ['神话中传说，世上最早时，天地浑然一体。世界像个鸡蛋，天地的开创人盘古就在蛋里。一万八千年后，盘古从蛋里走出来。蛋里淡淡的烟云冉冉上升，变成青天。混浊的沉渣逐渐凝聚，变成大地。天地近在咫尺。盘古弯曲着背把天地撑开。盘古顶开立地一万八千年，终于把天撑高。天地再也不会合在一起，盘古才安然死去。他呼出的气，变成风和云。他留下的声音，变成雷霆。他的眼睛变成太阳和月亮。盘古开创了世界。颂扬开创伟大事业，称开天辟地。', ''],
            '三顾茅庐': ['东汉末年，诸葛亮居住在隆中的茅庐里。谋士徐庶向刘备推荐说：诸葛亮是个奇才。刘备为了请诸亮帮助自己打天下，就同关羽、张飞一起去请他出山。可是诸葛亮不在家，刘备只好留下姓名，怏怏不乐地回去。隔了几天，刘备打听到诸葛亮回来了，又带着关羽、张飞冒着风雪前去。哪知诸葛亮又出门出去了，刘备他们又空走一趟。刘备第三次去隆中，终于见到了诸葛亮。在交谈中，诸葛亮对天下形势作了非常精辟的分析，刘备十分叹服。刘备三顾茅庐，使诸葛亮非常感动，答应出山相助。刘备尊诸葛亮为军师，对关羽、张飞说：我之有孔明，犹鱼之有水也！诸葛亮初出茅庐，就帮刘备打了不少胜仗，为刘备奠定了蜀汉的国基。成语三顾茅庐由此而来，', ''],
            '草船借箭': ['“草船借箭”这则成语的意思是运用智谋，凭借他人的人力或财力来达到自己的目的。这个成语来源于《三国演义》，用奇谋孔明借箭。三国时期，曹操率大军想要征服东吴，孙权、刘备联合抗曹。孙权手下有位大将叫周瑜，智勇双全，可是心胸狭窄，很妒忌诸葛亮（字孔明）的才干。因水中交战需要箭，周瑜要诸葛亮在十天内负责赶造十万支箭，哪知诸葛亮只要三天，还愿立下军令状，完不成任务甘受处罚。周瑜想，三天不可能造出十万支箭，正好利用这个机会来除掉诸葛亮。于是他一面叫军匠们不要把造箭的材料准备齐全，另一方面叫大臣鲁肃去探听诸葛亮的虚实。鲁肃见了诸葛亮。诸葛亮说：“这件事要请你帮我的忙。希望你能借给我20只船，每只船上30个军士，船要用青布慢子遮起来，还要一千多个草把子，排在船两边。不过，这事千万不能让周瑜知道。”鲁肃答应了，并按诸葛亮的要求把东西准备齐全。两天过去了，不见一点动静，到第三天四更时候，诸葛亮秘密地请鲁肃一起到船上去，说是一起去取箭。鲁肃很纳闷。诸葛亮吩咐把船用绳索连起来向对岸开去。那天江上大雾迷漫，对面都看不见人。当船靠近曹军水寨时，诸葛亮命船一字儿摆开，叫士兵擂鼓呐喊。曹操以为对方来进攻，又因雾大怕中埋伏，就派六千名弓箭手朝江中放箭，雨点般的箭纷纷射在草把子上。过了一会，诸葛亮又命船掉过头来，让另一面受箭。太阳出来了，雾要散了，诸葛亮令船赶紧往回开。这时船的两边草把子上密密麻麻地插满了箭，每只船上至少五、六千支，总共超过了十万支。鲁肃把借箭的经过告诉周瑜时，周瑜感叹地说：“诸葛亮神机妙算，我不如他。”', ''],
            '草木皆兵': ['这个成语来源于《晋书.苻坚载记》，坚与苻融登城而望王师，见部阵齐整，将士精锐；又北望八公山上草木，皆类人形。公元383年，基本上统一了北方的前秦皇帝苻坚，率领90万兵马，南下攻伐东晋。东晋王朝任命谢石为大将，谢玄为先锋，率领8万精兵迎战。秦军前锋苻融攻占寿阳（今安徽寿县）后，苻竖亲自率领八千名骑兵抵达这座城池。他听信苻融的判断，认为晋兵不堪一击，只要他的后续大军一到，一定可大获全胜。于是，他派一个名叫朱序的人去向谢石劝降。朱序原是东晋官员，他见到谢石后，报告了秦军的布防情况，并建议晋军在前秦后续大军未到达之前袭击洛涧（今安徽淮南东洛河）。谢石听从他的建议，出兵偷袭秦营，结果大胜。晋兵乘胜向寿阳进军。苻坚得知洛涧兵败，晋兵正向寿阳而来，大惊失色，马上和苻融登上寿阳城头，亲自观察淝水对岸晋军动静。当时正是隆冬时节，又是阴天，远远望去，淝水上空灰蒙的一片。仔细看去，那里桅杆林立，战船密布，晋兵持刀执戟，阵容甚为齐整。他不禁暗暗称赞晋兵布防有序，训练有素。接着，苻坚又向北望去。那里横着八公山，山上有八座连绵起伏的峰峦，地势非常险要。晋兵的大本营便驻扎在八公山下。随着一阵西北风呼啸而过，山上晃动的草木，就像无数士兵在运动。苻坚顿时面如土色，惊恐地回过头来对苻融说：晋兵是一支劲敌，怎么能说它是弱兵呢？不久，苻坚中谢玄的计，下令将军队稍向后退，让晋兵渡过淝水决战。结果，秦兵在后退时自相践踏，溃不成军，大败北归。这一战，便是历史上著名的淝水之战，是历史上以少胜多，以弱胜强的著名战例。', ''],
            '破釜沉舟': ['破釜沉舟”这则成语的釜是锅；舟是船。砸破烧饭用的锅子，凿沉船只，比喻拚死一战。这个成语来源于《史记.项羽本纪》，项羽乃悉引兵渡河，皆沉船，破釜甑，烧庐舍，持三日粮，以示士卒必死，无一还心。秦朝末年，秦二世派大将章邯攻打赵国。赵军不敌，退守巨鹿（今河北平乡西南），被秦军团团围住。楚怀王封宋义为上将军，项羽为副将，派他们率军去救援赵国。不料，宋义把兵带到安阳（今山东曹县东南）后，接连46天停滞不进。项羽忍不住，一再要求他赶紧渡江北上，赶到巨鹿，与被围赵军来个里应外合。但宋义另有所谋，想让秦、赵两军打得精疲力竭再进兵，这样便于取胜。他严令军中，不听调遣的人，不管是谁都要杀。与此同时，宋义又邀请宾客，大吃大喝，而士兵和百姓却忍饥挨饿。项羽忍无可忍，进营帐杀了宋义，并声称他勾结齐国反楚，楚王有密令杀他。将士们马上拥戴项羽代理上将军。项羽把杀宋义的事及原因报告了楚怀王，楚怀王只好正式任命他为上将军。项羽杀宋义的事，震惊了楚国，并在各国有了威名。他随即派出两名将军，率2万军队渡河去救巨鹿。在获悉取得小胜并接到增援的请求后，他下令全军渡河救援赵军。项羽在全军渡河之后，采取了一系列果断的行动：把所有的船只凿沉，击破烧饭用的锅子，烧掉宿营的屋子，只携带三天干粮，以此表示决心死战，没有一点后退的打算。这支有进无退的大军到了巨鹿外围，立即包围了秦军。经过9次激战，截断了秦军的补给线。负责围攻巨鹿的两名秦将，一名被活捉，另一名投火自焚。在这之前，来援助赵国的各路诸侯虽然有几路军队在巨鹿附近，但都不敢与秦军交锋。楚军的拚死决战并取得胜利，大大地提高了项羽的声威。从此，项羽率领的军队成了当时反秦力量中最强大的一支武装。后来，“皆沉船，破釜甑”演化为成语“破釜沉舟”，用来比喻拚死一战，决心很大。项羽也成了当时农民起义军的著名领袖人物，并在不久和刘邦的起义军一起，推翻了秦朝的统治。', ''],
            '穷兵黩武': ['东吴后期的名将陆抗，二十岁时就被任命为建武校尉；带领他父亲陆逊留下的部众五千人。公元264年，孙皓当了东吴的国君，三十八岁的陆抗担任镇军大将军。当时，东吴的朝政非常腐败。孙皓荒淫暴虐，宫女有好几千人，还向民间掠夺；又用剥面皮、凿眼睛筹酷刑任意杀人。陆抗对孙皓的所作所为非常不满，多次上疏，劝谏他对外加强防守，对内改善政治，以增强国力。他曾在奏疏中一次陈述当前应做的事达十六件之多。但是，孙皓对他的建议置之不理。公元272年，镇守西陵的吴将步阐投降晋朝。陆抗得知后、立即率军征讨步阐。他知道晋军一定会来接应步阐，', ''],
            '曲高和寡': ['宋玉是楚国伟大诗人屈原的学生。有一天，楚襄王问宋玉：现在不少人对你有意见，你是不是有什么不对的地方？宋玉转弯抹角地回答说：有位歌唱家在我们都城的广场上演唱，唱《下里》《巴人》这些通俗歌曲时，有几千听众跟着唱起来；唱《阳春》《白雪》这类高深歌曲时，能跟着唱的只有几十人；到了唱更高级的歌曲时，跟着唱的只有几个人了。从这里可以看出，曲调越是高深，能跟着一起唱的人就越少。宋玉这段话的意思是说自己品行高超，一般的人不能了解，所以有人说三道四。和（音贺）指跟着别人唱；寡是少的意思。这个成语后来比喻言论、作品很深，能理解的人很少。有时也用来讽刺别人自命不凡。', ''],
            '走马看花': ['唐朝中期，有位著名的诗人孟郊。他出身贫苦，从小勤奋好学，很有才华。但是，他的仕途却一直很不顺利，从青年到壮年，好几次参加进士考试都落了第。他虽然穷困潦倒，甚至连自己的家属都养不起，但他性情耿直，不肯走权贵之门。他决心刻苦攻读，用自己的真才实学，叩开仕途的大门。唐德宗贞元十三年(公元797年)，孟郊又赴京参加了一次进士考试，这次，他进士及第了，孟郊高兴极了。他穿上崭新的衣服，扎上彩带红花，骑着高头大马，在长安城里尽情地游览。京城美丽的景色使他赞叹，高中进士的喜悦又使他万分得意，于是，他写下了这首著名的《登科后》诗：昔日龌龃不足夸，今朝旷荡恩无涯；春风得意马蹄疾，一日看尽长安花。这首诗把诗人中了进士后的喜悦心情表现得淋漓尽致，其中“春风得意马蹄疾，一日看尽长安花”成为千古名句', ''],
            '刻舟求剑': ['这个成语来源于《吕氏春秋.察今》，楚人有涉江者，其剑自舟中坠于水，遽契其舟曰：是吾剑之所从坠。舟止，从其所契者入水求之。战国时，楚国有个人坐船渡江。船到江心，他一不小心，把随身携带的一把宝剑掉落江中。他赶紧去抓，已经来不及了。船上的人对此感到非常惋惜，但那楚人似乎胸有成竹，马上掏出一把小刀，在船舷上刻上一个记号，并向大家说：这是我宝剑落水的地方，所以我要刻上一个记号。大家都不理解他为什么这样做，也不再去问他。船靠岸后那楚人立即在船上刻记号的地方下水，去捞取掉落的宝剑。捞了半天，不见宝剑的影子。他觉得很奇怪，自言自语说：我的宝剑不就是在这里掉下去吗？我还在这里刻了记号呢，怎么会找不到的呢？至此，船上的人纷纷大笑起来，说：船一直在行进，而你的宝剑却沉入了水底不动，你怎么找得到你的剑呢？其实，剑掉落在江中后，船继续行驶，而宝剑却不会再移动。像他这样去找剑，真是太愚蠢可笑了。《吕氏春秋》的作者也在写完这个故事后评论说这个，刻舟求剑的人是太愚蠢可笑了！', '']
        }
        self.idiom = [
            '水漫金山', '重蹈覆辙', '行尸走肉', '金蝉脱壳', '百里挑一', '金玉满堂', '愚公移山', '魑魅魍魉', '背水一战', '霸王别姬',
            '天上人间', '不吐不快', '海阔天空', '情非得已', '满腹经纶', '兵临城下',
            '春暖花开', '插翅难逃', '黄道吉日', '天下无双', '偷天换日', '两小无猜', '卧虎藏龙', '珠光宝气', '簪缨世族', '花花公子',
            '绘声绘影', '国色天香', '相亲相爱', '八仙过海', '金玉良缘', '掌上明珠',
            '皆大欢喜', '生财有道', '极乐世界', '情不自禁', '龙生九子', '精卫填海', '海市蜃楼', '高山流水', '卧薪尝胆', '壮志凌云',
            '否极泰来', '金枝玉叶', '囊中羞涩', '霸王之资', '蠢若木鸡', '蠢头蠢脑',
            '露头露脸', '巍然不动', '巍然耸立', '巍然挺立', '攀高枝儿', '蹦蹦跳跳', '翻风滚雨', '翻来复去', '翻脸无情', '翻然改悔',
            '翻手为云', '邋邋遢遢', '懵里懵懂', '懵里懵懂', '嚣浮轻巧', '鹰派人物',
            '胸有成竹', '竹报平安', '安富尊荣', '荣华富贵', '贵而贱目', '目无余子', '子虚乌有', '有目共睹', '睹物思人', '人中骐骥',
            '骥子龙文', '文质彬彬', '彬彬有礼', '礼贤下士', '士饱马腾', '腾云驾雾',
            '雾里看花', '花言巧语', '语重心长', '长此以往', '往返徒劳', '劳而无功', '功成不居', '居官守法', '法外施仁', '仁浆义粟',
            '粟红贯朽', '朽木死灰', '灰飞烟灭', '灭绝人性', '性命交关', '关门大吉', '吉祥止止', '止于至善', '善贾而沽', '沽名钓誉', '誉不绝口', '口蜜腹剑', '剑戟森森', '森罗万象',
            '象箸玉杯', '杯弓蛇影', '影影绰绰', '绰约多姿', '姿意妄为', '为人作嫁', '嫁祸于人', '人情冷暖', '暖衣饱食', '食不果腹',
            '腹背之毛', '毛手毛脚', '脚踏实地', '地老天荒', '荒诞不经', '经纬万端', '端倪可察', '察言观色', '色若死灰', '灰头土面', '面有菜色', '色授魂与', '面面俱到', '与民更始',
            '始乱终弃', '弃瑕录用', '用舍行藏', '藏垢纳污', '污泥浊水', '水乳交融', '融会贯通', '通宵达旦', '旦种暮成', '成人之美',
            '美人迟暮', '暮云春树', '树大招风', '怜香惜玉',
            '风中之烛', '烛照数计', '计日程功', '功德无量', '量才录用', '用行舍藏', '藏头露尾', '尾大不掉', '掉以轻心', '心急如焚',
            '焚琴煮鹤', '鹤发童颜', '颜面扫地', '地上天官', '官逼民反', '反裘负刍', '刍荛之见', '见微知著', '著作等身',
            '身强力壮', '壮志凌云', '云消雨散', '散兵游勇', '勇猛精进', '进退失据', '据理力争', '争长论短', '短小精悍', '悍然不顾',
            '顾影自怜', '怜香惜玉', '玉液琼浆',
            '浆酒霍肉', '肉薄骨并', '并行不悖', '悖入悖出', '出奇制胜', '胜任愉快', '快马加鞭', '鞭辟入里', '里出外进', '进寸退尺',
            '尺寸可取', '取巧图便', '便宜行事',
            '事与愿违', '违心之论', '论功行赏', '赏心悦目', '目光如豆', '华而不实', '豆蔻年华', '是古非今', '今愁古恨', '恨之入骨',
            '骨腾肉飞', '飞沿走壁', '壁垒森严', '待理不理',
            '理屈词穷', '委曲求全', '全力以赴', '穷原竟委', '赴汤蹈火', '火烧眉毛', '燎原烈火', '毛羽零落', '落井下石', '石破天惊',
            '惊惶失措', '惊惶失措', '如运诸掌', '掌上明珠', '珠沉玉碎', '碎琼乱玉',
            '玉碎珠沉', '沉滓泛起', '起早贪黑', '黑更半夜', '夜雨对床', '床头金尽', '尽态极妍', '妍姿艳质', '质疑问难', '难以为继',
            '继往开来', '来龙去脉', '脉脉含情', '情见势屈', '屈打成招', '招摇过市', '招摇过市', '徒劳往返', '返老还童', '童牛角马',
            '马首是瞻', '瞻前顾后', '后顾之忧', '忧国奉公',
            '公子王孙', '孙康映雪', '雪上加霜', '霜露之病', '病病歪歪', '歪打正着', '着手成春', '春蚓秋蛇', '蛇口蜂针', '针锋相对',
            '对薄公堂', '堂堂正正', '正中下怀', '怀璧其罪', '罪大恶极', '极天际地','地丑德齐', '齐心协力', '力不胜任', '任重道远',
            '远见卓识', '识文断字', '字斟句酌', '酌盈剂虚',
            '虚舟飘瓦', '瓦釜雷鸣', '鸣锣开道', '道不拾遗', '遗大投艰', '艰苦朴素', '素丝羔羊', '羊肠小道', '说长道短', '短兵相接',
            '接踵而至', '至死不变', '变本加厉', '厉行节约', '约定俗成', '成仁取义', '义形于色', '色色俱全', '全军覆灭', '灭此朝食',
            '食日万钱', '钱可通神', '神施鬼设', '设身处地', '跃跃欲试',
            '地平天成', '成年累月', '月白风清', '清净无为', '为期不远', '远交近攻', '攻其无备', '备多力分', '分寸之末', '末学肤受',
            '受宠若惊', '惊涛骇浪', '浪子回头', '头疼脑热', '热火朝天', '天高地厚', '厚貌深情', '情同骨肉', '肉眼惠眉', '眉来眼去', '去伪存真', '真脏实犯', '犯上作乱', '乱头粗服',
            '服低做小', '小试锋芒', '芒刺在背', '背井离乡', '乡壁虚造', '造化小儿', '儿女情长', '长歌当哭', '哭天抹泪', '泪干肠断',
            '断鹤续凫', '凫趋雀跃', '跃然纸上', '上树拔梯', '梯山航海', '海枯石烂', '烂若披锦', '锦绣前程', '程门立雪', '雪虐风饕', '饕餮之徒', '徒劳无功', '功败垂成', '成千上万',
            '万象森罗', '罗雀掘鼠', '鼠窃狗盗', '盗憎主人', '人莫予毒', '毒手尊前', '前因后果', '果于自信', '信赏必罚', '罚不当罪',
            '罪恶昭彰', '彰善瘅恶', '恶贯满盈', '盈科后进', '进退两难', '难分难解', '解甲归田', '田月桑时', '时和年丰', '丰取刻与', '与世偃仰', '仰人鼻息', '息息相通', '通权达变',
            '变化无穷', '穷途末路', '路不拾遗', '遗臭万年', '年深日久', '久悬不决', '决一死战', '战天斗地',
            '地利人和', '和而不唱', '唱筹量沙', '沙里淘金', '金屋藏娇', '娇生惯养', '养精畜锐', '锐不可当',
            '当头棒喝', '喝西北风', '风雨同舟', '舟中敌国', '国色天香', '香火因缘', '缘木求鱼', '鱼龙混杂',
            '杂七杂八', '八拜之交', '交头接耳', '耳鬓斯磨', '磨砖成镜', '镜花水月', '月旦春秋', '秋高气爽',
            '爽然若失', '失惊打怪', '怪诞不经', '经久不息', '息事宁人', '人言啧啧', '啧有烦言', '言必有中',
            '中庸之道', '道路以目', '目瞪口呆', '呆头呆脑', '脑满肠肥', '肥马轻裘', '裘弊金尽', '尽力而为',
            '为富不仁', '仁至义尽', '尽心竭力', '力透纸背', '背道而驰', '驰名中外', '外合里差', '差强人意',
            '意在言外', '外圆内方', '方底圆盖', '盖世无双', '双管齐下', '下车伊始', '始终如一', '一蹶不振',
            '振臂一呼', '呼风唤雨', '雨沐风餐', '餐风露宿', '宿弊一清', '折槁振落', '落落大方', '方寸已乱',
            '乱琼碎玉', '玉洁冰清', '清风明月', '月盈则食', '食言而肥', '肥遁鸣高', '高朋满座', '座无虚席',
            '席卷天下', '下不为例', '例直禁简', '简明扼要', '要价还价', '价值连城', '城狐社鼠', '鼠腹鸡肠',
            '肠肥脑满', '满腔热枕', '枕石漱流', '流离转徙', '徙宅忘妻', '妻儿老小', '小本经营', '营私舞弊',
            '弊绝风清', '清尘浊水', '水磨工夫', '夫唱妇随', '随才器使', '随才器使', '使贪使愚', '愚昧无知',
            '知书达礼', '礼尚往来', '来者不拒', '来者不拒', '拒谏饰非', '非异人任', '任人唯亲', '亲密无间',
            '间不容发', '发指眦裂', '裂土分茅', '茅塞顿开', '开路先锋', '锋芒所向', '向隅而泣', '泣下如雨',
            '雨丝风片', '片言折狱', '宝山空回', '回光返照', '照本宣科', '科班出身', '身价百倍', '倍日并行',
            '行动坐卧', '卧薪尝胆', '胆破心寒', '寒木春华', '华不再扬', '扬长而去', '去粗取精', '精诚团结',
            '结党营私', '私心杂念', '念兹在兹', '兹事体大', '大势所趋', '趋炎附势', '势不两立', '立此存照',
            '照猫画虎', '虎背熊腰', '腰缠万贯', '贯朽粟陈', '陈词滥调', '调嘴学舌', '舌剑唇枪', '枪林弹雨',
            '雨过天青', '青出于蓝', '蓝田生玉', '玉卮无当', '当场出彩', '彩凤随鸦', '鸦雀无闻', '闻风而起',
            '起死回生', '生拉硬扯', '扯篷拉纤', '纤芥之疾', '纤芥之疾', '雷打不动', '动辄得咎', '咎由自取',
            '取辖投井', '井井有条''条三窝四', '四衢八街', '街头巷尾', '尾生之信', '信口开河', '河山带砺',
            '砺山带河', '河清难俟', '俟河之清', '清汤寡水', '水滴石穿', '水滴石穿', '石沉大海', '海立云垂',
            '垂涎欲滴', '滴水成冰', '冰清玉洁', '洁身自好', '好肉剜疮', '疮痍满目', '目不识丁', '丁公凿井',
            '井中视星', '星旗电戟', '戟指怒目', '目指气使', '使羊将狼', '狼心狗肺', '肺石风清', '清夜扪心', '心织笔耕',
            '耕当问奴', '奴颜婢膝', '膝痒搔背', '背信弃义', '义无反顾', '顾全大局', '局促不安',
            '安步当车', '车载斗量', '量才而为', '为渊驱鱼', '鱼游釜中', '中馈犹虚', '虚有其表', '表里如一', '一呼百诺',
            '诺诺连声', '声罪致讨', '讨价还价', '价增一顾', '顾盼自雄', '雄心壮志', '志美行厉',
            '厉兵秣马', '厉兵秣马', '速战速决', '决一雌雄', '雄才大略', '略见一斑', '斑驳陆离', '离弦走板', '板上钉钉',
            '钉嘴铁舌', '舌桥不下', '下马看花', '花样翻新', '新陈代谢', '谢天谢地', '地久天长',
            '长枕大被', '被山带河', '油腔滑调', '调兵遣将', '将伯之助', '助人为乐', '乐而不淫', '淫词艳曲', '曲终奏雅',
            '雅俗共赏', '赏罚分明', '明刑不戮', '戮力同心', '心心相印', '印累绶若', '若有所失',
            '失张失智', '智圆行方', '方枘圆凿', '凿凿有据', '据为己有', '有眼无珠', '珠光宝气', '气味相投', '投鼠忌器',
            '器宇轩昂', '昂首阔步', '步履维艰', '艰苦卓绝', '绝少分甘', '甘雨随车', '车水马龙',
            '龙飞凤舞', '舞衫歌扇', '扇枕温被', '被发缨冠', '冠冕堂皇', '皇天后土', '土阶茅屋', '屋乌之爱', '爱莫能助',
            '助我张目', '目挑心招', '发凡起例', '事必躬亲', '亲如骨肉', '肉跳心惊', '惊弓之鸟',
            '鸟枪换炮', '龙蛇飞动', '动人心弦', '弦外之音', '音容笑貌', '貌合心离', '离心离德', '德高望重', '重蹈覆辙',
            '辙乱旗靡', '靡靡之音', '音容宛在', '在所难免', '免开尊口', '口耳之学', '学而不厌',
            '厌难折冲', '冲口而出', '出谷迁乔', '乔龙画虎', '虎踞龙盘', '盘马弯弓', '弓折刀尽', '尽善尽美', '美意延年',
            '年高望重', '重温旧梦', '梦寐以求', '求全之毁', '毁家纾难', '难言之隐', '隐恶扬善',
            '善始善终', '终南捷径', '径情直行', '行成于思', '思潮起伏', '伏低做小', '小恩小惠', '惠而不费', '费尽心机',
            '机关算尽', '尽忠报国', '国士无双', '双宿双飞', '飞灾横祸', '祸从天降', '降格以求',
            '求同存异', '异名同实', '实至名归', '归真反璞', '璞玉浑金', '金玉锦绣', '绣花枕头', '头没杯案', '案牍劳形',
            '舌锋如火', '火伞高张', '张冠李戴', '戴月披星', '星移斗转', '转祸为福', '福至心灵',
            '灵丹圣药', '药笼中物', '物以类聚', '聚蚊成雷', '雷厉风行', '行将就木', '木本水源', '源源不断', '断烂朝报',
            '报冰公事', '事预则立', '立身处世', '世外桃源', '源源不绝', '绝甘分少', '少不经事',
            '事不师古', '兵连祸结', '结结巴巴', '巴三览四', '四面楚歌', '歌功颂德', '德厚流光', '光阴似箭', '箭在弦上',
            '上好下甚', '甚嚣尘上', '上下交困', '困知勉行', '行若无事', '事倍功半', '半夜三更',
            '更仆难数', '数见不鲜', '鲜车怒马', '马革裹尸', '尸居余气', '气冲牛斗', '斗筲之器', '盈盈一水', '水陆杂陈',
            '陈规陋习', '习焉不察', '察察为明', '明知故问', '问道于盲', '盲人摸象', '象齿焚身',
            '身不由主', '主客颠倒', '倒凤颠鸾', '鸾翔凤集', '集苑集枯', '枯木逢春', '春山如笑', '笑里藏刀', '刀山火海',
            '海外奇谈', '谈笑封侯', '侯门如海', '海阔天空', '空室清野', '野草闲花', '花颜月貌',
            '貌合神离', '离乡背井', '井蛙之见', '见仁见智', '智勇双全', '全受全归', '归马放牛', '牛骥同皂', '皂白不分',
            '分香卖履', '履舄交错', '错彩镂金', '金城汤池', '池鱼之殃', '殃及池鱼', '鱼烂而亡', '亡羊补牢', '牢不可破',
            '破颜微笑',
            '笑逐颜开', '开宗明义', '义薄云天', '天南地北', '北辕适楚', '楚囚对泣', '泣不成声', '声嘶力竭', '竭泽而渔',
            '渔人之利', '利令智昏', '昏天黑地', '地大物博', '博闻强识', '识途老马', '马到成功', '功德圆满', '满腹狐疑', '疑神疑鬼',
            '鬼使神差', '差三错四', '四时八节', '节衣缩食', '食而不化', '化整为零', '零打碎敲', '敲冰求火', '火树银花',
            '花好月圆', '圆颅方趾', '趾高气扬', '扬汤止沸', '沸沸扬扬', '扬幡招魂', '魂不附体', '体无完肤', '肤皮潦草', '草长莺飞',
            '飞鹰走狗', '狗吠非主', '主情造意', '意马心猿', '猿猴取月', '月露风云', '云蒸霞蔚', '蔚为大观', '观眉说眼',
            '眼馋肚饱', '饱食暖衣', '衣架饭囊', '囊空如洗', '洗耳恭听', '听而不闻', '闻鸡起舞', '舞文弄墨', '墨子泣丝', '丝恩发怨',
            '怨气冲天', '天罗地网', '网开三面', '面目全非', '非同小可', '可心如意', '意气扬扬', '扬眉吐气', '气涌如山',
            '山南海北', '北叟失马', '马仰人翻', '翻然改图', '图穷匕见', '见多识广', '广开言路', '路柳墙花', '花遮柳隐', '隐姓埋名',
            '名垂后世', '世风日下', '下车泣罪', '罪孽深重', '重于泰山', '山盟海誓', '誓死不二', '二心两意', '意气相投',
            '投机取巧', '巧取豪夺', '夺其谈经', '经年累月', '月下花前', '前思后想', '想入非非', '非亲非故', '故弄玄虚', '虚位以待',
            '待人接物', '物尽其用', '用兵如神', '神差鬼使', '使臂使指', '指不胜屈', '屈指可数', '数一数二', '二姓之好',
            '好高骛远', '远走高飞', '飞蛾投火', '火上弄冰', '冰天雪地', '地狱变相', '相机而动', '动如脱兔', '兔丝燕麦', '麦穗两歧',
            '歧路亡羊', '羊质虎皮', '皮里阳秋', '秋荼密网', '网开一面', '面红耳赤', '赤子之心', '心高气傲', '傲然屹立',
            '立功赎罪', '罪魁祸首', '首善之区', '区闻陬见', '见兔顾犬', '犬马之劳', '劳燕分飞', '火海刀山', '币重言甘', '甘棠遗爱',
            '山高水低', '低声下气', '气象万千', '千疮百孔', '孔席墨突', '突然袭击', '击节叹赏', '赏一劝百', '百年不遇',
            '遇事生风', '风雨交加', '加人一等', '等因奉此', '此起彼伏', '伏地圣人', '人欢马叫', '叫苦连天', '天高听卑', '卑礼厚币',
            '爱屋及乌', '乌焉成马', '马鹿异形', '形影相吊', '吊死问疾', '疾足先得', '得陇望蜀', '蜀犬吠日', '日升月恒',
            '恒河沙数', '数黑论黄', '黄雀伺蝉', '蝉不知雪', '雪窑冰天', '天真烂漫', '漫不经心', '心心念念', '念念不忘',
            '忘乎所以',
            '以指挠沸', '沸反盈天', '天上石麟', '麟趾呈祥', '祥麟威凤', '凤凰来仪', '仪静体闲', '闲云野鹤', '鹤发鸡皮',
            '皮里春秋', '秋风过耳', '耳食之谈', '谈笑自若', '谈笑自若', '若明若暗', '暗气暗恼', '恼羞成怒', '怒目而视', '视民如伤',
            '伤弓之鸟', '鸟语花香', '香花供养', '养痈成患', '患难与共', '共枝别干', '干卿底事', '事出有因', '因敌取资',
            '资深望重', '重睹天日', '日上三竿', '竿头直上', '上援下推', '推襟送抱', '抱蔓摘瓜', '绝处逢生', '多才多艺', '深恶痛绝',
            '腾蛟起凤', '历历可数', '数白论黄', '黄袍加身', '身外之物', '物换星移', '移樽就教', '教学相长', '长年累月',
            '月晕而风', '风流倜傥', '傥来之物', '物是人非', '非池中物', '物极必返', '反经行权', '权宜之计', '计出万全', '全无心肝', '肝肠寸断',
            '恕己及人', '一鞭先着', '井蛙之见', '夜宿晓行', '驰高骛远', '子承父业', '气谊相投', '划地为牢', '鹰派人物', '至高无上', '日中则移', '指挥若定',
            '一泻千里', '名闻遐迩', '暗约私期', '狗吠之警', '恨入心髓', '蝼蚁之诚', '覆公折足', '长春不老', '破觚为圆', '立吃地陷', '万赖俱寂', '指名道姓',
            '白鱼登舟', '官高爵显', '枯株朽木', '谦逊下士', '由来已久', '累教不改', '调脂弄粉', '修鳞养爪', '鹰拿燕雀', '悬圃蓬莱', '燕石妄珍', '指日可待',
            '暴虐无道', '暴虐无道', '舞词弄札', '萧敷艾荣', '奋不顾生', '如臂使指', '指不胜屈', '腹中兵甲', '指日可下', '腹背受敌', '腹热心煎', '腹热肠慌',
            '粉白黛黑', '黑白分明', '化为乌有', '有备无患', '患难之交', '交淡若水', '水过鸭背', '背城借一', '一塌糊涂', '涂脂抹粉', '明目张胆', '胆战心惊',
            '惊心悼胆', '胆大心小', '小廉曲谨', '谨毛失貌', '貌似强大', '大璞不完', '完事大吉', '吉光片羽', '羽毛未丰', '丰衣足食', '食肉寝皮', '皮相之见',
            '见笑大方', '方便之门', '门当户对', '对酒当歌', '歌舞升平', '平白无故', '从心所欲', '欲擒故纵', '大有人在', '在家出家', '吠形吠声', '接三连四',
            '故入人罪', '罪该万死', '死灰复燃', '燃眉之急', '急不暇择', '择善而从', '视同路人', '倒持泰阿', '头童齿豁', '惜墨如金', '感激涕零', '众擎易举'
        ]

    def launchRequest(self):

        """
        欢迎
        :return:
        """
        self.waitAnswer()
        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
        bodyTemplate.setPlainTextContent(r'欢迎来到蒲公英，在这里，您可以跟我一起学习英语，也可以跟我互斗成语！试着对我说，我怎么跟你玩')

        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'欢迎来到蒲公英，在这里，您可以跟我一起学习英语，也可以跟我互斗成语！试着对我说，我怎么跟你玩'
        }

    def welcome(self):

        """
        介绍
        :return:
        """


    def start_IdiomC(self):

        """
        成语接龙
        :return:
        """
        self.waitAnswer()
        rand_id = random.randint(0, 1000)
        idiom = self.idiom
        give_idiom = idiom[rand_id]

        self.setSessionAttribute("answer", give_idiom[-1], 0)
        self.setSessionAttribute("give_idiom", give_idiom, 0)
        self.setSessionAttribute("game_type", 'IdiomC', 0)
        self.setSessionAttribute("round_num", 1, 1)

        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
        bodyTemplate.setPlainTextContent(r'我先来，我出：' + give_idiom)

        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'我先来，我出' + give_idiom
        }

    def start_IdiomGuess(self):

        """
        猜成语
        :return:
        """
        self.waitAnswer()
        mode = self.getSlots('guess_mode')
        self.setSessionAttribute("game_type", 'IdiomGuess', 0)
        if mode == 'blank':

            rand_id = random.randint(0, 1000)
            rand_ids = random.randint(0, 3)
            answer = self.idiom[rand_id]
            give_idiom = answer.replace(answer[rand_ids] + answer[rand_ids + 1], '*')
            self.setSessionAttribute("real_answer", answer, 0)
            self.setSessionAttribute("give_idiom", give_idiom, '')
            self.setSessionAttribute("guan_num", 1, 1)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage('**************!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            bodyTemplate.setPlainTextContent(r'诶呀！我吃掉了成语的一部分，快来帮我还原吧!   ' + give_idiom)

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'诶呀！我吃掉了成语的一部分，快来帮我还原吧!   ' + give_idiom
            }
        elif mode == 'scene':

            self.setSessionAttribute("idiom_story_name", user_story, 0)
            self.setSessionAttribute("game_type", 'IdiomStory', 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage(self.idiom_story[user_story][1])
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' + user_story + '，，，' + idiom_story + '还想再听一遍吗，试着对我说：再来一遍')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story + '，，，' + idiom_story + '还想再听一遍吗，试着对我说，再来一遍'
            }
        elif mode == 'means':

            self.setSessionAttribute("idiom_story_name", user_story, 0)
            self.setSessionAttribute("game_type", 'IdiomStory', 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage(self.idiom_story[user_story][1])
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' + user_story + '，，，' + idiom_story + '还想再听一遍吗，试着对我说：再来一遍')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story + '，，，' + idiom_story + '还想再听一遍吗，试着对我说，再来一遍'
            }

    def tell_idiom_story(self):

        """
        成语故事
        :return:
        """
        self.waitAnswer()
        self.setSessionAttribute("game_type", 'IdiomStory', 0)
        user_story = self.getSlots('idiom_story')
        if not user_story:
            self.nlu.ask('idiom_story')
        elif user_story == 'random':

            rand_id = random.randint(0, 30)
            idiom_story = self.idiom_story[rand_id][0]

            self.setSessionAttribute("idiom_story_name", user_story, 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage(self.idiom_story[rand_id][1])
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' +  + '：' + idiom_story + '还想再听一遍吗，试着对我说：再来一遍')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story + '，，，，' + idiom_story + '还想再听一遍吗，试着对我说，再来一遍'
            }
        else:
            idiom_story = self.idiom_story[user_story][0]

            self.setSessionAttribute("idiom_story_name", user_story, 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage(self.idiom_story[user_story][1])
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' + user_story +  '：' + idiom_story + '还想再听一遍吗，试着对我说：再来一遍')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story +  '，，，，' + idiom_story + '还想再听一遍吗，试着对我说，再来一遍'
            }


    def answer_helper(self):

        """
        提示
        :return:
        """
        self.waitAnswer()
        answer = self.getSessionAttribute("answer", 0)
        give_idiom = self.getSessionAttribute("give_idiom", 0)
        a = 0
        helper_idiom = ''
        idiom = self.idiom
        while 1 == 1:
            try:
                test = idiom[a]
            except IndexError:
                break
            else:
                if idiom[a][0] == answer:
                    helper_idiom = idiom[a][0] + idiom[a][1]
                    if helper_idiom == give_idiom:
                        a = a + 1
                    else:
                        break
                else:
                    a = a + 1

        if helper_idiom == '' or helper_idiom == None:

            return {
                'outputSpeech': r'诶呀，提示不见了，努力想想吧'
            }

        else:

            card = TextCard(r'给你前两个字，想想：' + helper_idiom + '**' + '，如果实在想不到，可以对我说“跳过”')
            return {
                'card': card,
                'outputSpeech': r'给你前两个字，想想,' + helper_idiom + '如果实在想不到，可以对我说，跳过，'
            }

    def round(self):

        """
        读取轮回
        :return:
        """
        self.waitAnswer()
        return {
            'outputSpeech': r'您现在已经跟我大战第' + self.getSessionAttribute("idiom_num", 1) + '回合了'
        }

    def c_game(self):

        """
        继续游戏
        :return:
        """
        self.waitAnswer()
        give_idiom = self.getSessionAttribute("give_idiom", '')
        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage(
            'http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
        bodyTemplate.setPlainTextContent(r'好的，我们继续，我刚刚出了：' + give_idiom)

        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'好的，我们继续，我刚刚出了' + give_idiom
        }

    def answer(self):

        """
        回答
        :return:
        """
        self.waitAnswer()
        result = self.getSlots('idiom')
        try:
            user_answer = json.loads(result)
            user_answer = user_answer.get("origin")
        except:
            user_answer = result
        if not user_answer:
            self.nlu.ask('idiom')
        else:
            pass
        real_answer = self.getSessionAttribute("give_idiom", 0)
        answer = self.getSessionAttribute("answer", 0)
        a = 0

        if user_answer[0] != real_answer[3]:
            return {
                'outputSpeech': r'接错了哦，我的是，' + real_answer + '，哦！需要提示可以对我说，我需要提示，'
            }
        else:
            idiom = self.idiom
            while 1 == 1:
                    try:
                        test = idiom[a]
                    except IndexError:
                        break
                    else:
                        if idiom[a][0] == user_answer[-1]:
                            new_give_idiom = idiom[a]
                            if new_give_idiom == real_answer:
                                a = a + 1
                            else:
                                break
                        else:
                            a = a + 1
            if new_give_idiom == None or new_give_idiom == '':
                return {
                    'outputSpeech': '诶呀，你这下真的打败我了，我输了，对我说，你重新开始，试试'
                }
            else:
                self.setSessionAttribute("answer", new_give_idiom[-1], '')
                self.setSessionAttribute("give_idiom", new_give_idiom, '')
                self.setSessionAttribute("round_num", self.getSessionAttribute("round_num", 1) + 1, 1)

                bodyTemplate = BodyTemplate1()
                bodyTemplate.setBackGroundImage(
                    'http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
                bodyTemplate.setPlainTextContent(r'你真棒，被你接到了，那我接：' + new_give_idiom)

                directive = RenderTemplate(bodyTemplate)
                return {
                    'directives': [directive],
                    'outputSpeech': r'你真棒，被你接到了，那我接，' + new_give_idiom
                }

    def quesheng(self):
        
            """
            缺省
            :return:
            """
            self.waitAnswer()
            try:
                text = self.data['request']['query']['original']
            except:
                return {
                    'outputSpeech': r'我没有理解您的意思'
                }
            else:
                if len(text) == 4:
                    return {
                        'outputSpeech': r'很抱歉，您回答的成语我没能理解哦'
                    }
                elif '下一关' in text or '不会' in text:

                    rand_id = random.randint(0, 499)
                    give_idiom = self.idiom[rand_id]

                    self.setSessionAttribute("answer", give_idiom[-1], 0)
                    self.setSessionAttribute("give_idiom", give_idiom, 0)
                    self.setSessionAttribute("round_num", self.getSessionAttribute("round_num", '') + 1, 1)

                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        'http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
                    bodyTemplate.setPlainTextContent(r'好吧，要加油哦，那接下来我出：' + give_idiom)

                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': r'好吧，要加油哦，那接下来我出' + give_idiom
                    }
                else:
                    return {
                        'outputSpeech': r'您说的我没有理解，对不起'
                    }
