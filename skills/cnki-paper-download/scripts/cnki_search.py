"""
知网镜像检索脚本 - 基于破解的 /kns8s/brief/grid 接口（QueryJson结构已完整）
用法: python cnki_search.py "关键词" [--page 1] [--size 20] [--db CJFQ]
DB代码: CJFQ=学术期刊, CDMD=学位论文, CDFD=博士论文, CMFD=硕士论文
"""
import requests, pickle, json, sys, time, os, argparse

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
SESSION_PKL = os.path.join(TEMP, "cnki_session.pkl")

def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Referer": "https://pdf.ccki.top/kns8s/defaultresult/index",
        "X-Requested-With": "XMLHttpRequest",
    })
    with open(SESSION_PKL, "rb") as f:
        s.cookies = pickle.load(f)
    s.get("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=20)
    s.get("http://www.wxy88.top/cnkipdf.php", timeout=25)
    return s

def build_query_json(keyword, field="SU", dbcode="CJFQ"):
    """构造完整QueryJson（KNS8标准结构）
    Logic: AND=0, OR=1, NOT=2
    OperatorType: DEFAULT=0
    """
    return {
        "Platform": "", "Resource": "", "Classid": dbcode, "Products": "",
        "QNode": {
            "QGroup": [{
                "Key": "MutiGroup", "Title": "", "Logic": 0,
                "Items": [{
                    "Key": "", "Title": "", "Logic": 0,
                    "Field": field, "Operator": 0,
                    "Value": keyword, "Value2": ""
                }],
                "ChildItems": []
            }]
        },
        "ExScope": "0", "SearchType": "2", "Rlang": "",
        "KuaKuCode": "", "Expands": {}
    }

def search(s, keyword, page=1, page_size=20, dbcode="CJFQ", field="SU"):
    url = "https://pdf.ccki.top/kns8s/brief/grid"
    params = {
        "boolSearch": "false",
        "QueryJson": json.dumps(build_query_json(keyword, field, dbcode), ensure_ascii=False),
        "pageNum": str(page),
        "pageSize": str(page_size),
        "sortField": "", "sortType": "",
        "dstyle": "1", "boolSortSearch": "false", "sentenceSearch": "false",
        "productStr": "", "aside": "", "searchFrom": "home",
        "manageId": "", "subject": "",
        "language": "", "uniplatform": "",
    }
    return s.post(url, data=params, timeout=30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=20)
    args = parser.parse_args()

    s = get_session()
    r = search(s, args.keyword, page=args.page, page_size=args.size)
    print(f"状态: {r.status_code}, 大小: {len(r.text)}字符")
    out = os.path.join(TEMP, f"cnki_result_{args.keyword}_p{args.page}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"已保存: {out}")
    if "暂无数据" in r.text or "no-content" in r.text:
        print("⚠️ 无数据")
    elif "result-table-list" in r.text or "result-table" in r.text:
        print("✅ 有结果！")
