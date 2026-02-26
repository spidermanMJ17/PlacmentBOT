import pandas as pd
import math
import re
from collections import Counter
from agents import function_tool

#first extracting the data frame from csv file
df = pd.read_csv("Placement Drive 2026 Batch.csv")

@function_tool
def get_data() -> str:
    return df.to_string()

# _PRIORITY_COLUMN_KEYWORDS = (
#     "name",
#     "student",
#     "company",
#     "cgpa",
#     "cpi",
#     "offer",
#     "role",
#     "id",
#     "email",
# )


# def _safe_text(value: object) -> str:
#     if pd.isna(value):
#         return ""
#     return str(value).strip()


# def _tokenize(text: str) -> list[str]:
#     return re.findall(r"[a-z0-9]+", text.lower())


# def _row_to_text(row: pd.Series) -> str:
#     parts: list[str] = []
#     for column_name, cell_value in row.items():
#         value = _safe_text(cell_value)
#         if value:
#             parts.append(f"{column_name}: {value}")
#     return " | ".join(parts)


# def _build_row_vectors(dataframe: pd.DataFrame) -> tuple[list[str], list[Counter[str]], list[float]]:
#     row_texts: list[str] = []
#     vectors: list[Counter[str]] = []
#     norms: list[float] = []

#     for _, row in dataframe.iterrows():
#         text = _row_to_text(row)
#         row_texts.append(text)

#         token_counts = Counter(_tokenize(text))
#         vectors.append(token_counts)
#         norms.append(math.sqrt(sum(value * value for value in token_counts.values())))

#     return row_texts, vectors, norms


# _ROW_TEXTS, _ROW_VECTORS, _ROW_NORMS = _build_row_vectors(df)


# def _cosine_similarity(query_vector: Counter[str], row_vector: Counter[str], query_norm: float, row_norm: float) -> float:
#     if query_norm == 0 or row_norm == 0:
#         return 0.0

#     overlap_tokens = set(query_vector.keys()) & set(row_vector.keys())
#     dot_product = sum(query_vector[token] * row_vector[token] for token in overlap_tokens)
#     return dot_product / (query_norm * row_norm)


# def _select_relevant_columns(query_tokens: list[str], row_subset: pd.DataFrame, max_columns: int) -> list[str]:
#     selected_columns: list[str] = []
#     lower_columns = {column: column.lower() for column in row_subset.columns}

#     for column, lower_column in lower_columns.items():
#         if any(keyword in lower_column for keyword in _PRIORITY_COLUMN_KEYWORDS):
#             selected_columns.append(column)

#     for column, lower_column in lower_columns.items():
#         if any(token in lower_column for token in query_tokens):
#             selected_columns.append(column)

#     ordered_unique: list[str] = []
#     seen: set[str] = set()
#     for column in selected_columns:
#         if column not in seen:
#             seen.add(column)
#             ordered_unique.append(column)

#     if len(ordered_unique) < max_columns:
#         for column in row_subset.columns:
#             if column in seen:
#                 continue

#             has_value = row_subset[column].apply(lambda value: _safe_text(value) != "").any()
#             if has_value:
#                 ordered_unique.append(column)
#                 seen.add(column)

#             if len(ordered_unique) >= max_columns:
#                 break

#     return ordered_unique[:max_columns]


# @function_tool
# def get_data(query: str = "", top_k: int = 5, max_columns: int = 12) -> str:
#     """Retrieve only query-relevant rows/columns from placement CSV using local vector similarity."""
#     query = (query or "").strip()
#     top_k = max(1, min(int(top_k), 10))
#     max_columns = max(4, min(int(max_columns), 20))

#     if not query:
#         preview_rows = min(3, len(df))
#         preview = df.head(preview_rows).to_string(index=False)
#         return (
#             "No query received. Returning compact preview.\n"
#             f"Rows available: {len(df)}\n"
#             f"Columns available: {len(df.columns)}\n"
#             f"Sample columns: {', '.join(map(str, df.columns[:20]))}\n\n"
#             f"Sample rows:\n{preview}"
#         )

#     query_tokens = _tokenize(query)
#     query_vector = Counter(query_tokens)
#     query_norm = math.sqrt(sum(value * value for value in query_vector.values()))

#     scored_rows: list[tuple[int, float]] = []
#     for row_index, row_vector in enumerate(_ROW_VECTORS):
#         similarity = _cosine_similarity(query_vector, row_vector, query_norm, _ROW_NORMS[row_index])
#         if similarity > 0:
#             scored_rows.append((row_index, similarity))

#     if not scored_rows:
#         preview_rows = min(2, len(df))
#         fallback_preview = df.head(preview_rows).to_string(index=False)
#         return (
#             f"No semantic match for query: '{query}'.\n"
#             "Fallback preview:\n"
#             f"{fallback_preview}"
#         )

#     scored_rows.sort(key=lambda item: item[1], reverse=True)
#     best_row_indexes = [row_index for row_index, _ in scored_rows[:top_k]]
#     subset = df.iloc[best_row_indexes].copy()
#     subset.insert(0, "_similarity", [round(score, 4) for _, score in scored_rows[:top_k]])

#     selected_columns = ["_similarity"] + _select_relevant_columns(query_tokens, subset, max_columns=max_columns)
#     compact_subset = subset[selected_columns]

#     return (
#         f"Retrieved {len(compact_subset)} relevant rows for query: '{query}'\n"
#         f"Showing {len(selected_columns) - 1} selected data columns (+ similarity score)\n"
#         f"Columns: {', '.join(selected_columns)}\n\n"
#         f"{compact_subset.to_string(index=False)}"
#     )