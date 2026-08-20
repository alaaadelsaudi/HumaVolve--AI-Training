# Telecom RAG API — Final Assignment

## 1. Docker

The application is containerized using Docker.

**Build the image:**
```bash
docker build -t telecom-rag-api .
```

**Run the container:**
```bash
docker run -d --name telecom-rag -p 8000:8000 --env-file .env -v ${PWD}/faiss_index:/app/faiss_index telecom-rag-api
```

**Verify:**
The API is accessible at `http://localhost:8000/docs` while the container is running.

---

## 2. RAG Request & Response (Evidence)

**Endpoint:** `POST /api/v1/query`

**Request:**
```json
{
  "ticket": "النت فاصل عندي"
}


**Response:**
```json
{
  "ticket": "النت فاصل عندي",
  "response": "بناءً على السياق المتاح، يمكنك اتباع خطوات استكشاف الأخطاء وإصلاحها التالية:\n\n1. أعد تشغيل الراوتر (Router) وانتظر لمدة دقيقتين.\n2. قم بإعادة ضبط المصنع (Factory reset) عن طريق الضغط والاستمرار على دبوس إعادة الضبط لمدة 10 ثوانٍ، ثم أعد التهيئة باستخدام VLAN ID 35.\n\nملاحظات مصفوفة التصعيد:\n- مشاكل الفواتير: التحويل إلى الرقم 111.\n- قطع في ألياف الفايبر: التصعيد فوراً إلى قسم Tier 3 Fiber Ops، واتفاقية مستوى الخدمة SLA هي 12 ساعة.\n- انقطاع جماعي على مستوى المنطقة: يتم قراءة نص الانقطاع العام للعميل، ولا يتم إرسال فنيين فرديين.",
  "sources_count": 5,
  "execution_time_seconds": 11.58,
  "prompt_tokens": 300,
  "completion_tokens": 1155,
  "total_tokens": 1455
}


## 3. Cost Calculation

**Model used:** `gemini-3.6-flash`

**Pricing (Google AI Studio, Standard tier, August 2026):**
| Type | Price per 1M tokens |
|------|---------------------|
| Input | $0.75 |
| Output | $3.75 |

**Token usage from the request above:**
- `prompt_tokens`: 300
- `completion_tokens`: 1155
- `total_tokens`: 1455

**Calculation:**
input_cost = (300 / 1,000,000) × $0.75 = $0.000225
output_cost = (1155 / 1,000,000) × $3.75 = $0.00433125
─────────────────────────────────────────────────────
total_cost = $0.00455625 (≈ $0.0046 per request)


The cost was calculated by taking the exact `prompt_tokens` and `completion_tokens` values
returned in the API response's token usage metadata, and multiplying each by its
respective per-token rate from Google's official Gemini API pricing.


## 4. CI Pipeline (GitHub Actions)

A CI workflow is defined at `.github/workflows/ci.yml`. It triggers on every push to the
`main` branch, installs dependencies, and runs the pytest test suite, failing the workflow
if any test fails.