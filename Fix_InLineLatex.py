# %% 
import pyperclip
import re

def fix_inline_latex():
    """
    读取剪贴板中的Markdown文本,在行内公式结尾符号(*或$$)后添加空格
    在行内公式开始符号($或$$)前添加空格
    排除代码块中的内容
    """
    # 读取剪贴板内容
    text = pyperclip.paste()
    
    if not text:
        print("剪贴板为空")
        return
    
    # 先提取所有代码块,用占位符替换
    code_blocks = []
    
    # 匹配```代码块
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"___CODE_BLOCK_{len(code_blocks)-1}___"
    
    text = re.sub(r'```[\s\S]*?```', save_code_block, text)
    
    # 匹配`行内代码`
    text = re.sub(r'`[^`]+?`', save_code_block, text)
    
    # 使用栈匹配LaTeX公式并添加空格
    result = []
    i = 0
    
    while i < len(text):
        # 检查是否是$$
        if i < len(text) - 1 and text[i:i+2] == '$$':
            start = i
            # 检查前面是否需要添加空格
            if result and result[-1] not in (' ', '\n', '\t', '\r'):
                result.append(' ')
            
            i += 2
            # 查找配对的$$
            while i < len(text) - 1:
                if text[i:i+2] == '$$':
                    i += 2
                    # 检查后面是否需要添加空格
                    if i < len(text) and text[i] not in (' ', '\n', '\t', '\r'):
                        result.append(text[start:i] + ' ')
                    else:
                        result.append(text[start:i])
                    break
                i += 1
            else:
                # 没找到配对的,原样保留
                result.append(text[start:i])
        # 检查是否是单$
        elif text[i] == '$':
            start = i
            # 检查前面是否需要添加空格
            if result and result[-1] not in (' ', '\n', '\t', '\r'):
                result.append(' ')
            
            i += 1
            # 查找配对的$
            while i < len(text):
                if text[i] == '$':
                    i += 1
                    # 检查后面是否需要添加空格
                    if i < len(text) and text[i] not in (' ', '\n', '\t', '\r'):
                        result.append(text[start:i] + ' ')
                    else:
                        result.append(text[start:i])
                    break
                i += 1
            else:
                # 没找到配对的,原样保留
                result.append(text[start:i])
        else:
            result.append(text[i])
            i += 1
    
    text = ''.join(result)
    
    # 还原代码块
    for idx, code_block in enumerate(code_blocks):
        text = text.replace(f"___CODE_BLOCK_{idx}___", code_block)
    
    # 将处理后的文本写回剪贴板
    pyperclip.copy(text)
    print("处理完成！已将结果复制到剪贴板")

def fix_inline_BoldIta():
    """
    读取剪贴板中的Markdown文本,在行内加粗/斜体结尾符号(*或**)后添加空格
    在行内加粗/斜体开始符号(*或**)前添加空格
    排除代码块和LaTeX公式($...$或$$...$$)中的内容
    前后如果是空格或~波浪号则不加空格
    """
    text = pyperclip.paste()
    if not text:
        print("剪贴板为空")
        return

    code_blocks = []
    latex_blocks = []

    # 匹配```代码块
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"___CODE_BLOCK_{len(code_blocks)-1}___"

    # 匹配LaTeX公式块
    def save_latex_block(match):
        latex_blocks.append(match.group(0))
        return f"___LATEX_BLOCK_{len(latex_blocks)-1}___"

    # 提取代码块
    text = re.sub(r'```[\s\S]*?```', save_code_block, text)
    # 提取行内代码
    text = re.sub(r'`[^`]+?`', save_code_block, text)
    # 提取$$...$$公式
    text = re.sub(r'\$\$[\s\S]*?\$\$', save_latex_block, text)
    # 提取$...$公式（避免$$...$$已被替换）
    text = re.sub(r'\$[^$]*?\$', save_latex_block, text)

    # 处理加粗/斜体
    result = []
    i = 0
    while i < len(text):
        # 检查是否是**
        if i < len(text) - 1 and text[i:i+2] == '**':
            start = i
            # 检查前面是否需要添加空格
            if result and result[-1] not in (' ', '\n', '\t', '\r', '~'):
                result.append(' ')
            i += 2
            # 查找配对的**
            while i < len(text) - 1:
                if text[i:i+2] == '**':
                    i += 2
                    # 检查后面是否需要添加空格
                    if i < len(text) and text[i] not in (' ', '\n', '\t', '\r', '~'):
                        result.append(text[start:i] + ' ')
                    else:
                        result.append(text[start:i])
                    break
                i += 1
            else:
                result.append(text[start:i])
        # 检查是否是单*
        elif text[i] == '*':
            start = i
            # 检查前面是否需要添加空格
            if result and result[-1] not in (' ', '\n', '\t', '\r', '~', '*'):
                result.append(' ')
            i += 1
            # 查找配对的*
            while i < len(text):
                if text[i] == '*':
                    i += 1
                    # 检查后面是否需要添加空格
                    if i < len(text) and text[i] not in (' ', '\n', '\t', '\r', '~'):
                        result.append(text[start:i] + ' ')
                    else:
                        result.append(text[start:i])
                    break
                i += 1
            else:
                result.append(text[start:i])
        else:
            result.append(text[i])
            i += 1

    text = ''.join(result)

    # 还原LaTeX公式块
    for idx, latex_block in enumerate(latex_blocks):
        text = text.replace(f"___LATEX_BLOCK_{idx}___", latex_block)
    # 还原代码块
    for idx, code_block in enumerate(code_blocks):
        text = text.replace(f"___CODE_BLOCK_{idx}___", code_block)

    pyperclip.copy(text)
    print("处理完成！已将结果复制到剪贴板")

def fix_inline_tilde():
    """
    读取剪贴板中的Markdown文本,在成对~波浪号前后添加空格
    排除代码块中的内容
    如果~前面是*或**则不加空格
    前后如果是空格或~波浪号则不加空格
    """
    text = pyperclip.paste()
    if not text:
        print("剪贴板为空")
        return

    code_blocks = []

    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"___CODE_BLOCK_{len(code_blocks)-1}___"

    text = re.sub(r'```[\s\S]*?```', save_code_block, text)
    text = re.sub(r'`[^`]+?`', save_code_block, text)

    result = []
    i = 0
    while i < len(text):
        # 检查是否是成对~~
        if i < len(text) - 1 and text[i:i+2] == '~~':
            start = i
            # 检查前面是否需要添加空格
            if result:
                prev = ''.join(result[-2:]) if len(result) >= 2 else result[-1]
                if not (prev.endswith('*') or prev.endswith('**') or prev[-1] in (' ', '\n', '\t', '\r', '~')):
                    result.append(' ')
            i += 2
            # 查找配对的~~
            while i < len(text) - 1:
                if text[i:i+2] == '~~':
                    i += 2
                    # 检查后面是否需要添加空格
                    if i < len(text) and text[i] not in (' ', '\n', '\t', '\r', '~'):
                        result.append(text[start:i] + ' ')
                    else:
                        result.append(text[start:i])
                    break
                i += 1
            else:
                result.append(text[start:i])
        else:
            result.append(text[i])
            i += 1

    text = ''.join(result)
    for idx, code_block in enumerate(code_blocks):
        text = text.replace(f"___CODE_BLOCK_{idx}___", code_block)
    pyperclip.copy(text)
    print("处理完成！已将结果复制到剪贴板")

if __name__ == "__main__":
    fix_inline_latex()
    fix_inline_BoldIta()
    fix_inline_tilde()
# %%
