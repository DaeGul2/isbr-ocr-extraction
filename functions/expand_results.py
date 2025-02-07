import pandas as pd

def expand_results(final_result):
    """
    결과 딕셔너리를 DataFrame으로 변환하면서, 각 컬럼의 데이터가 여러 개일 경우 행을 확장.
    """
    max_rows = max(len(v) for v in final_result.values() if isinstance(v, list))
    expanded_data = []

    for i in range(max_rows):
        row = {}
        for key, values in final_result.items():
            row[key] = values[i] if i < len(values) else ""
        expanded_data.append(row)

    return pd.DataFrame(expanded_data)
