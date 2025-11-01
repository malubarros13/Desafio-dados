import pandas as pd
import numpy as np

INPUT_XLSX = "Cópia de Base_Membros_Desempenho.xlsx"
OUTPUT_CSV = "Base_Membros_Desempenho_tratada.csv"
OUTPUT_XLSX = "Base_Membros_Desempenho_tratada.xlsx"

df = pd.read_excel(INPUT_XLSX)

def padronizar_nivel(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower()
    if s in ("jr", "jr.", "junior", "júnior", "j r", "j"):
        return "Júnior"
    if s in ("pl", "pleno", "p"):
        return "Pleno"
    if s in ("sr", "sênior", "senior", "s r", "s"):
        return "Sênior"
    if s in ("n/d", "nd", "na", "n/a", "não informado", "nao informado", ""):
        return np.nan
    if "jun" in s:
        return "Júnior"
    if "plen" in s:
        return "Pleno"
    if "sen" in s:
        return "Sênior"
    return np.nan

def parse_nota(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace(",", ".")
    try:
        return float(s)
    except:
        return np.nan

def parse_engajamento(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower().replace(" ", "").replace(",", ".")
    if s in ("n/a","na","n/d","nd","naoinformado","nãoinformado",""):
        return np.nan
    if s.endswith("%"):
        s = s[:-1]
        try:
            return float(s)/100.0
        except:
            return np.nan
    try:
        v = float(s)
        if v > 1.0:
            v = v/100.0
        if v < 0:
            return np.nan
        return v
    except:
        return np.nan

cols = df.columns.str.lower()

def find_col(targets):
    for t in targets:
        if t in cols:
            return df.columns[list(cols).index(t)]
    for i,c in enumerate(cols):
        for t in targets:
            if t in c:
                return df.columns[i]
    return None

col_nivel = find_col(["nivel_senioridade","senior"])
col_tec = find_col(["avaliacao_tecnica","tec"])
col_comp = find_col(["avaliacao_comportamental","comp"])
col_eng = find_col(["engaj","pig"])

df[col_nivel] = df[col_nivel].apply(padronizar_nivel)
moda_val = df[col_nivel].mode(dropna=True)
moda_val = moda_val.iloc[0] if not moda_val.empty else "Pleno"
df[col_nivel] = df[col_nivel].fillna(moda_val)

for c in [col_tec, col_comp]:
    df[c] = df[c].apply(parse_nota)
    m = df[c].mean(skipna=True)
    if pd.isna(m): m=0.0
    df[c] = df[c].fillna(m).clip(0,10)

df[col_eng] = df[col_eng].apply(parse_engajamento)
m = df[col_eng].mean(skipna=True)
if pd.isna(m): m=0.0
df[col_eng] = df[col_eng].fillna(m).clip(0,1)

df["Score_Desempenho"] = (df[col_tec]*0.5 + df[col_comp]*0.5)
df["Status_Membro"] = df.apply(
    lambda r: "Em Destaque" if (r["Score_Desempenho"]>=7 and r[col_eng]>=0.8) else "Padrão",
    axis=1)

df.to_csv(OUTPUT_CSV, index=False, decimal=",", float_format="%.1f")
df.to_excel(OUTPUT_XLSX, index=False)
