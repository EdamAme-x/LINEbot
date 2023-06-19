from CHRLINE import *
import time, sys, os, json, time, requests,  glob, datetime, random, re
from enum import Enum
from gpt4free import you

ver = "v2.2.0"
author = "u8da9ac344a26c157e58bff09579e6deb"
mymid = "your account id"

initial_setting = {
    "prefix": "@",
    "autojoin": True,
    "autoread": True,
    "autologdel": True,
    "blist": [],
    "wlist": [],
    "invitelist": [],
    "kickers": {},
}
kicker = []
"""コマンドライン引数取得"""
login_data = sys.argv

"""ログイン"""
cl = CHRLINE("<mail>", "<pass>", device="IOSIPAD")

"""データ生成"""
data_json_file = os.path.isfile(
    f"...path\\{cl.mid}.json"
)
if data_json_file:
    pass
else:
    with open(
        f"...path\\{cl.mid}.json",
        "w",
    ) as f:
        json.dump(initial_setting, f, indent=4, ensure_ascii=False)

"""json読み込み"""
read_json = open(
    f"...path\\{cl.mid}.json"
)
data = json.load(read_json)

"""json保存する関数"""

def data_save():
    with open(
        f"...path\\{cl.mid}.json",
        "w",
    ) as f:
        json.dump(data, f, indent=4)

def log(op):
    current_time = time.localtime()
    
    formatted_time = time.strftime('%Y年%m月%d日', current_time)
    with open(f"...path\\{formatted_time}.txt", 'a', encoding='utf-8', errors='ignore') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f'{timestamp} [{op[0]}] {op}'
        f.write(log_msg + '\n \n')

def getChatJoinMids(gid):
    for i in cl.getChats([gid])[1]:
        return list(i[8][1][4].keys())

def authToken_login(token, device="IOSIPAD"):
    try:
        kicker = CHRLINE(token, device=device)
        kicker.getContact(author)
        return kicker.mid
    except:
        return "invalid"

def mail_login(mail, password, device="IOSIPAD"):
    try:
        kicker = CHRLINE(mail, password, device=device)
        kicker.getContact(author)
        return f"{kicker.mid}:{kicker.authToken}"
    except:
        return "invalid"

def get_newest_image_files(folder_path):
    """指定されたフォルダ内の最新の画像ファイルのパスを取得する関数"""
    files = os.listdir(folder_path)
    files = [
        file
        for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]
    if not files:
        return None
    newest_file = max(
        files, key=lambda x: os.path.getctime(os.path.join(folder_path, x))
    )
    return os.path.join(folder_path, newest_file)

def get_help_message():
    """コマンドリスト確認"""
    if data["prefix"] == "":
        prefix_ = "@"
    else:
        prefix_ = data["prefix"]
        
        helpms = f"""Self bot V.β
help
test
mid
└➥mid,mid:@
gid
ginfo
login
exec:cmd
un:num"""
    return helpms

# ----- BOT SETTING ------
ADMIN = []
TAGNOTREPLY = {}
TAGNOTREPLY_MIN = 1
ENABLE_ALLID_REGEX = True
ENABLE_LINETIME_REGEX = True
SEND_MESSAGE_COOLING = {}
COOLING_TIME = 5
NOT_COOLING_TEXT = ['sp']
ANNOUNCEMENT_RECORD = []
# ----- ----------- ------

chat = []

def botss(op, cl):
    opType = op.get(3, 0)
    if op[3] == 124 and cl.profile[1] in op[12]:

        """自動参加"""
        if data["autojoin"] == True:
            return
        cl.acceptChatInvitation(op[10])

    elif op[3] == 25:
        msg = op[20]
        to = msg[2]
        msgId = msg[4]
        msgTime = msg[5]
        msgType = msg[15]
        msgMetadata = msg.get(18, {})
        msg_from = msg[1]
        if msg[15] == 0:
            if msg[3] == 2:
                text = msg[10]

                """prefixついてなかったらreturn"""
                if not text.startswith(data["prefix"]):
                    return
                
                elif text.startswith(data["prefix"]):
                    prefix_len = len(data["prefix"])
                    text = text[prefix_len:]

                """コマンド処理"""
                if text == "help":
                    cl.replyMessage(msg, get_help_message())

                elif text == "test":
                    cl.replyMessage(msg, "ok")

                elif text.startswith("mid"):
                    try:
                        metadata = msg[18]
                        if "MENTION" in metadata:
                            key = eval(metadata["MENTION"])
                            tags = key["MENTIONEES"]
                            for tag in tags:
                                mid = tag["M"]
                                cl.replyMessage(msg, mid)
                        else:
                            cl.replyMessage(msg, cl.getProfile().mid)
                    except:
                        cl.replyMessage(msg, msg_from)

                elif text == "gid":
                    cl.replyMessage(msg, to)

                elif text == "login":
                    a = CHRLINE(device="IOSIPAD", noLogin=True)
                    for b in a.requestSQR():
                        cl.replyMessage(msg, b)
                        if b.startswith("URL:"):
                            image_folder_path = "...path\\CHRLINE\\.images"
                            image_file_path = get_newest_image_files(image_folder_path)
                            if image_file_path:
                                cl.sendImage(to, image_file_path)
                            else:
                                cl.replyMessage(msg,"No image found in the specified folder.",)
                    if a.authToken:
                        print(a.authToken)
                        _sbot = CHRLINE(a.authToken, device="IOSIPAD")
                        _sbot.sendMessage(to, "Loginに成功しました:D")
                        _sbot.trace(botss)

                elif text == "ginfo":  # get chat room infomation
                    gid = cl.getChats([to])[1][0]
                    g_info = "グル情報"
                    g_info += "\nグル名:\n" + gid[6]
                    g_info += "\ngid:\n" + gid[2]
                    try:
                        g_info += "\nグル作者:\n" + cl.getContact(gid[8][1][1])[22]
                    except:
                        g_info += (
                            "\nグル作者:\n"
                            + cl.getContact(gid[8][1][4][0])[22]
                            + " (inherit)"
                        )
                    try:
                        g_info += "\nグル画:\n%s%s" % (cl.LINE_OBS_DOMAIN, gid[7])
                    except:
                        g_info += "\nグル画:\n%s/%s" % (cl.LINE_OBS_DOMAIN, "None")
                    g_info += "\n作成日:\n" + time.strftime(
                        "%Y-%m-%d %I:%M:%S %p", time.localtime(gid[3] / 1000)
                    )
                    g_info += "\n" + "=" * 32
                    g_info += (
                        " \n参加人数: "
                        + str(len(gid[8][1][4]))
                        + "\n招待中: "
                        + str(len(gid[8][1][5]))
                    )
                    if gid[8][1][2] is False:
                        g_info += "\nうらる:あいてますよ"
                    else:
                        g_info += "\nうらる:とじてますぅ"
                    cl.replyMessage(msg, f"{g_info}")

                elif text.startswith("exec:"):  # cmd:command
                    command = msg[10][6:]
                    try:
                        exec(command)
                    except Exception as e:
                        cl.sendMessage(to, f"{e}")
                
                elif text.startswith("ai:"):
                    prompt = text[3:]
                    if prompt == 'q':
                        pass
                    else:
                        response = you.Completion.create(prompt=prompt, chat=chat)
                        if len(response.text) > 0:
                            response_text = response.text
                        else:
                            response_text = ""
                        response_text = response_text.encode('utf-8').decode('unicode-escape')
                        cl.replyMessage(msg, response_text)
                        chat.append({"question": prompt, "answer": response_text})

                elif text.startswith("un:"):
                    unsend_num = text[3:]
                    try:
                        int(unsend_num)
                    except:
                        return cl.sendMessage(to, "Please specify an integer")
                    msg_ids = cl.getRecentMessagesV2(to, 300)
                    unsend_len = int(unsend_num) + 1
                    unsend_ids = []
                    for i_ids in msg_ids:
                        if str(cl.mid) in str(i_ids[1]):
                            unsend_ids.append(str(i_ids[4]))
                            if len(unsend_ids) == unsend_len:
                                break
                            else:
                                pass
                        else:
                            pass
                    for unsend_id in unsend_ids:
                        try:
                            time.sleep(0.8)
                            cl.unsendMessage(unsend_id)
                        except:
                            cl.sendMessage(
                                to,
                                "Messages that are 24 hours old cannot be cancelled.",
                            )
                            break

                elif text.startswith("getdata") and msg[3] == 2:
                    try:
                        count = text[7:]
                        if count == '':
                            msgid = msg.get(21)
                            if msgid != None:
                                msgids = cl.getPreviousMessageIds(to, 32767)
                                target_msg = None
                                for i in msgids[1]:
                                    if msgid == str(i[2]):
                                        target_msg = i
                                        break
                                if target_msg is not None:
                                    target_msg = cl.getPreviousMessagesV2(to, target_msg[1], target_msg[2])[0]
                                    target_msg[17] = "N-project"
                                    cl.sendMessage(to, target_msg, relatedMessageId=msgid)
                                else:
                                    cl.sendMessage(to, "期限切れ")
                            else:
                                count = 1
                        if count != '':
                            count = int(count)
                            msgids = cl.getPreviousMessageIds(to, count + 10)
                            msgids = msgids[1]
                            msgidc = len(msgids)
                            cl.sendMessage(to, f'探しています{count}')
                            if msgidc >= count:
                                target_msg = msgids[count-1]
                                isFound = False
                                currI = 0
                                for i in msgids:
                                    if str(i[2]) == msg[4]:
                                        isFound = True
                                    else:
                                        if isFound:
                                            currI += 1
                                            if currI == count:
                                                target_msg = i
                                                break
                                target_msgid = target_msg[2]
                                cl.sendMessage(to, 'ここ', relatedMessageId=target_msgid)
                                target_msg = cl.getPreviousMessagesV2(to, target_msg[1], target_msg[2])[0]
                                target_msg[17] = "N-project" # overwrite content view for image or video...
                                cl.sendMessage(to, target_msg, relatedMessageId=target_msgid)
                            else:
                                cl.sendMessage(to, "期限切れ")
                    except Exception as e:
                        cl.sendMessage(to, f'数値でなければなりません: {count}')

    elif op[3] == 30:
        gid = op[10]
        seq = op[11]
        update_type = op[12]
        uuid = f"{gid}_{seq}_{update_type}"
        if 'cache' not in ANNOUNCEMENT_RECORD:
            ANNOUNCEMENT_RECORD['cache'] = []
        if uuid not in ANNOUNCEMENT_RECORD['cache']:
            ANNOUNCEMENT_RECORD['cache'].append(uuid)
        else:
            return
        if update_type == 'd' or update_type == 'u':
            reply = f"公告{seq}已被{'取消' if update_type == 'd' else '更新'}"
            relatedMessageId = None
            if gid in ANNOUNCEMENT_RECORD:
                for ann in ANNOUNCEMENT_RECORD[gid]:
                    if str(seq) == str(ann[1]):
                        annData = ann[3]
                        reply += f"\n原內容如下\n`{annData[2]}`\n連結:{annData[3]}"
                        # line://nv/chatMsg?chatId=c13d5e6c1c22464120eef2400407023e0&messageId=14603297007331
                        if '&messageId=' in annData[3]:
                            messageId = annData[3].split('&messageId=')
                            relatedMessageId = messageId[1]
                        break
            cl.sendMessage(gid, reply, relatedMessageId=relatedMessageId)
        ANNOUNCEMENT_RECORD[gid] = cl.getChatRoomAnnouncements(gid)
    elif op[3] == 40:
        # 已讀
        pass
    elif op[3] == 45:
        # NOTIFIED_UPDATE_CONTENT_PREVIEW
        # video message
        cl.react(op[12], random.choice([2, 3, 4, 5, 6]))
    elif op[3] == 48:
        print(f'dummy: {op}')
    elif op[3] == 55:
        # 已讀?
        pass
    elif op[3] == 60:
        # NOTIFIED_JOIN_CHAT
        pass
    elif op[3] == 61:
        # NOTIFIED_LEAVE_CHAT
        pass
    elif op[3] == 65:
        # 收回?
        gid = op[10]
        msgid = op[11]
        if gid in cl.custom_data.get('reviewMsg', []):
            msgids = cl.getPreviousMessageIds(gid, 1000)
            target_msg = None
            for i in msgids[1]:
                if msgid == str(i[2]):
                    target_msg = i
                    break
            reply = "找不到相關紀錄Orz"
            contentMetadata = None
            if target_msg is not None:
                target_msg = cl.getPreviousMessagesV2(gid, target_msg[1], target_msg[2])[0]
                # {1: 'ud4045303d1cf300eca5f32fb1ba85376', 2: 'cf2f6416ed319f353bbd26c046c3de3ad', 3: 2, 4: '14409743298380', 5: 1626511223716, 6: 1626511223716, 10: '嗚嗚屋', 14: False, 15: 0, 18: {'UNSENT': 'true', 'seq': '14409743298380'}, 19: 0, 27: []}
                if target_msg[15] == 0:
                    reply = f"@chrline 的原訊息如下:\n{target_msg[10]}"
                    arr = [
                        {
                            "S": str(0),
                            "E": str(8),
                            "M": target_msg[1]
                        }
                    ]
                    contentMetadata = {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}
                else:
                    return
            cl.sendMessage(gid, reply, contentMetadata=contentMetadata, relatedMessageId=msgid)
    elif op[3] == 124:
        #被邀請
        if cl.profile[1] in op[12]:
            cl.acceptChatInvitation(op[10])
            cl.sendMessage(op[10],"よろしくにゃ(^o^ )")
    elif op[3] == 127:
        #退群組
        if op[10] in cl.groups:
            cl.groups.remove(op[10])
    elif op[3] == 128:
        #NOTIFIED_DELETE_SELF_FROM_CHAT
        #if op[10] in cl.groups:
        #    cl.groups.remove(op[10])
        pass
    elif op[3] == 129:
        #加群組
        cl.groups.append(op[10])
    elif op[3] == 130:
        #別人加群組
        pass
    elif opType == 133:
        if op[12] == cl.profile[1]:
            if op[10] in cl.groups:
                cl.groups.remove(op[10])
    elif opType == 139:
        # SEND_REACTION
        # リアクションを送信したユーザーにメッセージを送信する
        sender_id = str(op[2])
        group_id = str(op[1])
        try:
            # 送信先がトークの場合
            cl.sendMessage(sender_id, "reactionを検知したぜ(^o^ )")
        except CHRLINE.exceptions.LineServiceException as e:
            # 送信先がグループまたはトークルームの場合
            if e.code == 0 and "midType" in e.message:
                cl.sendText(group_id, "reactionを検知したぜ(^o^ )")

    elif opType == 140:
        _msgid = op[10]
        _msgTime = op[2]
        _gid = json.loads(op[11])['chatMid']
        _uid = op[12]
        if _gid not in cl.custom_data.get('reactnotify', []):
            return
        msgids = cl.getPreviousMessageIds(_gid, 100)
        target_msg = None
        for i in msgids[1]:
            if _msgid == str(i[2]):
                target_msg = i
                break
        if target_msg is not None:
            target_msg = cl.getPreviousMessagesV2(_gid, target_msg[1], target_msg[2])[0]
            if target_msg[1] not in [_uid, cl.profile[1]]:
                if _gid not in TAGNOTREPLY:
                    TAGNOTREPLY[_gid] = {}
                if target_msg[1] not in TAGNOTREPLY[_gid]:
                    TAGNOTREPLY[_gid][target_msg[1]] = []
                TAGNOTREPLY[_gid][target_msg[1]] += [[_msgid, _msgTime, 'REACTION']]
        else:
            pass
    else:
        log(f"[{opType}]{op}")

cl.trace(botss)
