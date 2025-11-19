"""
第一关：基础HTTP请求
学习目标：
1. 使用 requests 库发送 HTTP 请求
2. 理解 HTTP 响应状态码
3. 添加基本的请求头（User-Agent）
4. 处理网页编码
"""

import requests


def basic_get_request():
    """基础GET请求示例"""
    print("=" * 60)
    print("示例1: 发送基础GET请求")
    print("=" * 60)
    
    url = 'https://httpbin.org/get'
    
    # 发送GET请求
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容类型: {response.headers.get('Content-Type')}")
    print(f"响应内容长度: {len(response.text)} 字符")
    print("\n前200个字符的响应内容:")
    print(response.text[:200])
    print()


def request_with_headers():
    """带请求头的请求示例"""
    print("=" * 60)
    print("示例2: 添加User-Agent请求头")
    print("=" * 60)
    
    url = 'https://httpbin.org/headers'
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 发送带请求头的GET请求
    response = requests.get(url, headers=headers)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print("\n响应内容:")
    print(response.text)
    print()


def request_with_params():
    """带参数的请求示例"""
    print("=" * 60)
    print("示例3: 发送带URL参数的请求")
    print("=" * 60)
    
    url = 'https://httpbin.org/get'
    
    # URL参数
    params = {
        'name': '小白魔修',
        'level': '初学者',
        'skill': '网络爬虫'
    }
    
    # 发送带参数的GET请求
    response = requests.get(url, params=params)
    
    print(f"请求URL: {response.url}")
    print(f"响应状态码: {response.status_code}")
    print("\n响应内容:")
    print(response.text)
    print()


def handle_encoding():
    """处理网页编码示例"""
    print("=" * 60)
    print("示例4: 处理网页编码")
    print("=" * 60)
    
    # 使用 quotes.toscrape.com 作为示例（一个专门用于练习爬虫的网站）
    url = 'http://quotes.toscrape.com/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"请求URL: {url}")
    print(f"原始编码: {response.encoding}")
    
    # 设置正确的编码
    response.encoding = 'utf-8'
    print(f"设置编码为: {response.encoding}")
    print(f"响应状态码: {response.status_code}")
    print("\n网页标题和前500个字符:")
    print(response.text[:500])
    print()


def handle_errors():
    """错误处理示例"""
    print("=" * 60)
    print("示例5: 处理请求错误")
    print("=" * 60)
    
    # 测试不存在的URL
    url = 'https://httpbin.org/status/404'
    
    try:
        response = requests.get(url, timeout=5)
        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        
        # 检查响应状态
        if response.status_code == 200:
            print("✓ 请求成功")
        elif response.status_code == 404:
            print("✗ 页面不存在 (404)")
        else:
            print(f"✗ 请求失败: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("✗ 请求超时")
    except requests.exceptions.RequestException as e:
        print(f"✗ 请求异常: {e}")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("🎓 欢迎来到第一关：基础HTTP请求")
    print("📚 在这一关，你将学习如何发送HTTP请求并处理响应")
    print("\n")
    
    # 运行所有示例
    try:
        basic_get_request()
        request_with_headers()
        request_with_params()
        handle_encoding()
        handle_errors()
        
        print("=" * 60)
        print("🎉 恭喜！你已完成第一关的学习")
        print("💡 现在你已经掌握了：")
        print("   ✓ 发送基础HTTP请求")
        print("   ✓ 添加请求头")
        print("   ✓ 传递URL参数")
        print("   ✓ 处理网页编码")
        print("   ✓ 基础错误处理")
        print()
        print("🚀 准备好进入第二关了吗？运行 level2_html_parsing.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n⚠️  程序执行出错: {e}")
        print("\n💡 提示: 某些示例网站可能无法访问（需要网络连接）")
        print("   但你已经学会了HTTP请求的核心概念！")
        print("\n请继续学习下一关或查看代码了解详细用法。")


if __name__ == '__main__':
    main()
