# Pandoc LaTeX → docx Formula Conversion

## Workflow
Write Markdown with inline `$...$` and display `$$...$$` LaTeX formulas → pandoc → docx with native OMML (Office Math Markup Language) formulas.

### Command
```bash
pandoc input.md -o output.docx
```
No special flags needed. Pandoc auto-detects LaTeX math and converts to OMML.

### Formula styles supported
- Inline: `$A_i = \frac{T^{prod}_i}{T^{env}_i}$`
- Display: `$$P_i = \frac{\beta \lambda \omega}{A_i}$$`
- Greek letters, fractions, subscripts/superscripts, \max, \cdot, \mathbf{1} — all ✅

### NOT supported by pandoc (v3.8.3)
- `\begin{cases}...\end{cases}` — pandoc parser rejects `\b` inside cases
- **Workaround**: Use `\max(0, x)` or `\mathbf{1}\{condition\}` instead of cases

### Verification script
```python
import zipfile, re
z = zipfile.ZipFile('output.docx')
xml = z.read('word/document.xml').decode('utf-8')
print(f'OMML: {xml.count("m:oMath")}, TeX leftover: {bool(re.findall(r"\\\\[a-zA-Z]+", xml))}')
```

### Pitfall: printf escape corruption
`printf` eats `\\f` (form feed) and `\\b` (backspace), corrupting `\frac` and `\beta`.
**Fix**: Use `write_file` tool to create .md files, not shell printf/echo.
