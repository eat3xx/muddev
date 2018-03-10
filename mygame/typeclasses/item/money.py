#coding=utf-8

class Money():

    TOTAL = 0

    def add(self, number):
        self.TOTAL += number

    def substract(self, number):
        self.TOTAL -= number

    def show(self):
        gold = self.TOTAL/100
        silver = self.TOTAL%100
        return "%s两黄金%s两白银" % (gold, silver)

if __name__ == "__main__":
    money = Money()
    money.TOTAL = 8734
    print money.show()
