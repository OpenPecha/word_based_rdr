from pathlib import Path

from src.rdr_to_cql import convert_rdr_to_cql

rdr_string = Path("src/data/TIB_train.RDR").read_text(encoding="utf-8")
cql_rules = convert_rdr_to_cql(rdr_string)
print(cql_rules)
