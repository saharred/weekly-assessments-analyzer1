
import os
import pandas as pd
import streamlit as st
from src.analyzer import load_all_excels, analyze, classify, DATA_DIR

st.set_page_config(page_title="Weekly Assessments Analyzer", layout="wide")

st.title("📊 Weekly Assessments Analyzer")
st.write("حلّل ملفات Excel داخل مجلد `data/`، واعرض ملخّصات لكل طالب ومادة وتصنيفات الأداء.")

with st.sidebar:
    st.header("⚙️ إعدادات بسيطة")
    data_dir = st.text_input("مسار البيانات", value=DATA_DIR)
    st.caption("ضع كل ملفات .xlsx داخل هذا المجلد.")

run = st.button("تشغيل التحليل الآن")

if run:
    try:
        raw = load_all_excels(data_dir)
        st.success(f"قرأت {len(raw)} صف بيانات بنجاح ✅")
        grp, overall = analyze(raw)

        st.subheader("ملخّص الطالب × المادة")
        st.dataframe(grp)

        st.subheader("الترتيب الإجمالي للطلاب")
        st.dataframe(overall)

        # تنزيل النتائج كـ CSV
        st.download_button("تنزيل ملخص الطالب × المادة (CSV)", grp.to_csv(index=False).encode("utf-8"), "student_subject_summary.csv", "text/csv")
        st.download_button("تنزيل الترتيب الإجمالي (CSV)", overall.to_csv(index=False).encode("utf-8"), "student_overall_ranking.csv", "text/csv")

        # فلترة حسب التصنيف
        st.subheader("فلترة حسب التصنيف")
        cat = st.selectbox("اختر تصنيف", ["Platinum","Gold","Silver","Bronze","Needs Improvement"])
        st.dataframe(overall[overall["category"]==cat])
    except SystemExit as e:
        st.error(str(e))
    except Exception as ex:
        st.exception(ex)
else:
    st.info("اضغطي زر **تشغيل التحليل الآن** بعد وضع ملفاتك في `data/`.")
