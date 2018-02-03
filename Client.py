#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
from magetool import urltool
import json
import sys
import time

f = open('../../btc/okexapikey/okexapikey.txt','r')
tmpstr = f.read()
f.close()

apikeydic = json.loads(tmpstr)

#初始化apikey，secretkey,url
apikey = apikeydic['apikey']
secretkey = apikeydic['secretkey']
okcoinRESTURL = 'www.okex.com'#'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

#现货API
# okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

#期货API
# okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)

# print (u' 现货行情 ')
# print (okcoinSpot.ticker('btc_usd'))

# print (u' 现货深度 ')
# print (okcoinSpot.depth('btc_usd'))

#print (u' 现货历史交易信息 ')
#print (okcoinSpot.trades())

#print (u' 用户现货账户信息 ')
#print (okcoinSpot.userinfo())

#print (u' 现货下单 ')
#print (okcoinSpot.trade('ltc_usd','buy','0.1','0.2'))

#print (u' 现货批量下单 ')
#print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))

#print (u' 现货取消订单 ')
#print (okcoinSpot.cancelOrder('ltc_usd','18243073'))

#print (u' 现货订单信息查询 ')
#print (okcoinSpot.orderinfo('ltc_usd','18243644'))

#print (u' 现货批量订单信息查询 ')
#print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))

#print (u' 现货历史订单信息查询 ')
#print (okcoinSpot.orderHistory('ltc_usd','0','1','2'))

#print (u' 期货行情信息')
#print (okcoinFuture.future_ticker('ltc_usd','this_week'))

#print (u' 期货市场深度信息')
#print (okcoinFuture.future_depth('btc_usd','this_week','6'))

#print (u'期货交易记录信息') 
# jsonstr = (okcoinFuture.future_trades('ltc_usd','quarter'))

# outsrt = json.dumps(jsonstr)

# print outsrt

#print (u'期货指数信息')
#print (okcoinFuture.future_index('ltc_usd'))

#print (u'美元人民币汇率')
#print (okcoinFuture.exchange_rate())

#print (u'获取预估交割价') 
#print (okcoinFuture.future_estimated_price('ltc_usd'))

#print (u'获取全仓账户信息')
#print (okcoinFuture.future_userinfo())

#print (u'获取全仓持仓信息')
#print (okcoinFuture.future_position('ltc_usd','this_week'))



class TradeTool(object):
    """docstring for ClassName"""
    def __init__(self,amount = 30,isTest = False):
        self.okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
        self.depthSells = []
        self.depthBuys = []
        self.amount = amount
        self.isTest = isTest
        self.IDs = []
        self.isOpen = False

    def setAmount(self,amount):
        self.amount = amount

    def printSet(self):
        print 'isTest:',self.isTest
        print 'amount:',self.amount

    def getDepth(self):
        turl = 'https://www.okex.com/api/v1/future_depth.do?symbol=ltc_usd&contract_type=quarter&size=20'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        buys = ddic['bids']
        sells = ddic['asks']
        return buys,sells

    def getAllOrderIDs(self):
        #future_orderinfo(self,symbol,contractType,orderId,status,currentPage,pageLength)
        tmpjson = self.okcoinFuture.future_orderinfo('ltc_usd','quarter','-1','1','1','30')
        dic = json.loads(tmpjson)
        self.IDs = []
        try:
            for t in dic['orders']:
                self.IDs.append(t['order_id'])
        except Exception as e:
            self.IDs = []
        

    #1:开多   2:开空   3:平多   4:平空
    def openShort(self):



        if self.isOpen:
            instr = raw_input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            print instr
            if instr != 'y':
                print '已开仓，选择本次不开仓'
                return

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        inputstr = raw_input("请输入：");
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None
        print inputidx,type(inputidx)

        print ('期货开空单')
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            tmps = self.depthBuys[::-1]
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1]

            self.isOpen = True
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + 0.001
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'2','0','10')
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - 0.001
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'2','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'2','0','10')
        else:
            print '输入数据错误'

    def closeShort(self):
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        inputstr = raw_input("请输入：");
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print ('期货平空单')
        
        if inputidx != None:
            self.depthBuys,self.depthSells = self.getDepth()
            atmp = list(self.depthSells)
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1]

            self.isOpen = False
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - 0.001
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'4','0','10')
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + 0.001
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'4','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'4','0','10')
        else:
            print '输入数据错误'

    def openLong(self):
        if self.isOpen:
            instr = raw_input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            print instr
            if instr != 'y':
                print '已开仓，选择本次不开仓'
                return
        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        inputstr = raw_input("请输入：");
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print ('期货开多单')
        
        
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            atmp = self.depthSells
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1]

            self.isOpen = True
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - 0.001
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'1','0','10')
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + 0.001
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'1','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'1','0','10')
        else:
            print '输入数据错误'
        

    def closeLong(self):

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        inputstr = raw_input("请输入：");
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print ('期货平多单')
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10
        
        
        # tmps = tmps[::-1]
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            tmps = self.depthBuys[::-1]
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1

            print -1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1]

            self.isOpen = False
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + 0.001
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'3','0','10')
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - 0.001
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'3','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,self.amount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(self.amount),'3','0','10')
        else:
            print '输入数据错误'

    def cleanAllTrade(self):
        self.getAllOrderIDs()
        time.sleep(0.1)
        if self.IDs:
            strids = self.IDs[0]
            if len(self.IDs) > 1:
                strids = ','.join(self.IDs)
            print self.okcoinFuture.future_cancel('ltc_usd','quarter',strids)
            print '所有定单已取消'
        self.isOpen = False

# print ('期货下单')
# print (okcoinFuture.future_trade('ltc_usd','quarter','147.205','30','1','0','10'))

#print (u'期货批量下单')
#print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))

#print (u'期货取消订单')
#print (okcoinFuture.future_cancel('ltc_usd','this_week','47231499'))

#print (u'期货获取订单信息')
# jsonstr =  (okcoinFuture.future_orderinfo('ltc_usd','quarter','-1','2','1','30'))

# print jsonstr

# outsrt = json.dumps(jsonstr)

# print(outsrt)

#print (u'期货逐仓账户信息')
#print (okcoinFuture.future_userinfo_4fix())

#print (u'期货逐仓持仓信息')
#print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))

def main(pAmount = 30, ispTest = True):
     tradetool = TradeTool(amount = pAmount,isTest = ispTest)
     pstr = '程序重新运行,\nos:开空\ncs:平空\nol:开多\ncl:平多\np:输出设置项\nset:设置每次成交量\nc:取消所有未成交定单\ntest:\n\t输入1表示使用测试方式运行\n\t0表示正试运行下单\nq:退出\n请输入:'
     while True:
        inputstr = raw_input(pstr);
        if inputstr == 'os':
            tradetool.openShort()
        elif inputstr == 'cs':
            tradetool.closeShort()
        elif inputstr == 'ol':
            tradetool.openLong()
        elif inputstr == 'cl':
            tradetool.closeLong()
        elif inputstr == 'set':
            intmp = raw_input("输入每次开单量:");
            try:
                intam = int(intmp)
                tradetool.amount = intam
            except Exception as e:
                print '输入参数错误'
        elif inputstr == 'q':
            print '程序退出成功'
            break
        elif inputstr == 'c':
            tradetool.cleanAllTrade()
        elif inputstr == 'p':
            tradetool.printSet()
        elif inputstr == 'test':
            outstr = '输入是否开启测试\n1.开启测试下单不会真正发送\n0.关闭测试模试,下单将会发送到平台\n请输入:'
            tstr = raw_input(outstr);
            if tstr == '1':
                tradetool.isTest = True
            elif tstr == '0':
                tradetool.isTest = False
            else:
                print '输入参数错误'
        else:
            print '输入错误，%s'%(pstr)

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        amount = int(args[1])
        if amount:
            main(pAmount = amount)
        elif args[1] == 'test': 
            print 'a程序使用测试方式运行\nmount未设置,使用默认值:30\n可在程序中重新设置\n，'
            main(ispTest = False)
    else:
        print '程序只接受一个参数,test或者下单数量'
   
