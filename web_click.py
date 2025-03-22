from playwright.sync_api import sync_playwright
import time
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
        time.sleep(2)  # 可以替换为更精确的等待方式
        
        # 在对话框输入内容
        page.fill("xpath=/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]", input_text)  # 选择器需要根据实际页面结构调整
        page.keyboard.press("Enter")  # 按回车键发送请求
        
        # 等待结果完全加载
        time.sleep(2)  # 可以替换为更精确的等待方式

        # 等待结果加载完成，等待特定元素出现
        # page.wait_for_selector("xpath=")
        
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

if __name__ == "__main__":
    input_text= "搜索一下：请搜索安徽省高级人民法院的领导班子组成。请以以下格式进行输出。如果公开资料个人信息较少也不要不填写，查找不到的部分写NA即可。所在法院：xx；姓名：xx；目前法院职务：领导目前除在法院任职外，在人大、政协等其他政法机构的同步任职情况（如不存在填写无）：xxx；性别：xx；籍贯：xx；年龄：xx；教育经历：xx；过往工作履历：xx；依据网址：xx。得到结果后以json格式输出"
    web_click(input_text)