
# Weekly Assessments Analyzer (Qatar Education)

تحليل تلقائي لتجميع شيتات التقييمات الأسبوعية من ملفات Excel متعددة،
مع لوحة تحكم بسيطة بـ Streamlit وتقارير جاهزة للتصدير.

## الفكرة باختصار
- تحط كل ملفات الإكسل الخام داخل مجلد `data/`
- تشغّل `python src/analyzer.py` عشان يعمل الدمج والتحليل ويطلع لك ملفات جاهزة في `outputs/`
- أو تشغّل الواجهة `streamlit run app.py` عشان تشوفي داشبورد تفاعلي.

> المجلد يحوي مثال بيانات مبسّط داخل `data/` لتجربة أولية.

## تركيب البيئة
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

python -m pip install -U pip
pip install -r requirements.txt
```

## تشغيل التحليل (سطر أوامر)
```bash
python src/analyzer.py
```

## تشغيل الواجهة (Streamlit)
```bash
streamlit run app.py
```

## هيكلة المجلدات
```
weekly-assessments-analyzer/
├─ app.py                 # واجهة Streamlit
├─ requirements.txt
├─ src/
│  └─ analyzer.py         # منطق التحليل والتصنيف
├─ data/
│  ├─ README.md           # إرشادات وضع البيانات
│  └─ samples/            # أمثلة بيانات
├─ outputs/               # يَنتج هنا ملفات Excel/CSV بعد التحليل
├─ tests/
│  └─ test_basic.py
└─ .github/workflows/python-ci.yml
```

## تنسيقات وافتراضات البيانات
- كل ملف/شيت يمثل مادة أو شعبة، ويحتوي الأعمدة التالية (على الأقل):
  - `student_name` اسم الطالب
  - `subject` المادة (مثلاً: Math, Arabic)
  - `assessment_id` رقم/اسم التقييم الأسبوعي
  - `is_solved` هل الطالب حل هذا التقييم (1 حل / 0 لم يحل)
- يمكنك تعديل أسماء الأعمدة من خلال متغيرات البيئة أو إعدادات في الكود.

## التصنيفات الافتراضية
- Platinum: ≥ 90%
- Gold: 80–89%
- Silver: 70–79%
- Bronze: 60–69%
- Needs Improvement: < 60%

> تقدرِ تغيري العتبات من أعلى ملف `src/analyzer.py`.

## التصدير
النواتج تُحفظ في `outputs/` كالتالي:
- `student_subject_summary.xlsx`: ملخص لكل طالب × مادة
- `student_overall_ranking.xlsx`: ترتيب وتصنيف إجمالي لكل طالب

## النشر على GitHub
1) اعملي مستودع جديد على GitHub (Public أو Private).
2) رفعي الملفات مباشرة من المتصفح (Upload files) أو استخدمي الأوامر:
```bash
git init
git add .
git commit -m "Initial commit: Weekly Assessments Analyzer"
git branch -M main
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git push -u origin main
```
3) (اختياري) فعّلي GitHub Actions للفحص الآلي.

بالتوفيق ✨
