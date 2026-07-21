# معمارية الشورة (Shurah Architecture)

## الطبقات الأساسية

### 🥇 Decision Engine
محرك اتخاذ القرار. يستقبل `DecisionRequest` ويرجع `DecisionResult`.

### 🥈 Memory Engine
يبني معرفة طويلة المدى عن المستخدم والمشروع والتفضيلات.

### 🥉 Knowledge Engine
يفهم السؤال قبل إرساله ويحدد أفضل النماذج المناسبة.

### 4️⃣ واجهة المستخدم
طبقة عرض بسيطة. ليست مصدر القيمة.

## Pipeline

```
DecisionRequest → Validation → Intent Analysis → Model Selection
→ Parallel Execution → Response Normalization → Evidence Extraction
→ Conflict Detection → Decision Reasoning → Recommendation Builder
→ Explanation Generator → DecisionResult
```

## القواعد المعمارية

1. Decision Engine لا يقرأ قاعدة البيانات مباشرة
2. Decision Engine لا يستدعي APIs بنفسه
3. Decision Engine Stateless
4. كل قرار يجب أن يكون قابلاً للتفسير
5. عدم اليقين جزء من الناتج
6. كل مرحلة في Pipeline يمكن استبدالها دون تغيير العقد
