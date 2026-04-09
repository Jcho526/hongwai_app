import cv2
import numpy as np
from PIL import Image
import json
import os
from datetime import datetime

class ThermalImageAnalyzer:
    def __init__(self, dict_path='thermal_dict.json'):
        """
        初始化热图分析器
        
        参数：
        - dict_path: 热图字典文件路径
        """
        self.dict_path = dict_path
        self.knowledge_base = None
        self.thermal_dictionary = None
        self.body_regions = None
        
        # 加载热图字典
        self._load_dictionary()
        
        # 颜色映射表（用于将热图颜色转换为温度类型）
        self.color_temperature_map = {
            'white': 'high',
            'red': 'high',
            'purple': 'high',
            'yellow': 'normal',
            'green': 'low',
            'blue': 'low',
            'black': 'low'
        }
    
    def _load_dictionary(self):
        """
        加载热图字典数据
        """
        try:
            with open(self.dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.knowledge_base = data['knowledge_base']
                self.thermal_dictionary = data['thermal_dictionary']
                self.body_regions = data['body_regions']
            print(f"成功加载热图字典: {self.dict_path}")
        except Exception as e:
            print(f"加载热图字典失败: {str(e)}")
            raise
    
    def preprocess_image(self, image_path, target_size=(640, 480)):
        """
        热图预处理
        
        参数：
        - image_path: 热图文件路径
        - target_size: 目标尺寸 (width, height)
        
        返回：
        - 预处理后的图像 (numpy数组)
        """
        try:
            # 读取图像
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"无法读取图像: {image_path}")
            
            # 调整尺寸
            resized_img = cv2.resize(img, target_size)
            
            # 转换为RGB颜色空间
            rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            
            return rgb_img
        except Exception as e:
            print(f"预处理图像失败: {str(e)}")
            raise
    
    def extract_features(self, image):
        """
        提取热图特征
        
        参数：
        - image: 预处理后的热图 (numpy数组)
        
        返回：
        - 特征字典
        """
        features = {
            'symmetry_score': self._calculate_symmetry(image),
            'color_distribution': self._analyze_color_distribution(image),
            'abnormal_regions': self._detect_abnormal_regions(image),
            'temperature_statistics': self._calculate_temperature_stats(image)
        }
        return features
    
    def _calculate_symmetry(self, image):
        """
        计算热图左右对称性
        
        参数：
        - image: 热图 (numpy数组)
        
        返回：
        - 对称性得分 (0-1，1表示完全对称)
        """
        height, width, _ = image.shape
        mid_x = width // 2
        
        # 分割左右两部分
        left_half = image[:, :mid_x]
        right_half = image[:, mid_x:]
        
        # 水平翻转右侧，使其与左侧对齐
        right_half_flipped = cv2.flip(right_half, 1)
        
        # 调整右侧尺寸以匹配左侧
        if left_half.shape[1] != right_half_flipped.shape[1]:
            right_half_flipped = right_half_flipped[:, :left_half.shape[1]]
            left_half = left_half[:, :right_half_flipped.shape[1]]
        
        # 计算差异
        diff = cv2.absdiff(left_half, right_half_flipped)
        diff_score = np.sum(diff) / (left_half.size * 255)  # 归一化差异得分
        
        # 转换为对称性得分 (0-1)
        symmetry_score = 1 - diff_score
        
        return round(symmetry_score, 2)
    
    def _analyze_color_distribution(self, image):
        """
        分析热图颜色分布
        
        参数：
        - image: 热图 (numpy数组)
        
        返回：
        - 颜色分布字典
        """
        # 将图像转换为PIL格式，便于颜色分析
        pil_img = Image.fromarray(image)
        
        # 获取图像像素
        pixels = list(pil_img.getdata())
        
        # 颜色分类
        color_counts = {
            'white': 0,
            'red': 0,
            'purple': 0,
            'yellow': 0,
            'green': 0,
            'blue': 0,
            'black': 0
        }
        
        for pixel in pixels:
            r, g, b = pixel
            
            # 简单的颜色分类逻辑
            if r > 200 and g > 200 and b > 200:  # 白色
                color_counts['white'] += 1
            elif r > 150 and g < 100 and b < 100:  # 红色
                color_counts['red'] += 1
            elif r > 100 and g < 100 and b > 100:  # 紫色
                color_counts['purple'] += 1
            elif r > 150 and g > 150 and b < 100:  # 黄色
                color_counts['yellow'] += 1
            elif r < 100 and g > 150 and b < 100:  # 绿色
                color_counts['green'] += 1
            elif r < 100 and g < 100 and b > 150:  # 蓝色
                color_counts['blue'] += 1
            else:  # 黑色或其他
                color_counts['black'] += 1
        
        # 计算各颜色占比
        total_pixels = len(pixels)
        color_distribution = {
            color: round(count / total_pixels, 4) 
            for color, count in color_counts.items()
        }
        
        return color_distribution
    
    def _detect_abnormal_regions(self, image):
        """
        检测异常区域
        
        参数：
        - image: 热图 (numpy数组)
        
        返回：
        - 异常区域列表
        """
        # 这里实现简单的异常区域检测，基于颜色分布
        color_distribution = self._analyze_color_distribution(image)
        abnormal_regions = []
        
        # 检查高温异常（白色、红色、紫色占比过高）
        high_temp_colors = ['white', 'red', 'purple']
        high_temp_ratio = sum(color_distribution[color] for color in high_temp_colors)
        
        if high_temp_ratio > 0.3:  # 高温区域超过30%，视为异常
            abnormal_regions.append({
                'type': 'high_temperature',
                'ratio': round(high_temp_ratio, 2),
                'description': f"高温区域占比过高: {high_temp_ratio*100:.1f}%"
            })
        
        # 检查低温异常（绿色、蓝色、黑色占比过高）
        low_temp_colors = ['green', 'blue', 'black']
        low_temp_ratio = sum(color_distribution[color] for color in low_temp_colors)
        
        if low_temp_ratio > 0.5:  # 低温区域超过50%，视为异常
            abnormal_regions.append({
                'type': 'low_temperature',
                'ratio': round(low_temp_ratio, 2),
                'description': f"低温区域占比过高: {low_temp_ratio*100:.1f}%"
            })
        
        return abnormal_regions
    
    def _calculate_temperature_stats(self, image):
        """
        计算温度统计信息
        
        参数：
        - image: 热图 (numpy数组)
        
        返回：
        - 温度统计字典
        "