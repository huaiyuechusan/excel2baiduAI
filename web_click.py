from playwright.sync_api import sync_playwright
import time
import json
import pyperclip

def web_click(input_text):
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # headless=False可以看到浏览器操作过程
        
        # 创建新的浏览器上下文和页面
        context = browser.new_context()
        page = context.new_page()
        
        # 导航到目标页面（这里使用百度页面作为示例）
        page.goto("https://chat.baidu.com/search")
        
        
        # 等待对话框出现
        time.sleep(5)  # 可以替换为更精确的等待方式
        
        # 在对话框输入内容
        page.fill("xpath=/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]", input_text)  # 选择器需要根据实际页面结构调整
        page.keyboard.press("Enter")  # 按回车键发送请求
        page.fill("xpath=/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]","")
        
        # 等待结果加载完成，等待特定元素（发送按钮再去出现）出现。
        # page.wait_for_selector("xpath=/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/i")
        """
        /html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/i
        /html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/i
        /html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/i
        """
        """"
        /html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/i
        /html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/i
        """
        page.wait_for_selector(
               'text="DeepSeek-R1满血版 回答完成"',
                timeout=600000
            )

        # 点击Copy按钮
        page.get_by_text('Copy Code').click() 
        
        # 获取剪贴板内容（需要系统支持）
        time.sleep(1)  # 给一点时间让内容复制到剪贴板
        copied_json = pyperclip.paste()
        
        # 打印到控制台
        print("复制的JSON内容:")
        print(copied_json)
        
        # 关闭浏览器
        browser.close()
        return copied_json

if __name__ == "__main__":
    input_text= "搜索一下。\n    请搜索安徽省合肥市中级人民法院的领导班子组成。\n    请以以下格式进行输出。\n    如果公开资料个人信息较少也不要不填写，查找不到的部分写NA即可。\n    所在法院：xx；领导姓名，：xx；领导在法院的职务：xx；\n    领导目前除在法院任职外，在人大、政协等其他政法机构的同步任职情况（如不存在填写无）：xxx；\n    领导性别：xx；领导籍贯：xx；领导出生年份：xx；领导受教育经历：xx；领导最高学历：xx;\n    领导上任前在其他职位的历史任职信息：xx；\n    信息依据的网站地址：xx。\n    得到结果后以json格式输出，必须返回严格JSON格式。"
    leaders_json = web_click(input_text)
    # 解析JSON字符串为Python对象（如果返回的是字符串）
    if isinstance(leaders_json, str):
        leaders = json.loads(leaders_json)
    else:
        leaders = leaders_json