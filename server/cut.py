import re


class cut:

    def __init__(self):
        self.indices = None
        self.content_list = None

    def cut_Chinese_double_quotation_marks(self, speak_text):
        # text = '“唔，要来了。”随着腋下玩弄的愈发快速，徐贤慢慢进入嘎嘎嘎状态“我要，把嘎嘎嘎，射满我嘎嘎嘎 。”'
        content = speak_text
        pattern = r"[“]"  # 左边
        self.content_list = re.split(pattern, content)

        # 假设列表字符串为 lst，待搜索的字符串为 target
        target = r'”'  # 待搜索的字符串
        self.indices = []  # 保存目标字符串在列表中的下标
        for i, s in enumerate(self.content_list):
            flag = 0
            if target in s:
                # 找到目标字符串
                parts = s.split(target)  # 将字符串切片成两部分
                self.content_list.pop(i)  # 删除原字符串
                self.content_list.insert(i, parts[0])  # 插入第一部分
                if parts[1] and parts[1] != ' ':  # 如果第二部分非空，则插入
                    self.content_list.insert(i + 1, parts[1])  # 插入第二部分
                flag = 1
            self.indices.append(flag)  # 记录布尔值
        targets = ['。', '，', '！', '？']
        for target in targets:
            for j, i in enumerate(self.indices):
                content = self.content_list[j]
                # print(content)
                if i == 1:
                    if len(content) >= 100:
                        if target in content:  # “双引号内。双引号内”
                            parts = content.split(target)  # ['双引号内','双引号内']
                            self.content_list.pop(j)
                            self.indices.pop(j)
                            temp = j

                            for part in parts:  # '双引号内'
                                self.content_list.insert(temp, part)
                                self.indices.insert(temp, 1)
                                temp += 1
                if i == 0:
                    if len(content) >= 100:
                        if target in content:  # “双引号内。双引号内”
                            parts = content.split(target)  # ['双引号内','双引号内']
                            self.content_list.pop(j)
                            self.indices.pop(j)
                            temp = j
                            for part in parts:  # '双引号内'
                                self.content_list.insert(temp, part)
                                self.indices.insert(temp, 0)
                                temp += 1
        for c, content in enumerate(self.content_list):
            if content == '' or content == ' ':
                self.content_list.pop(c)
                self.indices.pop(c)

        for j, i in enumerate(self.indices):  # 遍历对话
            if len(self.content_list[j]) < 5:
                self.indices[j] = 0
        # for j, i in enumerate(self.indices):  # 遍历对话
        #     if i == 1:
        #         print(self.content_list[j])

        # for j, i in enumerate(self.indices):  # 遍历旁白
        #     if i == 0:
        #         print(self.content_list[j])

        # print(self.content_list)

        return self.content_list, self.indices



# if __name__ == '__main__':
#     cut = cut()
#     cut.cut_Chinese_double_quotation_marks()
