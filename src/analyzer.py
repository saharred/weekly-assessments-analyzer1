
import os
import glob
import pandas as pd
from pathlib import Path

# ==== إعدادات يمكن تعديلها ====
DATA_DIR = os.environ.get("DATA_DIR", "data")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")

COL_STUDENT = os.environ.get("COL_STUDENT", "student_name")
COL_SUBJECT = os.environ.get("COL_SUBJECT", "subject")
COL_ASSESSMENT = os.environ.get("COL_ASSESSMENT", "assessment_id")
COL_SOLVED = os.environ.get("COL_SOLVED", "is_solved")

# عتبات التصنيف
PLATINUM = int(os.environ.get("TH_PLATINUM", 90))
GOLD_MIN = int(os.environ.get("TH_GOLD_MIN", 80))
SILVER_MIN = int(os.environ.get("TH_SILVER_MIN", 70))
BRONZE_MIN = int(os.environ.get("TH_BRONZE_MIN", 60))

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def classify(pct: float) -> str:
    if pct >= PLATINUM:
        return "Platinum"
    if pct >= GOLD_MIN:
        return "Gold"
    if pct >= SILVER_MIN:
        return "Silver"
    if pct >= BRONZE_MIN:
        return "Bronze"
    return "Needs Improvement"

def load_all_excels(folder: str) -> pd.DataFrame:
    files = glob.glob(os.path.join(folder, "*.xlsx"))
    frames = []
    for f in files:
        try:
            # نقرأ كل الشيتات
            xls = pd.ExcelFile(f)
            for sheet in xls.sheet_names:
                df = pd.read_excel(f, sheet_name=sheet)
                # نتاكد من وجود الأعمدة الأساسية
                expected = {COL_STUDENT, COL_SUBJECT, COL_ASSESSMENT, COL_SOLVED}
                if not expected.issubset(df.columns):
                    # نحاول نصلح أسماء أعمدة شائعة
                    col_map = {}
                    for c in df.columns:
                        lc = str(c).strip().lower()
                        if lc in ["student", "اسم الطالب", "student_name"]:
                            col_map[c] = COL_STUDENT
                        elif lc in ["subject", "المادة"]:
                            col_map[c] = COL_SUBJECT
                        elif lc in ["assessment", "assessment_id", "التقييم"]:
                            col_map[c] = COL_ASSESSMENT
                        elif lc in ["is_solved", "solved", "حل", "status"]:
                            col_map[c] = COL_SOLVED
                    if col_map:
                        df = df.rename(columns=col_map)
                if expected.issubset(df.columns):
                    frames.append(df[list(expected)].copy())
        except Exception as e:
            print(f"Warning: failed to read {f}: {e}")
    if not frames:
        raise SystemExit("لم يتم العثور على أي بيانات صالحة داخل مجلد data/. تأكد من الأعمدة الصحيحة.")
    cat = pd.concat(frames, ignore_index=True)
    # تنظيف
    cat[COL_STUDENT] = cat[COL_STUDENT].astype(str).str.strip()
    cat[COL_SUBJECT] = cat[COL_SUBJECT].astype(str).str.strip()
    cat[COL_ASSESSMENT] = cat[COL_ASSESSMENT].astype(str).str.strip()
    cat[COL_SOLVED] = pd.to_numeric(cat[COL_SOLVED], errors="coerce").fillna(0).astype(int)
    return cat

def analyze(df: pd.DataFrame):
    # لكل طالب × مادة: عدد التقييمات الكلي و عدد المحلول
    grp = df.groupby([COL_STUDENT, COL_SUBJECT], as_index=False).agg(
        total_assessments=(COL_ASSESSMENT, "nunique"),
        solved=(COL_SOLVED, "sum"),
    )
    grp["solve_pct"] = (grp["solved"] / grp["total_assessments"]).round(4) * 100.0

    # إجمالي الطالب عبر كل المواد
    overall = grp.groupby(COL_STUDENT, as_index=False).agg(
        subjects=("subject", "nunique"),
        total_assessments=("total_assessments", "sum"),
        solved=("solved", "sum"),
        avg_pct=("solve_pct", "mean"),
    )
    overall["avg_pct"] = overall["avg_pct"].round(2)
    overall["rank"] = overall["avg_pct"].rank(ascending=False, method="dense").astype(int)
    overall["category"] = overall["avg_pct"].apply(classify)

    return grp, overall.sort_values(["rank", COL_STUDENT])

def export(grp: pd.DataFrame, overall: pd.DataFrame):
    out1 = os.path.join(OUTPUT_DIR, "student_subject_summary.xlsx")
    out2 = os.path.join(OUTPUT_DIR, "student_overall_ranking.xlsx")
    with pd.ExcelWriter(out1, engine="openpyxl") as writer:
        grp.to_excel(writer, sheet_name="summary", index=False)
    with pd.ExcelWriter(out2, engine="openpyxl") as writer:
        overall.to_excel(writer, sheet_name="overall", index=False)
    print(f"✅ Saved: {out1}\n✅ Saved: {out2}")

def main():
    df = load_all_excels(DATA_DIR)
    grp, overall = analyze(df)
    export(grp, overall)

if __name__ == "__main__":
    main()
