
import pandas as pd
from src.analyzer import analyze

def test_analyze_basic():
    df = pd.DataFrame({
        "student_name": ["A","A","B"],
        "subject": ["Math","Arabic","Math"],
        "assessment_id": ["W1","W1","W1"],
        "is_solved": [1,0,1]
    })
    grp, overall = analyze(df)
    assert "solve_pct" in grp.columns
    assert "avg_pct" in overall.columns
