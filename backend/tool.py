"""
tool.py
Custom LangChain tools for structured Titanic dataset queries.

These tools complement the pandas agent by exposing specific, reliable
data-extraction functions that the agent can call explicitly.
"""

import pandas as pd
from langchain.tools import tool

from config import get_settings
from logger import get_logger

log = get_logger(__name__)
settings = get_settings()

# Load once — shared across all tools
_df: pd.DataFrame | None = None


def _get_df() -> pd.DataFrame:
    global _df
    if _df is None:
        _df = pd.read_csv(settings.data_path)
        log.info(f"Tools: dataset loaded ({len(_df)} rows)")
    return _df


# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def get_survival_rate(pclass: int | None = None, sex: str | None = None) -> str:
    """
    Return the survival rate for the Titanic dataset, optionally filtered by
    passenger class (1, 2 or 3) and/or sex ('male' or 'female').
    """
    df = _get_df().copy()
    if pclass is not None:
        df = df[df["Pclass"] == pclass]
    if sex is not None:
        df = df[df["Sex"].str.lower() == sex.lower()]
    if df.empty:
        return "No passengers match the given filters."
    rate = df["Survived"].mean() * 100
    total = len(df)
    survivors = df["Survived"].sum()
    return (
        f"Survival rate: {rate:.1f}% "
        f"({int(survivors)} survived out of {total} passengers)"
    )


@tool
def get_dataset_summary() -> str:
    """
    Return a high-level statistical summary of the Titanic dataset including
    shape, columns, missing values, and basic survival statistics.
    """
    df = _get_df()
    missing = df.isnull().sum()
    missing_report = "\n".join(
        f"  {col}: {cnt} missing" for col, cnt in missing.items() if cnt > 0
    )
    return (
        f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
        f"Columns: {', '.join(df.columns.tolist())}\n"
        f"Overall survival rate: {df['Survived'].mean()*100:.1f}%\n"
        f"Missing values:\n{missing_report or '  None'}"
    )


@tool
def get_age_stats() -> str:
    """Return descriptive statistics for passenger ages."""
    df = _get_df()
    stats = df["Age"].describe()
    return (
        f"Age statistics:\n"
        f"  Count : {int(stats['count'])}\n"
        f"  Mean  : {stats['mean']:.1f}\n"
        f"  Median: {df['Age'].median():.1f}\n"
        f"  Min   : {stats['min']:.0f}\n"
        f"  Max   : {stats['max']:.0f}\n"
        f"  Std   : {stats['std']:.1f}"
    )


# ── Tool registry exposed to agent ───────────────────────────────────────────
CUSTOM_TOOLS = [get_survival_rate, get_dataset_summary, get_age_stats]
