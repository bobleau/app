import subprocess
import json
import sqlite3
from datetime import datetime

DB_FILE = "cmd_output.db"

def init_db():
    """初始化数据库：如果表不存在则创建"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 创建一个纯中文列名的表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cmd_output_sql (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            执行时间 TEXT,
            内存类型 TEXT,
            总容量 TEXT,
            已使用 TEXT,
            空闲 TEXT,
            共享内存 TEXT,
            缓存与缓冲 TEXT,
            可用容量 TEXT,
            原始JSON数据树 TEXT
        )
    ''')
    conn.commit()
    conn.close()

def capture_cmd_output_to_db():
    # 指令：利用linux的shell指令，获取需要的回显信息。带有管道符的过滤指令，并使用 shell=True 执行
    cmd = "free -h"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return

    lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 确保数据库表已初始化
    init_db()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        # 解析以 Mem: 或 Swap: 开头的行，优雅跳过表头    
        if parts[0].startswith("Mem") or parts[0].startswith("Swap"):
            row_type = parts[0].replace(":", "") # 提取出 "Mem" 或 "Swap"
            row_values = parts[1:]               # 提取出后面所有的数值

            # 【对齐算法】
            # 标准 Mem 有 6 个数值，而 Swap 只有 3 个数值（Total, Used, Free）
            # 如果是 Swap 行，后面缺了 3 个字段，我们用 "-" 动态填充进去，防止网页和 Excel 出现空格子或错位
            
            # 自动补齐 Swap 行缺少的 3 个字段
            if len(row_values) < 6:
                row_values += ["-"] * (6 - len(row_values))
            
            # 构造原始 JSON 数据树
            row_json = {
                "CaptureTime": current_time,
                "Type": row_type,
                "Total": row_values[0],
                "Used": row_values[1],
                "Free": row_values[2],
                "Shared": row_values[3],
                "Buff_Cache": row_values[4],
                "Available": row_values[5]
            }
            json_str = json.dumps(row_json, ensure_ascii=False)

            # 🚀 高效的 SQL 插入语句，瞬间完成，不像.xlsx文件插入新数据前必须读取原有的旧数据内容
            cursor.execute('''
                INSERT INTO cmd_output_sql (执行时间, 内存类型, 总容量, 已使用, 空闲, 共享内存, 缓存与缓冲, 可用容量, 原始JSON数据树)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_time, row_type, row_values[0], row_values[1], row_values[2], row_values[3], row_values[4], row_values[5], json_str))
            
    conn.commit()
    conn.close()
    print(f"【成功】数据已直接追加至 SQLite 数据库文件: {DB_FILE}")

if __name__ == "__main__":
    capture_cmd_output_to_db()
