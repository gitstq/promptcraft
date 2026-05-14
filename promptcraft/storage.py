#!/usr/bin/env python3
"""
数据存储层 - SQLite本地存储
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class Storage:
    """Prompt数据存储管理器"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化存储
        
        Args:
            db_path: 数据库文件路径，默认为 ~/.promptcraft/prompts.db
        """
        if db_path is None:
            home = Path.home()
            config_dir = home / ".promptcraft"
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / "prompts.db"
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Prompts表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    description TEXT,
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '[]',
                    variables TEXT DEFAULT '[]',
                    model_type TEXT DEFAULT 'general',
                    is_favorite INTEGER DEFAULT 0,
                    use_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 优化历史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS optimization_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id INTEGER,
                    original_content TEXT,
                    optimized_content TEXT,
                    improvements TEXT,
                    score_before REAL,
                    score_after REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
                )
            """)
            
            # 分类表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    icon TEXT DEFAULT '📁',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 插入默认分类
            default_categories = [
                ('general', '通用', '📋'),
                ('coding', '编程开发', '💻'),
                ('writing', '写作创作', '✍️'),
                ('analysis', '数据分析', '📊'),
                ('translation', '翻译', '🌐'),
                ('chat', '对话聊天', '💬'),
                ('image', '图像生成', '🎨'),
            ]
            
            for name, desc, icon in default_categories:
                cursor.execute("""
                    INSERT OR IGNORE INTO categories (name, description, icon)
                    VALUES (?, ?, ?)
                """, (name, desc, icon))
            
            conn.commit()
    
    def create_prompt(self, prompt_data: Dict[str, Any]) -> int:
        """
        创建新Prompt
        
        Returns:
            新创建的Prompt ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prompts (title, content, description, category, tags, 
                                   variables, model_type, is_favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prompt_data['title'],
                prompt_data['content'],
                prompt_data.get('description', ''),
                prompt_data.get('category', 'general'),
                json.dumps(prompt_data.get('tags', [])),
                json.dumps(prompt_data.get('variables', [])),
                prompt_data.get('model_type', 'general'),
                1 if prompt_data.get('is_favorite', False) else 0
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_prompt(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """获取单个Prompt"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def list_prompts(self, category: Optional[str] = None, 
                     tag: Optional[str] = None,
                     favorite_only: bool = False,
                     search: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出Prompts
        
        Args:
            category: 按分类筛选
            tag: 按标签筛选
            favorite_only: 仅显示收藏
            search: 搜索关键词
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM prompts WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if favorite_only:
                query += " AND is_favorite = 1"
            
            if search:
                query += " AND (title LIKE ? OR content LIKE ? OR description LIKE ?)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern] * 3)
            
            query += " ORDER BY is_favorite DESC, updated_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            prompts = [self._row_to_dict(row) for row in rows]
            
            # 标签筛选在Python中处理（因为tags是JSON）
            if tag:
                prompts = [p for p in prompts if tag in p.get('tags', [])]
            
            return prompts
    
    def update_prompt(self, prompt_id: int, prompt_data: Dict[str, Any]) -> bool:
        """更新Prompt"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            update_fields = []
            params = []
            
            if 'title' in prompt_data:
                update_fields.append("title = ?")
                params.append(prompt_data['title'])
            
            if 'content' in prompt_data:
                update_fields.append("content = ?")
                params.append(prompt_data['content'])
            
            if 'description' in prompt_data:
                update_fields.append("description = ?")
                params.append(prompt_data['description'])
            
            if 'category' in prompt_data:
                update_fields.append("category = ?")
                params.append(prompt_data['category'])
            
            if 'tags' in prompt_data:
                update_fields.append("tags = ?")
                params.append(json.dumps(prompt_data['tags']))
            
            if 'variables' in prompt_data:
                update_fields.append("variables = ?")
                params.append(json.dumps(prompt_data['variables']))
            
            if 'model_type' in prompt_data:
                update_fields.append("model_type = ?")
                params.append(prompt_data['model_type'])
            
            if 'is_favorite' in prompt_data:
                update_fields.append("is_favorite = ?")
                params.append(1 if prompt_data['is_favorite'] else 0)
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            
            query = f"UPDATE prompts SET {', '.join(update_fields)} WHERE id = ?"
            params.append(prompt_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """删除Prompt"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def increment_use_count(self, prompt_id: int):
        """增加使用计数"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE prompts 
                SET use_count = use_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (prompt_id,))
            conn.commit()
    
    def add_optimization_history(self, history_data: Dict[str, Any]) -> int:
        """添加优化历史"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO optimization_history 
                (prompt_id, original_content, optimized_content, improvements, 
                 score_before, score_after)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                history_data.get('prompt_id'),
                history_data['original_content'],
                history_data['optimized_content'],
                json.dumps(history_data.get('improvements', [])),
                history_data.get('score_before', 0),
                history_data.get('score_after', 0)
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_optimization_history(self, prompt_id: int) -> List[Dict[str, Any]]:
        """获取优化历史"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM optimization_history 
                WHERE prompt_id = ? 
                ORDER BY created_at DESC
            """, (prompt_id,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """获取所有分类"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM prompts")
            total_prompts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM prompts WHERE is_favorite = 1")
            favorite_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM categories")
            category_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(use_count) FROM prompts")
            total_uses = cursor.fetchone()[0] or 0
            
            return {
                'total_prompts': total_prompts,
                'favorite_count': favorite_count,
                'category_count': category_count,
                'total_uses': total_uses
            }
    
    def export_data(self, format_type: str = 'json') -> str:
        """
        导出所有数据
        
        Args:
            format_type: 'json' 或 'markdown'
        """
        prompts = self.list_prompts()
        
        if format_type == 'json':
            return json.dumps(prompts, ensure_ascii=False, indent=2)
        
        elif format_type == 'markdown':
            lines = ["# PromptCraft Export\n"]
            for p in prompts:
                lines.append(f"## {p['title']}\n")
                lines.append(f"**分类**: {p['category']}  ")
                lines.append(f"**标签**: {', '.join(p.get('tags', []))}  ")
                lines.append(f"**模型**: {p['model_type']}  ")
                lines.append(f"**收藏**: {'⭐' if p['is_favorite'] else ''}  \n")
                lines.append(f"**描述**: {p.get('description', '无')}  \n")
                lines.append("```\n")
                lines.append(p['content'])
                lines.append("\n```\n")
            return '\n'.join(lines)
        
        else:
            raise ValueError(f"不支持的格式: {format_type}")
    
    def import_data(self, data: str, format_type: str = 'json'):
        """导入数据"""
        if format_type == 'json':
            prompts = json.loads(data)
            for p in prompts:
                p.pop('id', None)  # 移除ID，让数据库自动生成
                p.pop('created_at', None)
                p.pop('updated_at', None)
                self.create_prompt(p)
        else:
            raise ValueError(f"不支持的格式: {format_type}")
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        result = dict(row)
        # 解析JSON字段
        for field in ['tags', 'variables']:
            if field in result and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []
        # 转换布尔值
        if 'is_favorite' in result:
            result['is_favorite'] = bool(result['is_favorite'])
        return result
