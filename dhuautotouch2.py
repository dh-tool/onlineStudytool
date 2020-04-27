__author__ = "carl"
import uiautomator2 as u2
from time import sleep
import os
import subprocess
from optparse import OptionParser
import re

def finddevices():
    data = subprocess.Popen('adb devices', stdout=subprocess.PIPE, universal_newlines=True)
    data_info = data.stdout.read()
    devices = re.findall(r'(.*?)\s+device', data_info)
    if len(devices) > 1:
        deviceIds = devices[1:]
        print('共找到%s个手机' % str(len(devices)-1))
        for i in deviceIds:
            print('ID为%s' % i)
        return deviceIds
    else:
        print('没有找到手机，请检查')
        return

devicelst=finddevices()
d = u2.connect(devicelst[0])
d.click_post_delay = 1.5
applist=d.app_list_running()
if applist:
    print(applist)
    sess = d.session("com.fingertip.main")
    '''d.app_start("com.fingertip.main", ".MainActivity")'''
    print('app_start')
    d(resourceId="com.fingertip.main:id/tab_personal_layout").click()
    if(d(resourceId="com.fingertip.main:id/lg_name_et")):
        d(resourceId="com.fingertip.main:id/lg_name_et").set_text('')
        d(resourceId="com.fingertip.main:id/lg_password_tv").set_text('')
        d(resourceId="com.fingertip.main:id/lg_login_btn").click()
d.xpath('//*[@resource-id="com.fingertip.main:id/tab_server_layout"]/android.widget.LinearLayout[1]').click()
sleep(3)
d(resourceId="com.fingertip.main:id/server_3_ly").click()
print('点击考勤查询')
sleep(3)
d(resourceId="com.fingertip.main:id/item_work_course_img").click()
print('考勤时间')
courcelst=d(resourceId="com.fingertip.main:id/course_ware_name_text")
lastname=courcelst[len(courcelst)-1].get_text()
namelist=[]

topposi=courcelst[0].bounds()[1]
bottomposi=courcelst[len(courcelst)-1].bounds()[1]
d.swipe(0, bottomposi, 0, topposi, 0.5)
print(topposi)
print(bottomposi)
print(lastname)
while lastname not in namelist:
    namelist.append(lastname)
    print(len(namelist))
    acourcelst=d(resourceId="com.fingertip.main:id/course_ware_name_text")
    lastname=acourcelst[len(courcelst)-1].get_text()
    topposi=acourcelst[0].bounds()[1]
    bottomposi=acourcelst[len(courcelst)-1].bounds()[1]
    d.swipe(0, bottomposi, 0, topposi, 0.5)
    print("lastname",lastname)
    print(namelist)
    print(topposi)
    print(bottomposi)
  