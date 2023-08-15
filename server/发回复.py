from nonebot.rule import to_me
from nonebot.plugin import on_command

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
# Message = on_command("天气", rule=to_me(), aliases={"Message", "查天气"}, priority=10, block=True)

@weather.handle()
async def handle_function():
    # await weather.send("天气是...")
    from nonebot.exception import MatcherException

    try:
        # Message.send(Messagesegment.record())
        await weather.finish("天气是...")

    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here

 