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
        # main intent
        self.addLaunchHandler(self.launchRequest)
        self.addIntentHandler('welcome', self.welcome)
        self.addIntentHandler('next_one', self.next_one)
        self.addIntentHandler('answer', self.answer)
        self.addIntentHandler('answer_helper', self.answer_helper)
        self.addIntentHandler('c_game', self.c_game)
        self.addIntentHandler('round', self.round)
        self.addIntentHandler('ai.dueros.common.default_intent', self.quesheng)
        # idiom intent
        self.addIntentHandler('start_IdiomC', self.start_IdiomC)
        self.addIntentHandler('tell_idiom_story', self.tell_idiom_story)
        self.addIntentHandler('start_IdiomGuess', self.start_IdiomGuess)
        # english intent
        self.addIntentHandler('study_english_word', self.study_english_word)
        self.addIntentHandler('tell_english_joke', self.tell_joke)
        self.addIntentHandler('tell_english_story', self.tell_english_story)
        self.addIntentHandler('english_songs', self.english_songs)
        # english data
        self.english_song = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', '']
        ]
        self.english_joke = [
            ['Teacher: whoever answers my next question, can go home.老师：谁能回到我下一个问题，谁就可以回家了。One boy throws his bag out the window.一个小男孩把书包扔到窗外。Teacher: who just threw that?!老师：谁刚刚把书包扔出去了?Boy: Me! I’m going home now.男孩：我!我现在要回家了。', ''],
            ['What dog can jump higher than a building?什么狗比大楼跳的还高?Anydog, buildings cannot jump!任何一只狗，大楼又跳不起来。', ''],
            ["Sister's boyfriend: No, dont do that. Here is a nickel.Little brother: That makes a buck and a quarter I love made this mont弟弟：我看见你亲我姐姐了，如果你不给我五分钱，我就告诉我爸。姐姐的男朋友：不要那样做。给你五分钱。弟弟：我这个月已经赚了一块两毛五了。", ''],
            ["Dentist: I'm sorry, madam, but I'll have to charge you twenty-five dollars for pulling your son's tooth.Mother: Twenty-five dollars! But I thought you only charged five dollars for an extraction.Dentist: I usually do. But your son yelled so loud, he scared four other patients out of the office.牙科医生：对不起，夫人，为给您的儿子拔牙，我得收二十五美元。母亲：二十五美元!可是我知道您拔一颗牙只要五美元呀?牙科医生：是的。但是您儿子这么大声地叫唤，他都吓跑四位病人了。", ""],
            ["Younger Scout: How can I tell the difference between a mushroom and a toadstool?Older Scout: Just eat one before you go to bed. If you wake up the next morning, it was a mushroom.年少的童子军：我怎样才能把蘑菇和毒蕈区别开呢?年长的童子军：上床前吃一个。如果你第二天早上醒来，那就是蘑菇。", ""],
            ["‘Do you believe in life after death?’the boss asked one of his employees. ‘Yes, Sir.’ the new recruit replied.‘Well, then, that makes everything just fine,’ the boss went on. 'After you left early yesterday to go to your grandmother's funeral, she stopped in to see you.“你相信人能死后重生吗?”老板问他的一个员工。 “我相信，先生”。这位刚上班不久的员工回答。 “哦，那还好”。老板接着说。 “你昨天提早下班去参加你祖母的葬礼后，她老人家到这儿看你来了。”", ""],
            ["The fine-furniture store where I work has been in business since the 1920s. Recently I received a call from a woman who wanted to replace some chairs from a dining set purchased from us in the 1930s. I assured her we could help and sought the assistance of the office manager. “You'll never believe this one, ”I told him.“ I just got a call from a customer who bought some chairs from us in the 1930s. ”Before I could finish repeating her request, he interrupted and said, “Don't tell me she hasn't received them yet!”我所工作的精品家具商店是从20世纪二十年代以来就营业的。最近我接到一个妇女的电话。她想换一套餐具中的一些椅子。这套餐具她是在三十年代从我们这儿买的。我向她保证说我们可以帮她的忙，于是我向部门经理寻求帮助。“你永远也不会相信，”我对他说，“我刚接到一个顾客的电话，她在三十年代从我们这里买了一些椅子。” 我还没来得及说她的要求，经理就打断了我的话：“你别告诉我她到现在还没收到货!”", ""],
            ["A husband and wife,both 91,stood before a judge,asking for a divorce.“I don't understand,”He said,“Why do you want a divorce at this time of life?”the husband explained “Well , you see,We wanted to wait until the children died.”有一个丈夫和妻子都是91岁，他们站在法官面前，要求离婚。“我不明白，”法官说，“你们为什么到了这把年纪还要离婚?”丈夫解释道：“嗯，你是知道的，我们以前是哟等到孩子们都死了。”", ""],
            ["Teacher: What is the plural of man,Tom?Tom: Men.Teacher: Good. And the plural of child?Tom : Twins.老师: 汤姆，“男人”这个词的复数形式是什么?汤姆:男人们。老师: 答得好。那“孩子”的复数形式呢?汤姆: 双胞胎", ""],
            ["Mike was late for school. He said to his teacher, Mr. Black, “Excuse me for my coming late, sir. I watched a football match in my dream.”“Why did it make you late?”inquired the teacher.　“Because neither team could win the game, so it lasted a long time.” replied Mike.麦克上学迟到了。他对布莱克老师说：“对不起，老师，今天早上我迟到了。因为我在梦里观看了一场球赛。”“为什么它会让你迟到呢?”老师问道。因为这两个队都没有能力获胜，所以就持续的时间长了。”麦克回答说。", ""],
            ["After burying his mother nine months earlier, a client of the local mortuary finally had enough money to purchase the expensive coffin he'd originally wanted. So we exhumed the body and transferred his deceased mother into the new steel casket. “What's so special about this coffin?” I asked the funeral director. He replied, “It has a lifetime warranty.”在将母亲下葬9个月后，当地殡仪馆的一个客户终于攒够了钱去买那副他早就相中的价值不菲的棺材了。他把母亲的棺材挖了出来，将尸体转移到了那副新的钢制棺材中。“这副棺材有什么特别?”，我问葬礼的承办人。他回答说，“这种棺材终生保修", ""],
            ["“Oh, my poor man,”exclaimed the kind old lady， “It must be dreadful to be lame. But it would be much worse if you were blind.”“You're absolutely right,”said the beggar, obviously an old hand at the game.“When I was blind, people kept giving me foreign coins.”“啊，可怜的人。”善良的老妇人惊叹道。“脚瘸就够惨的了，要是眼瞎就更糟了。”“你说的一点儿没错。”那乞丐说。他显然是乞讨老手。“我眼瞎的时候，人们老是给我外币。”", ""],
            ["A newspaper organized a contest for the best answer to the question: “If a fire broke out in the Louvre, and if you could only save one painting, which one would you carry out?”The winning reply was: “The one nearest the exit.”一份报纸组织了一场竞赛，为下面的问题征集最佳答案：“如果卢浮宫起了火，而你只能救出一幅画，你将救出哪一幅?”获奖的答案是：“最接近门口的那一幅。”", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],

        ]
        self.english_story = [
            ['国王有两个孩子：法瑞克斯和赫勒，这两个孩子看不到后母残忍对待，当可怜的孩子要被斩首时，他们被上帝派来的公羊给救了，接下来这两个孩子的命运是怎样的呢？下面来看看今天的双语故事短文：金色的羊毛。King Athamus of northern Greece had two children， Phrixus and Helle．After he left his first wife and mar ried Ino，a wicked woman，the two children received all the cruel treatment that a stepmother coulddevise ，At one timethe kingdom was ruined by a famine．', ''],
            ['King Athamus of northern Greece had two children， Phrixus and Helle．After he left his first wife and mar ried Ino，a wicked woman，the two children received all the cruel treatment that a stepmother coulddevise ，At one timethe kingdom was ruined by a famine．希腊北部国王阿塔玛斯有两个孩子，法瑞克斯和赫勒。当国王离开第一个妻子和一个名叫伊诺的坏女人结婚后，两个孩子受到后母残忍虐待，整个王国也受到毁灭性瘟疫的侵袭。', ''],
            ['Ino persuaded her credulous husband intobelievingthat his son，Phrixus，was the actual cause of the disaster，and should be sacrificed to Zeus to endit．The poor boy was then placed on the altar and was about tobe knifed when a ram with goldenfleecewas sent down by thegods and carried off the two children on its back．伊诺在爱轻信的丈夫耳边进谗言，终于使国王相信：他的儿子法瑞克斯是这次灾害的罪魁祸首，并要将他献给宙斯以结束瘟疫。可怜的孩子被推上了祭坛，将要被处死。正在此时，上帝派了一只浑身上下长着金色羊毛的公羊来将两个孩子驮在背上带走了。', ''],
            ['As they flew over the strait that divides Asia from Europe，Helle，faint at the vast expanse of waterbelow ，fell into the sea and was drowned．Thus the sea of Helle，Hellespont，became the ancient name of the strip of water．Her brother kept on and arrived in Colchis on the eastern shore of the Black Sea．There he sacrificed the ram to Zeus and gave its golden fleece to King Aeetes，who nailed it on a sacred tree and put a sleepless dragon incharge ．当他们飞过隔开欧洲和亚洲的海峡时，赫勒由于看到浩瀚的海洋而头晕目眩，最终掉进大海淹死了。这片海洋古时候的名称叫赫勒之海，赫勒拉旁海峡便由此而来。金色公羊驮着法瑞克斯继续向前飞去，来到了黑海东岸的科尔契斯。在那里，法瑞克斯将公羊献给了宙斯；而将金羊毛送给了埃厄忒斯国王。国王将羊毛钉在一棵圣树上，并派了一条不睡觉的龙负责看护。', ''],
            ['人的一生中会有不少的朋友，而今天我们的故事讲述的是在教堂结识的新朋友竟是我的邻居，故事内容究竟是怎样的呢？我们一起来读读：', ''],
            ['We described the friendly neighborhood we lived in，and listened sympathetically as they lamented that theirs was just the opposite.我们的话题开始谈到了邻居，我们说我们的邓居如何如何的好。当他们说到他们的邻居恰恰相反时，我们表示了对他们的同情。 ', ''],
            ['Saying our good-byes, we got in our cars and drove home.后来，我们向他们道了别，开车回到了家。', ''],
            ['The Frog and the Cow：Baby frogs went on a picnic in the woods. Getting out of the pond for the first time, they sang merrily.Then, they found a cow grazing in a field. "Oh, my! What is that?" "It is huge!" All of them wondered what kind of animal it was. "Let's ask Daddy."They returned home in a hurry and shouted, "Daddy, we saw a strange animal." "What kind of animal was it?""It had large horns on its head and its body was way bigger than you. Even if we all add up our power, we can not defeat that animal."The father was curious what the animal looked like. "Really? Was it bigger than my stomach?" "Yes. Much bigger than that!"The father frog blew up his stomach largely, "Well, now, I'm as big as the animal, right?" "No, you are as big as the animal's heel." The father puffed himself up deeply and blew up his stomach enormously."How about now? Am I as big as the animal, huh?" "No, not even." Thinking he could not be outdone, the father frog puffed up his stomach even more.The father frog's stomach was blown up as big as he could get. Right at that very moment, the father frog's stomach burst with a bang.中文：小青蛙们在树林里野餐。这是他们第一次从池塘里出来，他们正在愉快地唱歌。突然，他们发现了一头正在牧场上吃草的奶牛。“哦，天哪！那是什么？好大啊！”他们都很好奇那究竟是什么动物。“咱们问爸爸吧。”他们匆匆忙忙地回了家，大声喊道：“爸爸，我们看到了一只奇怪的动物。”“什么样的动物啊？”“头上有很大的触角，身体比你大得多。就算我们所有人都加起来，都很难打败它。”父亲对他的描述感到很好奇。“真的吗？它比我的肚子还大吗？”“是啊，可比你的肚子大得多！”父亲使劲鼓起了自己的肚子，“现在呢，现在我和那个动物一样大了，对吧？”“不，你现在也就只有那只动物的脚跟那么大。”父亲气急了，又使劲鼓了股他的肚子。“现在呢？现在我和那动物一样大了吧？”“不，还是小。”父亲认为自己不能认输，于是它又深呼吸了一下，肚子又大了一圈。就这样他不停地吹气，肚子已经达到极限了。就在这一瞬间，青蛙爸爸的肚子砰的一声爆炸了。', ''],
            ['说到电视机想必大家都见过，但收音机有人知道但不一定会用吧。现在的网络条件比之前好，以至于现在很多年轻人都忽视了收音机，下面来看看今天的双语故事短文：收音机和电视机。', ''],
            ['Radio and television are very popular in the world today. Millions of people watch TV. Perhaps more people listen to the radio.现在，收音机和电视机在世界上都很流行。数以百万计的人看电视。也许听收音机的人更多。', ''],
            ['The TV is more useful than the radio. 电视机比收音机更有用。', ''],
            ['On TV we can see and hear what is happening in the world.在电视上我们可以看到和听到世界上正在发生的事。', ''],
            ['But radio isn‘t lost. It is still with us. 可是收音机并没有消失，它还和我们在一起。', ''],
            ['That’s because a radio is very small， and it‘s easy to carry. You can put one in your pocket and listen to it on the bus or on your bike when you go to school.这是因为收音机很小，便于携带。你可以放在口袋里，在坐车或汽车上学时收听。', ''],
            ['今天的这篇英语故事比较简短，讲述的是：公鸡和母鸡一起出门旅行，在旅途中的事情及到海尔家后遇到的“趣”事，本故事非常适合小朋友们学习，一起来读读吧：', ''],
            ['There were once a cock and a hen who wanted to take a journey together. So the cock built a beautiful carriage, which had four red wheels, and harnessed four mice to it. The hen seated herself in it with the cock, and they drove away together.', ''],
            ['Not long afterwards they met a cat who said, "Where are you going?" The cock replied, "We are going to the house of Herr Korbes." "Take me with you," said the cat. The cock answered, "Most willingly, get up behind, lest you fall off in front. Take great care not to dirty my little red wheels. And you little wheels, roll on, and you little mice pipe out, as we go forth on our way to the house of ', ''],
            ['After this came a millstone, then an egg, then a duck, then a pin, and at last a needle, who all seated themselves in the carriage, and drove with them. When, however, they reached the house of Herr Korbes, Herr Korbes was not there.', ''],
            ['The mice drew the carriage into the barn, the hen flew with the cock upon a perch. The cat sat down by the hearth, the duck on the well-pole. The egg rolled itself into a towel, the pin stuck itself into the chair-cushion, the needle jumped on to the bed in the middle of the pillow, and the millstone laid itself over the door.', ''],
            ['Then Herr Korbes came home, went to the hearth, and was about to light the fire, when the cat threw a quantity of ashes in his face. He ran into the kitchen in a great hurry to wash it off, and the duck splashed some water in his face. He wanted to dry it with the towel, but the egg rolled up against him, broke, and glued up his eyes. He wanted to rest, and sat down in the chair, and then the pin pricked him. He fell in a passion, and threw himself on his bed, but as soon as he laid his head on the pillow, the needle pricked him, so that he screamed aloud, and was just going to run out into the wide world in his rage, but when he came to the house-door, the millstone leapt down and struck him dead. Herr Korbes must have been a very wicked man!', ''],
            ['今天的这篇英语故事比较简短，讲述的是：海里的动物有章鱼，鲨鱼、鲸鱼、扁蛟鱼、海星、龙虾等等，本故事的内容非常的简短特别适合小朋友们学习，一起来读读吧：', ''],
            ['There are all kinds of animals in the sea.', ''],
            ['Look! They are coming.', ''],
            ['This is an octopus. The octopus is spraying ink.', ''],
            ['This is a shark. The shark has sharp teeth.', ''],
            ['This is a whale. The whale shoots water into the air.', ''],
            ['a sea turtle. The sea turtle has a hard shell.', ''],
            ['These are starfishes. The starfishes have five legs.', ''],
            ['These are angelfishes. The angelfishes have beautiful colors.', ''],
            ['This is a lobster. The lobster has strong claws.', ''],
            ['This is a jellyfish. The jellyfish has a soft body.', ''],
            ['They are different. But all of them live in the sea.', ''],
            ['在海洋里有各种各样的动物。', ''],
            ['看！他们过来了。', ''],
            ['这时一条章鱼，章鱼在喷墨。', ''],
            ['这是一条鲨鱼，鲨鱼有锐利的牙齿。', ''],
            ['这是一只鲸鱼，鲸把水喷射到空中。', ''],
            ['这是一只海龟，海龟有坚硬的壳。', ''],
            ['这些是海星，海星有五条腿。', ''],
            ['这些是扁蛟鱼，扁姣鱼有美丽的花纹。', ''],
            ['这是一只龙虾，龙虾有强壮的爪子。', ''],
            ['这是一个水母，水母有一个柔软的身体。', ''],
            ['他们各不相同，但他们都居住在海洋里。', ''],
            ['每天读一篇小学生英语故事可以让儿童更早接触英语，并且英语故事比较有趣，会使孩子对英语产生兴趣，这样有利于他们以后的英语学习。今天的这篇英语故事比较简短，非常适合小朋友们学习，一起来读读吧：', ''],
            ['"I had another bad dream," she told her fiancé. "It was about you again. You and your ex-girlfriend were kissing. I yelled at you to stop it. You looked right at me, and then you laughed at me! She laughed, too. Then you both went back to kissing. I tried not to watch, but when I covered my eyes, something pulled my hands away. I tried to leave, but my feet were glued to the ground. Finally, I woke up. Of course, it was very difficult to get back to sleep.', ''],
            ['"I had to drive home from Las Vegas this morning. It's a wonder I didn't crash 50 times. Instead of seeing traffic in front of me, all I saw was you and her. I can't take any more dreams like this. We're going to have to break up. We can be friends, but just friends. That way, I won't be jealous anymore, and I won't have these bad dreams anymore."', ''],
            ['"Why didn't you call me up and tell me about your dream?" he asked. "They say that the more you talk about bad dreams, the sooner you'll stop having them."', ''],
            ['She disagreed. She thought that the only solution was to break up and be just friends. She loved him, but these dreams had become so frequent that she was actually afraid to go to sleep. She was losing weight and having stomachaches from the stress.', ''],
            ['He didn't know what to do. He wanted her to have pleasant dreams. He wanted her to have a life without', ''],
            ['. He wanted her to be his wife. This was it, she repeated; if she had just one more bad dream, they were through. He squeezed her hand, but said nothing.', ''],
            ['今天的这篇英语故事比较简短，讲述的是：老人有一只顽皮的猴子，一天一只苍蝇落在了睡着的老人鼻子上，于是一场猴子与苍蝇的战斗开始了，究竟是谁会胜利呢？本故事的内容非常的简短特别适合小朋友们学习，一起来找找答案吧：', ''],
            ['It’s very hot.. An old man is asleep on the chair.', ''],
            ['A fly comes and sits on the end of the man’s nose.', ''],
            ['The old man has a naughty monkey.', ''],
            ['He chases the fly. The fly comes back again and sits on the old man’s nose again.', ''],
            ['The monkey chases it away again and again. This happens five or six times. The monke', ''],
            ['He jumps up, runs to the garden and picks up a large stone.', ''],
            ['When the fly sits on the old man’s nose again, the monkey hits it hard with the stone. He kills the fly and breaks the old man’s nose.', ''],
            ['天气很热。一位老人在椅子上睡着了。', ''],
            ['一只苍蝇飞来落在老人的鼻子上。', ''],
            ['老人有一只顽皮的猴子。', ''],
            ['猴子在追打苍蝇。 苍蝇再次飞落在老人的鼻子上，猴子一再追打苍蝇。 这样往返了五六次，猴子很生气。他跳着跑到花园，捡起一块大石头。', ''],
            ['当苍蝇再次落在老人的鼻子上时，猴子用石头击中老人的鼻子上的苍蝇。 他砸死了苍蝇也打破', ''],
            ['There is a wolf. He is very hungry and has no strength to find food. As he lies under a large tree, a dog sees him. The dog sees the wolf is so thin and hungry, and he feels sorry for him and says, “You are so terrible! Are you hungry?”', ''],
            ['“Yes,” says the wolf, “I’m hungry because you are guarding the sheep. Now I am so weak that I can’t find food. I think I will do.”', ''],
            ['“Why not help me?” Asks the dog, “I work regularly and I eat regularly. You could do the same. You can help me guard the sleep. In that way, I will not worry about your stealing the sleep, and you will not worry about going hungry. It’s good for us.', ''],
            ['The wolf thinks it over and thinks the dog is right. So they walk to the dog’s house. As they are walking, the wolf sees that only the hair of the dog’s neck is very thin. He is curious about this. So he asks the dog about it.', ''],
            ['“Oh, don’t worry about that,” says the dog, “It’s the place where the collar ties on the neck. My master chains me up at night,”', ''],
            ['“Chained up!” shouts the wolf, “Do you mean that you are chained up at night? If I come to live with you, will I be chained up at night, too?”', ''],
            ['“That’s night,” says the dog, “But, you’ll get used to it.”', ''],
            ['“But, if I am chained up, I won’t be free.” After saying this, the wolf turns round and ', ''],
            ['The dog shouts, “Wait! Come back! I’m not free, but I’m healthy. I have good food, and a warm place to sleep. I like enjoying life. In fact, I’m freer than you are.”', ''],
            ['对于大多数中国人来说，学外语意味着学英语。想要学好英语得下功夫才行，现在很多孩子在儿童时期就开始学英语了。', ''],
            ['如何培养儿童学习英语的乐趣呢？不妨试着用英语给孩子们讲讲故事，本期为您推荐的故事是：城里老鼠和乡下老鼠（双语）', ''],
            ['Once there were two mice. They were friends. One mouse lived in the country; the other mouse lived in the city. After many years the Country mouse saw the City mouse; he said, "Do come and see me at my house in the country." So the City mouse went. The City mouse said, "This food is not good, and your house is not good. Why do you live in a hole in the field? You should come and live in the city. You would live in a nice house made of stone. You would have nice food to eat. You must come and see me at my house in the city."', ''],
            ['The Country mouse went to the house of the City mouse. It was a very good house. Nice food was set ready for them to eat. But just as they began to eat they heard a great noise. The City mouse cried, " Run! Run! The cat is coming!" They ran away quickly and hid.', ''],
            ['After some time they came out. When they came out, the Country mouse said, "I do not like living in the city. I like living in my hole in the field. For it is nicer to be poor and happy, than to be ', ''],
            ['从前，有两只老鼠，它们是好朋友。一只老鼠居住在乡村，另一只住在城里。很多年以后，乡下老鼠碰到城里老鼠，它说：“你一定要来我乡下的家看看。”于是，城里老鼠就去了。乡下老鼠领着它到了一块田地上它自己的家里。它把所有最精美食物都找出来给城里老鼠。城里老鼠说：“这东西不好吃，你的家也不好，你为什么住在田野的地洞里呢？你应该搬到城里去住，你能住上用石头造的漂亮房子，还会吃上美味佳肴，你应该到我城里的家看看。”', ''],
            ['乡下老鼠就到城里老鼠的家去。房子十分漂亮，好吃的东西也为他们摆好了。可是正当他们要开始吃的时候，听见很大的一阵响声，城里的老鼠叫喊起来：“快跑！快跑！猫来了！”他们飞快地跑开躲藏起来。', ''],
            ['过了一会儿，他们出来了。当他们出来时，乡下老鼠说：“我不喜欢住在城里，我喜欢住在田野我的洞里。因为这样虽然贫穷但是快乐自在，比起虽然富有却要过着提心吊胆的生活来说，要好些。”', ''],
            ['如何培养儿童学习英语的乐趣呢？不妨试着用英语给孩子们讲讲故事，本期为您推荐的故事是：', ''],
            ['An old woman had a cat. The cat was very old; she could not run quickly, and she could not bite, because she was so old. One day the old cat saw a mouse; she jumped and caught the mouse. But she could not bite it; so the mouse got out of her mouth and ran away, because the cat could not bi', ''],
            ['Then the old woman became very angry because the cat had not killed the mouse. She began to hit the cat. The cat said, "Do not hit your old servant. I have worked for you for many years, and I would work for you still, but I am too old. Do not be unkind to the old, but remember what good work the old did when they were young."', ''],
            ['一位老妇有只猫，这只猫很老，它跑不快了，也咬不了东西，因为它年纪太大了。一天，老猫发现一只老鼠，它跳过去抓这只老鼠，然而，它咬不住这只老鼠。因此，老鼠从它的嘴边溜掉了，因为老猫咬不了它', ''],
            ['于是，老妇很生气，因为老猫没有把老鼠咬死。她开始打这只猫，猫说：“不要打你的老仆人，我已经为你服务了很多年，而且还愿意为你效劳，但是，我实在太老了，对年纪大的不要这么无情，要记住老年人在年青时所做过的有益的事情。”', ''],
            ['如何培养儿童学习英语的乐趣呢？不妨试着用英语给孩子们讲讲故事，本期为您推荐的是关于动物的英语故事短文：狐狸和公鸡（双语）', ''],
            ['One morning a fox sees a cock.He think,"This is my breakfast.''', ''],
            ['He comes up to the cock and says,"I know you can sing very well.Can you sing for me?''The cock is glad.He closes his eyes and begins to sing.', ''],
            ['he fox sees that and caches him in his mouth and carries him away. The people in the fie', ''],
            ['They cry,"Look,look!The fox is carrying the cock away.''The cock says to the fox,"Mr Fox,do you understand?The people say you are carrying their cock away.Tell them it is yours.Not the', ''],
            ['The fox opens his mouth ang says,"The cock is mine,not yours.''Just then the cock runs away from the fox and flies into the tree. ', ''],
            ['一天早上，一只狐狸看到了一只公鸡。他想：这是我的早餐。', ''],
            ['他朝公鸡走来，对他说：“我知道，你能唱得非常好听，你能唱给我听么？”公鸡很高兴。他闭上眼睛开始唱歌。狐狸看到这些抓住它放到自己的嘴里走了。在田地里的人们看到了狐狸。', ''],
            ['大喊大叫：“看，看！狐狸抓住公鸡逃走了。”公鸡对狐狸说：“狐狸先生，你能理解么？人们认为你叼走了公鸡。告诉他们这是你的，不是他们的。”', ''],
            ['狐狸张开她的嘴说：“公鸡是我的，不是你们的。”就在那时，。公鸡跑到了树底下。', ''],
            ['今天的这篇英语故事比较简短，非常适合小朋友们学习，一起来读读吧：', '']
            ['The monkey mother has two little monkeys. She likes the younger, not the other.猴妈妈生了两个猴子。她喜欢年幼的小猴子而不喜欢年长的大猴子。', ''],
            ['One day, they were playing in a forest when a wolf came，running at them. The monkey ran away with the younger monkey in a hurry and left the older alone. She climbed up a tree and held the younger in her arms.一天，他们正在森林里玩的时候，一只狼来了并向他们扑去。猴子匆忙带着小猴子跑了，单独留下大猴子。她跑着小猴子爬到树上。', ''],
            ['After some time, the wolf went away slowly. The monkey took the baby out of her arms. She was surprised to see that the baby had died, for the baby was held in arms too highly. Very long time later, she remembered to look for the older baby. The older baby was hiding in a wood. So he saved himself.过些时候，狼慢慢地离开了。母猴从他的怀里放下小猴子。她吃惊的发现猴宝宝已经死了，因为小猴子在她的怀里被搂地太紧了。过了很长时间，她才想起去寻找那只大猴子。大猴子藏在一个大洞里，他救了自己', '']
        ]
        # idiom data
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
            '卧薪尝胆': ['春秋时期，吴王夫差凭着自己国力强大，领兵攻打越国。结果越国战败，越王勾践于是被抓到吴国。吴王为了羞辱越王，因此派他看墓与喂马这些奴仆才做的工作。越王心里虽然很不服气，但仍然极力装出忠心顺从的样子。吴王出门时，他走在前面牵着马；吴王生病时，他在床前尽力照顾，吴王看他这样尽心伺候自己，觉得他对自己非常忠心，最后就允许他返回越国。越王回国后，决心洗刷自己在吴国当囚徒的耻辱。为了告诫自己不要忘记复仇雪恨，他每天睡在坚硬的木柴上，还在门上吊一颗苦胆，吃饭和睡觉前都要品尝一下，为的就是要让自己记住教训。除此之外，他还经常到民间视察民情，替百姓解决问题，让人民安居乐业，同时加强军队的训练。经过十年的艰苦奋斗，越国变得国富兵强，于是越王亲自率领军队进攻吴国，也成功取得胜利，吴王夫差羞愧得在战败后自杀。后来，越国又趁胜进军中原，成为春秋末期的一大强国。 ', ''],
            '四面楚歌': ['项羽和刘邦原来约定以鸿沟（在今河南荣县境贾鲁河）东西边作为界限，互不侵犯。后来刘邦听从张良和陈平的规劝，觉得应该趁项羽衰弱的时候消灭他，就又和韩信、彭越、刘贾会合兵力追击正在向东开往彭城（即今江苏徐州）的项羽部队。终于布置了几层兵力，把项羽紧紧围在垓下（在今安徽灵璧县东南）。这时，项羽手下的兵士已经很少，粮食又没有了。夜里听见四面围住他的军队都唱起楚地的民歌，不禁非常吃惊地说：刘邦已经得到了楚地了吗？为什么他的部队里面楚人这么多呢？说看，心里已丧失了斗志，便从床上爬起来，在营帐里面喝酒，并和他最宠爱的妃子虞姬一同唱歌。唱完，直掉眼泪，在一旁的人也非常难过，都觉得抬不起头来。虞姬自刎于项羽的马前，项羽英雄末路，带了仅剩兵卒至乌江，最终自刎于江边。以后人们就用四面楚歌这个词，形容人们遭受各方面攻击或逼迫，而陷于孤立窘迫的境地。凡是陷于此种境地者，其命运往往是很悲惨的。例如某人因经常与坏人为伍，不事生产，游手好闲，但后来却被那些坏人逼迫得无以为生，而求助于别人时，别人又因他平日行为太坏，绝不同情理睬，这人所处的境地便是四面楚歌。', ''],
            '指鹿为马': ['秦朝二世的时候，宰相赵高掌握了朝政大权。他因为害怕群臣中有人不服，就想了一个主意。有一天上朝时，他牵着一只梅花鹿对二世说：陛下，这是我献的名马，它一天能走一千里，一夜能走八百里。二世听了，大笑说：承相啊，这明明是一只鹿，你却说是马，真是错得太离谱了！赵高说：这确实是一匹马，陛下怎么说是鹿呢？二世觉得纳闷，就让群臣百官来评判。大家心想，说实话会得罪承相，说假话又怕欺骗陛下，就都不出声。这时赵高盯着群臣，指着鹿大声问：大家看，这样身圆腿瘦，耳尖尾粗，不是马是甚么？大家都害怕赵高的势力，知道不说不行，就都说是马，赵高非常得意，二世被弄胡涂了，明明是鹿，怎么大家都说是马呢？他以为自己疯了，从此越来越胡涂，朝政上的事都完全由赵高来操纵。赵高暗中把那些说实话的人杀掉，又派人杀死二世，霸占整个朝廷，最后终于导致秦朝灭亡。', ''],
            '画龙点睛': ['传说古时候有个画家叫张僧繇，他画龙画得特别好。有一次，他在金陵（现在南京）安乐寺的墙壁上画了四条巨龙，那龙画得活灵活现，非常逼真，只是都没有眼睛。人们问张僧繇：“为什么不把眼睛画出来。”他说：“眼睛可不能轻易画呀！一画了，龙就会腾空飞走的！”大家听了，谁也不信，都认为他在说大话。后来，经不起人们一再请求，张僧繇只好答应把龙的眼睛画出来。奇怪的事情果然发生了，他刚刚点出第二条龙的眼睛，突然刮起了大风，顷刻间电闪雷鸣。两条巨龙转动着光芒四射的眼睛冲天而起，腾空而去。围观的人，个个看得目瞪口呆，对张僧繇更佩服了。成语“画龙点睛”就是从这个传说中来的。现在一般用来比喻写作、讲话时，在关键性的地方用上一两句精辟的语言来点明含义，使内容更加生动有力。这种手法也称为“点睛”之笔。', ''],
            '攀龙附凤': ['“攀龙附凤”这则成语的“龙、凤”是形容有权势的人。比喻巴结或投靠有权势的人。这个成语来源于《汉书.叙转下》，午阳鼓刀，滕公厩驺，颖阴商贩，曲周庸夫，攀龙附凤，并乘天衢。西汉的开国皇帝刘邦，出身于一个农民家庭，他的父母连名字都没有。刘邦原名季，意思是“老三”，直到做了皇帝，才改名为邦。刘邦三十岁时，当了秦朝沛县的一个乡村小吏——亭长。他为人豁达大度，胸怀开朗，做事很有气魄，很多人都和他合得来。当地的萧何、樊哙、夏侯婴等，都是他的好朋友。这些人后来都为刘邦建立汉朝出了大力。樊哙是刘邦的同乡，是个杀狗卖狗的。陈胜、吴广发动起义后，沛县县令惊恐万分，打算投起义之机响应陈胜，就派樊哙去召刘邦来相助。不料刘邦带了几百人来时，县令又反悔起来。于是，刘邦说服城里人杀了县令，带领二三千人马誓师起兵。夏侯婴与刘邦也早就有了交情。他原来是县衙里的马夫，每次奉命为过往使者赶车，回来时经过刘邦那里，总要与刘邦闲谈很长时间，直到日落西山才走。后来夏侯婴当了县吏，与刘邦交往更密切了。一天刘邦与他闹着玩，一不小心打伤了他。有人告刘邦身为亭长，动手打人，应当严惩，夏侯婴赶紧为他解释。不料，后来夏侯婴反以伪证罪被捕下狱，坐了一年多班房。后来刘邦在沛县起兵，他和樊哙主动参加，并担任部将。刘邦的势力逐渐发展后，有个名叫灌婴的人又来投奔他。灌婴是睢阳人，本为贩卖丝绸的小商人。此人后来也成为刘邦的心腹，领兵转战各地，立了不少战功。公元前208年，刘邦根据各路起义军开会的决定，带领人马西攻秦都咸阳。第二年初，刘邦大军兵临陈留，把营扎在城郊，当地有个名叫郦食其的小吏前来献计。郦食其对刘邦说，现在您兵不满万人，又缺乏训练，要西攻强秦，如进虎口。不如先攻取陈留，招兵买马，等兵强马壮后再打天下。郦食其还表示，他和陈留县令相好，愿意前去劝降；如县令不降，就把他杀了。刘邦采纳了郦食其的计谋。郦食其连夜进陈留城劝说县令，但那县令不肯起义。于是郦食其半夜割下他的头颅来见刘邦。第二天刘邦攻城时，把那县令的头颅高悬在竹竿上，结果守军开城门投降。在陈留，刘邦补充了大量粮食、武器和兵员。接着郦食其又推荐了他颇有智勇的弟弟郦商，郦商又给刘邦带来了四千人。刘邦就任命他为副将，带领这支队伍西攻开封。后来，刘邦又战胜项羽，在公元前202年即皇帝位，建立了西汉王朝。刘邦当皇帝后大封功臣，樊哙、夏侯婴、灌婴、郦商等人也先后被封为舞阳侯、当汝阴侯、颖阴侯和曲周侯。', ''],
            '叶公好龙': ['春秋时，有位叫叶公的人非常喜欢龙。他家的屋梁上、柱子上和门窗上都雕刻着龙的图案，墙上也绘着龙。传说天上的真龙知道此事后很受感动，专程到叶公家里来，把头从窗口伸进屋子里，把尾巴横在客堂上。叶公看到后，吓得面无血色，魂不附体，抱头就跑。原来他并不是真正喜欢龙。他爱的是假龙，怕的是真龙。这个成语比喻表面上爱好某一事物，实际上并不是真正爱好它，甚至是畏惧它。', ''],
            '精卫填海': ['传说，很久以前，炎帝有个女儿叫女娃，炎帝很喜欢她，经常带她到东海去游泳。女娃非常勇敢，大风大浪从不畏惧。女娃长大后，每天都要自己到东海去游泳。有一天，她不幸被大海淹死了。女娃死后变成了一只鸟，每天从山上衔来石头和草木，投入东海，然后发出“精卫”“精卫”的叫声，好像在呼唤着自己。精卫鸟日复一日，年复一年，顽强不息，坚持不懈，决心要把东海填平。这句成语比喻矢志不移，努力不懈。后人常以“精卫填海”这个成语比喻深仇大恨，立志必报。或比喻不畏艰难险阻，矢志不移的坚毅决心。', ''],
            '八仙过海': ['传说吕洞宾等八位神仙去赴西王母的的蟠桃会，途经东海，只见巨浪汹涌。吕洞宾提议各自投一样东西到海里，然后各显神通过海。于是铁拐李把拐杖投到水里，自己立在水面过海；韩湘子以花蓝技水而渡；吕洞宾、蓝采和、张果老、汉钟离、曹国舅。何仙姑也分别把自己的萧、拍板、纸驴、鼓、玉版、竹罩投到海里，站在上面逐浪而过。八位神仙都靠自己的神通渡过了东海。八仙过海根据这个传说而来。八仙过海比喻各自有一套办法或本领去完成任务。', ''],
            '开天辟地': ['神话中传说，世上最早时，天地浑然一体。世界像个鸡蛋，天地的开创人盘古就在蛋里。一万八千年后，盘古从蛋里走出来。蛋里淡淡的烟云冉冉上升，变成青天。混浊的沉渣逐渐凝聚，变成大地。天地近在咫尺。盘古弯曲着背把天地撑开。盘古顶开立地一万八千年，终于把天撑高。天地再也不会合在一起，盘古才安然死去。他呼出的气，变成风和云。他留下的声音，变成雷霆。他的眼睛变成太阳和月亮。盘古开创了世界。颂扬开创伟大事业，称开天辟地。', ''],
            '三顾茅庐': ['东汉末年，诸葛亮居住在隆中的茅庐里。谋士徐庶向刘备推荐说：诸葛亮是个奇才。刘备为了请诸亮帮助自己打天下，就同关羽、张飞一起去请他出山。可是诸葛亮不在家，刘备只好留下姓名，怏怏不乐地回去。隔了几天，刘备打听到诸葛亮回来了，又带着关羽、张飞冒着风雪前去。哪知诸葛亮又出门出去了，刘备他们又空走一趟。刘备第三次去隆中，终于见到了诸葛亮。在交谈中，诸葛亮对天下形势作了非常精辟的分析，刘备十分叹服。刘备三顾茅庐，使诸葛亮非常感动，答应出山相助。刘备尊诸葛亮为军师，对关羽、张飞说：我之有孔明，犹鱼之有水也！诸葛亮初出茅庐，就帮刘备打了不少胜仗，为刘备奠定了蜀汉的国基。成语三顾茅庐由此而来', ''],
            '草船借箭': ['“草船借箭”这则成语的意思是运用智谋，凭借他人的人力或财力来达到自己的目的。这个成语来源于《三国演义》，用奇谋孔明借箭。三国时期，曹操率大军想要征服东吴，孙权、刘备联合抗曹。孙权手下有位大将叫周瑜，智勇双全，可是心胸狭窄，很妒忌诸葛亮（字孔明）的才干。因水中交战需要箭，周瑜要诸葛亮在十天内负责赶造十万支箭，哪知诸葛亮只要三天，还愿立下军令状，完不成任务甘受处罚。周瑜想，三天不可能造出十万支箭，正好利用这个机会来除掉诸葛亮。于是他一面叫军匠们不要把造箭的材料准备齐全，另一方面叫大臣鲁肃去探听诸葛亮的虚实。鲁肃见了诸葛亮。诸葛亮说：“这件事要请你帮我的忙。希望你能借给我20只船，每只船上30个军士，船要用青布慢子遮起来，还要一千多个草把子，排在船两边。不过，这事千万不能让周瑜知道。”鲁肃答应了，并按诸葛亮的要求把东西准备齐全。两天过去了，不见一点动静，到第三天四更时候，诸葛亮秘密地请鲁肃一起到船上去，说是一起去取箭。鲁肃很纳闷。诸葛亮吩咐把船用绳索连起来向对岸开去。那天江上大雾迷漫，对面都看不见人。当船靠近曹军水寨时，诸葛亮命船一字儿摆开，叫士兵擂鼓呐喊。曹操以为对方来进攻，又因雾大怕中埋伏，就派六千名弓箭手朝江中放箭，雨点般的箭纷纷射在草把子上。过了一会，诸葛亮又命船掉过头来，让另一面受箭。太阳出来了，雾要散了，诸葛亮令船赶紧往回开。这时船的两边草把子上密密麻麻地插满了箭，每只船上至少五、六千支，总共超过了十万支。鲁肃把借箭的经过告诉周瑜时，周瑜感叹地说：“诸葛亮神机妙算，我不如他。”', ''],
            '草木皆兵': ['这个成语来源于《晋书.苻坚载记》，坚与苻融登城而望王师，见部阵齐整，将士精锐；又北望八公山上草木，皆类人形。公元383年，基本上统一了北方的前秦皇帝苻坚，率领90万兵马，南下攻伐东晋。东晋王朝任命谢石为大将，谢玄为先锋，率领8万精兵迎战。秦军前锋苻融攻占寿阳（今安徽寿县）后，苻竖亲自率领八千名骑兵抵达这座城池。他听信苻融的判断，认为晋兵不堪一击，只要他的后续大军一到，一定可大获全胜。于是，他派一个名叫朱序的人去向谢石劝降。朱序原是东晋官员，他见到谢石后，报告了秦军的布防情况，并建议晋军在前秦后续大军未到达之前袭击洛涧（今安徽淮南东洛河）。谢石听从他的建议，出兵偷袭秦营，结果大胜。晋兵乘胜向寿阳进军。苻坚得知洛涧兵败，晋兵正向寿阳而来，大惊失色，马上和苻融登上寿阳城头，亲自观察淝水对岸晋军动静。当时正是隆冬时节，又是阴天，远远望去，淝水上空灰蒙的一片。仔细看去，那里桅杆林立，战船密布，晋兵持刀执戟，阵容甚为齐整。他不禁暗暗称赞晋兵布防有序，训练有素。接着，苻坚又向北望去。那里横着八公山，山上有八座连绵起伏的峰峦，地势非常险要。晋兵的大本营便驻扎在八公山下。随着一阵西北风呼啸而过，山上晃动的草木，就像无数士兵在运动。苻坚顿时面如土色，惊恐地回过头来对苻融说：晋兵是一支劲敌，怎么能说它是弱兵呢？不久，苻坚中谢玄的计，下令将军队稍向后退，让晋兵渡过淝水决战。结果，秦兵在后退时自相践踏，溃不成军，大败北归。这一战，便是历史上著名的淝水之战，是历史上以少胜多，以弱胜强的著名战例。', ''],
            '破釜沉舟': ['破釜沉舟”这则成语的釜是锅；舟是船。砸破烧饭用的锅子，凿沉船只，比喻拚死一战。这个成语来源于《史记.项羽本纪》，项羽乃悉引兵渡河，皆沉船，破釜甑，烧庐舍，持三日粮，以示士卒必死，无一还心。秦朝末年，秦二世派大将章邯攻打赵国。赵军不敌，退守巨鹿（今河北平乡西南），被秦军团团围住。楚怀王封宋义为上将军，项羽为副将，派他们率军去救援赵国。不料，宋义把兵带到安阳（今山东曹县东南）后，接连46天停滞不进。项羽忍不住，一再要求他赶紧渡江北上，赶到巨鹿，与被围赵军来个里应外合。但宋义另有所谋，想让秦、赵两军打得精疲力竭再进兵，这样便于取胜。他严令军中，不听调遣的人，不管是谁都要杀。与此同时，宋义又邀请宾客，大吃大喝，而士兵和百姓却忍饥挨饿。项羽忍无可忍，进营帐杀了宋义，并声称他勾结齐国反楚，楚王有密令杀他。将士们马上拥戴项羽代理上将军。项羽把杀宋义的事及原因报告了楚怀王，楚怀王只好正式任命他为上将军。项羽杀宋义的事，震惊了楚国，并在各国有了威名。他随即派出两名将军，率2万军队渡河去救巨鹿。在获悉取得小胜并接到增援的请求后，他下令全军渡河救援赵军。项羽在全军渡河之后，采取了一系列果断的行动：把所有的船只凿沉，击破烧饭用的锅子，烧掉宿营的屋子，只携带三天干粮，以此表示决心死战，没有一点后退的打算。这支有进无退的大军到了巨鹿外围，立即包围了秦军。经过9次激战，截断了秦军的补给线。负责围攻巨鹿的两名秦将，一名被活捉，另一名投火自焚。在这之前，来援助赵国的各路诸侯虽然有几路军队在巨鹿附近，但都不敢与秦军交锋。楚军的拚死决战并取得胜利，大大地提高了项羽的声威。从此，项羽率领的军队成了当时反秦力量中最强大的一支武装。后来，“皆沉船，破釜甑”演化为成语“破釜沉舟”，用来比喻拚死一战，决心很大。项羽也成了当时农民起义军的著名领袖人物，并在不久和刘邦的起义军一起，推翻了秦朝的统治。', ''],
            '穷兵黩武': ['东吴后期的名将陆抗，二十岁时就被任命为建武校尉；带领他父亲陆逊留下的部众五千人。公元264年，孙皓当了东吴的国君，三十八岁的陆抗担任镇军大将军。当时，东吴的朝政非常腐败。孙皓荒淫暴虐，宫女有好几千人，还向民间掠夺；又用剥面皮、凿眼睛筹酷刑任意杀人。陆抗对孙皓的所作所为非常不满，多次上疏，劝谏他对外加强防守，对内改善政治，以增强国力。他曾在奏疏中一次陈述当前应做的事达十六件之多。但是，孙皓对他的建议置之不理。公元272年，镇守西陵的吴将步阐投降晋朝。陆抗得知后、立即率军征讨步阐。他知道晋军一定会来接应步阐，', ''],
            '曲高和寡': ['宋玉是楚国伟大诗人屈原的学生。有一天，楚襄王问宋玉：现在不少人对你有意见，你是不是有什么不对的地方？宋玉转弯抹角地回答说：有位歌唱家在我们都城的广场上演唱，唱《下里》《巴人》这些通俗歌曲时，有几千听众跟着唱起来；唱《阳春》《白雪》这类高深歌曲时，能跟着唱的只有几十人；到了唱更高级的歌曲时，跟着唱的只有几个人了。从这里可以看出，曲调越是高深，能跟着一起唱的人就越少。宋玉这段话的意思是说自己品行高超，一般的人不能了解，所以有人说三道四。和（音贺）指跟着别人唱；寡是少的意思。这个成语后来比喻言论、作品很深，能理解的人很少。有时也用来讽刺别人自命不凡。', ''],
            '势如破竹': ['三国末年，晋武帝司马炎灭掉蜀国，夺取魏国政权以后，准备出兵攻打东吴，实现统一全中国的愿望。他召集文武大臣们商量灭大计。多数人认为，吴国还有一定实力，一举消灭它恐怕不易，不如有了足够的准备再说。大将杜预不同意多数人的看法，写了一道奏章给晋武帝。杜预认为，必须趁目前昊国衰弱，忙灭掉它，不然等它有了实力就很难打败它了。司马炎看了杜预的奏章，找自己的最信任的大臣张华征求意见。张华很同意杜预的分析，也劝司马炎快快攻打吴国，以免留下后患。于是司马炎就下了决心，任命杜预作征南大将军。公元279年，晋武帝司马炎调动了二十多万兵马，分成六路水陆并进，攻打吴国，一路战鼓齐鸣，战旗飘扬，战士威武雄壮。第二年就攻占了江陵，斩了吴国一员大将，率领军队乘胜追击。在沅江、湘江以南的吴军听到风声吓破了胆，纷纷打开城门投降。司马炎下令让杜预从小路向吴国国都建业进发。此时，有人担心长江水势暴涨，不如暂收兵等到冬天进攻更有利。杜预坚决反对退兵，他说：“现在趁士气高涨，斗志正旺，取得一个又一个胜利，势如破竹（像用快刀劈竹子一样，劈过几节后竹子就迎刃破裂），一举攻击吴国不会再费多大力气了！”晋朝大军在杜预率领下，直冲向吴都建业，不久就攻占建业灭了吴国。晋武帝统一了全国。 ', ''],
            '室如悬磬': ['有一次，齐孝公出兵去征伐鲁国，鲁君想派人去说服齐国，制止齐国的侵略，但是不知道用什么言词去说服他们，便去问展禽。展禽沉思了一会儿，就说：“我听人说过，处在大国的地位，才可以教导小国；处在小国的地位，却只能服侍大国。惟有这样，才能消除战争。我从来都没有听过，单靠言词就能平息乱事的。假如是个小国，还很自大的话，只会引起大国的恼怒，增加乱事，现在乱事已经开始，不是靠言词就能收到成效的。”展禽说完，就叫乙喜去犒劳齐军，并且对他们说：“我们的君王没有才干，不能好好的管理边界上的事情，以至于劳驾你们，还连累你们的军队露宿在我们的边境上，所以特别派我来犒劳你们所有的兵士。”齐侯说：“你们到现在才恐慌吗？”乙喜说：“敝国现在有德高望重的人辅政，所以并不恐慌。”齐孝公说：“你们室如悬磬，田野里连青草都没得生长，怎么会说不恐慌呢？磬，就是指空无所有的意思。室如悬磬，就是用来比喻穷得什么东西也没有。它和“家徒四壁”都一样，是用来形容极端的贫乏、困苦。', ''],
            '手不释卷': ['三国时，吕蒙是吴国的大将。一次，他点兵3万，用船80余只袭击荆州。水手一律身着白衣，大批精兵埋伏在船舱里。黑夜，船到当阳江边，烽火台的汉兵厉声盘问。吴军诈称是商船，要求靠岸避风，汉兵信以为真。约至二更，船上吴军突然袭击，占据了烽火台。随后，吕蒙带兵长驱直入，轻取荆州。吕蒙作战勇猛，平时却不肯读书。孙权劝道：你读点历史和兵法，用兵更高明。孙权道：汉先武帝从前行伍出身，却‘手不释卷’。从此，吕蒙勤勉自学，受益匪浅。手不释卷：手里不离开书本，形容读书勤奋。', ''],
            '首鼠两端': ['这句成语见于《史记·魏其武安侯列传》：“武安已罢朝，出止车门，召韩御史大夫载，怒曰：‘与长孺共一老秃翁，何为首西汉武帝时，王太后有个同母异父的弟弟叫田蚡。他靠着王太后的势力做了丞相，掌握大权。田蚡是个卑鄙阴险、骄横自私的人物，因为有王太后这座靠山，加之汉武帝当时还年轻，所以他胡作非为，骄横奢侈，营私舞弊，随意诬陷自己所不快的人。田蚡向窦婴要城南田，窦婴不给，又听说灌夫也替窦婴抱不平，由此跟灌夫和窦婴结了怨（窦婴和灌夫都是在平定七国之乱中立了功的大臣）。又因为灌夫掌握着田蚡贪污受贿的事，所以田蚡欲将他和窦婴置之死地有一次，田蚡结婚，王太后为了扩大自己的势力，便下了诏书，吩咐诸侯、宗室、大臣们都到丞相府去祝贺。窦婴和灌夫也去了。酒席上，灌夫因向客人敬酒遭到冷遇，气得破口大骂起来。为此，田蚡拘捕了灌夫。此事闹到了武帝那里，武帝便召集大臣们来研究。窦婴坚决反对对灌夫治罪，有的大臣则赞成治罪，有的惧伯田蚡的威势，采取模棱两可的态度。御史大夫韩安国说：“灌夫在平定七国之乱时，立了大功，虽说酒后闹事，但没有死罪。可丞相说他不对，也有道理，究竟如何处置，请皇上定吧！”洞外时，总是左顾右盼，畏首畏尾，故称“首鼠两端”，人们常用这句成语形容迟疑不定或动摇不定。 ', ''],
            '熟能生巧': ['宋代有个叫陈尧咨的人，射箭技术极为高超，常因此而骄傲。一天，他正在给大家表演射箭，箭全射中靶心，于是就向旁边卖油的老头吹嘘起来。然而老人却说：没有什么了不起，只不过是手法熟练而已罢了。说着，拿来一个葫芦，在葫芦口放上一枚铜钱，用勺子舀了一勺油，高高地举起倒了下去。倒下去的油像一条线一样穿过钱眼而过，金部流进了葫芦，而铜钱上一点油也没沾上。老头说：干任何事都一样，熟能生巧。这个成语指做事熟练了，就会掌握窍门，做得更好。 ', ''],
            '双管齐下': ['唐朝人张瑽，官为员外郎。不久，他从员外郎的地位降为衡州司马。后来，他又被调为忠州司马，在官场上很不得志。但是，他喜欢绘画。而且画得很好。他尤其擅长画松石山水。他画松树时，总是双手各握一支毛笔。他用一支笔画新枝，另一支笔画枯枝。用两支笔画出来的松树，不论是新枝还是枯枝，都生动逼真。人们喜欢他的画，纷纷上门求索。大家称赞他的画为神品。他绘画的方式，则被人们称为双管齐下。成语双管齐下原指手握双管同时作画。后用来比喻为了达到某一目的，同时采用两种办法或两件事同时进行。 ', ''],
            '水滴石穿': ['宋朝时，张乖崖在崇阳当县令。当时，常有军卒侮辱将帅、小吏侵犯长官的事。张乘崖认为这是一种反常的事，下决心要整治这种现象。一天，他在衙门周围巡行。突然，他看见一个小吏从府库中慌慌张张地走出来。张乘崖喝住小吏，发现他头巾下藏着一文钱。那个小吏支吾了半天，才承认是从府军中偷来的。张乘崖把那个小吏带回大堂，下令拷打。那小吏不服气：一文钱算得了什么！你也只能打我，不能杀我！张乘崖大怒，判道：一日一钱，千日千钱，绳锯木断，水滴石穿', ''],
            '水落石出': ['苏轼，字子瞻，号东坡居士，是名文学家苏洵的长子。神宗当皇帝的时候，采用王安石的变法政策，苏轼因不赞成新法，和王安石辩论。那时王安石很为神宗所器重，苏轼敌不过他，被贬到湖北当团练副使，他在黄州的东坡地方，建筑了一间居住，所以又称苏东坡。自号东坡居士。苏东坡喜欢山水，时时出去游玩。赤壁是三国时东吴和蜀汉联军大破曹操的地方；但赤壁在湖北有三处，一在汉水之侧，竟陵之东，即复州；一在齐安之步下，即黄州；一在江夏之西南一百里，今属汉阳县。江夏西南一百里之赤壁，正是曹公败处，东坡所游之赤壁在黄州汉川门外，不是曹公失败的地方，东坡自己也知道，他先后做了两篇赤壁赋，只是借题发挥而已，名同地异，因他的才思横溢，文笔流利，写得唯妙唯肖，使后人对于赤壁这地方，都怀有向往的心情，在后赤壁赋中，他有这样几句“...于是携酒与鱼，复游于赤壁之下，江流有声，断岸千尺，山高月小，水落石出，曾日月之几何，而江山不可复识矣。…”“水落石出”苏轼的赋中，本来是指冬的一种风景，但后人把这水落石出四字，用做真相毕露被悉破的意思。也有人把一件事情的原委弄清楚以后，等到真相大白，也叫做水落石出。 ', ''],
            '水深火热': ['齐国出兵攻打燕国。战场上一片混乱，老百姓家破人亡。齐宣王亲自督战，十分得意。齐国大小官员，有的赞扬齐宣王的壮举，有的私下里批评君主不仁不爱。孟子是大学问家，历来主张仁爱，反对战争，他当然很不高兴。齐宣王凯旋归来，设酒宴招待文武百官。齐宣王说：有人对我攻打燕国有意见，现在我50天就征服了他们，这不是天意吗？群臣们一声不吭，你看看我，我看看你。孟子，你倒说说看。齐宣王有点咄咄逼人。孟子回答说：如果您占领燕国，燕国人民很高兴，您就去占领吧！齐宣王很不高兴。孟子继续说：如水益深，如火益热，燕国的百姓会来送水、送饭，争相欢迎吗？成语水深火热本意是：使得水更加深，火更加热。比喻人民生活极端痛苦，如处在深水、热火之中。 ', ''],
            '司空见惯': ['唐代诗人刘禹锡，因为性格放荡不羁，在京中受人排挤，被贬做苏州刺史。当地有一个曾任过司空官职的人名叫李绅，因仰慕刘禹锡的诗名，邀请他饮酒，并请了几个歌女在席上作陪。席间，刘禹锡一时诗兴大发，作诗一首：高髻云鬓新样妆，春风一曲杜韦娘，司空见惯浑闲事，断尽苏州刺史肠。司空见惯这句成语，就是从刘禹锡这首诗中得来的。诗中所用的司空两个字，是唐代一种官职的名称，相当于清代的尚书。从刘禹锡的诗来看，整句成语的意思，就是指李司空对这样的事情已经见惯，不觉得奇怪了。这是一句很常用的成语，但有很多人仍会把它用错，因为寻常的事情，如果是发生得很自然，便不可以引用这句成语。如早晨的时候，太阳从东方出来，到黄昏的时候，太阳便在西方没落，这样便不能说司空见惯。有些事情发生得很偶然，但又是常常可能发生或见到的，这时用这个成语就比较恰当。比方大都市街道上的车辆，平常都是很安全地来往着，但很多时候又会发生意外，不是辗伤了人，便是撞了车，这样的事情我们看多了，则用司空见惯四个字就恰当了。 ', ''],
            '死不旋踵': ['“死不旋踵”原作“死不还踵”。这个成语，原出自《淮南子·泰族训》。原文说：“墨子服役者百八十人，皆可使赴火蹈刃，死不还踵。”意思是：春秋战国之际的著名思想家墨子的学生有180人，他们都是不避艰险、奋不顾身、至死也不会回头的人物。《后汉书·党锢列传·李膺传》里记载着“死不旋踵”的故事。东汉桓帝时代，宦官专权，与大官僚集团斗争十分激烈。世家豪族李膺做司隶校尉时，宦官头子张让的弟弟张朔做野王（现在河南省沁阳县）县令，贪赃枉法，凶暴残民，甚至杀戮孕妇。张朔害怕受到李膺的惩罚，于是畏罪逃到张让家里，躺在一根空心的屋柱内。李膺知道这个情况后，亲率役卒，冲进张让家里，砍破屋柱，把张朔捉来杀了。张让向桓帝告状，桓帝召李膺进宫，责问他为什么不先请示就把张朔处以死刑。李膺回答说：“现在我到任已经10天了，怕犯了积压案件的过失，想不到竟得了办案快的罪名。我自知有罪，死期就在眼前，但我并不惧怕（原文是“诚自知衅责，死不旋踵”），特请宽限5天，让我把那些坏蛋惩办完，卸了任再来受刑。”桓帝听了，回头对张让说：“这是你弟弟罪有应得，司隶校尉有什么过错？”“旋踵”是转动脚后跟，即后退的意思，有时也比喻时间很短。后来，人们引用“死不旋踵”这个成语，来比喻不避艰险，即使死也不后退或死在眼前也不怕。 ', ''],
            '死而不朽': ['公元前549年，鲁国的大夫穆叔奉命到晋国去访问。晋国的卿范宣子接待了他，并且与他交谈起来。范宣子问穆叔道：“古人有话说：‘死而不朽。’你知道它说的是什么吗?”穆叔不清楚范宣子提出这个问题的用意，没有马上口答。范宣子以为穆叔答不上，得意他说：“我的祖先，虞舜前是陶唐氏，夏朗后是御龙氏，在商朗是象韦氏，在周朝则是唐社氏。周王室衰败以后，由晋国主持中原的盟会，执政的是范氏。所谓‘死而不朽’，恐怕说的就是这个吧!”穆叔听他这样说，觉得很不入耳，便说：“据我所听到的，这叫做世禄，也就是世世代代享受禄位，而不是‘不朽，。鲁国有一位已经去世的大夫，叫藏文种。死了以后，他的话世世代代没有被人们废弃。所谓‘不朽’。，说的是这个吧。”他接他又说：“我听说，最高的是树立德行，其次是树立功业，再其次是树立言论。如果能做到这样，虽然死了也久久不会被人们废弃。这叫做三不朽。若只是保存和接受姓氏，用来守住宗庙，世世代代不断绝祭祀，那是每个国家都有的，不能说是不朽。', ''],
            '死灰复燃': ['西汉时，韩安国是汉景帝与梁孝王身边一个很受欢迎的人。但是他年轻的时候，也曾经发生过一段曲折的故事。由于受到某件事的牵连，他被送进监狱等最后的判决下来。在监狱里有一个叫田甲的看守，对他非常不礼貌，常常毫不留情地羞辱他。有一次安国被欺负得太过份，就告诉田甲说：“你不要以为我这辈子就没有出人头地的一天，暂时熄了火的灰烬，难道就没有可能再烧起来吗？”田甲得意地说：“如果会的话，我一定会撒泡尿浇熄它。”可是，过了不久，安国无罪释放，而且还当上了大官。这时，田甲只好低头向韩安国认错。', ''],
            '死里逃生': ['从前楚国有个人叫次非，在一次机会中得到一把宝剑，便高兴地渡河回家。当船划到河中心的时候。突然出现两条蛟龙，绕着他的船兴风作浪。船上的人都叮坏了，不知道该怎么样辨。次非却镇争地问船夫：“照这样下去的话，全船的人不是等死吗？”。船夫消极地说：“这注定必死无疑，还能有什么辨法呢？”次非沉思片刻，立刻拔出宝剑说：“以前丢了性命的人，之所以会死在这里，就是因为他们虽然有武器，但不敢和蛟龙拼命。”次非一说完话，便跳进江里，杀了这两条蛟龙。全船的人也就得救了。', ''],
            '随珠弹雀': ['《庄子·让王篇》有这么一个故事：鲁侯（或谓即鲁哀公）听说颜阖是个贤明的人，想请他出来为国家出点力，便派人先送一份礼物去。颜阖家里很穷，住在一个破烂的村子里，这一天正披着件粗麻布旧衣，在那儿喂牛。鲁侯派的人来了，向颜阖问道：“喂，这儿是颜阖的家吗？”颜阖说：“是的，这是我的家。”那人这才知道他就是颜阖，便说明来意，把带去的礼物当面交给他。颜阖不受，说：“恐怕你听错了？要是送错，你会获罪的，还是回去问问清楚吧！”那人就这样被打发走了。可是不一会，又来了，说：“没有错，就是送给您的，无论如何，求您一定收下！”那人放下礼物就走，颜阖还有什么办法推辞呢。仞之雀，世必笑之。是何也？则其所用者重而所要者轻也！”比喻所用代价太大而收获太微、得不偿失，后来就叫“随珠弹雀。”（“随”也可以写作“隋”。春秋时随国在今湖北随县，为楚国所灭。南北朝时，杨坚受封于随，他把“随”改名为“隋”。后来杨坚做了皇帝，又以“隋”为国号，即隋朝，他就是隋文帝。从此，“随侯之珠”，也写作“隋侯之珠”。）', ''],
            '所向无前': ['岑彭字君然，南阳棘阳（今河南新野东北）人。王莽末年，岑彭为南阳棘阳县令，因为汉兵攻破城池，他逃奔到前队大夫甄阜那儿。甄阜令岑彭戴罪立功，坚守城池。后因汉兵攻打数月，城中粮尽，岑彭不得已开城投降。汉将想杀岑彭，大司徒伯升劝解说：岑彭是一郡之长官，坚心为其主守城，那是忠节。现在他归附我们，是相信正义，应当鼓励。这样，更始帝便封岑彭为归德侯。后来，他们又归顺了刘秀。待刘秀即位（为光武帝）后，岑做了廷尉，行使大将军的职权。从建武元年至11年，岑彭多次率部队南征北战，为东汉王朝屡立战功。', ''],
            '泰山压卵': ['孙惠是晋惠帝时齐王冏的谋士。在齐王失败之后，孙惠受到了成都王的重用，后来成都王起兵攻打长沙王，孙惠十分失望，才退隐。不久，东海王在下邳起兵，孙惠知道，就上书东海王，指出历代王朝危亡的情形，都是枝叶先雕零，才引起上下根株的死亡。因此，劝东海王应该一心平乱，匡扶王朝。同时还颂扬东海王的实力：“这种强大的力量，就像是乌获摧毁冰块；令孟贲折断枯树；使猛兽吞食狐狸；用泰山来压卵一样，这是没有办法相比的……”最后，东海王被孙惠恳切的言词打动，才起用了他。', ''],
            '贪得无厌': ['智伯，是春秋时代的人，他的野心很大，有一次他还联合了韩、赵、魏三国，把中行氏给灭掉，侵占了中行氏的领土。过了几年，他又派人向韩国要求割地，韩国惧怕，就给了他一块有万户人家的土地。智伯这回知道了食髓知味，又向魏国要求割地，魏国本来不想给，但是也怕围攻，只好和韩国一样，也给了他一块土地。智伯心中更高兴了，向赵国索取蔡和皋狼这两个地方；但是赵襄王拒绝了，智伯便结合韩国和魏国要攻打赵国。赵襄王采用谋士的计策，迁都晋阳，准备了充足的粮食来抵抗智伯。这样经过了三年，智伯始终没有办法攻下晋阳。但是，赵国的粮食快要用完了，派人去游说魏和韩，教他们联合起来，倒戈攻打智伯。因为智伯的野心太大了，魏国、韩国就答应了。于是，赵国连夜出兵，韩、魏两国跟着响应，把智伯击败，并瓜分他的土地；当时，天下的人不但不同情智伯，反而讥笑他“贪得无厌”，得到报应。', ''],
            '贪小失大': ['战国时，秦国想并吞近邻的蜀国，但由于秦蜀之间的秦岭山高路险，攻取不便。有人给秦王出了条妙计，秦王听后非常高兴，立刻派人用石头凿刻了一条石牛，在后面放了许多金银财宝，说是石牛拉出来的粪便。然后把石牛放在秦蜀之间的路上，作为礼物送给蜀王。蜀王听说后，马上令人开山修路。路修好后，秦兵以护送石牛为由，开始进攻蜀国，蜀国因此而灭亡。这个成语比喻因贪图小利而造成重大损失', ''],
            '坦腹东床': ['晋代太傅郗鉴，派一位门客到丞相王导家里去选女婿。王导告诉门客说：“你到东面的房子里，任意挑选吧︰”门客回来告诉郗鉴说：“王家的男孩都很好，听说我来选女婿，就都拘谨起来。只有一个男孩在东面的床上露着肚子躺着，好象没听见似的。”郗鉴说：“这个人做女婿最好。”原来，这个人就是王羲之，于是郗鉴把女儿嫁给了他。', ''],
            '探骊得珠': ['很久很久以前，有一户人家住在黄河边上，靠割芦苇、编帘子簸箕为生，日子过得非常贫困。', ''],
            '螳臂当车': ['颜阖担任卫灵公大儿子蒯瞆的老师，但蒯瞆自以为将来会当国君，作威作福，蛮不讲理。颜阖感到十分为难，于是对卫国大夫蘧伯玉诉苦。蘧伯玉劝他说：“你的意图是好的，但实际上是不可能的。你知道嘛，螳螂吗想举起它的臂膀，以挡住前进中的车子，这是不可能的啊！” ', ''],
            '天夺之魄': ['公元前５９４年，狄人（赤狄）丞相丰舒执政后杀了他的国君潞子婴儿的夫人，又伤了潞子的眼睛。潞子的夫人是晋景公的姐姐。因此，晋国在同年夏季出兵攻打赤狄，不到一个月的时间，即灭了赤狄。君的先人）去向周朝的天子进献俘虏的狄人。赵同依仗晋国强大，对周天子表现得很不恭敬，很傲慢。周天子的儿子刘康公看了很不高兴，骂道：“不及１０年，原叔（即赵同）必有大咎，天夺之魄矣！”意思是说，要不了１０年，赵同必定遭到大祸，老天爷已将他的魂魄夺走了。“天夺之魄”这个成语用来比喻人已离死期不远了。', ''],
            '天花乱坠': ['两晋南北朝时佛教盛行，全国有寺庙3万多所，僧尼200多万。南朝的梁武帝带头求神拜佛，在全国大建寺庙。他曾经三次舍身同泰寺，他还聘请古印度僧人波罗末到中国讲经。波罗末翻译了不少印度佛经，并培养了许多中国弟子。有了经书，讲经的风气更加兴盛。为了宣传民众，佛教徒编了许许多多讲经的传说。其中一则是：云光法师讲经，感动了上天，天上的鲜花纷纷坠落。后来，佛教在中国分成许多宗派，影响最大的是“禅宗”。宋真宗时，道原和尚编了一本《景德传灯录》，记载了禅宗师徒的故事。书中讲到对佛意要真正领会，反对“讲得天花乱坠”。从此，人们用“天花乱坠”来形容说话极其动听，但多指过分夸张，不切实际。', ''],
            '天经地义': ['公元前520年周景王姬贵死后，按习俗由他正夫人所生的世子姬敬继位。但是，景王生前曾与大夫宾孟商讨过，打算立非正夫人所生的长子姬朝为世子。这样，姬朝也有资格继位。于是，周王室发生了激烈的王位之争。', ''],
            '天罗地网': ['元朝李寿卿写了一本《伍员吹箫》的杂剧，内容是这样的：春秋时代，楚平王听信奸臣费无极的怂恿，把太子的妻子改作自己的妻子。太子的老师是太傅伍奢，是个刚正不阿的人。费无极怕伍奢帮助太子惩罚他，又怂恿楚平王杀害了伍奢及其全家人。太子得到消息，连夜逃走了。太子知道伍奢的第二个儿子伍员镇守樊城，就日夜兼程，赶到樊城。他把伍奢全家被害的情况告诉了伍员，并叫他提防。费无极果然派儿子费得雄来见伍员，说楚平王因伍员有功，召他返朝受赏。伍员怒斥道：若不是太子报信，我险些被打入天罗地网。伍员把费得雄痛打一顿，弃官逃到吴国，在街上吹箫求乞。后来，伍员受到吴王的重用，终于发兵伐楚，报了杀亲之仇。天罗地网，就是天为罗，地为网，比喻四周包围得十分严密，难以逃脱', ''],
            '天下无双': ['信陵君魏无忌窃符救赵后，怕哥哥魏王追究，避居赵国。他听说毛公和薛公很有才能，便去邀请。但两人不肯来见。他打听到毛公藏在赌徒中，薛公藏在卖酒人家，便去寻访，终于结识了两人。', ''],
            '天涯海角': ['韩愈，字退之，是唐代中叶时的伟大文学家。他二岁时就死了父亲，不久他的母亲又死去。幼时依靠他哥哥韩会和嫂嫂郑夫人过活。韩会有一个嗣子（愈次兄介之子，出继与长兄会为嗣）叫老成，排行十二，所以小名叫十二郎，年纪比韩愈小一点。后来韩会四十二岁的时候，因宰相元载的事，贬为韶州刺史，不到几个月就病死在韶州，这时韩愈只有十一岁，十二郎也很小。韩愈虽然有三个哥哥（会、弁、介），都很早离开了人世。这时，继承祖先后代的，只有韩愈和他的侄子十二郎两个人，零丁孤苦，没有一天离开过。', ''],
            '天衣无缝': ['古时候有个叫郭翰的先生，他能诗善画，性格诙谐，喜欢开玩笑。盛夏的一个夜晚，他在树下乘凉，但见长天如碧，白云舒卷，明月高挂，清风徐来，满院飘香。这时，一位长得异常美丽的仙女含笑站在郭翰面前。看，很诧异仙女的衣服是没有缝的。 ####仙女说：天衣无缝，你连这个都不懂，还称什么才子，我看你是十足的大傻瓜。 ####郭翰听完哈哈大笑，再一瞧，仙女不见了。', ''],
            '天真烂漫': ['南宋末年，有位姓郑的画家曾以太学生的资格，参加博学词科考试。后来北方蒙古贵族南侵，他向朝廷上书主张抵抗，但未被采纳', ''],
            '天之骄子': ['西汉时，匈奴常侵扰边郡。汉武帝派兵出击，多次得胜。公元90年，匈奴骑兵又侵占五原、酒泉，杀掠当地百姓。汉武帝派大将李广利等率军反击匈奴。匈奴单于（最高首领）丢弃了粮草、武器，却保存着实力。李广利大败匈奴。这时，他家属犯罪下狱的消息传来，他很担忧。谋士献计要他将功折罪。于是他挥兵北进，浴血沙场。后匈奴单于又乘机领兵袭击李广利。他招架不住，便投降了。单于为了笼络住李广利，把女儿嫁给他。一年后，李广利遭到匈奴丁灵王卫律的嫉妒，被害死。单于致书汉武帝：强胡，天之骄子。他要汉朝每年赠他美酒、绸缎等。汉武帝只得承认强胡难灭，以后与匈奴时和时战。匈奴人自称天之骄子即为天所骄宠，故极强盛。后也指非常勇敢或有特殊贡献的人。 ', ''],
            '同仇敌忾': ['东周春秋时期，有一首流传于军中的歌谣，表现了士兵们慷慨从军；同心对敌的乐观精神和保卫祖国的英雄气概。这首歌谣分为三节，可以反复咏唱。其中第一节是这样的：”谁说没有衣服?我的战袍就是你的。国王兴兵打仗，快把刀枪修好。我与你共同对付仇敌。”“同仇”这个词就来源于上面的歌谣。公元前623年，卫国的宁俞出使鲁国，鲁文王设宴招待。席间，文王让乐工演唱《湛露》和《彤TONG弓》，宁俞一听就知道。这是周天子对诸侯恩赐、褒奖时的宴乐。为此，他在席间不作任何答谢之辞。文王对宁俞在席间表示沉默不理解。宴饮完毕后，命人私下询问他是什么原因。宁俞回答说：“当年诸侯以周天子对敌人的愤恨为同恨，所以为天子献上战功。天子为了酬谢诸侯，在酒宴中赐彤弓，赋《湛露》，这是应该的。但如今我们卫国来到鲁国表示友好，大王学天子赐诸侯的礼节，也命乐工演唱《湛露》和《彤弓》。在这种情况下，我只好沉默不言了。”“敌忾”这个词就来源宁俞说的话。 ', ''],
            '同甘共苦': ['战国时，燕国太子姬平继承了王位，史称燕昭王。怎么治理，才能富民强国，燕昭王真感到束手无策。一天，他听说郭隗善出点子，很有计谋。于是赶紧派人去把郭魄请来，对他说：“你能否替我找到一个有本领的人，帮我强国复仇?”郭魄说：“只要你广泛选拔有本领的人，并且要亲自去访问他，那么，天下有本领的人就都会投奔到燕国来。”“那么我去访问哪一个才好呢?”郭隗回答说：“先重用我这个本领平平的人吧!天下本领高强的人看到我这样的人都被您重用，那么，他们肯定会不顾路途遥远，前来投奔您的。”燕昭王立刻尊郭隗为老师，并替他造了一幢华丽住宅。消息一传开，乐毅、邹衍、剧辛等有才能的人，纷纷从魏、齐、赵等国来到燕国，为燕昭王效力。燕昭王很高兴，都委以重任，开关备至；无论谁家有婚丧娶等事，他都亲自过问。就这样，他与百姓同事安乐，共度苦难二十八年，终于把燕国治理得国富民强，受到举国上下的一致拥戴。 ', ''],
            '同工异曲': ['唐代杰出的散文家韩愈。曾经担任过国子监博士。他学识渊博，讲起课来旁征博引，兼通百家，出口成章，妙语连珠，深受大学生们的欢迎。有一次，他写了一篇题为《进学解》的文章，来发泄自己才学极高却遭到贬斥的愤感情绪。一天早上，韩愈教导大学生们说：“学业由勤奋而精进，由嬉游而荒废；为人行事由深思远虑而获得成就，由因循、随便而道致毁败。如今圣上和群臣融洽相处，公正无私，有才能的人都得到了任用，谁说才多反而不被举用?”说到这里，大学生们哄堂大笑起来，有人站出来问道：“先生在骗人!弟子跟先生学了几年，深知先生终年苦学不倦，对待学业可称得上是非常勤奋。先生埋头于儒家典籍之中，玩味它的精华，然后写成文章，住处内充满了自己的著作。上取法学习于虞舜、夏禹时代的著述，《尚书》、《诗经》，下及《庄子》、《史记》以及西汉扬雄和司马相如的著作，它们各有特色，都是好文章，就像乐曲虽不同，都同样美妙动听。先生的文章内容丰富，语句洒脱畅达。先生的为人行事，也早巳由深思远虑而获得成就，但为什么自己常常弄得进退两难呢?”', ''],
            '投笔从戎': ['班超是东汉一个很有名气的将军，他从小就很用功，对未来也充满了理想。有一天，他正在抄写文件的时候，写着写着，突然觉得很闷，忍不住站起来，丢下笔说：“大丈夫应该像傅介子、张骞那样，在战场上立下功劳，怎么可以在这种抄抄写写的小事中浪费生命呢！”', ''],
            '投鼠忌器': ['三国初期，汉献帝与丞相曹操、皇叔刘备一起去打猎。曹操为了显示自己的武力，竟跟汉献帝齐头并进。汉南帝见不远处有只兔子，就叫刘备射，说是要看看皇叔的箭法。刘备连忙弯弓射箭，正好命中兔子，献帝连夸好箭法。南帝又看见一只大鹿，连射三箭不中，就叫曹操射。曹操拿过南帝的金比箭，一箭就射中了鹿。将士们见射中鹿的是金比箭，以为是献帝射的，都高呼万岁，曹操得意地站到献帝前接受欢呼。关云长实在看不下去，要拍马刀砍曹操，刘备忙暗示他不可轻举妄动。事后，关云长问刘备为什么不让杀曹操，他说：投鼠忌器，他身边还有献帝呢。投鼠忌器的意思是老鼠靠近器物，用东西砸老鼠又怕砸坏老鼠附近的用具。现常用来比喻做事有所顾忌，不敢放手进行。', ''],
            '图穷匕见': ['战国时，荆轲奉燕国太子丹的命令，以燕国的地图作为礼物献给秦王，匕首就藏在地图卷里，试图伺机刺杀秦王，但最后失败。《战国策？燕策三》：“轲既取图奉之，发图，图穷而匕首见。”', ''],
            '屠龙之技': ['有个人叫朱泙漫，他想学一种出奇的本领，听说支离本领”。', ''],
            '土崩瓦解': ['商纣王是商朝的末代君主，是一个暴虐无道的昏君。他贪恋酒色、荒淫无度，整日花天酒地，寻欢作乐，不理朝政。队从容关一直驻扎到蒲水。士兵不下数万，但打起仗来，因为兵士不愿意为纣王战死，所以“倒矢而射”把兵器扔在一边。商朝军队士气如此低落，商朝的政权自然是岌岌可危了。', ''],
            '兔死狗烹': ['越王句践大夫范蠡，曾经替越国出过了不少力，使得越国得以打败吴国，成为霸王。对越国来说，范蠡可是个大功臣，本来他是可以安享富贵的，但是范蠡却没有这么做，他宁愿舍弃荣华富贵，而自行引退，过着淡泊的生活。就在众人一片惋惜声中，范蠡又托人带了一封信给从前的同事大夫文种，他劝文种也舍弃功名富贵，以免招惹灾祸。范蠡为什么会这样劝文种呢？原来，他早就看出越王是个只能共患难，却不能共享乐的人，所以他在信中说道：“……飞鸟尽，良弓藏，狡兔死，走狗烹，……”，“兔死狗烹”就是从信中这几句话引申出来的。国，终于被杀，这就是“兔死狗烹”，也就是一般人所说的“有事就用你，无事就给你一个罪名”这句话。 ', ''],
            '退避三舍': ['春秋时候，晋献公听信谗言，杀了太子申生，又派人捉拿申生的弟弟重耳。重耳闻讯，逃出了晋国，在外流忘十几年。', ''],
            '脱颖而出': ['战国时，秦国攻打赵国。赵国平原君奉命到楚国求助，毛遂请求跟着去。平原君说：“有本事的人，在人群中，就如锥子放在布袋中，尖儿立刻露出来。你在我家已有三年，但我未听说过你的名字。看来你没有什么能耐，还是不要去了。”毛遂说：“若我真的能如锥子，放在布袋里，就会连锥子上面的环也露出，岂止只露出尖儿︰”后来毛遂就跟着去，并起了非常重要的作用。', ''],
            '外强中干': ['春秋时代的晋献公死后，晋公子夷吾结束逃亡生活，回到晋国继承王位当上了国君。很快就打到晋国的一个城镇，为了抵抗强大的秦军，晋惠公亲自领兵反抗。他下令拉战车的马，一定要用郑国的骏马。有位大臣看到，连忙对晋惠公说：郑国的马看起来虽然很强壮，但是实际上却很虚弱，打起仗来一紧张就会不听指挥。到那时，进退不得，大王还是不要做此决定吧！但是晋惠公一点都不愿意听大臣的劝告，果然，没多久晋惠公的马车就出不听指挥，而晋惠公一下就被秦军捉住，当了俘虏，晋国因此而大败。', ''],
            '完璧归赵': ['战国时代，赵王无意间得到了一块宝玉和氏璧，秦昭襄王听说后非常想要据为己有，因此就派人到赵国，对赵王说秦国愿意以十五个城与赵国交换这块玉。赵王心里非常舍不得，但是因为赵国国势很弱，因此不敢得罪秦王，怕秦王一不高兴，就派兵攻打赵国。为了这件事，赵王伤透了脑筋。', ''],
            '走马看花': ['唐朝中期，有位著名的诗人孟郊。他出身贫苦，从小勤奋好学，很有才华。但是，他的仕途却一直很不顺利，从青年到壮年，好几次参加进士考试都落了第。他虽然穷困潦倒，甚至连自己的家属都养不起，但他性情耿直，不肯走权贵之门。他决心刻苦攻读，用自己的真才实学，叩开仕途的大门。唐德宗贞元十三年(公元797年)，孟郊又赴京参加了一次进士考试，这次，他进士及第了，孟郊高兴极了。他穿上崭新的衣服，扎上彩带红花，骑着高头大马，在长安城里尽情地游览。京城美丽的景色使他赞叹，高中进士的喜悦又使他万分得意，于是，他写下了这首著名的《登科后》诗：昔日龌龃不足夸，今朝旷荡恩无涯；春风得意马蹄疾，一日看尽长安花。这首诗把诗人中了进士后的喜悦心情表现得淋漓尽致，其中“春风得意马蹄疾，一日看尽长安花”成为千古名句', '']
        }
        self.idiom_mean = [
            ['白手空拳', '形容手中一无所有。', ''],
            ['百般无赖', '采用所有卑鄙的方法。', ''],
            ['百川赴海', '百：表示多。川：江河。所有江河都流归大海。比喻众望所归或大势所趋。也比喻许多事物由分散而汇集到一处', ''],
            ['尺有所短', '比喻事物有其短处，并非在所有的情况下都是合适的。', ''],
            ['百川之主', '比喻事物有其短处，并非在所有的情况下都是合适的。', ''],
            ['赤贫如洗', '赤贫：穷得一无所有。形容极其贫穷。', ''],
            ['赤手光拳', '赤手：空手。两手空空，一无所有。比喻无任何凭借或一无所有。', ''],
            ['川泽纳污', '以湖泊江河能容纳各种水流的特性。比喻人有涵养，能包容所有的善恶、毁誉。', ''],
            ['垂磬之室', '磐：用石、玉制成的曲尺状打击乐器。像垂磬一样一无所有的房屋。形容十分贫困。', ''],
            ['殚财竭力', '殚、竭：尽。用尽所有的财力和人力。形容竭尽全力。', ''],
            ['凡百一新', '凡：全部；百：指事物多。所有的事物都有了新气象。', ''],
            ['分外之物', '自己名分之外的事物。指本不属于自己所有的东西，或薪俸外的收入。', ''],
            ['旮旮旯旯', '房屋、庭院、街道的所有角落及曲折隐蔽之处。', ''],
            ['盖世英雄', '盖世：压倒当世。超出当代所有的人。用以形容非常杰出的英雄人物。', ''],
            ['各行各业', '泛指所有的人所从事的各种行业。', ''],
            ['归了包堆', '所有的都包括在内，总共。', ''],
            ['环堵萧然', '环堵：围绕着四堵墙；萧然：萧条的样子。形容室中空无所有，极为贫困。', ''],
            ['黄帝子孙', '黄帝：古代传说中中华民族的共同祖先，姬姓，号轩辕氏、有熊氏。黄帝轩辕氏的子孙后代。指每个中国人或所有的中国人。', ''],
            ['浑身解数', '浑身：全身，指所有的；解数：那套数，指武艺。所有的本领，全部的权术手腕。', ''],
            ['浑俗和光', '浑俗：与世俗混同；和光：混合所有光彩。比喻不露锋芒，与世无争。也比喻无能，不中用。', ''],
            ['家道壁立', '家道：家庭经济情况；壁立：四立的墙壁。形容家贫如洗，一无所有，贫困到极点。', ''],
            ['家家户户', '每家每户。指所有的人家', ''],
            ['家徒壁立', '徒：只，仅仅。家里只有四面的墙壁。形容十分贫困，一无所有。', ''],
            ['家徒四壁', '徒：只，仅仅。家里只有四面的墙壁。形容十分贫困，一无所有。', ''],
            ['交口同声', '犹言众口一词。所有的人都说同样的话。', ''],
            ['竭忠尽智', '毫无保留地献出一片忠诚和所有才智。', ''],
            ['尽其所能', '能：能力。把所有本事都用上。', ''],
            ['尽人皆知', '尽：全部，所有。人人都知道。', ''],
            ['尽锐出战', '把所有的精锐部队派出作战。比喻派出了主力，用上了杀手锏。', ''],
            ['尽多尽少', '指尽其所有。', ''],
            ['九江八河', '泛指所有的江河。', ''],
            ['九州八极', '九州：中国古代地域共划分为九州；八极：九州之外最边远的地方。指天下所有远近的地区。', ''],
            ['居徒四壁', '徒：只，仅仅。家里只有四面的墙壁。形容十分贫困，一无所有。', ''],
            ['空空荡荡', '形容冷冷清清，空无所有的情景或指心里没着落的感觉', ''],
            ['空空洞洞', '空虚，空无所有。', ''],
            ['空空妙手', '指小偷。也形容手中一无所有。', ''],
            ['空空如也', '空空：诚恳，虚心。原形容诚恳、虚心的样子。现形容一无所有。', ''],
            ['空拳赤手', '赤手：空手。两手空空，一无所有。比喻无任何凭借或一无所有。', ''],
            ['连街倒巷', '犹言满街倾巷。指所有地方。', ''],
            ['两袖清风', '衣袖中除清风外，别无所有。比喻做官廉洁。也比喻穷得一无所有。', ''],
            ['掠人之美', '掠：夺取。夺取别人的成绩、荣誉归自己所有。', ''],
            ['妙手空空', '指小偷，也形容手中一无所有', ''],
            ['男女老少', '泛指所有的人。', ''],
            ['男女老幼', '泛指所有的人。', ''],
            ['普渡众生', '众生：指一切有生命的动物及人。佛教语。普遍引渡所有的人，使他们脱离苦海，登上彼岸。', ''],
            ['千人一状', '所有人都是一个面孔。比喻都是老一套，没有变化。', ''],
            ['倾囊相助', '囊：口袋。把衣袋里所有的钱都拿出来帮助别人。', ''],
            ['倾身营救', '比喻尽所有的力量设法去援救。', ''],
            ['倾注全力', '倾注：把精神或力量集中到一个目标。把所有力量集中在一个目标。', ''],
            ['清风两袖', '衣袖中除清风外，别无所有。比喻做官廉洁。也比喻穷得一无所有。', ''],
            ['穷山竭泽', '穷：寻求到尽头。寻遍所有的山与河。', ''],
            ['穷思毕精', '毕：尽。用尽所有的精力。', ''],
            ['人人皆知', '皆：都。所有的人都知道。', ''],
            ['扫锅刮灶', '指倾其所有。', ''],
            ['色即是空', '佛家语。指世家一切色法(物质)的本性(内在真实性)都是空无所有。', ''],
            ['身贫如洗', '穷得像死过似的，一无所有。', ''],
            ['十室九空', '室：人家。十家有九家一无所有。形容人民大量死亡或逃亡后的荒凉景象。', ''],
            ['食毛践土', '毛：指地面所生之谷物；贱：踩。原意是吃的食物和居住的土地都是国君所有。封建官吏用以表示感戴君主的恩德。', ''],
            ['世人皆知', '世人：所有人。指很多人都知道。', ''],
            ['水净鹅飞', '比喻人财两失，一无所有。亦比喻民穷财尽。', ''],
            ['通上彻下', '①指从天到地。②从上到下。指所有的人。', ''],
            ['投鞭断流', '把所有的马鞭投到江里，就能截断水流。比喻人马众多，兵力强大。', ''],
            ['万马齐喑', '喑：哑。所有的马都沉寂无声。旧时形容人民不敢讲话。现也比喻沉闷的政治局面。', ''],
            ['万能钥匙', '指能打开所有锁的钥匙。比喻解决一切困难的办法。', ''],
            ['万念俱灰', '所有的想法和打算都破灭了。形容极端灰心失望的心情。', ''],
            ['万念俱寂', '俱：全部。所有的欲望、打算都消失了。', ''],
            ['万物一府', '府：收藏财物的地方。所有的财物收藏在一起。指事物一体，无所分别。', ''],
            ['万物之情', '所有事物的情状。', ''],
            ['万象澄澈', '澄、澈：水清。万物都澄静清澈。形容月夜所有的景物澄静而清澈。', ''],
            ['小惠未遍', '惠：恩惠；遍：普遍。一点小的恩惠，不能使所有的人都得到。', ''],
            ['心心念念', '心心：指所有的心思；念念：指所有的念头。心里老是想着。指想做某件事或得到某种东西。', ''],
            ['一称心力', '一：全；称：相符合；必力：运用心思的能力。所有都跟自己所设想的心思相合。', ''],
            ['一辞同轨', '犹众口一词。所有的人都说同样的话。', ''],
            ['一家一火', '指所有家当什物。', ''],
            ['一览无遗', '览：看；遗：遗留。一眼看去，所有的景物全看见了。形容建筑物的结构没有曲折变化，或诗文内容平淡，没有回味。', ''],
            ['一览无余', '览：看；余：剩余。一眼看去，所有的景物全看见了。形容建筑物的结构没有曲折变化，或诗文内容平淡，没有回味。', ''],
            ['一切万物', '宇宙间所有的事物。', ''],
            ['英才盖世', '才：才能；盖世：压倒当世，超出世上所有的。形容超出当代、无与伦比的才能。', ''],
            ['有口皆碑', '碑：指记功碑。所有人的嘴都是活的记功碑。比喻人人称赞。', ''],
            ['占为己有', '将不是自己的东西占为自己所有。', ''],
            ['终成泡影', '结果一场空，一无所有。', ''],
            ['占为己有', '将不是自己的东西占为自己所有。', ''],
            ['众口难调', '调：协调。原意是各人的口味不同，很难做出一种饭菜使所有的人都感到好吃。比喻做事很难让所有的人都满意。', ''],
            ['众口一词', '所有的人都说同样的话。', ''],
            ['众目共睹', '所有人的眼睛都看到了。形容非常明显。亦作“众目共视”、“众目具瞻”。', ''],
            ['众目共视', '所有人的眼睛都看到了。形容非常明显。同“众目共睹”。', ''],
            ['众啄同音', '犹众口一词。所有的人都说同样的话。', ''],
            ['诸亲好友', '总称所有亲友。', ''],
            ['逐兔先得', '逐：追逐。指众人追野兔，谁先得到就归谁所有。', ''],
            ['杼柚空虚', '形容生产废弛，贫无所有。', ''],
            ['一览全收', '览：看。一眼看去，所有的景物全看见了。形容建筑物的结构没有曲折变化，或诗文内容平淡，没有回味。', '']
        ]
        self.idiom = [
            '水漫金山', '重蹈覆辙', '行尸走肉', '金蝉脱壳', '百里挑一', '金玉满堂', '愚公移山', '魑魅魍魉', '背水一战', '霸王别姬',
            '天上人间', '不吐不快', '海阔天空', '情非得已', '满腹经纶', '兵临城下', '气味相投', '投鼠忌器', '屋乌之爱', '爱莫能助',
            '春暖花开', '插翅难逃', '黄道吉日', '天下无双', '偷天换日', '两小无猜', '卧虎藏龙', '珠光宝气', '簪缨世族', '花花公子',
            '绘声绘影', '国色天香', '相亲相爱', '八仙过海', '金玉良缘', '掌上明珠', '淫词艳曲', '曲终奏雅', '德高望重', '重蹈覆辙',
            '皆大欢喜', '生财有道', '极乐世界', '情不自禁', '龙生九子', '精卫填海', '海市蜃楼', '高山流水', '卧薪尝胆', '壮志凌云',
            '否极泰来', '金枝玉叶', '囊中羞涩', '霸王之资', '蠢若木鸡', '蠢头蠢脑', '清夜扪心', '心织笔耕', '离弦走板', '板上钉钉',
            '露头露脸', '巍然不动', '巍然耸立', '巍然挺立', '攀高枝儿', '蹦蹦跳跳', '翻风滚雨', '翻来复去', '翻脸无情', '翻然改悔',
            '翻手为云', '邋邋遢遢', '懵里懵懂', '懵里懵懂', '嚣浮轻巧', '鹰派人物', '耕当问奴', '奴颜婢膝', '膝痒搔背', '背信弃义',
            '胸有成竹', '竹报平安', '安富尊荣', '荣华富贵', '贵而贱目', '目无余子', '子虚乌有', '有目共睹', '睹物思人', '人中骐骥',
            '骥子龙文', '文质彬彬', '彬彬有礼', '礼贤下士', '士饱马腾', '腾云驾雾', '源源不绝', '绝甘分少', '少不经事', '美意延年',
            '雾里看花', '花言巧语', '语重心长', '长此以往', '往返徒劳', '劳而无功', '功成不居', '居官守法', '法外施仁', '仁浆义粟',
            '粟红贯朽', '朽木死灰', '灰飞烟灭', '灭绝人性', '性命交关', '关门大吉', '吉祥止止', '止于至善', '善贾而沽', '沽名钓誉',
            '象箸玉杯', '杯弓蛇影', '影影绰绰', '绰约多姿', '姿意妄为', '为人作嫁', '嫁祸于人', '人情冷暖', '暖衣饱食', '食不果腹',
            '腹背之毛', '毛手毛脚', '脚踏实地', '地老天荒', '荒诞不经', '经纬万端', '端倪可察', '察言观色', '色若死灰', '灰头土面',
            '面有菜色', '色授魂与', '面面俱到', '与民更始', '美人迟暮', '暮云春树', '树大招风', '怜香惜玉', '义无反顾', '顾全大局',
            '始乱终弃', '弃瑕录用', '用舍行藏', '藏垢纳污', '污泥浊水', '水乳交融', '融会贯通', '通宵达旦', '旦种暮成', '成人之美',
            '风中之烛', '烛照数计', '计日程功', '功德无量', '量才录用', '用行舍藏', '藏头露尾', '尾大不掉', '掉以轻心', '心急如焚',
            '焚琴煮鹤', '鹤发童颜', '颜面扫地', '地上天官', '官逼民反', '反裘负刍', '刍荛之见', '见微知著', '著作等身', '局促不安',
            '身强力壮', '壮志凌云', '云消雨散', '散兵游勇', '勇猛精进', '进退失据', '据理力争', '争长论短', '短小精悍', '悍然不顾',
            '浆酒霍肉', '肉薄骨并', '并行不悖', '悖入悖出', '出奇制胜', '胜任愉快', '快马加鞭', '鞭辟入里', '里出外进', '进寸退尺',
            '尺寸可取', '取巧图便', '便宜行事', '顾影自怜', '怜香惜玉', '玉液琼浆', '誉不绝口', '口蜜腹剑', '剑戟森森', '森罗万象',
            '事与愿违', '违心之论', '论功行赏', '赏心悦目', '目光如豆', '华而不实', '豆蔻年华', '是古非今', '今愁古恨', '恨之入骨',
            '理屈词穷', '委曲求全', '全力以赴', '穷原竟委', '赴汤蹈火', '火烧眉毛', '燎原烈火', '毛羽零落', '落井下石', '石破天惊',
            '惊惶失措', '惊惶失措', '如运诸掌', '掌上明珠', '珠沉玉碎', '碎琼乱玉', '报冰公事', '事预则立', '立身处世', '世外桃源',
            '玉碎珠沉', '沉滓泛起', '起早贪黑', '黑更半夜', '夜雨对床', '床头金尽', '尽态极妍', '妍姿艳质', '质疑问难', '难以为继',
            '继往开来', '来龙去脉', '脉脉含情', '情见势屈', '屈打成招', '招摇过市', '招摇过市', '徒劳往返', '返老还童', '童牛角马',
            '马首是瞻', '瞻前顾后', '后顾之忧', '忧国奉公', '远见卓识', '识文断字', '字斟句酌', '酌盈剂虚', '表里如一', '一呼百诺',
            '公子王孙', '孙康映雪', '雪上加霜', '霜露之病', '病病歪歪', '歪打正着', '着手成春', '春蚓秋蛇', '蛇口蜂针', '针锋相对',
            '对薄公堂', '堂堂正正', '正中下怀', '怀璧其罪', '罪大恶极', '极天际地','地丑德齐', '齐心协力', '力不胜任', '任重道远',
            '虚舟飘瓦', '瓦釜雷鸣', '鸣锣开道', '道不拾遗', '遗大投艰', '艰苦朴素', '素丝羔羊', '羊肠小道', '说长道短', '短兵相接',
            '接踵而至', '至死不变', '变本加厉', '厉行节约', '约定俗成', '成仁取义', '义形于色', '色色俱全', '全军覆灭', '灭此朝食',
            '食日万钱', '钱可通神', '神施鬼设', '设身处地', '跃跃欲试', '骨腾肉飞', '飞沿走壁', '壁垒森严', '待理不理',
            '受宠若惊', '惊涛骇浪', '浪子回头', '头疼脑热', '热火朝天', '天高地厚', '厚貌深情', '情同骨肉',
            '肉眼惠眉', '眉来眼去', '去伪存真', '真脏实犯', '犯上作乱', '乱头粗服', '分寸之末', '末学肤受',
            '服低做小', '小试锋芒', '芒刺在背', '背井离乡', '乡壁虚造', '造化小儿', '儿女情长', '长歌当哭',
            '断鹤续凫', '凫趋雀跃', '跃然纸上', '上树拔梯', '梯山航海', '海枯石烂', '烂若披锦', '锦绣前程',
            '程门立雪', '雪虐风饕', '饕餮之徒', '徒劳无功', '功败垂成', '成千上万', '哭天抹泪', '泪干肠断',
            '万象森罗', '罗雀掘鼠', '鼠窃狗盗', '盗憎主人', '人莫予毒', '毒手尊前', '前因后果', '果于自信',
            '罪恶昭彰', '彰善瘅恶', '恶贯满盈', '盈科后进', '进退两难', '难分难解', '解甲归田', '田月桑时',
            '时和年丰', '丰取刻与', '与世偃仰', '仰人鼻息', '息息相通', '通权达变', '信赏必罚', '罚不当罪',
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
            '井中视星', '星旗电戟', '戟指怒目', '目指气使', '使羊将狼', '狼心狗肺', '肺石风清',
            '安步当车', '车载斗量', '量才而为', '为渊驱鱼', '鱼游釜中', '中馈犹虚', '虚有其表',
            '诺诺连声', '声罪致讨', '讨价还价', '价增一顾', '顾盼自雄', '雄心壮志', '志美行厉',
            '厉兵秣马', '厉兵秣马', '速战速决', '决一雌雄', '雄才大略', '略见一斑', '斑驳陆离',
            '钉嘴铁舌', '舌桥不下', '下马看花', '花样翻新', '新陈代谢', '谢天谢地', '地久天长',
            '长枕大被', '被山带河', '油腔滑调', '调兵遣将', '将伯之助', '助人为乐', '乐而不淫',
            '雅俗共赏', '赏罚分明', '明刑不戮', '戮力同心', '心心相印', '印累绶若', '若有所失',
            '失张失智', '智圆行方', '方枘圆凿', '凿凿有据', '据为己有', '有眼无珠', '珠光宝气',
            '器宇轩昂', '昂首阔步', '步履维艰', '艰苦卓绝', '绝少分甘', '甘雨随车', '车水马龙',
            '龙飞凤舞', '舞衫歌扇', '扇枕温被', '被发缨冠', '冠冕堂皇', '皇天后土', '土阶茅屋',
            '助我张目', '目挑心招', '发凡起例', '事必躬亲', '亲如骨肉', '肉跳心惊', '惊弓之鸟',
            '鸟枪换炮', '龙蛇飞动', '动人心弦', '弦外之音', '音容笑貌', '貌合心离', '离心离德',
            '辙乱旗靡', '靡靡之音', '音容宛在', '在所难免', '免开尊口', '口耳之学', '学而不厌',
            '厌难折冲', '冲口而出', '出谷迁乔', '乔龙画虎', '虎踞龙盘', '盘马弯弓', '弓折刀尽', '尽善尽美',
            '年高望重', '重温旧梦', '梦寐以求', '求全之毁', '毁家纾难', '难言之隐', '隐恶扬善',
            '善始善终', '终南捷径', '径情直行', '行成于思', '思潮起伏', '伏低做小', '小恩小惠', '惠而不费', '费尽心机',
            '机关算尽', '尽忠报国', '国士无双', '双宿双飞', '飞灾横祸', '祸从天降', '降格以求',
            '求同存异', '异名同实', '实至名归', '归真反璞', '璞玉浑金', '金玉锦绣', '绣花枕头', '头没杯案', '案牍劳形',
            '舌锋如火', '火伞高张', '张冠李戴', '戴月披星', '星移斗转', '转祸为福', '福至心灵',
            '灵丹圣药', '药笼中物', '物以类聚', '聚蚊成雷', '雷厉风行', '行将就木', '木本水源', '源源不断', '断烂朝报',
            '事不师古', '兵连祸结', '结结巴巴', '巴三览四', '四面楚歌', '歌功颂德', '德厚流光', '光阴似箭', '箭在弦上',
            '上好下甚', '甚嚣尘上', '上下交困', '困知勉行', '行若无事', '事倍功半', '半夜三更',
            '更仆难数', '数见不鲜', '鲜车怒马', '马革裹尸', '尸居余气', '气冲牛斗', '斗筲之器', '盈盈一水', '水陆杂陈',
            '陈规陋习', '习焉不察', '察察为明', '明知故问', '问道于盲', '盲人摸象', '象齿焚身',
            '身不由主', '主客颠倒', '倒凤颠鸾', '鸾翔凤集', '集苑集枯', '枯木逢春', '春山如笑', '笑里藏刀', '刀山火海',
            '海外奇谈', '谈笑封侯', '侯门如海', '海阔天空', '空室清野', '野草闲花', '花颜月貌', '破颜微笑', '忘乎所以',
            '貌合神离', '离乡背井', '井蛙之见', '见仁见智', '智勇双全', '全受全归', '归马放牛', '牛骥同皂', '皂白不分',
            '分香卖履', '履舄交错', '错彩镂金', '金城汤池', '池鱼之殃', '殃及池鱼', '鱼烂而亡', '亡羊补牢', '牢不可破',
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
            '以指挠沸', '沸反盈天', '天上石麟', '麟趾呈祥', '祥麟威凤', '凤凰来仪', '仪静体闲', '闲云野鹤', '鹤发鸡皮',
            '皮里春秋', '秋风过耳', '耳食之谈', '谈笑自若', '谈笑自若', '若明若暗', '暗气暗恼', '恼羞成怒', '怒目而视', '视民如伤',
            '伤弓之鸟', '鸟语花香', '香花供养', '养痈成患', '患难与共', '共枝别干', '干卿底事', '事出有因', '因敌取资',
            '资深望重', '重睹天日', '日上三竿', '竿头直上', '上援下推', '推襟送抱', '抱蔓摘瓜', '绝处逢生', '多才多艺',
            '腾蛟起凤', '历历可数', '数白论黄', '黄袍加身', '身外之物', '物换星移', '移樽就教', '教学相长', '长年累月',
            '月晕而风', '风流倜傥', '傥来之物', '物是人非', '非池中物', '物极必返', '反经行权', '权宜之计', '计出万全', '全无心肝', '肝肠寸断', '深恶痛绝',
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
        bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/d794e4f2-b2d5-4302-c42d-f34781a54abf/%E8%92%B2%E5%85%AC%E8%8B%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-22T04%3A58%3A51Z%2F-1%2F%2Fd5bb19cee3e1245f859866dfbd810f2353636fa3d1ca6e93f6a210bcc152f8a3')
        bodyTemplate.setPlainTextContent(r'欢迎来到蒲公英，在这里，您可以跟我一起学习英语，也可以跟我互斗成语！试着对我说，我怎么跟你玩')
        bodyTemplate.set_title('蒲公英')

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
        self.waitAnswer()
        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage(
            'http://dbp-resource.gz.bcebos.com/d794e4f2-b2d5-4302-c42d-f34781a54abf/%E8%92%B2%E5%85%AC%E8%8B%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-22T04%3A58%3A51Z%2F-1%2F%2Fd5bb19cee3e1245f859866dfbd810f2353636fa3d1ca6e93f6a210bcc152f8a3')
        bodyTemplate.setPlainTextContent(r'使用手册：我们这里有成语接龙、猜成语，也有英语故事、成语故事、英语笑话，还有英语电影推荐和学习英语单词与短语，快来一起吧')
        bodyTemplate.set_title('蒲公英使用介绍')

        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'使用手册：我们这里有成语接龙、猜成语，也有英语故事、成语故事、英语笑话，还有英语电影推荐和学习英语单词与短语，快来一起吧'
        }

    def start_IdiomC(self):

        """
        成语接龙
        :return:
        """
        self.waitAnswer()
        rand_id = random.randint(0, 1100)
        idiom = self.idiom
        give_idiom = idiom[rand_id]

        self.setSessionAttribute("answer", give_idiom[-1], 0)
        self.setSessionAttribute("give_idiom", give_idiom, 0)
        self.setSessionAttribute("game_type", 'IdiomC', 0)
        self.setSessionAttribute("round_num", 1, 1)

        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage('://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
        bodyTemplate.setPlainTextContent(r'我先来，我出：' + give_idiom)
        bodyTemplate.set_title(r'第一关')

        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'我先来，我出' + give_idiom
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
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' + '：' + idiom_story + '，，，还想再听一遍吗，试着对我说：再来一遍')
            bodyTemplate.set_title(user_story)

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story + '，，，，' + idiom_story + '，，，还想再听一遍吗，试着对我说，再来一遍'
            }
        else:
            idiom_story = self.idiom_story[user_story][0]

            self.setSessionAttribute("idiom_story_name", user_story, 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage(self.idiom_story[user_story][1])
            bodyTemplate.setPlainTextContent(r'好的，我们来听：' + user_story +  '：' + idiom_story + '还想再听一遍吗，试着对我说：再来一遍')
            bodyTemplate.set_title(user_story)

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好的，我们来听：' + user_story +  '，，，，' + idiom_story + '还想再听一遍吗，试着对我说，再来一遍'
            }

    def start_IdiomGuess(self):

        """
        猜成语
        :return:
        """
        self.waitAnswer()
        mode = self.getSlots('guess_mode')

        if mode == 'blank':

            rand_id = random.randint(0, 1100)
            rand_ids = random.randint(0, 3)
            answer = self.idiom[rand_id]
            give_idiom = answer.replace(answer[rand_ids] + answer[rand_ids + 1], '*')
            self.setSessionAttribute("real_answer", answer, 0)
            self.setSessionAttribute("give_idiom", give_idiom, '')
            self.setSessionAttribute("game_type", 'IdiomGuessBlank', 0)
            self.setSessionAttribute("guan_num", 1, 1)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
            bodyTemplate.setPlainTextContent(r'诶呀！我吃掉了成语的一部分，快来帮我还原吧!   ' + give_idiom)
            bodyTemplate.set_title(r'第一关')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'诶呀！我吃掉了成语的一部分，快来帮我还原吧!   ' + give_idiom
            }
        elif mode == 'means':

            rand_id = random.randint(0, 20)
            ask = self.idiom_mean[rand_id][1]
            self.setSessionAttribute("idiom_means_num", rand_id, 0)
            self.setSessionAttribute("game_type", 'IdiomStoryMeans', 0)

            bodyTemplate = BodyTemplate1()
            bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/530c5773-9c9b-671c-6212-4af927f1455a/%E6%8A%80%E8%83%BD%E5%BC%80%E5%A7%8B%E9%A1%B5%E8%83%8C%E6%99%AF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-07T04%3A26%3A33Z%2F-1%2F%2F5cca0655decbf96a8b6a6d2602d240e4a7376df72228e3d404f218c603949e42')
            bodyTemplate.setPlainTextContent(r'好啊，这个是哪个成语的意思呢：' + ask)
            bodyTemplate.set_title(r'第一关')

            directive = RenderTemplate(bodyTemplate)
            return {
                'directives': [directive],
                'outputSpeech': r'好啊，这个是哪个成语的意思呢，，，，' + ask
            }
        elif not mode:
            self.nlu.ask('guess_mode')

    def tell_english_story(self):

        """
        英语故事
        :return:
        """
        self.setSessionAttribute("game_type", 'EnglishStory', 0)

    def tell_english_joke(self):

        """
        英语笑话
        :return:
        """
        self.setSessionAttribute("game_type", 'EnglishJoke', 0)

    def study_english_word(self):

        """
        学习英语单词
        :return:
        """
        self.setSessionAttribute("game_type", 'EnglishWord', 0)

    def english_songs(self):

        """
        英语歌曲
        :return:
        """
        self.setSessionAttribute("game_type", 'EnglishSong', 0)

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

    def next_one(self):

        """
        下一个
        :return:
        """
        pass

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
                    'outputSpeech': r'您说的我没有理解，对不起，您可以对我说，使用手册'
                }
            else:
                if len(text) == 4:
                    return {
                        'outputSpeech': r'您说的我没有理解，对不起，您可以对我说，使用手册'
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
                        'outputSpeech': r'您说的我没有理解，对不起，您可以对我说，使用手册'
                    }
