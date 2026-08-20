# pandoc公式转换完整路径

> 来源：2026.8.12-8.14 省自科基金申报书公式Word化实战

## 核心路径

```
Markdown（含LaTeX公式）→ pandoc → Word（OMML原生公式）
```

## 步骤

### 1. 写Markdown
```markdown
# 标题

减排效率：

$$A_i = \frac{T^{prod}_{i}}{T^{env}_{i}}$$

或有奖惩：

$$F(e_i) = P \cdot \max(0, e - E^{*})$$
```

### 2. 转换
```bash
pandoc 申报书.md -o 申报书.docx
```

### 3. 验证
```python
import zipfile, re
from docx import Document

z = zipfile.ZipFile('申报书.docx')
xml = z.read('word/document.xml').decode('utf-8')

# OMML公式数
omml = xml.count('m:oMath')
print(f'OMML公式数: {omml}')

# TeX残留（应为空）
tex = re.findall(r'\\\\[a-zA-Z]+', xml)
print(f'TeX残留: {tex if tex else "无"}')

# 内容完整性
doc = Document('申报书.docx')
text = '\n'.join(p.text for p in doc.paragraphs)
print(f'总字数: {len(text)}')
```

通过标准：OMML>0、TeX残留=无、关键内容存在

## 已知陷阱

### cases环境渲染失败
```latex
% ❌ pandoc把cases渲染为TeX源码
$$F(e) = \begin{cases} P \cdot (e - E^*) & e > E^* \\ 0 & e \leq E^* \end{cases}$$

% ✅ 改用indicator function
$$F(e) = P \cdot (e - E^*) \cdot \mathbf{1}\{e > E^*\}$$
```

### printf吃掉反斜杠
```bash
# ❌ printf把\\frac的\f变成form feed
printf '$$P_i = \\frac{\\beta \\lambda}{A_i}$$' > test.md

# ✅ 用write_file写md文件（Python工具，不经printf/echo）
```

### 大公式文件转换
- 100+个OMML公式正常转换（实测194个）
- pandoc对标准LaTeX数学语法支持良好
- 希腊字母（\beta, \lambda等）转为Unicode字符在OMML中

## 文件大小参考
- 9500字 + 194公式 → docx 27KB
- 8600字 + 116公式 → docx 19KB
