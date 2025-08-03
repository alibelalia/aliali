import requests
import urllib.parse
import sys

# استقبال الرابط وقائمة البايلودات
target_url = input("🔗 أدخل الرابط (مع الباراميتر): ").strip()
payloads_file = input("📄 أدخل مسار ملف البايلودات: ").strip()

# التأكد من وجود علامة = في الرابط
if '=' not in target_url:
    print("❌ الرابط لا يحتوي على باراميتر صالح.")
    sys.exit()

param_name = target_url.split('=')[0] + '='

# تحميل البايلودات
try:
    with open(payloads_file, 'r') as f:
        payloads = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("❌ لم يتم العثور على ملف البايلودات.")
    sys.exit()

print(f"\n🚀 بدء اختبار {len(payloads)} بايلودات على الرابط:\n{target_url}\n")

# تجربة كل بايلود
for i, payload in enumerate(payloads, 1):
    test_url = param_name + urllib.parse.quote(payload)
    full_url = test_url

    try:
        res = requests.get(full_url, timeout=10)
        if payload in res.text:
            print(f"[✅ XSS محتمل] البايلود ظهر في الصفحة: {payload}")
        else:
            print(f"[❌] {i}/{len(payloads)} - غير فعال: {payload}")
    except Exception as e:
        print(f"[⚠️] {i}/{len(payloads)} - خطأ في الاتصال: {e}")

print("\n🏁 انتهى الفحص.")
