#!/usr/bin/env python3
"""
命令行接口 - 使用Rich库提供美观的终端界面
"""
import sys
import json
from typing import Optional
from pathlib import Path

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.tree import Tree
    from rich import box
except ImportError:
    print("错误: 缺少必要的依赖。请运行: pip install click rich")
    sys.exit(1)

from .core import PromptManager
from . import __version__

console = Console()

# 创建管理器实例
def get_manager():
    return PromptManager()


@click.group()
@click.version_option(version=__version__, prog_name="promptcraft")
def cli():
    """🎨 PromptCraft - 轻量级AI Prompt优化与管理工具"""
    pass


# ==================== Prompt管理命令 ====================

@cli.command()
@click.argument('title')
@click.argument('content')
@click.option('--description', '-d', help='Prompt描述')
@click.option('--category', '-c', default='general', help='分类')
@click.option('--tags', '-t', help='标签（逗号分隔）')
@click.option('--model', '-m', default='general', help='模型类型')
@click.option('--favorite', '-f', is_flag=True, help='标记为收藏')
def create(title: str, content: str, description: Optional[str], 
           category: str, tags: Optional[str], model: str, favorite: bool):
    """创建新Prompt"""
    manager = get_manager()
    
    tag_list = [t.strip() for t in tags.split(',')] if tags else []
    
    prompt_id = manager.create(
        title=title,
        content=content,
        description=description or '',
        category=category,
        tags=tag_list,
        model_type=model,
        is_favorite=favorite
    )
    
    console.print(f"✅ [green]Prompt创建成功！ID: {prompt_id}[/green]")


@cli.command()
@click.argument('prompt_id', type=int)
def show(prompt_id: int):
    """显示Prompt详情"""
    manager = get_manager()
    prompt = manager.get(prompt_id)
    
    if not prompt:
        console.print(f"❌ [red]Prompt ID {prompt_id} 不存在[/red]")
        return
    
    # 创建信息面板
    favorite_star = "⭐ " if prompt['is_favorite'] else ""
    
    info_table = Table(show_header=False, box=box.SIMPLE)
    info_table.add_column("属性", style="cyan")
    info_table.add_column("值", style="white")
    
    info_table.add_row("ID", str(prompt['id']))
    info_table.add_row("标题", f"{favorite_star}{prompt['title']}")
    info_table.add_row("分类", prompt['category'])
    info_table.add_row("标签", ", ".join(prompt.get('tags', [])) or "无")
    info_table.add_row("模型", prompt['model_type'])
    info_table.add_row("使用次数", str(prompt.get('use_count', 0)))
    info_table.add_row("创建时间", prompt['created_at'])
    info_table.add_row("更新时间", prompt['updated_at'])
    
    if prompt.get('description'):
        info_table.add_row("描述", prompt['description'])
    
    console.print(Panel(info_table, title="📋 Prompt信息", border_style="blue"))
    
    # 显示内容
    syntax = Syntax(prompt['content'], "markdown", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="📝 Prompt内容", border_style="green"))
    
    # 显示变量
    variables = prompt.get('variables', [])
    if variables:
        var_tree = Tree("🔧 变量")
        for var in variables:
            var_tree.add(f"{{{{{var}}}}}")
        console.print(var_tree)


@cli.command()
@click.option('--category', '-c', help='按分类筛选')
@click.option('--tag', '-t', help='按标签筛选')
@click.option('--favorite', '-f', is_flag=True, help='仅显示收藏')
@click.option('--search', '-s', help='搜索关键词')
@click.option('--limit', '-l', type=int, default=20, help='显示数量限制')
def list(category: Optional[str], tag: Optional[str], favorite: bool, 
         search: Optional[str], limit: int):
    """列出所有Prompts"""
    manager = get_manager()
    
    filters = {}
    if category:
        filters['category'] = category
    if tag:
        filters['tag'] = tag
    if favorite:
        filters['favorite_only'] = True
    if search:
        filters['search'] = search
    
    prompts = manager.list(**filters)
    
    if not prompts:
        console.print("📭 [yellow]没有找到Prompts[/yellow]")
        return
    
    table = Table(title=f"📚 Prompt列表 (共{len(prompts)}个)", box=box.ROUNDED)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("标题", style="white")
    table.add_column("分类", style="magenta")
    table.add_column("标签", style="yellow")
    table.add_column("⭐", justify="center")
    table.add_column("使用", justify="right")
    
    for p in prompts[:limit]:
        favorite_mark = "★" if p['is_favorite'] else ""
        tags = ", ".join(p.get('tags', [])[:2])  # 只显示前2个标签
        table.add_row(
            str(p['id']),
            p['title'][:40] + ('...' if len(p['title']) > 40 else ''),
            p['category'],
            tags or "-",
            favorite_mark,
            str(p.get('use_count', 0))
        )
    
    console.print(table)
    
    if len(prompts) > limit:
        console.print(f"[dim]... 还有 {len(prompts) - limit} 个Prompt[/dim]")


@cli.command()
@click.argument('prompt_id', type=int)
@click.option('--title', help='新标题')
@click.option('--content', help='新内容')
@click.option('--description', help='新描述')
@click.option('--category', help='新分类')
@click.option('--model', help='新模型类型')
def update(prompt_id: int, **kwargs):
    """更新Prompt"""
    manager = get_manager()
    
    # 过滤掉None值
    update_data = {k: v for k, v in kwargs.items() if v is not None}
    
    if not update_data:
        console.print("⚠️ [yellow]没有提供任何更新内容[/yellow]")
        return
    
    success = manager.update(prompt_id, **update_data)
    
    if success:
        console.print(f"✅ [green]Prompt {prompt_id} 更新成功[/green]")
    else:
        console.print(f"❌ [red]Prompt {prompt_id} 不存在或更新失败[/red]")


@cli.command()
@click.argument('prompt_id', type=int)
@click.confirmation_option(prompt='确定要删除这个Prompt吗?')
def delete(prompt_id: int):
    """删除Prompt"""
    manager = get_manager()
    
    success = manager.delete(prompt_id)
    
    if success:
        console.print(f"✅ [green]Prompt {prompt_id} 已删除[/green]")
    else:
        console.print(f"❌ [red]Prompt {prompt_id} 不存在[/red]")


@cli.command()
@click.argument('prompt_id', type=int)
def favorite(prompt_id: int):
    """切换收藏状态"""
    manager = get_manager()
    
    prompt = manager.get(prompt_id)
    if not prompt:
        console.print(f"❌ [red]Prompt {prompt_id} 不存在[/red]")
        return
    
    manager.toggle_favorite(prompt_id)
    new_status = "收藏" if not prompt['is_favorite'] else "取消收藏"
    console.print(f"✅ [green]已{new_status} Prompt {prompt_id}[/green]")


# ==================== 使用功能 ====================

@cli.command()
@click.argument('prompt_id', type=int)
@click.option('--var', '-v', multiple=True, help='变量值 (格式: name=value)')
@click.option('--copy', is_flag=True, help='复制到剪贴板')
def use(prompt_id: int, var: tuple, copy: bool):
    """使用Prompt（替换变量）"""
    manager = get_manager()
    
    # 解析变量
    variables = {}
    for v in var:
        if '=' in v:
            name, value = v.split('=', 1)
            variables[name] = value
    
    try:
        result = manager.use(prompt_id, variables)
        
        console.print(Panel(result, title="📝 生成的Prompt", border_style="green"))
        
        # 复制到剪贴板
        if copy:
            try:
                import pyperclip
                pyperclip.copy(result)
                console.print("📋 [green]已复制到剪贴板[/green]")
            except ImportError:
                console.print("⚠️ [yellow]未安装pyperclip，无法复制到剪贴板[/yellow]")
        
    except ValueError as e:
        console.print(f"❌ [red]{e}[/red]")


@cli.command()
@click.argument('prompt_id', type=int)
def preview(prompt_id: int):
    """预览Prompt（不增加使用计数）"""
    manager = get_manager()
    
    try:
        result = manager.preview(prompt_id)
        
        console.print(Panel(result['original'], title="📄 原始内容", border_style="blue"))
        console.print(Panel(result['processed'], title="📝 处理后内容", border_style="green"))
        
        if result['variables_missing']:
            console.print("[yellow]⚠️ 未替换的变量:[/yellow]")
            for var in result['variables_missing']:
                console.print(f"  - {{{{{var}}}}}")
        
    except ValueError as e:
        console.print(f"❌ [red]{e}[/red]")


# ==================== 优化功能 ====================

@cli.command()
@click.argument('prompt_id', type=int)
def analyze(prompt_id: int):
    """分析Prompt质量"""
    manager = get_manager()
    
    try:
        result = manager.analyze(prompt_id)
        
        # 总评分
        score = result['total_score']
        grade = result['grade']
        color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        
        console.print(f"\n[bold]总体评分: [{color}]{score}/100[/{color}] ({grade})[/bold]\n")
        
        # 各项评分
        table = Table(title="📊 详细评分", box=box.ROUNDED)
        table.add_column("维度", style="cyan")
        table.add_column("得分", justify="right")
        table.add_column("权重", justify="right")
        table.add_column("问题", style="yellow")
        
        for category, data in result['categories'].items():
            score_color = "green" if data['score'] >= 80 else "yellow" if data['score'] >= 60 else "red"
            issues = ", ".join(data['issues']) if data['issues'] else "无"
            table.add_row(
                data['name'],
                f"[{score_color}]{data['score']}[/{score_color}]",
                f"{int(data['weight']*100)}%",
                issues[:30] + ('...' if len(issues) > 30 else '')
            )
        
        console.print(table)
        
        # 改进建议
        if result['suggestions']:
            console.print("\n💡 [bold]改进建议:[/bold]")
            for suggestion in result['suggestions']:
                console.print(f"  • {suggestion}")
        else:
            console.print("\n✨ [green]Prompt质量良好，无需改进！[/green]")
        
    except ValueError as e:
        console.print(f"❌ [red]{e}[/red]")


@cli.command()
@click.argument('prompt_id', type=int)
@click.option('--save', is_flag=True, help='保存优化结果')
def optimize(prompt_id: int, save: bool):
    """优化Prompt"""
    manager = get_manager()
    
    try:
        result = manager.optimize(prompt_id, save=save)
        
        console.print(f"\n[bold]优化结果:[/bold]")
        console.print(f"  原评分: {result.score_before}/100")
        
        score_color = "green" if result.score_after >= 80 else "yellow"
        console.print(f"  新评分: [{score_color}]{result.score_after}/100[/{score_color}]")
        
        improvement = result.score_after - result.score_before
        if improvement > 0:
            console.print(f"  提升: [green]+{improvement:.1f}[/green]\n")
        
        # 显示改进项
        console.print("[bold]改进内容:[/bold]")
        for item in result.improvements:
            console.print(f"  ✓ {item}")
        
        # 显示优化后的内容
        console.print(Panel(result.optimized, title="📝 优化后的Prompt", border_style="green"))
        
        if save:
            console.print("\n✅ [green]已保存优化结果[/green]")
        else:
            console.print("\n💡 [dim]使用 --save 参数保存优化结果[/dim]")
        
    except ValueError as e:
        console.print(f"❌ [red]{e}[/red]")


# ==================== 导入导出 ====================

@cli.command()
@click.argument('file_path')
@click.option('--format', 'fmt', type=click.Choice(['json', 'markdown']), default='json')
def export(file_path: str, fmt: str):
    """导出Prompts到文件"""
    manager = get_manager()
    
    try:
        manager.export(format_type=fmt, file_path=file_path)
        console.print(f"✅ [green]已导出到: {file_path}[/green]")
    except Exception as e:
        console.print(f"❌ [red]导出失败: {e}[/red]")


@cli.command()
@click.argument('file_path')
@click.option('--format', 'fmt', type=click.Choice(['json']), default='json')
def import_file(file_path: str, fmt: str):
    """从文件导入Prompts"""
    manager = get_manager()
    
    try:
        manager.import_from_file(file_path, fmt)
        console.print(f"✅ [green]已从 {file_path} 导入[/green]")
    except Exception as e:
        console.print(f"❌ [red]导入失败: {e}[/red]")


# ==================== 统计信息 ====================

@cli.command()
def stats():
    """显示统计信息"""
    manager = get_manager()
    
    stats_data = manager.get_stats()
    
    table = Table(title="📊 PromptCraft 统计", box=box.DOUBLE)
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="white", justify="right")
    
    table.add_row("总Prompt数", str(stats_data['total_prompts']))
    table.add_row("收藏数", f"⭐ {stats_data['favorite_count']}")
    table.add_row("分类数", str(stats_data['category_count']))
    table.add_row("总使用次数", str(stats_data['total_uses']))
    
    console.print(table)
    
    # 显示分类
    categories = manager.get_categories()
    if categories:
        console.print("\n📁 [bold]分类列表:[/bold]")
        for cat in categories:
            console.print(f"  {cat.get('icon', '📁')} {cat['name']} - {cat.get('description', '')}")


# ==================== 快捷命令 ====================

@cli.command()
def init():
    """初始化PromptCraft（首次运行）"""
    manager = get_manager()
    
    console.print(Panel.fit(
        "🎨 [bold]PromptCraft[/bold] - 轻量级AI Prompt优化与管理工具\n\n"
        "✅ 数据库已初始化\n"
        "✅ 默认分类已创建\n\n"
        "使用 [cyan]promptcraft --help[/cyan] 查看所有命令",
        title="欢迎使用",
        border_style="green"
    ))


# 入口点
def main():
    """CLI入口点"""
    cli()


if __name__ == '__main__':
    main()
