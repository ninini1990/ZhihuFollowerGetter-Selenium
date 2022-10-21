# Author: 尼尼尼@知乎
# Author: 备份公众号： 尼尼尼不打拳
# HomePage: https://www.zhihu.com/people/nidaye2


import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from util.JsonUtil import getJsonUserOption
from util.TimeUtil import customSleep, getWaitTime, getReportTimeStamp
from util.WinUtil import getWinDesktopPath

from project.BrowserHandler import launchBrowser, getBrowserOptions, getPageCount, getPageUrl


# 获取知乎用户ID
userOptions = getJsonUserOption()
zhihuUserId = userOptions['zhihuUserId']

#启动浏览器
launchBrowser()

# 执行提示
print('============开始执行============')
print('===!!! 注意：config文件夹下，userOption.json中的"zhihuUserId"，必须先修改成自己的知乎用户ID!!!===')

# 登录时间
print('请在弹出的浏览器窗口中，手工登录自己的知乎账户，此处固定等待两分钟...')
print('如果已经是自己账户已登录的状态，则无需操作。等待执行即可。')
time.sleep(120)

# 初始化浏览器
print('开始初始化浏览器...')

opts = getBrowserOptions()
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
browser.implicitly_wait(10)

customSleep(5)
print('浏览器初始化完成')


# 检查功能函数
def checkLink(browser):
    try:
        # 设置全局变量
        allLinkList = []
        # pageBase = 'https://www.zhihu.com/people/poet0/followers?page='
        # pageBase = 'https://www.zhihu.com/people/nidaye2/followers?page='
        pageBase = 'https://www.zhihu.com/people/' + zhihuUserId + '/followers?page='

        # 获取对应页面Seletor
        # selectors = getJsonSelectors()
        # selector = selectors[pageName]

        # 进入该页面类型的首页
        url = getPageUrl(pageBase, 1)
        browser.get(url)

        # 获取该页面类型的总页数
        pageCount = getPageCount(browser)
        pageNum = 1

        time.sleep(5)

        # 获取该页面类型要检查的全部链接
        print("开始获取页面中的链接...")
        # while(pageNum <= 2):
        while(pageNum <= pageCount):
            print('页数: ', pageNum)
        # 拼接页面URL并打开对应页面
            pageUrl = getPageUrl(pageBase, str(pageNum))
            browser.get(pageUrl)

            # 等待页面加载
            customSleep(getWaitTime())
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # 获取当前页上所有关注者链接
            currentFollowerList = browser.find_elements(By.CSS_SELECTOR, 'div[class="List-item"]')
            for item in currentFollowerList:
                headNode = item.find_element(By.CSS_SELECTOR, 'div[class="UserItem-title"] a')
                #userNameNode = item.find_element(By.CSS_SELECTOR, 'div[class="css-1gomreu"]')
                # print(headNode.is_displayed())
                # userName = headNode.get_attribute('innerHTML')
                # print('用户名为：', userName)
                #nameNode = item.find_element(By.CSS_SELECTOR,'div[class="css-1gomreu"]');
                userName = headNode.text

                link = headNode.get_property('href')

                statusNode = item.find_element(By.CSS_SELECTOR, 'span[class="FollowStatus"]')
                status = statusNode.text

                metaNode = item.find_element(By.CSS_SELECTOR, 'div[class="ContentItem-meta"]')
                # desc =''
                # try:
                #     descNode = metaNode.find_element(By.CSS_SELECTOR, 'div[class="ztext"]')
                #     desc = descNode.text
                # except Exception as e:
                #     print('没有简介')

                # spanNodes = metaNode.find_elements(By.CSS_SELECTOR, 'div[class="ContentItem-status"] > span')
                # print(len(spanNodes))
                # follower = '0'
                # if len(spanNodes) != 0:
                #     follower = spanNodes[-1].text

                followerNode = item.find_element(By.CSS_SELECTOR, 'div[class="ContentItem"]')
                follower = 0

                # 有时关注者信息的JSON解析会出错，做一下异常处理. 异常时赋值为 -1
                try:
                    dataStr = followerNode.get_attribute('data-za-extra-module')
                    dataDict = json.loads(dataStr)
                    follower = dataDict['card']['content']['follower_num']
                except Exception as e:
                    follower = -1
                    print('当前关注者JSON处理出错，继续下一个:', e)

                temp = {'pageNum': str(pageNum), 'link': link, 'userName': userName, 'follower': follower, 'status': status}
                # print(temp)
                allLinkList.append(temp)

            pageNum = pageNum + 1

        # 按关注者数量降序排列
        allLinkList.sort(key=lambda item: item['follower'], reverse=True)
        # 生成结果
        print('正在生成结果...总数量：', len(allLinkList))
        stylePath = '\"' + __file__ + "\\..\\scripts\\style.css" + '\"'

        # 组装html
        htmlHeader = '<!DOCTYPE html><html lang="cn"><head><meta charset="utf-8"><title> 统计结果 </title><link rel="stylesheet" href=' + stylePath +'></head><body>'

        summary = '<p><div><b> 关注者总数量: ' + str(len(allLinkList)) + '</b><p><div><b>注：如显示为 -1 表示获取数据异常，不代表真实数据。</b></div><p><table class="hovertable">'

        table = '<th>所属页码</th><th>用户</th><th>关注者数量</th><th>互关状态</th>'

        # 存在被屏蔽回答时，填充报告页面
        for item in allLinkList:
            pageNum = item['pageNum']
            link = '<a href=' + item['link'] + ' target = "_blank">' + item['userName'] + '</a>'
            cell = '<tr><td>' + pageNum + '</td><td>' + link + '</td><td>' + str(item['follower']) + '</td><td>' + item['status'] +'</td><tr>'
            table = table + cell

        htmlFoot = '</table></div></body></html>'
        reportPage = htmlHeader + summary + table + htmlFoot

        reportFileName = 'report_' + getReportTimeStamp() + '.html'
        reportFilePath = getWinDesktopPath() + reportFileName

        try:
            f = open(reportFilePath, 'w', encoding="utf-8")
            f.write(reportPage)
            f.close()
            print("生成结果文件成功:  {0}".format(reportFilePath))
            print('============关注者信息统计完成,请查看报告文件============')
            return reportFilePath
        except Exception as e:
            print("生成结果文件失败", e)

    except Exception as e:
        print("发生错误：", e)

    finally:
        input('按回车键退出...')


# 执行入口
checkLink(browser)


