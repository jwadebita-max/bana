import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from groq import Groq
from .models import FoodItem
import os
from dotenv import load_dotenv
load_dotenv()

# 🔑 مفتاح Groq API الخاص بك
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("\n🟢 [GROQ AI] زبون جديد اتصل بالخدمة")
        await self.accept()

    async def disconnect(self, close_code):
        print(f"\n🔴 [GROQ AI] تم قطع الاتصال (Code: {close_code})")

    async def receive(self, text_data):
        print(f"\n📥 [الطلب المباشر]: {text_data}")
        text_data_json = json.loads(text_data)
        user_speech = text_data_json.get('message', '').strip()

        response_data = await self.process_voice_with_groq(user_speech)
        print(f"📤 [الرد النهائي للـ Frontend]: {response_data}")
        await self.send(text_data=json.dumps(response_data, ensure_ascii=False))

    @sync_to_async
    def process_voice_with_groq(self, user_speech):
        all_products = list(FoodItem.objects.all())
        print(f"📦 عدد المنتجات في الداتابيز: {len(all_products)}")

        if not all_products:
            return {'status': 'not_found', 'message': 'لا توجد منتجات في قاعدة البيانات.'}

        if not user_speech:
            return {'status': 'not_found', 'message': 'لم أستمع لأي طلب.'}

        products_payload = [{
            'id': p.id,
            'name': p.name,
            'category': p.category,
            'price': float(p.price),
            'rating': getattr(p, 'rating', 5),
            'description': p.description or ''
        } for p in all_products]

        system_prompt = f"""
You are an intelligent ordering assistant for the Moroccan restaurant app "BENNA".
Analyze the user's voice request and match it to our menu products or navigation commands.

Menu Items (JSON):
{json.dumps(products_payload, ensure_ascii=False)}

Rules:
1. Understand Moroccan Darija slang, Arabic phonetic typos (e.g. "صلاه", "الشلاطه" means salad/سلطة), French, and English.
2. If the user asks to go back to the home page, main page, or all products ("رجعني للرئيسية", "الصفحة الرئيسية", "جميع المنتجات", "الكل"), return a special command or all product IDs, and set navigation intent.
3. Match against product names, categories, prices, ratings, and descriptions from anywhere in the menu (even if the user is currently viewing a specific product detail page).
4. Return ONLY a valid JSON array of matching product integer IDs. Example output: [1, 2, 3]
5. If the user wants to go to home/all items, you can return all IDs or a specific signal, but for normal search, return the IDs array [].
Do NOT write any markdown, code blocks, or extra sentences. ONLY return the JSON array [].
"""

        try:
            print("⚡ جاري الاتصال بـ Groq AI...")
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_speech}
                ],
                model="qwen/qwen3.8-27b",
                temperature=0.1,
            )

            raw_text = chat_completion.choices[0].message.content.strip()
            print(f'📥 [رد Groq الخام]: "{raw_text}"')

            # استخراج الأرقام (IDs)
            matched_ids = [int(num) for num in re.findall(r'\d+', raw_text)]
            print(f"🔍 [المنتجات المطابقة IDs]: {matched_ids}")

            if matched_ids:
                matched_items = FoodItem.objects.filter(id__in=matched_ids)

                # 🌟 إرجاع البيانات مع الـ ID ورابط صفحة التفاصيل
                items = [{
                    'id': item.id,
                    'name': item.name,
                    'price': float(item.price),
                    'description': item.description or '',
                    'image': item.image.url if item.image else '',
                    'rating': getattr(item, 'rating', 5),
                    'detail_url': f"/product/{item.id}/"
                } for item in matched_items]

                if items:
                    # 🚀 إذا تم العثور على منتج واحد محدد بالصوت، نرسل رابط التحويل المباشر له
                    redirect_id = items[0]['id'] if len(items) == 1 else None
                    redirect_url = items[0]['detail_url'] if len(items) == 1 else None

                    return {
                        'status': 'success',
                        'category': 'groq_ai_search',
                        'redirect_id': redirect_id,
                        'redirect_url': redirect_url,
                        'items': items
                    }

        except Exception as e:
            print(f"❌ [خطأ تقني في Groq]: {e}")

        return {'status': 'not_found', 'message': 'عذراً، لم أجد هذا الطلب في القائمة.'}