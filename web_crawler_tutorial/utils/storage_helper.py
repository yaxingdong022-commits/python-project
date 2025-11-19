"""
存储辅助函数
提供数据存储相关的工具方法
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime


def ensure_dir(directory: str) -> None:
    """
    确保目录存在，不存在则创建
    
    Args:
        directory: 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_to_json(data: Any, 
                 filename: str,
                 output_dir: str = 'output') -> bool:
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
        output_dir: 输出目录
    
    Returns:
        是否成功
    """
    try:
        ensure_dir(output_dir)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filepath}")
        return True
    except Exception as e:
        print(f"保存JSON失败: {e}")
        return False


def save_to_csv(data: List[Dict], 
                filename: str,
                output_dir: str = 'output') -> bool:
    """
    保存数据到CSV文件
    
    Args:
        data: 字典列表
        filename: 文件名
        output_dir: 输出目录
    
    Returns:
        是否成功
    """
    try:
        if not data:
            print("没有数据可保存")
            return False
        
        ensure_dir(output_dir)
        filepath = os.path.join(output_dir, filename)
        
        # 获取所有字段
        fieldnames = list(data[0].keys())
        
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"数据已保存到: {filepath}")
        return True
    except Exception as e:
        print(f"保存CSV失败: {e}")
        return False


def append_to_file(content: str, 
                   filename: str,
                   output_dir: str = 'output') -> bool:
    """
    追加内容到文件
    
    Args:
        content: 要追加的内容
        filename: 文件名
        output_dir: 输出目录
    
    Returns:
        是否成功
    """
    try:
        ensure_dir(output_dir)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
            if not content.endswith('\n'):
                f.write('\n')
        
        return True
    except Exception as e:
        print(f"追加文件失败: {e}")
        return False


def generate_filename(prefix: str = 'data', 
                      extension: str = 'json') -> str:
    """
    生成带时间戳的文件名
    
    Args:
        prefix: 文件名前缀
        extension: 文件扩展名
    
    Returns:
        文件名
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"


def read_from_json(filename: str, 
                   output_dir: str = 'output') -> Any:
    """
    从JSON文件读取数据
    
    Args:
        filename: 文件名
        output_dir: 输出目录
    
    Returns:
        读取的数据
    """
    try:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取JSON失败: {e}")
        return None


def read_from_csv(filename: str, 
                  output_dir: str = 'output') -> List[Dict]:
    """
    从CSV文件读取数据
    
    Args:
        filename: 文件名
        output_dir: 输出目录
    
    Returns:
        数据列表
    """
    try:
        filepath = os.path.join(output_dir, filename)
        data = []
        
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data
    except Exception as e:
        print(f"读取CSV失败: {e}")
        return []
