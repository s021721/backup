#-*- coding:utf-8 -*-
#run like: python alarm.py 002233 GTR(LSS) 12
#or write batch items in txt file like 002233 GTR 12
#then call python alarm.py d:/stocks.txt
from array import *
from time import sleep
import tushare
import time
from sys import argv
import winsound
import threading
import easyquotation
toAlarmCnt=3
quotation= easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

def chinese(data):  
	count = 0  
	for s in data:  
		if ord(s) > 127:  
			count += 1  
	return count  

#conditionsMap like GTR(LSS) 13
def stockAlarm(stockCodeList, conditionsMap):
	remainAlarmCntMap={}
	print ("**** Alarm stock list",stockCodeList)
	while 1:
		try:						
			sleep(1.5)
			#从两个数据源得到股价避免乌龙指
			priceList1= tushare.get_realtime_quotes(stockCodeList)			
			priceMap2=quotation.stocks(stockCodeList)
			
			maxStockNameLen=0
			skipStocks=""
			attnStr="********************"

			print (attnStr + time.strftime(" %H:%M:%S ", time.localtime()) + attnStr)
			for i in range(0, len(priceList1)):
				#print (priceList1)
				stockCode=priceList1.ix[i,'code']
				stockName=priceList1.ix[i,'name']
				
				if len(stockName) > maxStockNameLen:
					maxStockNameLen=len(stockName)
				if stockCode not in remainAlarmCntMap.keys():
					remainAlarmCntMap[stockCode]=toAlarmCnt

				condition=conditionsMap[stockCode]
				isLss=(condition.split(' ')[0].lower()=='lss')
				isGtr=(condition.split(' ')[0].lower()=='gtr')
				tgtPrice=float(condition.split(' ')[1])
				condition=condition.split(' ')[0] + " " + '%.2f'%float(tgtPrice)
				#print (isLss, isGtr, tgtPrice,condition.split(' ')[0])
				
				curPrice=float(priceList1.ix[i,'price'])
				curPrice2=priceMap2[stockCode]['now']

				twoPriceGap=abs(curPrice2-curPrice)
				#print ("twoPriceGap",twoPriceGap, '',curPrice)
				#如果两个数据源得到的股价差距过大，跳过本次检查
				if twoPriceGap >= 0.03:
					#print (stockCode,stockName,"big gap",'%.2f'%float(twoPriceGap), "two price: ", curPrice,curPrice2)
					skipStocks=skipStocks + stockCode + " " + stockName + " " + "big gap" + " " + '%.2f'%float(twoPriceGap) + "  " + "two price: " + "  " + str(curPrice) + " " + str(curPrice2) + "\n"
					continue

				curPriceStr= '%.2f'%float(curPrice)
				#上涨下跌gap控制在0-9避免乌龙指
				upDownGap=(100 * abs(curPrice-tgtPrice))/curPrice
				isRightGap=(upDownGap>0 and upDownGap <= 9)
				#print ("upDownGap",upDownGap,isRightGap)

				matchAlart=False
				isPlayAlarmSound=False
				if isGtr and curPrice <= tgtPrice:
					remainAlarmCntMap[stockCode]=toAlarmCnt
				if isLss and curPrice >= tgtPrice:
					remainAlarmCntMap[stockCode]=toAlarmCnt
				if  isLss and curPrice < tgtPrice:
					matchAlart=True
					if isRightGap and remainAlarmCntMap[stockCode] > 0:
						isPlayAlarmSound=True
						remainAlarmCntMap[stockCode]=remainAlarmCntMap[stockCode]-1
				if isGtr and curPrice > tgtPrice:
					matchAlart=True
					if isRightGap and remainAlarmCntMap[stockCode] > 0:
						isPlayAlarmSound=True
						remainAlarmCntMap[stockCode]=remainAlarmCntMap[stockCode]-1
				matchStr='False'
				if matchAlart:
					matchStr='****** True'
				if isPlayAlarmSound:
					matchStr='### True'
				mat = "{:8}{:6}{:8}{:12}{:12}"
				number = chinese(stockName)
				newStr = '{0:{wd}}'.format(stockName,wd=10-number)
				print(mat.format(stockCode,newStr, curPriceStr, condition, matchStr))
				if isPlayAlarmSound:
					winsound.PlaySound('d:\sound\stockAlert.wav', winsound.SND_FILENAME)
			print (skipStocks)
		except Exception as e:
			print (e)
			#return
#批量监控命令行传入的列表文件d:/stockAlarmList.txt
if 'txt' in argv[1]:
	stockCodeListAry=[]
	conditionsMap={}
	stockAlarm
	with open(argv[1],'r') as infile:
		for line in infile:
			if len(line.split(' ')) < 2:
				continue
			stockCode=line.split(' ')[0]
			conditionsMap[stockCode]=(line.split(' ')[1] + ' ' + line.split(' ')[2]).strip('\n')
			stockCodeListAry.append(stockCode)
	stockAlarm(stockCodeListAry,	conditionsMap)  
else:
	stockAlarm([argv[1]],{argv[1]:argv[2] + ' ' + argv[3]})
