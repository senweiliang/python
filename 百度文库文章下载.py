from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
import time
def get_html():
	mobile_emulation = {"deviceName": "Google Nexus 5"}
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("mobileEmulation",mobile_emulation)
	browser = Browser('chrome', options=chrome_options)
	browser.visit(url)
	return browser.html,path,file_name
def download(wb_data,path,file_name):
	soup=BeautifulSoup(wb_data,'lxml')
	paragraphs=soup.find_all('p',attrs={'class':'txt'})#根据需要修改
	with open(path+'\\'+file_name+'.txt','wb') as file:
		for i in paragraphs:
			words=i.get_text(strip=True)
			if words:
				file.write(words.encode('UTF-8')+b'\r\n')	
if __name__=='__main__':
	url=input('请输入手机版百度文库url:')
	path=input('请输入保存途径:').replace('\\','/')+'/'
	print(path)
	file_name=input('请输入保存的文件名称:')
	wb_data,path,file_name=get_html()
	download(wb_data,path,file_name)
