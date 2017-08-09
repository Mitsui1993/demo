from wxpy import *

bot = Bot(cache_path=True)

my_friend = bot.friends().search('小明',sex='MALE',city='深圳')[0]
#向匹配的好友发送文本
my_friend.send('开始魔法')

#引用图灵接口
tuling = Tuling(api_key='5a3d19d6e46f4cc0be4258ba49171743')

# my_friend.send('开启魔法')

#打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print(msg)

#无参，则表示回复所有好友，引用图灵机器人
@bot.register()
def reply_my_friend(msg):
    tuling.do_reply(msg)

#回复 my_friend的消息(优先匹配后注册的函数！)
@bot.register(my_friend)
def reply_my_friend(msg):
    return '我是学舌的机器人:{}'.format(msg.text)

#自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    #接受好友请求
    new_friend = msg.card.accept()
    #向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求')

embed()