import pandas as pd

df = pd.read_csv("all_data.csv")

disabilities = df["subjects"].apply(lambda sub: "Disabilities" in sub)
deafness = df["subjects"].apply(lambda sub: "Deafness" in sub)
blindness = df["subjects"].apply(lambda sub: "Blindness" in sub)
prostheses = df["subjects"].apply(lambda sub: "Prostheses" in sub)
amputation = df["subjects"].apply(lambda sub: "AMPUTATION" in sub)

data = df[disabilities | deafness | blindness | prostheses | amputation].copy()
data["date"] = data["date"].apply(lambda d: d.split("T")[0])
data = data.sort_values("date").reset_index(drop=True)
data.to_csv("data.csv")