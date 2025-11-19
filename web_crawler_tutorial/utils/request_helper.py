"""
请求辅助函数
提供封装好的HTTP请求方法
"""

import time
import random
import requests
from typing import Optional, Dict
from config.settings import (
    REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY, 
    USER_AGENTS, DEFAULT_HEADERS
)


def get_random_user_agent() -> str:
    """获取随机User-Agent"""
    return random.choice(USER_AGENTS)


def make_request(url: str, 
                  method: str = 'GET',
                  headers: Optional[Dict] = None,
                  params: Optional[Dict] = None,
                  data: Optional[Dict] = None,
                  timeout: int = REQUEST_TIMEOUT,
                  max_retries: int = MAX_RETRIES) -> Optional[requests.Response]:
    """
    发送HTTP请求，带重试机制
    
    Args:
        url: 目标URL
        method: 请求方法 (GET, POST等)
        headers: 自定义请求头
        params: URL参数
        data: POST数据
        timeout: 超时时间
        max_retries: 最大重试次数
    
    Returns:
        Response对象或None（失败时）
    """
    if headers is None:
        headers = DEFAULT_HEADERS.copy()
    
    # 添加随机User-Agent
    if 'User-Agent' not in headers:
        headers['User-Agent'] = get_random_user_agent()
    
    for attempt in range(max_retries):
        try:
            if method.upper() == 'GET':
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=params,
                    timeout=timeout
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url, 
                    headers=headers, 
                    params=params,
                    data=data,
                    timeout=timeout
                )
            else:
                raise ValueError(f"不支持的请求方法: {method}")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"达到最大重试次数，请求失败: {url}")
                return None
    
    return None


def download_file(url: str, 
                  save_path: str,
                  headers: Optional[Dict] = None) -> bool:
    """
    下载文件
    
    Args:
        url: 文件URL
        save_path: 保存路径
        headers: 自定义请求头
    
    Returns:
        是否成功
    """
    try:
        response = make_request(url, headers=headers)
        if response:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"文件下载失败: {e}")
        return False


def check_robots_txt(base_url: str) -> str:
    """
    检查网站的robots.txt
    
    Args:
        base_url: 网站根URL
    
    Returns:
        robots.txt内容
    """
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    try:
        response = make_request(robots_url)
        if response:
            return response.text
        return "无法访问 robots.txt"
    except Exception as e:
        return f"检查 robots.txt 失败: {e}"
