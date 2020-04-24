# Python+uiautomator2手机UI自动化
东华网校在线学习小工具，可以辅助点击下一个视频按钮，基于OCR，winform
设备连接方法，有两种
1. 通过WiFi，假设设备IP 192.168.5.4和您的PC在同一网络中

import uiautomator2 as u2
 
d = u2.connect('192.168.5.4') # alias for u2.connect_wifi('192.168.5.4')
print(d.info)
2. 通过USB， 假设设备序列是123456789F（见adb devices）

import uiautomator2 as u2
 
d = u2.connect('123456789F') # alias for u2.connect_usb('123456789F')
print(d.info)
检查并维持设备端守护进程处于运行状态
d.healthcheck()
连接本地USB设备
需要设备曾经使用 python -m uiautomator2 init 初始化过

d = u2.connect_usb("{Your-Device-Serial}")
如何停用UiAutomator的守护程序?
1. 直接打开uiautomator app（init成功后，就会安装上的），点击关闭UIAutomator

2.  d.service("uiautomator").stop()

打开调试开关
>>> d.debug = True
>>> d.info
12:32:47.182 $ curl -X POST -d '{"jsonrpc": "2.0", "id": "b80d3a488580be1f3e9cb3e926175310", "method": "deviceInfo", "params": {}}' 'http://127.0.0.1:54179/jsonrpc/0'
12:32:47.225 Response >>>
{"jsonrpc":"2.0","id":"b80d3a488580be1f3e9cb3e926175310","result":{"currentPackageName":"com.android.mms","displayHeight":1920,"displayRotation":0,"displaySizeDpX":360,"displaySizeDpY":640,"displayWidth":1080,"productName"
:"odin","screenOn":true,"sdkInt":25,"naturalOrientation":true}}
<<< END
安装应用，只能从URL安装
d.app_install（' http://some-domain.com/some.apk '）
安装应用
d.app_start（“ com.example.hello_world ”）＃ start包名称
停止应用
＃相当于`am force-stop`，因此你可能丢失数据 
d.app_stop（ “ com.example.hello_world ”） 
＃相当于`pm clear` 
d.app_clear（ ' com.example.hello_world '）
推送和拉取文件
把文件推送到设备
# push to a folder
d.push("foo.txt", "/sdcard/")
# push and rename
d.push("foo.txt", "/sdcard/bar.txt")
# push fileobj
with open("foo.txt", 'rb') as f:
    d.push(f, "/sdcard/")
# push and change file access mode
d.push("foo.sh", "/data/local/tmp/", mode=0o755)
从设备中提取文件
d.pull("/sdcard/tmp.txt", "tmp.txt")
 
# FileNotFoundError will raise if the file is not found on the device
d.pull("/sdcard/some-file-not-exists.txt", "tmp.txt")
跳过弹窗，禁止弹窗
d.disable_popups（） ＃自动跳过弹出窗口 
d.disable_popups（假）＃禁用自动跳过弹出窗口
Session
Session represent an app lifestyle. 可用于启动应用，检测应用崩溃

启动应用
sess = d.session（“ com.netease.cloudmusic ”）
Attach to the running app
sess = d.session（“ com.netease.cloudmusic ”，attach = True）
检测应用崩溃
# When app is still running
sess(text="Music").click() # operation goes normal
 
# If app crash or quit
sess(text="Music").click() # raise SessionBrokenError
# other function calls under session will raise SessionBrokenError too
# check if session is ok.
# Warning: function name may change in the future
sess.running() # True or False
检索设备信息
获取基本信息
d.info
以下是可能的输出：

{ 
    u'displayRotation': 0,
    u'displaySizeDpY': 640,
    u'displaySizeDpX': 360,
    u'currentPackageName': u'com.android.launcher',
    u'productName': u'takju',
    u'displayWidth': 720,
    u'sdkInt': 18,
    u'displayHeight': 1184,
    u'naturalOrientation': True
}
获取窗口大小
print(d.window_size())
# device upright output example: (1080, 1920)
# device horizontal output example: (1920, 1080)
获取最新的应用信息。对于某些Android设备，输出可能为空
print(d.current_app())
# Output example 1: {'activity': '.Client', 'package': 'com.netease.example', 'pid': 23710}
# Output example 2: {'activity': '.Client', 'package': 'com.netease.example'}
# Output example 3: {'activity': None, 'package': None}
获取设备序列号
print(d.serial)
# output example: 74aAEDR428Z9
关键事件
打开/关闭屏幕
d.screen_on（）＃打开屏幕 
d.screen_off（）＃关闭屏幕
获取当前屏幕状态
d.info.get（' screenOn '）＃ require Android> = 4.4
Home / Back 按键操作
d.press("home") # press the home key, with key name
d.press("back") # press the back key, with key name
d.press(0x07, 0x02) # press keycode 0x07('0') with META ALT(0x02)
目前支持这些密钥名称：
home
back
left
right
up
down
center
menu
search
enter
delete ( or del)
recent (recent apps)
volume_up
volume_down
volume_mute
camera
power
 

解锁屏幕
d.unlock()
# This is equivalent to
# 1. launch activity: com.github.uiautomator.ACTION_IDENTIFY
# 2. press the "home" key
手势与设备的交互
点击屏幕
d.click（x，y）
双击
d.double_click（x，y）
d.double_click（X，Y，0.1）＃默认之间的两个点击持续时间为0.1秒
长按一下屏幕
d.long_click（x，y）
d.long_click（X，Y，0.5）＃长按0.5秒（默认）
Swipe
d.swipe(sx, sy, ex, ey)
d.swipe(sx, sy, ex, ey, 0.5) # swipe for 0.5s(default)
拖动
d.drag(sx, sy, ex, ey)
d.drag(sx, sy, ex, ey, 0.5) # Drag for 0.5s(default)
滑动点   多用于九宫格解锁，提前获取到每个点的相对坐标（这里支持百分比）
# swipe from point(x0, y0) to point(x1, y1) then to point(x2, y2)
# time will speed 0.2s bwtween two points
d.swipe((x0, y0), (x1, y1), (x2, y2), 0.2)
注意：单击，滑动，拖动操作支持百分比位置值。例：

d.long_click(0.5, 0.5) 表示长按屏幕中心

屏幕相关的
检索/设置设备方向     --可能的方向如下
natural or n
left or l
right or r
upsidedown or u (can not be set)
# 检索方向。输出可以是 "natural" or "left" or "right" or "upsidedown"
orientation = d.orientation
 
# WARNING: not pass testing in my TT-M1
# set orientation and freeze rotation.
# notes: setting "upsidedown" requires Android>=4.3.
d.set_orientation('l') # or "left"
d.set_orientation("l") # or "left"
d.set_orientation("r") # or "right"
d.set_orientation("n") # or "natural"
Freeze/Un-freeze rotation
# freeze rotation
d.freeze_rotation()
# un-freeze rotation
d.freeze_rotation(False)
截图
# 截取并保存到计算机上的文件，需要Android> = 4.2。
d.screenshot("home.jpg")
 
# 得到PIL.Image格式的图像. 但你必须先安装pillow
image = d.screenshot() # default format="pillow"
image.save("home.jpg") # or home.png. Currently, 只支持png and jpg格式的图像
 
# 得到OpenCV的格式图像。当然，你需要numpy和cv2安装第一个
import cv2
image = d.screenshot(format='opencv')
cv2.imwrite('home.jpg', image)
 
# 获取原始JPEG数据
imagebin = d.screenshot(format='raw')
open("some.jpg", "wb").write(imagebin)
Dump UI hierarchy
# get the UI hierarchy dump content (unicoded).
xml = d.dump_hierarchy()
打开通知或快速设置
d.open_notification（）
d.open_quick_settings（）
选择
Selector是一种在当前窗口中标识特定UI对象的便捷机制。
# 选择文本为'Clock'的对象，其className为'android.widget.TextView'd 
d(text='Clock', className='android.widget.TextView')
选择器支持以下参数。有关详细信息，请参阅UiSelector Java文档。
text，textContains，textMatches，textStartsWith
className， classNameMatches
description，descriptionContains，descriptionMatches，descriptionStartsWith
checkable，checked，clickable，longClickable
scrollable，enabled，focusable，focused，selected
packageName， packageNameMatches
resourceId， resourceIdMatches
index， instance
 

Children and siblings
children
# get the children or grandchildren
d(className="android.widget.ListView").child(text="Bluetooth")
siblings
# get siblings
d(text="Google").sibling(className="android.widget.ImageView")
children by text or description or instance
# get the child matching the condition className="android.widget.LinearLayout"
# and also its children or grandchildren with text "Bluetooth"
d(className="android.widget.ListView", resourceId="android:id/list") \
 .child_by_text("Bluetooth", className="android.widget.LinearLayout")
 
# 通过允许滚动搜索来获取子项
d(className="android.widget.ListView", resourceId="android:id/list") \
 .child_by_text(
    "Bluetooth",
    allow_scroll_search=True,
    className="android.widget.LinearLayout"
  )
child_by_description is to find children whose grandchildren have the specified description, other parameters being similar to child_by_text.

child_by_instance是在子层次结构中的任何位置找到具有子UI元素的子元素，该元素位于指定的实例中。它在可见视图上执行而无需滚动.

UiScrollable，getChildByDescription，getChildByText，getChildByInstance
UiCollection，getChildByDescription，getChildByText，getChildByInstance
 

打开WIFI旁边的ON
要将开关小部件单击到TextView的“Wi-Fi”，我们需要先选择切换小部件。但是，根据UI层次结构，存在多个交换机窗口小部件并且具有几乎相同的属性。通过className选择将不起作用。或者，以下选择策略将有助于：

d(className="android.widget.ListView", resourceId="android:id/list") \
  .child_by_text("Wi‑Fi", className="android.widget.LinearLayout") \
  .child(className="android.widget.Switch") \
  .click()
相对定位
此外，我们可以使用相对定位方法来获取视图：left，right，top，bottom。

d(A).left(B)，选择A左侧的B.
d(A).right(B)，选择A右侧的B.
d(A).up(B)，选择B以上A.
d(A).down(B)，在A下选择B.
因此，对于上述情况，我们可以选择它：

##选择“Wi-Fi”右侧的“开关” 
d(text="Wi‑Fi").right(className="android.widget.Switch").click()
多个实例
有时屏幕可能包含多个具有相同属性的视图，例如文本，那么您必须使用选择器中的“instance”属性来选择一个合格的实例，如下所示：

d（text = “ Add new ”，instance = 0）   ＃表示带有文本“Add new”的第一个实例
另外，uiautomator2提供了类似列表的API（类似于jQuery）：

# get the count of views with text "Add new" on current screen
d(text="Add new").count
 
# same as count property
len(d(text="Add new"))
 
# get the instance via index
d(text="Add new")[0]
d(text="Add new")[1]
...
 
# iterator 迭代器
for view in d(text="Add new"):
    view.info  # ...
注意：以列表方式使用选择器时，必须确保屏幕上的UI元素保持不变。否则，当迭代列表时可能发生Element-Not-Found错误

获取所选的ui对象状态及其信息

检查特定的UI对象是否存在

d(text="Settings").exists # True if exists, else False
d.exists(text="Settings") # alias of above property.
 
# advanced usage
d(text="Settings").exists(timeout=3) # wait Settings appear in 3s, same as .wait(3)
检索特定UI对象的信息
d(text = “ Settings ”).info
以下是可能的输出：

{ u'contentDescription': u'',
u'checked': False,
u'scrollable': False,
u'text': u'Settings',
u'packageName': u'com.android.launcher',
u'selected': False,
u'enabled': True,
u'bounds': {u'top': 385,
            u'right': 360,
            u'bottom': 585,
            u'left': 200},
u'className': u'android.widget.TextView',
u'focused': False,
u'focusable': True,
u'clickable': True,
u'chileCount': 0,
u'longClickable': True,
u'visibleBounds': {u'top': 385,
                    u'right': 360,
                    u'bottom': 585,
                    u'left': 200},
u'checkable': False
}
获取/设置/清除可编辑字段的文本（例如，EditText小部件）
d（text = “ Settings ”）.get_text（）   # get widget text 
d（text = “ Settings ”）.set_text（“ My text ... ”）   ＃设置文本 
d（text = “ Settings ”）.clear_text（ ）   ＃清除文字
获取Widget中心点
x, y = d(text="Settings").center()
对选定的UI对象执行单击操作
执行单击特定对象
# 单击特定ui对象的中心
d(text="Settings").click()
# wait元素最多显示10秒然后单击 
d(text="Settings").click(timeout=10)
# 请在10秒时点击，默认的超时0
clicked = d(text='Skip').click_exists(timeout=10.0)
# 点击直到元素不见了，返回布尔
is_gone = d(text="Skip").click_gone(maxretry=10, interval=1.0) # maxretry default 10, interval default 1.0
长按特定的UI对象
# 长按特定UI对象的中心
d(text="Settings").long_click()
特定UI对象的手势操作
将UI对象拖向另一个点或另一个UI对象
# notes : Android<4.3不能使用drag.
# 0.5S后，将UI对象拖动到屏幕点（x，y）
d(text="Settings").drag_to(x, y, duration=0.5)
# drag the UI object to (the center position of) another UI object, in 0.25 second
d(text="Settings").drag_to(text="Clock", duration=0.25)
两点手势操作，从一个点到另一个点
d(text="Settings").gesture((sx1, sy1), (sx2, sy2), (ex1, ey1), (ex2, ey2))
特定UI对象上的两点手势
支持两种手势：
In，从边缘到中心
Out，从中心到边缘
# notes : pinch can not be set until Android 4.3.
# 从边缘到中心. here is "In" not "in"
d(text="Settings").pinch_in(percent=100, steps=10)
# 从中心到边缘
d(text="Settings").pinch_out()
等到特定UI出现或消失
# 一直等到UI对象出现
d(text="Settings").wait(timeout=3.0) # return bool
# 一直等到UI对象消失
d(text="Settings").wait_gone(timeout=1.0)
默认超时为20秒。有关详细信息，请参阅全局设置

在特定的ui对象上执行fling（可滚动）
对特定的ui对象执行fling（可滚动）
可能的属性

horiz 要么 vert
forward或backward或toBeginning或toEnd
# fling forward(default) vertically(default) 
d(scrollable=True).fling()
# fling forward horizontally
d(scrollable=True).fling.horiz.forward()
# fling backward vertically
d(scrollable=True).fling.vert.backward()
# fling to beginning horizontally
d(scrollable=True).fling.horiz.toBeginning(max_swipes=1000)
# fling to end vertically
d(scrollable=True).fling.toEnd()
在特定的ui对象上执行Scroll（可滚动））
Possible properties:

horiz or vert
forward or backward or toBeginning or toEnd, or to
# scroll forward(default) vertically(default)
d(scrollable=True).scroll(steps=10)
# scroll forward horizontally
d(scrollable=True).scroll.horiz.forward(steps=100)
# scroll backward vertically
d(scrollable=True).scroll.vert.backward()
# scroll to beginning horizontally
d(scrollable=True).scroll.horiz.toBeginning(steps=100, max_swipes=1000)
# scroll to end vertically
d(scrollable=True).scroll.toEnd()
# scroll forward vertically until specific ui object appears
d(scrollable=True).scroll.to(text="Security")
Watcher
当selector找不到匹配项时，您可以注册watchers 以执行某些操作。

注册watchers
当selector找不到匹配项时，uiautomator2将运行所有注册的watcher。

条件匹配时单击目标
d.watcher("AUTO_FC_WHEN_ANR").when(text="ANR").when(text="Wait") \
                             .click(text="Force Close")
# d.watcher(name) ## creates a new named watcher.
#  .when(condition)  ## the UiSelector condition(条件) of the watcher.
#  .click(target)  ## 对目标UiSelector执行单击操作
关于点击还有一个技巧。您可以使用不带参数的click。

d.watcher("ALERT").when(text="OK").click()
# Same as
d.watcher("ALERT").when(text="OK").click(text="OK")
Press key when a condition becomes true
d.watcher("AUTO_FC_WHEN_ANR").when(text="ANR").when(text="Wait") \
                             .press("back", "home")
# d.watcher(name) ## creates a new named watcher.
#  .when(condition)  ## the UiSelector condition of the watcher.
#  .press(<keyname>, ..., <keyname>.()  ## 按顺序依次按键.
检查命名的watcher是否被触发
触发watcher，这意味着watcher已经运行且所有条件都匹配。

d.watcher("watcher_name").triggered
# 在指定的watcher触发的情况下为true，否则为false
删除已命名的watcher
# remove the watcher
d.watcher("watcher_name").remove()
列出所有watcher
d.watchers
# 所有注册watchers的列表
检查是否有任何条件触发的watcher
d.watchers.triggered
#  true in case of any watcher triggered
重置reset所有触发的watcher
# reset all triggered watchers, after that, d.watchers.triggered will be false.
d.watchers.reset()
删除watcher
# remove all registered watchers
d.watchers.remove()
# remove the named watcher, same as d.watcher("watcher_name").remove()
d.watchers.remove("watcher_name")
强制运行所有watcher
# force to run all registered watchers
d.watchers.run()
页面更新时运行所有watcher。
通常可以用来自动点击权限确认框，或者自动安装

d.watcher("OK").when(text="OK").click(text="OK")
# enable auto trigger watchers
d.watchers.watched = True
 
# disable auto trigger watchers
d.watchers.watched = False
 
# get current trigger watchers status
assert d.watchers.watched == False
另外文档还是有很多没有写，推荐直接去看源码init .py

全局设置
# set delay 1.5s after each UI click and click
d.click_post_delay = 1.5 # default no delay
 
# set default element wait timeout (seconds)
d.wait_timeout = 30.0 # default 20.0
UiAutomator中的超时设置(隐藏方法)

>> d.jsonrpc.getConfigurator() 
{'actionAcknowledgmentTimeout': 500,
 'keyInjectionDelay': 0,
 'scrollAcknowledgmentTimeout': 200,
 'waitForIdleTimeout': 0,
 'waitForSelectorTimeout': 0}
 
>> d.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})
{'actionAcknowledgmentTimeout': 500,
 'keyInjectionDelay': 0,
 'scrollAcknowledgmentTimeout': 200,
 'waitForIdleTimeout': 100,
 'waitForSelectorTimeout': 0}
为了防止客户端程序响应超时，waitForIdleTimeout状语从句：waitForSelectorTimeout目前已对划线0

参考：谷歌uiautomator配置器

输入法
这种方法通常用于不知道控件的情况下的输入。第一步需要切换输入法，然后发送ADB广播命令，具体使用方法如下

d.set_fastinput_ime(True) # 切换成FastInputIME输入法
d.send_keys("你好123abcEFG") # adb广播输入
d.clear_text() # 清除输入框所有内容(Require android-uiautomator.apk version >= 1.0.7)
d.set_fastinput_ime(False) # 切换成正常的输入法
Toast
在手机的屏幕上显示Toast
d.toast.show("Hello world")
d.toast.show("Hello world", 1.0) # 显示 1.0s, 默认 1.0s
获取 Toast
# [Args]
# 5.0: max wait timeout. Default 10.0
# 10.0: cache time. return cache toast if already toast already show up in recent 10 seconds. Default 10.0 (Maybe change in the furture)
# "default message": return if no toast finally get. Default None
d.toast.get_message(5.0, 10.0, "default message")
 
# common usage
assert "Short message" in d.toast.get_message(5.0, default="")
 
# clear cached toast
d.toast.reset()
# Now d.toast.get_message(0) is None
XPath
For example: 其中一个节点的内容

<android.widget.TextView
  index="2"
  text="05:19"
  resource-id="com.netease.cloudmusic:id/qf"
  package="com.netease.cloudmusic"
  content-desc=""
  checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false"
  scrollable="false" long-clickable="false" password="false" selected="false" visible-to-user="true"
  bounds="[957,1602][1020,1636]" />
xpath定位和使用方法

# wait exists 10s
d.xpath("//android.widget.TextView").wait(10.0)
# find and click
d.xpath("//*[@content-desc='分享']").click()
# get all text-view text, attrib and center point
for elem in d.xpath("//android.widget.TextView").all():
    print("Text:", elem.text)
    # Dictionary eg: 
    # {'index': '1', 'text': '999+', 'resource-id': 'com.netease.cloudmusic:id/qb', 'package': 'com.netease.cloudmusic', 'content-desc': '', 'checkable': 'false', 'checked': 'false', 'clickable': 'false', 'enabled': 'true', 'focusable': 'false', 'focused': 'false','scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'visible-to-user': 'true', 'bounds': '[661,1444][718,1478]'}
    print("Attrib:", elem.attrib)
    # Coordinate eg: (100, 200)
    print("Position:", elem.center())
测试方法
$ adb forward tcp:9008 tcp:9008
$ curl 127.0.0.1:9008/ping
# expect: pong
 
$ curl -d '{"jsonrpc":"2.0","method":"deviceInfo","id":1}' 127.0.0.1:9008/jsonrpc/0
# expect JSON output
Google uiautomator与uiautomator2的区别
API相似但是不完全兼容
uiautomator2是安卓项目，而uiautomator是Java项目
uiautomator2可以输入中文，而uiautomator的Java工程需借助utf7输入法才能输入中文
uiautomator2必须明确EditText框才能向里面输入文字，uiautomator直接指定父类也可以在子类中输入文字
uiautomator2获取控件速度比uiautomator快
远程查看
手机python -m uiautomator2 init之后，浏览器输入 <device_ip:7912>，会发现一个远程控制功能，延迟非常低噢。^_^

手机USB连接后，自动调用init命令
adbkit-init

项目原地址：https://github.com/openatx/uiautomator2
————————————————
版权声明：本文为CSDN博主「Ricky_Frog」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ricky_yangrui/java/article/details/81415365
