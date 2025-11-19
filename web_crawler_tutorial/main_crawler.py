"""
主程序 - 小白魔修成长为网络爬虫工程师
这个程序展示了完整的学习路径
"""

import sys


def print_banner():
    """打印欢迎横幅"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🧙 小白魔修成长为网络爬虫工程师 🚀")
    print("=" * 70)
    print()
    print("  这是一个循序渐进的网络爬虫学习教程")
    print("  通过四个关卡，你将掌握从基础到高级的所有爬虫技能")
    print()
    print("=" * 70)
    print()


def print_menu():
    """打印菜单"""
    print("📚 请选择你要学习的关卡：")
    print()
    print("  1️⃣  第一关：基础HTTP请求")
    print("      - 学习使用 requests 库")
    print("      - 理解HTTP请求和响应")
    print("      - 处理网页编码")
    print()
    print("  2️⃣  第二关：HTML解析")
    print("      - 使用 XPath 和 BeautifulSoup")
    print("      - 提取网页数据")
    print("      - 数据清洗")
    print()
    print("  3️⃣  第三关：高级爬虫技术")
    print("      - 异常处理和重试")
    print("      - 日志记录")
    print("      - 多页面爬取")
    print()
    print("  4️⃣  第四关：专业级爬虫框架")
    print("      - 异步并发爬取")
    print("      - 速率限制")
    print("      - 架构设计")
    print()
    print("  🎯 运行所有关卡（推荐按顺序学习）")
    print("  ❌ 退出")
    print()
    print("=" * 70)


def run_level(level: int):
    """运行指定关卡"""
    if level == 1:
        print("\n🎮 启动第一关：基础HTTP请求")
        print("-" * 70)
        import level1_basic_request
        level1_basic_request.main()
    
    elif level == 2:
        print("\n🎮 启动第二关：HTML解析")
        print("-" * 70)
        import level2_html_parsing
        level2_html_parsing.main()
    
    elif level == 3:
        print("\n🎮 启动第三关：高级爬虫技术")
        print("-" * 70)
        import level3_advanced_crawler
        level3_advanced_crawler.main()
    
    elif level == 4:
        print("\n🎮 启动第四关：专业级爬虫框架")
        print("-" * 70)
        import asyncio
        import level4_professional_crawler
        asyncio.run(level4_professional_crawler.main())


def run_all_levels():
    """运行所有关卡"""
    print("\n🎯 开始完整的学习之旅！")
    print("=" * 70)
    
    levels = [1, 2, 3, 4]
    
    for level in levels:
        input(f"\n按 Enter 键开始第 {level} 关...")
        run_level(level)
        
        if level < 4:
            print("\n" + "=" * 70)
            input(f"✓ 第 {level} 关完成！按 Enter 键继续下一关...")
    
    print("\n" + "=" * 70)
    print(" " * 15 + "🏆 恭喜你完成所有关卡！")
    print("=" * 70)
    print()
    print("你已经掌握了：")
    print("  ✓ 基础HTTP请求")
    print("  ✓ HTML解析技术")
    print("  ✓ 高级爬虫策略")
    print("  ✓ 专业级爬虫框架")
    print()
    print("继续学习的方向：")
    print("  • 学习 Scrapy 框架")
    print("  • 掌握 Selenium 动态网页爬取")
    print("  • 探索分布式爬虫")
    print("  • 研究反爬虫和验证码识别")
    print()
    print("=" * 70)


def main():
    """主函数"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("请输入你的选择 (1-4, 或 'all', 'exit'): ").strip().lower()
            
            if choice in ['exit', 'quit', 'q', 'x']:
                print("\n👋 感谢使用！继续加油学习爬虫技术！")
                break
            
            elif choice in ['all', 'a']:
                run_all_levels()
                break
            
            elif choice in ['1', '2', '3', '4']:
                level = int(choice)
                run_level(level)
                
                print("\n" + "=" * 70)
                continue_learning = input("\n是否继续学习其他关卡？(y/n): ").strip().lower()
                if continue_learning not in ['y', 'yes']:
                    print("\n👋 感谢使用！继续加油学习爬虫技术！")
                    break
            
            else:
                print("\n❌ 无效的选择，请重新输入")
                input("按 Enter 键继续...")
        
        except KeyboardInterrupt:
            print("\n\n👋 程序被中断，再见！")
            break
        
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            input("按 Enter 键继续...")


if __name__ == '__main__':
    main()
