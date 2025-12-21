def process_position(pos_str):
    """
    处理经纬度字符串：
    输入格式：N031.12.37.142,E121.19.54.741
    输出格式：31.210317:121.331872（冒号分隔，6位小数）
    
    格式说明：
    - N031.12.37.142 表示北纬31度12分37.142秒
    - E121.19.54.741 表示东经121度19分54.741秒
    """
    try:
        # 去掉空格
        pos_str = pos_str.strip()
        
        # 分割纬度和经度
        if ',' in pos_str:
            lat_str, lon_str = pos_str.split(',', 1)
        elif '，' in pos_str:  # 中文逗号
            lat_str, lon_str = pos_str.split('，', 1)
        else:
            return None
        
        # 处理纬度
        lat_decimal = parse_dot_dms_format(lat_str.strip())
        if lat_decimal is None:
            return None
        
        # 处理经度
        lon_decimal = parse_dot_dms_format(lon_str.strip())
        if lon_decimal is None:
            return None
        
        # 格式化为冒号分隔（保留6位小数）
        return f"{lat_decimal:.6f}:{lon_decimal:.6f}"
        
    except Exception as e:
        print(f"处理位置时出错: {e}")
        return None

def parse_dot_dms_format(dms_str):
    """
    解析点分隔的度分秒格式
    输入格式：N031.12.37.142 或 E121.19.54.741
    返回：小数格式的坐标值
    """
    try:
        # 去掉前缀（N, E, S, W）
        dms_str = dms_str.strip()
        if dms_str.startswith('N') or dms_str.startswith('S'):
            prefix_removed = dms_str[1:]
        elif dms_str.startswith('E') or dms_str.startswith('W'):
            prefix_removed = dms_str[1:]
        else:
            prefix_removed = dms_str  # 如果没有前缀，直接使用
        
        # 按点号分割
        parts = prefix_removed.split('.')
        
        if len(parts) < 3:
            return None
        
        # 提取度、分、秒
        # 注意：度可能有3位数（如031），分和秒是2位数
        degrees = int(parts[0])
        
        # 分
        minutes = int(parts[1])
        
        # 秒（可能包含小数部分）
        seconds_str = parts[2]
        if len(parts) > 3:
            # 如果有第四部分，说明秒有小数
            seconds_str = f"{parts[2]}.{parts[3]}"
        
        seconds = float(seconds_str)
        
        # 计算小数格式：度 + 分/60 + 秒/3600
        decimal_value = degrees + minutes/60 + seconds/3600
        
        return decimal_value
        
    except Exception as e:
        print(f"解析点分隔度分秒格式时出错: {e}, 输入: {dms_str}")
        return None

def validate_coordinate_format(coord_str):
    """
    验证坐标字符串格式是否正确
    要求格式：N031.12.37.142,E121.19.54.741
    """
    try:
        # 基本格式检查
        if ',' not in coord_str and '，' not in coord_str:
            return False
        
        # 分割检查
        if ',' in coord_str:
            lat_str, lon_str = coord_str.split(',', 1)
        else:
            lat_str, lon_str = coord_str.split('，', 1)
        
        # 检查前缀
        lat_str = lat_str.strip()
        lon_str = lon_str.strip()
        
        if not (lat_str.startswith('N') or lat_str.startswith('S')):
            return False
        if not (lon_str.startswith('E') or lon_str.startswith('W')):
            return False
        
        # 检查点分隔格式
        lat_without_prefix = lat_str[1:]
        lon_without_prefix = lon_str[1:]
        
        # 应该至少有3个点号（度.分.秒）
        if lat_without_prefix.count('.') < 2 or lon_without_prefix.count('.') < 2:
            return False
        
        # 尝试解析
        lat_decimal = parse_dot_dms_format(lat_str)
        lon_decimal = parse_dot_dms_format(lon_str)
        
        return lat_decimal is not None and lon_decimal is not None
        
    except Exception:
        return False

def format_coordinate_to_string(lat_decimal, lon_decimal, decimal_places=6):
    """
    将小数格式的经纬度格式化为字符串
    格式：纬度:经度
    示例：31.210317:121.331872
    """
    return f"{lat_decimal:.{decimal_places}f}:{lon_decimal:.{decimal_places}f}"

def convert_to_dot_dms_format(decimal_value, prefix=''):
    """
    将小数格式转换为点分隔的度分秒格式
    输入：31.210317
    输出：N031.12.37.142
    """
    try:
        degrees = int(decimal_value)
        minutes_decimal = (decimal_value - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60
        
        # 格式化：度保持3位，分2位，秒保留3位小数
        degrees_str = f"{degrees:03d}"
        minutes_str = f"{minutes:02d}"
        seconds_str = f"{seconds:.3f}"
        
        # 秒可能需要拆分整数和小数部分
        seconds_parts = seconds_str.split('.')
        if len(seconds_parts) == 2:
            seconds_int = seconds_parts[0].zfill(2)
            seconds_frac = seconds_parts[1]
            return f"{prefix}{degrees_str}.{minutes_str}.{seconds_int}.{seconds_frac}"
        else:
            return f"{prefix}{degrees_str}.{minutes_str}.{seconds_parts[0].zfill(2)}.000"
            
    except Exception as e:
        print(f"转换为点分隔度分秒格式时出错: {e}")
        return None