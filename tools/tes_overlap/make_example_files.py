import pandas as pd

A = pd.DataFrame({
    "transcript":["A1","A2","A3","A4"],
    "chrom":["chr1","chr1","chr2","chr3"],
    "strand":["+","-","+","+"],
    "start":[1000,5000,10000,20000],
    "end":[2000,5500,10100,20500],
})
B = pd.DataFrame({
    "transcript":["B1","B2","B3","B4"],
    "chrom":["chr1","chr1","chr2","chr3"],
    "strand":["+","-","+","+"],
    "start":[1100,5080,10050,30000],
    "end":[2090,5600,10120,30500],
})

# CSV
A.to_csv("examples/A.csv", index=False)
B.to_csv("examples/B.csv", index=False)

# XLSX
A.to_excel("examples/A.xlsx", index=False)
B.to_excel("examples/B.xlsx", index=False)

print("Wrote examples/A.{csv,xlsx} and examples/B.{csv,xlsx}")

