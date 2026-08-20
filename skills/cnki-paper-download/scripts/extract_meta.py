"""
从下载的PDF提取元数据，生成GB/T 7714格式文献清单
PDF第一页通常含：标题/作者/期刊名/年份/卷期/页码
"""
import os, re, json

DIR = r"D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易"

def extract_first_page_text(path):
    """用正则直接从PDF二进制提取第一页文本（简化版，用PyPDF2更准但可能没装）"""
    try:
        import PyPDF2
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) > 0:
                return reader.pages[0].extract_text() or ""
    except ImportError:
        pass
    except Exception as e:
        return f"PDF读取失败: {e}"
    return ""

# 尝试PyPDF2
try:
    import PyPDF2
    print("✅ PyPDF2可用")
except ImportError:
    print("⚠️ PyPDF2未安装，尝试安装")
    import subprocess
    subprocess.run(["pip", "install", "PyPDF2", "-q"], check=False)
    try:
        import PyPDF2
        print("✅ PyPDF2安装成功")
    except:
        print("❌ PyPDF2不可用")

# 提取每篇的元数据
papers = []
for fname in sorted(os.listdir(DIR)):
    if not fname.endswith(".pdf"):
        continue
    path = os.path.join(DIR, fname)
    text = extract_first_page_text(path)
    papers.append({"file": fname, "first_page": text[:1500]})

# 输出供分析
with open(r"D:\BaiduSyncdisk\AIKnowledgeBase\Hermesagent\hermes-data\scripts\_pdf_meta.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)
print(f"已提取 {len(papers)} 篇元数据到 _pdf_meta.json")
for p in papers[:3]:
    print(f"\n--- {p['file'][:40]} ---")
    print(p["first_page"][:400])
