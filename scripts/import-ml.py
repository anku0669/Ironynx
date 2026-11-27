#!/usr/bin/env python3
"""Import only the pinned, educationally licensed public problem bank."""
import json, sys, pathlib, shutil
source=pathlib.Path(sys.argv[1])
dest=pathlib.Path(sys.argv[2])
manifest=json.loads((dest/"catalog.json").read_text())
files={p.stem:p for p in (source/"build").glob("*.json") if p.stem.isdigit()}
assert set(files)=={p["id"] for p in manifest["problems"]}, "Pinned manifest mismatch"
records=[]
for p in manifest["problems"]:
    d=json.loads(files[p["id"]].read_text())
    assert str(d["id"])==p["id"] and isinstance(d["title"],str)
    records.append({k:d.get(k) for k in ("id","title","category","difficulty")})
(dest/"problems").mkdir(exist_ok=True)
for id,path in files.items():
    shutil.copyfile(path,dest/"problems"/(id+".json"))
shutil.copyfile(source/"LICENSE",dest/"LICENSE.txt")
manifest["problems"]=records
(dest/"catalog.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
print(f"Validated and imported {len(records)} records")
