import datetime

ProjectStarTime = datetime.datetime(2020, 3, 22)


class MACNode(object):
    ID = None
    usdt = 0
    superiorID = None
    attendRound = 0  # 默认加入时刻是0时刻加入
    level = 1  # 默认是第一级加入
    subNodeNum = 0  # 默认没有小弟

    interestDate = None  # // interestIncome累计到哪一天
    interestIncome = None  # // 已累计入账的收益，由开始收入 + 今天的全体收入构成
    subNodeList = None  # // 下线
    vipTagList = None  # // 是否vip, 每日更新
    vipSuperior = None  # // VIP上线
    vipSubList = None  # // 子节点是否是VIP

    ruleStatus = None  # // 是否应用规则
    staticIncome = None  # // 静态收益
    subStaticIncome = None  # // 下级贡献的收益
    dynamicIncome = None  # // 动态收益
    withdrawStatus = None  # // 是否提现
    withdrawMoney = None  # // 目前可以提现额度

    def __init__(self, ID, usdt=0, superior=None, attendRound=None):
        self.ID = ID
        self.usdt = usdt

        if superior is not None:
            self.superiorID = superior.ID

        if attendRound is None:
            self.attendRound = self.calRound()
        else:
            self.attendRound = attendRound

    def calRound(self):
        today = datetime.datetime.now()
        Round = (today - ProjectStarTime).days

        print(f"Node attend this project at Round {Round}")
        return Round


if __name__ == "__main__":
    ID = "111"

    l1 = MACNode("222", 333)
