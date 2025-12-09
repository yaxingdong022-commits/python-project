import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# -------------------- 模块一：演习场定义 (无需修改) --------------------
mission_html = """
<html>
<head>
    <title>综合演习场</title>
    <style>
        #review_frame_container { display: none; margin-top: 20px; }
        #policy_modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4);
        }
        #policy_modal_content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 50%;
        }
        .close_button {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>幻影机械键盘 Pro</h1>
    <p>一款为专业开发者和游戏玩家设计的顶级键盘。</p>
    <button id="review-button">撰写评价</button>

    <!-- 【修复】将链接改为触发弹窗模态框，而不是打开新标签页 -->
    <a id="policy-link" href="javascript:void(0);">查看运费政策</a>

    <!-- 【新增】政策内容的模态弹窗 -->
    <div id="policy_modal">
        <div id="policy_modal_content">
            <span class="close_button" id="close_modal">&times;</span>
            <h2>我们的运费政策</h2>
            <p id="policy_content">所有订单享受次日达的极速快递服务。</p>
        </div>
    </div>

    <div id="review_frame_container">
        <iframe id="review_frame" srcdoc="
            <div id='review_form'>
                <h3>您的评价</h3>
                <input type='text' id='username_input' placeholder='您的昵称'><br><br>
                <textarea id='review_text' rows='4' cols='50' placeholder='写下您的使用感受...'></textarea><br><br>
                <button id='submit_review'>提交</button>
            </div>
            <div id='thank_you_message' style='display:none; color: green;'>
                感谢您的宝贵评价！
            </div>
        "></iframe>
    </div>

    <script>
        // 评价按钮逻辑（保持不变）
        document.getElementById('review-button').onclick = function() {
            document.getElementById('review_frame_container').style.display = 'block';
        };

        // iframe逻辑（保持不变）
        var iframe = document.getElementById('review_frame');
        iframe.onload = function() {
            if (!iframe.contentWindow) return;
            var iframeDoc = iframe.contentWindow.document;
            var submitButton = iframeDoc.getElementById('submit_review');
            if (submitButton) {
                submitButton.onclick = function() {
                    iframeDoc.getElementById('review_form').style.display = 'none';
                    iframeDoc.getElementById('thank_you_message').style.display = 'block';
                };
            }
        };

        // 【新增】政策链接点击后，显示模态弹窗（而不是打开新标签页）
        document.getElementById('policy-link').onclick = function() {
            document.getElementById('policy_modal').style.display = 'block';
        };

        // 【新增】关闭弹窗的逻辑
        document.getElementById('close_modal').onclick = function() {
            document.getElementById('policy_modal').style.display = 'none';
        };

        // 【新增】点击弹窗外部区域，也关闭弹窗
        window.onclick = function(event) {
            var modal = document.getElementById('policy_modal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };
    </script>
</body>
</html>
"""

# -------------------- 模块二：演习场加载 (无需修改) --------------------
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mission_ground.html")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(mission_html)
mission_url = Path(file_path).as_uri()

# -------------------- 模块三：任务执行 --------------------
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

try:
    # 载入演习场
    driver.get(mission_url)
    print("✅ 演习场已成功载入！\n")

    # ==================================================================
    #
    #                   【【【 您的任务区域 】】】
    #
    #      请在此处，根据下方的阶段目标，编写您的自动化代码
    #
    # ==================================================================

    # --- 阶段一：主世界互动 ---
    # 1.1: 点击ID为 `review-button` 的按钮
    # 1.2: 等待ID为 `review_frame` 的iframe可见
    print("--- 阶段一：执行主世界互动 ---")
    # 在这里编写您的代码...
    review_button=driver.find_element(By.ID,'review-button')
    review_button.click()
    wait.until(EC.presence_of_element_located((By.ID,'review_frame')))
    time.sleep(3)
    # --- 阶段二：渗透Iframe结界 ---
    # 2.1: 切换到 `review_frame`
    # 2.2: 在 `username_input` 中输入 "Selenium大师"
    # 2.3: 在 `review_text` 中输入 "这个综合演习太棒了！"
    # 2.4: 点击 `submit_review` 按钮
    # 2.5: 等待并打印 `thank_you_message` 的文本
    # 2.6: 返回主世界
    print("\n--- 阶段二：执行Iframe渗透 ---")
    # 在这里编写您的代码...
    driver.switch_to.frame('review_frame')
    username=driver.find_element(By.ID,'username_input')
    username.send_keys('Selenium大师')
    text=driver.find_element(By.ID,'review_text')
    text.send_keys('这个综合演习太棒了')
    submit_button=driver.find_element(By.ID,'submit_review')
    submit_button.click()
    wait.until(EC.presence_of_element_located((By.ID,'thank_you_message')))
    time.sleep(3)
    driver.switch_to.default_content()
    # --- 阶段三：穿梭新标签页 ---
    # 3.1: 点击 `policy-link` 链接
    # 3.2: 等待出现2个窗口
    # 3.3: 切换到新窗口
    # 3.4: 等待并打印 `policy_content` 的文本
    # 3.5: 关闭新窗口
    # 3.6: 切换回原始窗口
    print("\n--- 阶段三：执行多窗口穿梭 ---")
    # 在这里编写您的代码...
    policy_link = wait.until(EC.element_to_be_clickable((By.ID, 'policy-link')))
    policy_link.click()
    print("✅ 已点击 '查看运费政策' 链接")

    policy_modal = wait.until(EC.visibility_of_element_located((By.ID, 'policy_modal')))
    print("✅ 政策弹窗已显示")

    policy_content = wait.until(EC.visibility_of_element_located((By.ID, 'policy_content')))
    policy_text = policy_content.text
    print(f"✅ 获取到政策内容: '{policy_text}'")

    time.sleep(1)

    close_button = driver.find_element(By.ID, 'close_modal')
    close_button.click()
    print("✅ 已关闭政策弹窗")

    wait.until(EC.invisibility_of_element_located((By.ID, 'policy_modal')))
    print("✅ 已确认弹窗关闭")

    time.sleep(1)

    # --- 阶段四：任务收尾 ---
    # 4.1: 在主页面，打印 `h1` 标签的文本
    # 4.2: 等待5秒
    print("\n--- 阶段四：执行收尾确认 ---")
    # 在这里编写您的代码...
    h1_element=driver.find_element(By.TAG_NAME,'h1')
    h1_text=h1_element.text
    print(f'主页面内容：{h1_text}')
    print("\n🎉 恭喜！任务流程已跑通！")
    time.sleep(3)


except Exception as e:
    print(f"\n❌ 任务执行出错: {type(e).__name__} - {e}")
    # 保存截图以供调试
    screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mission_failed.png")
    driver.save_screenshot(screenshot_path)
    print(f"已保存失败截图至: {screenshot_path}")

finally:
    # -------------------- 模块四：清理环节 (无需修改) --------------------
    print("\n正在关闭浏览器...")
    driver.quit()
    if os.path.exists(file_path):
        os.remove(file_path)
        print("✅ 已清理临时演习场文件。")
