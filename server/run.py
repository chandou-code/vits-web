import math

from flask import Flask, request, send_file, render_template
import sqlite3
import time
import requests

import io

app = Flask(__name__)


def ban(ip):
    banned_ips = ['182.127.10.131', '117.50.33.44', '117.50.33.6', '116.198.10.48', '39.171.193.37']
    if ip in banned_ips:
        return True


def disguise_ip(ip):
    # print(f'进入ip{ip}')
    affections = ['111.58.90.211', '111.58.91.80', '117.136.99.181']
    if ip in affections:
        # print('ip隐藏')
        return '183.178.60.221'
    else:
        return ip


def get_speaker():
    with open('speaker.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    decoded_string = content.encode().decode('unicode_escape')
    result_list = eval(decoded_string)
    return result_list


def role2id(role):
    speaker = get_speaker()
    import re
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        name = re.sub(pattern, "", speaker[e], re.S)
        if name != speaker[e]:
            speaker[e] = name
    for s in range(len(speaker)):
        if role == speaker[s]:
            return s


def id2role(id):
    import re
    speaker = get_speaker()
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        speaker[e] = re.sub(pattern, "", speaker[e], re.S)
    return speaker[int(id)]


# def get_random():
#     import random
#     import time
#     now_seconds = int(time.time())  # 秒
#     now_minute = int(now_seconds / 60)  # 分
#     now_ten_minute = int(now_minute / 10)
#     random.seed(now_ten_minute)
#     random_num1 = random.randint(87, 147)
#     random_num2 = random.randint(87, 147)
#     return random_num1, random_num2, now_ten_minute


def save_it2(client_ip, speak_text, id_speaker, url):
    local_time = time.localtime(time.time())

    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    formatted_time = formatted_time.replace('\n ', '').replace('\n', '')
    # print(formatted_time)
    # with open('log.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # if lines:
    #
    #     last_line = lines[-1].strip()  # 获取最后一行数据
    #     last_data = last_line.split('|')[0] if '|' in last_line else ''
    # else:
    #     last_data = ''
    #
    # if last_data != f'{client_ip},{speak_text},{id2role(id_speaker)}':
    #     # print('添加')
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f'{formatted_time}|{client_ip} |{speak_text}|----------{url}|{id2role(id_speaker)}\n')


def get_location(ip):
    url = f'https://res.abeim.cn/api-ip_info?ip={ip}'
    r = requests.get(url)
    data = r.json()['data']
    ip_pos = data['ip_pos']
    ip_isp = data['ip_isp']
    end = f'{ip_pos}{ip_isp}{ip}'
    return end


@app.errorhandler(404)
def page_not_found(error=None):
    # 自定义的 404 错误处理函数
    return '404 Not Found', 404


def show_table():
    import sqlite3

    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 查询表中的所有数据
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()

    # 打印查询结果

    # 关闭数据库连接
    conn.close()
    return rows


def inner_text(client_ip, speak_text, id_speaker, url):
    import time
    local_time = time.localtime(time.time())

    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    # 连接到数据库
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 插入数据
    time = formatted_time
    location = client_ip
    text = speak_text
    url = url
    speaker = id2role(id_speaker)

    cursor.execute("INSERT INTO records (time, location, text, url, speaker) VALUES (?, ?, ?, ?, ?)",
                   (time, location, text, url, speaker))

    # 提交更改
    conn.commit()

    # 关闭数据库连接
    conn.close()

@app.route('/models',methods=['GET'])
def get_models():
    models = {0: '特别周', 1: '无声铃鹿', 2: '东海帝皇（帝宝，帝王）', 3: '丸善斯基', 4: '富士奇迹', 5: '小栗帽',
              6: '黄金船',
              7: '伏特加', 8: '大和赤骥', 9: '大树快车', 10: '草上飞', 11: '菱亚马逊', 12: '目白麦昆', 13: '神鹰',
              14: '好歌剧', 15: '成田白仁', 16: '鲁道夫象征（皇帝）', 17: '气槽', 18: '爱丽数码', 19: '星云天空',
              20: '玉藻十字', 21: '美妙姿势', 22: '琵琶晨光', 23: '摩耶重炮', 24: '曼城茶座', 25: '美浦波旁',
              26: '目白赖恩', 27: '菱曙', 28: '雪中美人', 29: '米浴', 30: '艾尼斯风神', 31: '爱丽速子（爱丽快子）',
              32: '爱慕织姬', 33: '稻荷一', 34: '胜利奖券', 35: '空中神宫', 36: '荣进闪耀', 37: '真机伶',
              38: '川上公主',
              39: '黄金城（黄金城市）', 40: '樱花进王', 41: '采珠', 42: '新光风', 43: '东商变革', 44: '超级小海湾',
              45: '醒目飞鹰（寄寄子）', 46: '荒漠英雄', 47: '东瀛佐敦', 48: '中山庆典', 49: '成田大进', 50: '西野花',
              51: '春丽（乌拉拉）', 52: '青竹回忆', 53: '微光飞驹', 54: '美丽周日', 55: '待兼福来', 56: 'mr cb（cb先生）',
              57: '名将怒涛（名将户仁）', 58: '目白多伯', 59: '优秀素质', 60: '帝王光辉', 61: '待兼诗歌剧',
              62: '生野狄杜斯',
              63: '目白善信', 64: '大拓太阳神', 65: '双涡轮（两立直，两喷射，二锅头，逆喷射）', 66: '里见光钻（萨托诺金刚石）',
              67: '北部玄驹', 68: '樱花千代王', 69: '天狼星象征', 70: '目白阿尔丹', 71: '八重无敌', 72: '鹤丸刚志',
              73: '目白光明', 74: '成田拜仁（成田路）', 75: '也文摄辉', 76: '小林历奇', 77: '北港火山', 78: '奇锐骏',
              79: '苦涩糖霜', 80: '小小蚕茧', 81: '骏川手纲（绿帽恶魔）', 82: '秋川弥生（小小理事长）',
              83: '乙名史悦子（乙名记者）', 84: '桐生院葵', 85: '安心泽刺刺美', 86: '樫本理子', 87: '神里绫华（龟龟）',
              88: '琴', 89: '空（空哥）', 90: '丽莎', 91: '荧（荧妹）', 92: '芭芭拉', 93: '凯亚', 94: '迪卢克', 95: '雷泽',
              96: '安柏', 97: '温迪', 98: '香菱', 99: '北斗', 100: '行秋', 101: '魈', 102: '凝光', 103: '可莉',
              104: '钟离',
              105: '菲谢尔（皇女）', 106: '班尼特', 107: '达达利亚（公子）', 108: '诺艾尔（女仆）', 109: '七七', 110: '重云',
              111: '甘雨（椰羊）', 112: '阿贝多', 113: '迪奥娜（猫猫）', 114: '莫娜', 115: '刻晴', 116: '砂糖', 117: '辛焱',
              118: '罗莎莉亚', 119: '胡桃', 120: '枫原万叶（万叶）', 121: '烟绯', 122: '宵宫', 123: '托马', 124: '优菈',
              125: '雷电将军（雷神）', 126: '早柚', 127: '珊瑚宫心海（心海，扣扣米）', 128: '五郎', 129: '九条裟罗',
              130: '荒泷一斗（一斗）', 131: '埃洛伊', 132: '申鹤', 133: '八重神子（神子）', 134: '神里绫人（绫人）',
              135: '夜兰',
              136: '久岐忍', 137: '鹿野苑平藏', 138: '提纳里', 139: '柯莱', 140: '多莉', 141: '云堇',
              142: '纳西妲（草神）',
              143: '深渊使徒', 144: '妮露', 145: '赛诺', 146: '债务处理人', 147: '坎蒂丝', 148: '真弓快车', 149: '秋人',
              150: '望族', 151: '艾尔菲', 152: '艾莉丝', 153: '艾伦', 154: '阿洛瓦', 155: '天野', 156: '天目十五',
              157: '愚人众-安德烈', 158: '安顺', 159: '安西', 160: '葵', 161: '青木', 162: '荒川幸次', 163: '荒谷',
              164: '有泽', 165: '浅川', 166: '麻美', 167: '凝光助手', 168: '阿托', 169: '竺子', 170: '百识',
              171: '百闻',
              172: '百晓', 173: '白术', 174: '贝雅特丽奇', 175: '丽塔', 176: '失落迷迭', 177: '缭乱星棘', 178: '伊甸',
              179: '伏特加女孩', 180: '狂热蓝调', 181: '莉莉娅', 182: '萝莎莉娅', 183: '八重樱', 184: '八重霞',
              185: '卡莲',
              186: '第六夜想曲', 187: '卡萝尔', 188: '姬子', 189: '极地战刃', 190: '布洛妮娅', 191: '次生银翼',
              192: '理之律者%26希儿', 193: '理之律者', 194: '迷城骇兔', 195: '希儿', 196: '魇夜星渊', 197: '黑希儿',
              198: '帕朵菲莉丝', 199: '不灭星锚', 200: '天元骑英', 201: '幽兰黛尔', 202: '派蒙bh3', 203: '爱酱',
              204: '绯玉丸', 205: '德丽莎', 206: '月下初拥', 207: '朔夜观星', 208: '暮光骑士', 209: '格蕾修',
              210: '留云借风真君', 211: '梅比乌斯', 212: '仿犹大', 213: '克莱因', 214: '圣剑幽兰黛尔', 215: '妖精爱莉',
              216: '特斯拉zero', 217: '苍玄', 218: '若水', 219: '西琳', 220: '戴因斯雷布', 221: '贝拉', 222: '赤鸢',
              223: '镇魂歌', 224: '渡鸦', 225: '人之律者', 226: '爱莉希雅', 227: '天穹游侠', 228: '琪亚娜',
              229: '空之律者',
              230: '薪炎之律者', 231: '云墨丹心', 232: '符华', 233: '识之律者', 234: '特瓦林', 235: '维尔薇',
              236: '芽衣',
              237: '雷之律者', 238: '断罪影舞', 239: '阿波尼亚', 240: '榎本', 241: '厄尼斯特', 242: '恶龙',
              243: '范二爷',
              244: '法拉', 245: '愚人众士兵', 246: '愚人众士兵a', 247: '愚人众士兵b', 248: '愚人众士兵c',
              249: '愚人众a',
              250: '愚人众b', 251: '飞飞', 252: '菲利克斯', 253: '女性跟随者', 254: '逢岩', 255: '摆渡人',
              256: '狂躁的男人', 257: '奥兹', 258: '芙萝拉', 259: '跟随者', 260: '蜜汁生物', 261: '黄麻子', 262: '渊上',
              263: '藤木', 264: '深见', 265: '福本', 266: '芙蓉', 267: '古泽', 268: '古田', 269: '古山', 270: '古谷昇',
              271: '傅三儿', 272: '高老六', 273: '矿工冒', 274: '元太', 275: '德安公', 276: '茂才公', 277: '杰拉德',
              278: '葛罗丽', 279: '金忽律', 280: '公俊', 281: '锅巴', 282: '歌德', 283: '阿豪', 284: '狗三儿',
              285: '葛瑞丝', 286: '若心', 287: '阿山婆', 288: '怪鸟', 289: '广竹', 290: '观海', 291: '关宏',
              292: '蜜汁卫兵', 293: '守卫1', 294: '傲慢的守卫', 295: '害怕的守卫', 296: '贵安', 297: '盖伊',
              298: '阿创',
              299: '哈夫丹', 300: '日语阿贝多（野岛健儿）', 301: '日语埃洛伊（高垣彩阳）', 302: '日语安柏（石见舞菜香）',
              303: '日语神里绫华（早见沙织）', 304: '日语神里绫人（石田彰）', 305: '日语白术（游佐浩二）',
              306: '日语芭芭拉（鬼头明里）', 307: '日语北斗（小清水亚美）', 308: '日语班尼特（逢坂良太）',
              309: '日语坎蒂丝（柚木凉香）', 310: '日语重云（齐藤壮马）', 311: '日语柯莱（前川凉子）',
              312: '日语赛诺（入野自由）',
              313: '日语戴因斯雷布（津田健次郎）', 314: '日语迪卢克（小野贤章）', 315: '日语迪奥娜（井泽诗织）',
              316: '日语多莉（金田朋子）', 317: '日语优菈（佐藤利奈）', 318: '日语菲谢尔（内田真礼）',
              319: '日语甘雨（上田丽奈）',
              320: '日语（畠中祐）', 321: '日语鹿野院平藏（井口祐一）', 322: '日语空（堀江瞬）', 323: '日语荧（悠木碧）',
              324: '日语胡桃（高桥李依）', 325: '日语一斗（西川贵教）', 326: '日语凯亚（鸟海浩辅）',
              327: '日语万叶（岛崎信长）',
              328: '日语刻晴（喜多村英梨）', 329: '日语可莉（久野美咲）', 330: '日语心海（三森铃子）',
              331: '日语九条裟罗（濑户麻沙美）', 332: '日语丽莎（田中理惠）', 333: '日语莫娜（小原好美）',
              334: '日语纳西妲（田村由加莉）', 335: '日语妮露（金元寿子）', 336: '日语凝光（大原沙耶香）',
              337: '日语诺艾尔（高尾奏音）', 338: '日语奥兹（增谷康纪）', 339: '日语派蒙（古贺葵）', 340: '日语琴（斋藤千和）',
              341: '日语七七（田村由加莉）', 342: '日语雷电将军（泽城美雪）', 343: '日语雷泽（内山昂辉）',
              344: '日语罗莎莉亚（加隈亚衣）', 345: '日语早柚（洲崎绫）', 346: '日语散兵（柿原彻也）',
              347: '日语申鹤（川澄绫子）',
              348: '日语久岐忍（水桥香织）', 349: '日语女士（庄子裕衣）', 350: '日语砂糖（藤田茜）',
              351: '日语达达利亚（木村良平）', 352: '日语托马（森田成一）', 353: '日语提纳里（小林沙苗）',
              354: '日语温迪（村濑步）', 355: '日语香菱（小泽亚李）', 356: '日语魈（松冈祯丞）', 357: '日语行秋（皆川纯子）',
              358: '日语辛焱（高桥智秋）', 359: '日语八重神子（佐仓绫音）', 360: '日语烟绯（花守由美里）',
              361: '日语夜兰（远藤绫）', 362: '日语宵宫（植田佳奈）', 363: '日语云堇（小岩井小鸟）',
              364: '日语钟离（前野智昭）',
              365: '杰克', 366: '阿吉', 367: '江舟', 368: '鉴秋', 369: '嘉义', 370: '纪芳', 371: '景澄', 372: '经纶',
              373: '景明', 374: '晋优', 375: '阿鸠', 376: '酒客', 377: '乔尔', 378: '乔瑟夫', 379: '约顿',
              380: '乔伊斯',
              381: '居安', 382: '君君', 383: '顺吉', 384: '纯也', 385: '重佐', 386: '大岛纯平', 387: '蒲泽',
              388: '勘解由小路健三郎', 389: '枫', 390: '枫原义庆', 391: '荫山', 392: '甲斐田龍馬', 393: '海斗',
              394: '惟神晴之介', 395: '鹿野奈奈', 396: '卡琵莉亚', 397: '凯瑟琳', 398: '加藤信悟', 399: '加藤洋平',
              400: '胜家', 401: '茅葺一庆', 402: '和昭', 403: '一正', 404: '一道', 405: '桂一', 406: '庆次郎',
              407: '阿贤',
              408: '健司', 409: '健次郎', 410: '健三郎', 411: '天理', 412: '杀手a', 413: '杀手b', 414: '木南杏奈',
              415: '木村', 416: '国王', 417: '木下', 418: '北村', 419: '清惠', 420: '清人', 421: '克列门特',
              422: '骑士',
              423: '小林', 424: '小春', 425: '康拉德', 426: '大肉丸', 427: '琴美', 428: '宏一', 429: '康介',
              430: '幸德',
              431: '高善', 432: '梢', 433: '克罗索', 434: '久保', 435: '九条镰治', 436: '久木田', 437: '昆钧',
              438: '菊地君', 439: '久利须', 440: '黑田', 441: '黑泽京之介', 442: '响太', 443: '岚姐', 444: '兰溪',
              445: '澜阳', 446: '劳伦斯', 447: '乐明', 448: '莱诺', 449: '莲', 450: '良子', 451: '李当', 452: '李丁',
              453: '小乐', 454: '灵', 455: '小玲', 456: '琳琅a', 457: '琳琅b', 458: '小彬', 459: '小德', 460: '小楽',
              461: '小龙', 462: '小吴', 463: '小吴的记忆', 464: '理正', 465: '阿龙', 466: '卢卡', 467: '洛成',
              468: '罗巧',
              469: '北风狼', 470: '卢正', 471: '萍姥姥', 472: '前田', 473: '真昼', 474: '麻纪', 475: '真',
              476: '愚人众-马克西姆', 477: '女性a', 478: '女性b', 479: '女性a的跟随者', 480: '阿守', 481: '玛格丽特',
              482: '真理', 483: '玛乔丽', 484: '玛文', 485: '正胜', 486: '昌信', 487: '将司', 488: '正人', 489: '路爷',
              490: '老章', 491: '松田', 492: '松本', 493: '松浦', 494: '松坂', 495: '老孟', 496: '孟丹',
              497: '商人随从',
              498: '传令兵', 499: '米歇尔', 500: '御舆源一郎', 501: '御舆源次郎', 502: '千岩军教头', 503: '千岩军士兵',
              504: '明博', 505: '明俊', 506: '美铃', 507: '美和', 508: '阿幸', 509: '削月筑阳真君', 510: '钱眼儿',
              511: '森彦', 512: '元助', 513: '理水叠山真君', 514: '理水疊山真君', 515: '朱老板', 516: '木木',
              517: '村上',
              518: '村田', 519: '永野', 520: '长野原龙之介', 521: '长濑', 522: '中野志乃', 523: '菜菜子', 524: '楠楠',
              525: '成濑', 526: '阿内', 527: '宁禄', 528: '牛志', 529: '信博', 530: '伸夫', 531: '野方', 532: '诺拉',
              533: '纪香', 534: '诺曼', 535: '修女', 536: '纯水精灵', 537: '小川', 538: '小仓澪', 539: '冈林',
              540: '冈崎绘里香', 541: '冈崎陆斗', 542: '奥拉夫', 543: '老科', 544: '鬼婆婆', 545: '小野寺',
              546: '大河原五右卫门', 547: '大久保大介', 548: '大森', 549: '大助', 550: '奥特', 551: '派蒙',
              552: '派蒙2',
              553: '病人a', 554: '病人b', 555: '巴顿', 556: '派恩', 557: '朋义', 558: '围观群众', 559: '围观群众a',
              560: '围观群众b', 561: '围观群众c', 562: '围观群众d', 563: '围观群众e', 564: '铜雀', 565: '阿肥',
              566: '兴叔',
              567: '老周叔', 568: '公主', 569: '彼得', 570: '乾子', 571: '芊芊', 572: '乾玮', 573: '绮命', 574: '杞平',
              575: '秋月', 576: '昆恩', 577: '雷电影', 578: '兰道尔', 579: '雷蒙德', 580: '冒失的帕拉德', 581: '伶一',
              582: '玲花', 583: '阿仁', 584: '家臣们', 585: '梨绘', 586: '荣江', 587: '戎世', 588: '浪人',
              589: '罗伊斯',
              590: '如意', 591: '凉子', 592: '彩香', 593: '酒井', 594: '坂本', 595: '朔次郎', 596: '武士a',
              597: '武士b',
              598: '武士c', 599: '武士d', 600: '珊瑚', 601: '三田', 602: '莎拉', 603: '笹野', 604: '聪美', 605: '聪',
              606: '小百合', 607: '散兵', 608: '害怕的小刘', 609: '舒伯特', 610: '舒茨', 611: '海龙', 612: '世子',
              613: '谢尔盖', 614: '家丁', 615: '商华', 616: '沙寅', 617: '阿升', 618: '柴田', 619: '阿茂',
              620: '式大将',
              621: '清水', 622: '志村勘兵卫', 623: '新之丞', 624: '志织', 625: '石头', 626: '诗羽', 627: '诗筠',
              628: '石壮', 629: '翔太', 630: '正二', 631: '周平', 632: '舒杨', 633: '齐格芙丽雅', 634: '女士',
              635: '思勤',
              636: '六指乔瑟', 637: '愚人众小兵d', 638: '愚人众小兵a', 639: '愚人众小兵b', 640: '愚人众小兵c',
              641: '吴老五', 642: '吴老二', 643: '滑头鬼', 644: '言笑', 645: '吴老七', 646: '士兵h', 647: '士兵i',
              648: '士兵a', 649: '士兵b', 650: '士兵c', 651: '士兵d', 652: '士兵e', 653: '士兵f', 654: '士兵g',
              655: '奏太',
              656: '斯坦利', 657: '掇星攫辰天君', 658: '小头', 659: '大武', 660: '陶义隆', 661: '杉本', 662: '苏西',
              663: '嫌疑人a', 664: '嫌疑人b', 665: '嫌疑人c', 666: '嫌疑人d', 667: '斯万', 668: '剑客a', 669: '剑客b',
              670: '阿二', 671: '忠胜', 672: '忠夫', 673: '阿敬', 674: '孝利', 675: '鹰司进', 676: '高山',
              677: '九条孝行',
              678: '毅', 679: '竹内', 680: '拓真', 681: '卓也', 682: '太郎丸', 683: '泰勒', 684: '手岛', 685: '哲平',
              686: '哲夫', 687: '托克', 688: '大boss', 689: '阿强', 690: '托尔德拉', 691: '旁观者', 692: '天成',
              693: '阿大', 694: '蒂玛乌斯', 695: '提米', 696: '户田', 697: '阿三', 698: '一起的人', 699: '德田',
              700: '德长', 701: '智树', 702: '利彦', 703: '胖乎乎的旅行者', 704: '藏宝人a', 705: '藏宝人b',
              706: '藏宝人c',
              707: '藏宝人d', 708: '阿祇', 709: '恒雄', 710: '露子', 711: '话剧团团长', 712: '内村', 713: '上野',
              714: '上杉', 715: '老戴', 716: '老高', 717: '老贾', 718: '老墨', 719: '老孙', 720: '天枢星', 721: '老云',
              722: '有乐斋', 723: '丑雄', 724: '乌维', 725: '瓦京', 726: '菲尔戈黛特', 727: '维多利亚', 728: '薇尔',
              729: '瓦格纳', 730: '阿外', 731: '侍女', 732: '瓦拉', 733: '望雅', 734: '宛烟', 735: '琬玉', 736: '战士a',
              737: '战士b', 738: '渡辺', 739: '渡部', 740: '阿伟', 741: '文璟', 742: '文渊', 743: '韦尔纳',
              744: '王扳手',
              745: '武沛', 746: '晓飞', 747: '辛程', 748: '星火', 749: '星稀', 750: '辛秀', 751: '秀华', 752: '阿旭',
              753: '徐刘师', 754: '矢部', 755: '八木', 756: '山上', 757: '阿阳', 758: '颜笑', 759: '康明', 760: '泰久',
              761: '安武', 762: '矢田幸喜', 763: '矢田辛喜', 764: '义坚', 765: '莺儿', 766: '盈丰', 767: '宜年',
              768: '银杏', 769: '逸轩', 770: '横山', 771: '永贵', 772: '永业', 773: '嘉久', 774: '吉川', 775: '义高',
              776: '用高', 777: '阳太', 778: '元蓉', 779: '玥辉', 780: '毓华', 781: '有香', 782: '幸也', 783: '由真',
              784: '结菜', 785: '韵宁', 786: '百合', 787: '百合华', 788: '尤苏波夫', 789: '裕子', 790: '悠策',
              791: '悠也',
              792: '于嫣', 793: '柚子', 794: '老郑', 795: '正茂', 796: '志成', 797: '芷巧', 798: '知易', 799: '支支',
              800: '周良', 801: '珠函', 802: '祝明', 803: '祝涛'}
    return models

@app.route('/API', methods=['GET'])
def API():
    return render_template('API.html')
@app.route('/run', methods=['GET'])
def run():
    speak_text = request.args.get('text')
    client_ip = request.remote_addr
    if ban(client_ip):
        return '被封禁'

    if len(speak_text) > 600:
        return '合成过长，600'
    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    noisew = request.args.get('noisew', type=float)
    lang = request.args.get('lang', type=str)
    if lang is None:
        lang = 'zh'
    if noisew is None:
        noisew = 0.4
    if voice_noise is None:
        voice_noise = 0.25
    if voice_length is None:
        voice_length = 1.8
    speak_text = speak_text.replace('\n ', '').replace('\n', '')

    user_agent = request.headers.get('User-Agent')
    # if client_ip == '182.127.9.193':
    #     return page_not_found()
    url = f'http://100.92.125.90:23456/voice/vits?text={speak_text}&id={id_speaker}&lang={lang}&format=wav&length={voice_length}&noise={voice_noise}&noisew={noisew}'
    r = requests.get(url)
    new_url = f'http://www.纯度.site:5000/second_run?text={speak_text}&id_speaker={id_speaker}&length={voice_length}&noise={voice_noise}&noisew={noisew}&lang={lang}'

    inner_text(get_location(disguise_ip(client_ip)), speak_text, id_speaker, new_url)

    stream = io.BytesIO(r.content)
    # 其他代码...

    return send_file(stream, mimetype='audio/wav')


@app.route('/second_run', methods=['GET'])
def second_run():
    speak_text = request.args.get('text')
    client_ip = request.remote_addr
    if ban(client_ip):
        return '被封禁'
    if len(speak_text) > 600:
        return '合成过长，600'

    # if len(speak_text) > 300:
    #     return 'sb'
    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    noisew = request.args.get('noisew', type=float)
    lang = request.args.get('lang', type=str)
    if lang is None:
        lang = 'zh'
    if noisew is None:
        noisew = 0.4
    if voice_noise is None:
        voice_noise = 0.25
    if voice_length is None:
        voice_length = 1.8
    speak_text = speak_text.replace('\n ', '').replace('\n', '')

    url = f'http://100.92.125.90:23456/voice/vits?text={speak_text}&id={id_speaker}&lang={lang}&format=wav&length={voice_length}&noise={voice_noise}&noisew={noisew}'
    r = requests.get(url)
    # new_url = f'http://175.178.176.3:5000/second_run?text={speak_text}&id_speaker={id_speaker}&length={voice_length}&noise={voice_noise}&noisew={noisew}'

    # inner_text(get_location(client_ip), speak_text, id_speaker, new_url)
    # client_ip = request.remote_addr
    # user_agent = request.headers.get('User-Agent')
    # save_it2(get_location(client_ip), speak_text, id_speaker, user_agent)

    stream = io.BytesIO(r.content)
    # 其他代码...

    return send_file(stream, mimetype='audio/wav')


@app.route('/can_only_myself', methods=['GET'])
def content():
    client_ip = request.remote_addr
    if ban(client_ip):
        return '被封禁'
    # # 获取当前页码，默认为 1
    # with open('log.txt', 'r', encoding='utf-8') as f:
    #     my_list = f.readlines()
    # my_list = [line.replace('\n ', '').replace('\n', '') for line in my_list]
    # my_list = [x for x in my_list if x]
    # # my_list.reverse()
    rows = show_table()
    urls = []
    rows.reverse()
    for row in rows:
        urls.append(
            f'|{row[1]}|{row[2]}|<span class="styled-text">{row[3]}</span>|<a href="{row[4]} "target="_blank">播放</a>|{row[5]}')

    urls = [elem for elem in urls if elem]
    page = int(request.args.get('page', 1))

    # 计算总页数
    total_pages = (len(urls) - 1) // 40 + 1

    # 根据当前页码和每页显示的数量计算切片范围
    start = (page - 1) * 40
    end = page * 40

    # 对列表进行切片，获取当前页的数据
    current_data = urls[start:end]

    return render_template('page.html', data=current_data, page=page, total_pages=total_pages, urls=urls)


@app.route('/can_only_myself2', methods=['GET'])
def content_forward():
    client_ip = request.remote_addr
    if ban(client_ip):
        return '被封禁'
    # # 获取当前页码，默认为 1
    # with open('log.txt', 'r', encoding='utf-8') as f:
    #     my_list = f.readlines()
    # my_list = [line.replace('\n ', '').replace('\n', '') for line in my_list]
    # my_list = [x for x in my_list if x]
    # # my_list.reverse()
    rows = show_table()
    urls = []
    # rows.reverse()
    for row in rows:
        urls.append(
            f'|{row[1]}|{row[2]}|<span class="styled-text">{row[3]}</span>|<a href="{row[4]} "target="_blank">播放</a>|{row[5]}')

    urls = [elem for elem in urls if elem]
    page = int(request.args.get('page', 1))

    # 计算总页数
    total_pages = (len(urls) - 1) // 40 + 1

    # 根据当前页码和每页显示的数量计算切片范围
    start = (page - 1) * 40
    end = page * 40

    # 对列表进行切片，获取当前页的数据
    current_data = urls[start:end]

    return render_template('page.html', data=current_data, page=page, total_pages=total_pages, urls=urls)


@app.route('/if', methods=['GET'])
def if_online():
    url = 'http://100.92.125.90:23456/if'
    r = requests.get(url)
    if r.text == 'True':
        return 'True'


# @app.route('/random', methods=['GET'])
# def ra():
#     global indices, content_list
#     speak_text = request.args.get('text')
#     voice_length = request.args.get('length', type=float)
#     voice_noise = request.args.get('noise', type=float)
#     content_list, indices = cut.cut_Chinese_double_quotation_marks(speak_text)
#
#     random_num1, random_num2, now_ten_minute = get_random()
#     content = ''.join(content_list)
#     save_random(random_num1, random_num2, now_ten_minute, content)
#     url = f'http://100.92.125.90:23456/voice/vits?text={speak_text}&id={random_num1}&format=wav&lang=zh&length={voice_length}&noise={voice_noise}'
#     r = requests.get(url)
#     stream = io.BytesIO(r.content)
#     temp_wav_file = f"temp.wav"
#     with open(temp_wav_file, "wb") as f:
#         f.write(stream.getvalue())
#     return send_file(temp_wav_file, mimetype='audio/wav')
#


# @app.route('/emo', methods=['GET'])
# def emo():
#     global indices, content_list
#     speak_text = request.args.get('text')
#     id_speaker = request.args.get('id_speaker', type=str)
#     voice_length = request.args.get('length2', type=float)
#     voice_noise = request.args.get('noise', type=float)
#     url = f'http://100.92.125.90:23456/voice/vits?text={speak_text}&id={id_speaker}&format=wav&lang=zh&length={voice_length}&noise={voice_noise}'
#     r = requests.get(url)
#     stream = io.BytesIO(r.content)

#
# return send_file(stream, mimetype='audio/wav')


@app.route('/')
def html():
    client_ip = request.remote_addr
    if ban(client_ip):
        return 'sb'
    return render_template('main.html')


if __name__ == '__main__':
    # print(get_speaker())
    app.run(host='0.0.0.0')
