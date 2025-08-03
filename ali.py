import requests
import urllib.parse

# تعديل هذا المتغير بالرابط المستهدف
target_url = input("[?] أدخل الرابط (مثال: https://example.com/page.php?id=): ").strip()

# ملف البايلودات
payload_file = "payloads.txt"

# مؤشرات الخطأ
sql_errors = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "pg_query",
    "mysql_fetch",
    "ORA-",
    "unknown column",
]

# فتح ملف النتائج
result_file = open("vuln_results.txt", "w", encoding="utf-8")

print("\n[+] بدء الفحص...\n")

# تحميل البايلودات
with open(payload_file, "r", encoding="utf-8") as f:
    payloads = [line.strip() for line in f if line.strip()]

for payload in payloads:
    test_url = target_url + urllib.parse.quote(payload)
    try:
        r = requests.get(test_url, timeout=7)
        content = r.text.lower()

        if any(err in content for err in sql_errors):
            print(f"[!!!] احتمال ثغرة في: {test_url}")
            result_file.write(f"[VULN] {test_url}\n")
        else:
            print(f"[--] غير مشبوه: {payload}")
    except Exception as e:
        print(f"[X] خطأ مع {payload} → {e}")

result_file.close()
print("\n[✔] انتهى الفحص. النتائج المشبوهة محفوظة في: vuln_results.txt")
