import datetime

ProjectStarTime = datetime.datetime(2020, 3, 22)


class MACNode(object):
    ID = 0
    Address = None
    Balance = 0
    parentID = 0
    parentAddress = None
    name = None
    tel = None
    email = None

    attendRound = 0  # 默认加入时刻是0时刻加入

    subNodeNum = 0  # 默认没有小弟
    level = 1  # 默认是第一级加入
    IDleft = 1  # 加入的左值
    IDright = 2  # 加入的右值
    vipTag = None  # // 是否vip, 每日更新

    untilNowIncome = None  # // 已累计入账的收益
    staticIncome = None  # // 静态收益
    subStaticIncome = None  # // 下级贡献的收益
    dynamicIncome = None  # // 动态收益

    withdrawStatus = None  # // 是否提现

    subNodeList = None  # // 下线
    vipSubList = None  # // 子节点是否是VIP

    withdrawMoney = None  # // 目前可以提现额度

    def __init__(self, ID, Address, Balance=0, parentNode=None, attendRound=None):
        self.ID = ID
        self.Address = Address
        self.Balance = Balance

        if parentNode is not None:
            self.parentAddress = parentNode.Address
            self.parentID = parentNode.ID

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
    Address = "111"

    l1 = MACNode("1","MAN.222", 333)
