"""
知网镜像检索脚本 v2 - 使用捕获的真实请求参数
用法: python cnki_search_v2.py "关键词" [--page 1] [--size 20]
"""
import requests, pickle, json, sys, time, os, argparse

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
SESSION_PKL = os.path.join(TEMP, "cnki_session.pkl")

# 从真实请求捕获的关键参数
CLASSID = "WD0FTY92"
KUAKU_CODE = "YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,EMRPGLPA,WQ0UVIAA,BLZOG7CK,PWFIRAGL,NN3FJMUV,NLBO1Z6R"
PRODUCT_STR = "YSTT4HG0,LSTPFY1C,RMJLXHZ3,JQIRZIYA,JUP3MUPD,1UR4K4HZ,BPBAFJ5S,RMJLXHZ3,NN3FJMUV,JQIRZIYA"

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

def build_query_json(keyword, field="SU", page=1, page_size=20):
    """真实格式 QueryJson"""
    return {
        "Platform": "", "Resource": "CROSSDB", "Classid": CLASSID, "Products": "",
        "QNode": {"QGroup": [{
            "Key": "Subject", "Title": "", "Logic": 0,
            "Items": [{
                "Field": field, "Value": keyword,
                "Operator": "TOPRANK", "Logic": 0, "Title": "主题"
            }],
            "ChildItems": []
        }]},
        "ExScope": 1, "SearchType": 2, "Rlang": "BOTH",
        "KuaKuCode": KUAKU_CODE, "Expands": {}, "SearchFrom": 1
    }

def search(s, keyword, page=1, page_size=20, field="SU"):
    url = "https://pdf.ccki.top/kns8s/brief/grid"
    params = {
        "boolSearch": "true",
        "QueryJson": json.dumps(build_query_json(keyword, field, page, page_size), ensure_ascii=False),
        "pageNum": str(page),
        "pageSize": str(page_size),
        "sortField": "FFD", "sortType": "desc",
        "dstyle": "listmode",
        "productStr": PRODUCT_STR,
        "aside": "", "searchFrom": "home",
        "manageId": "", "subject": "", "language": "", "uniplatform": "NZKPT",
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
    out = os.path.join(TEMP, f"cnki_v2_{args.keyword}_p{args.page}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"已保存: {out}")
    if "暂无数据" in r.text:
        import re
        m = re.search(r'value="([^"]*)"', r.text)
        print(f"⚠️ 错误: {m.group(1) if m else r.text[:200]}")
    elif len(r.text) > 1000:
        print("✅ 检索成功！")
