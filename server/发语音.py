import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
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

alipay_voice = on_command("八重神子说", aliases={"#八重神子说"})
@alipay_voice.handle()
async def alipay(matcher: Matcher, args: Message = CommandArg()):
    content = args.extract_plain_text()
    print(content)
    if not content:
        return
    try:
        if 1 <= len(content) <= 600:
            url = f"http://175.178.176.3:5000/run?text={content}&id_speaker=133&length=1.5&noise=0.25&noisew=0.4"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    content = response.content
                    await alipay_voice.send(MessageSegment.record(content))
                    # 处理返回的内容
                else:
                    print(f"请求失败，状态码：{response.status_code}")


        else:
            await matcher.send("字数超出限制")
    except:
        pass
