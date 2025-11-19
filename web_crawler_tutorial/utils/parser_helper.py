"""
解析辅助函数
提供HTML解析相关的工具方法
"""

from typing import List, Optional
from lxml import etree
from bs4 import BeautifulSoup


def parse_with_xpath(html: str, xpath: str) -> List[str]:
    """
    使用XPath解析HTML
    
    Args:
        html: HTML字符串
        xpath: XPath表达式
    
    Returns:
        匹配结果列表
    """
    try:
        tree = etree.HTML(html)
        results = tree.xpath(xpath)
        # 处理结果，确保返回字符串列表
        return [str(r) if not isinstance(r, str) else r for r in results]
    except Exception as e:
        print(f"XPath解析失败: {e}")
        return []


def parse_with_bs4(html: str, 
                   tag: str, 
                   attrs: Optional[dict] = None,
                   class_: Optional[str] = None) -> List:
    """
    使用BeautifulSoup解析HTML
    
    Args:
        html: HTML字符串
        tag: 标签名
        attrs: 属性字典
        class_: CSS类名
    
    Returns:
        匹配元素列表
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        if class_:
            results = soup.find_all(tag, class_=class_)
        elif attrs:
            results = soup.find_all(tag, attrs=attrs)
        else:
            results = soup.find_all(tag)
        
        return results
    except Exception as e:
        print(f"BeautifulSoup解析失败: {e}")
        return []


def extract_text(element) -> str:
    """
    从元素中提取文本
    
    Args:
        element: BeautifulSoup元素或lxml元素
    
    Returns:
        文本内容
    """
    try:
        if hasattr(element, 'get_text'):
            # BeautifulSoup元素
            return element.get_text(strip=True)
        elif hasattr(element, 'text'):
            # lxml元素
            return element.text.strip() if element.text else ''
        else:
            return str(element).strip()
    except Exception as e:
        print(f"提取文本失败: {e}")
        return ""


def extract_links(html: str, base_url: str = '') -> List[str]:
    """
    提取HTML中的所有链接
    
    Args:
        html: HTML字符串
        base_url: 基础URL（用于补全相对路径）
    
    Returns:
        链接列表
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 处理相对路径
            if base_url and not href.startswith('http'):
                href = base_url.rstrip('/') + '/' + href.lstrip('/')
            links.append(href)
        
        return links
    except Exception as e:
        print(f"提取链接失败: {e}")
        return []


def extract_images(html: str, base_url: str = '') -> List[str]:
    """
    提取HTML中的所有图片链接
    
    Args:
        html: HTML字符串
        base_url: 基础URL（用于补全相对路径）
    
    Returns:
        图片链接列表
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        images = []
        
        for img in soup.find_all('img', src=True):
            src = img['src']
            # 处理相对路径
            if base_url and not src.startswith('http'):
                src = base_url.rstrip('/') + '/' + src.lstrip('/')
            images.append(src)
        
        return images
    except Exception as e:
        print(f"提取图片失败: {e}")
        return []


def clean_text(text: str) -> str:
    """
    清理文本（去除多余空白、换行等）
    
    Args:
        text: 原始文本
    
    Returns:
        清理后的文本
    """
    import re
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 去除首尾空白
    text = text.strip()
    return text
