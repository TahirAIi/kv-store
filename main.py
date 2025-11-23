from fastapi import  FastAPI, HTTPException, Request
import json

app = FastAPI()
MEMTABLE_LIMIT = 2000
memtable = {}


open("manifest.txt", "a").close()

@app.get("/{key}")
def get_value(key: str):
    if key in memtable:
        return memtable[key]
    else:
        temp = get_next_sst_file_id() - 1
        while temp > 0:
            filename = f"sst-{temp}.json"
            with open(filename, "r") as sst_file:
                list_of_dicts = json.load(sst_file)
                for d in list_of_dicts:
                    if d["key"] == key:
                        return d["value"]
            temp -= 1
    raise HTTPException(status_code=404, detail="Key not found")

@app.put("/{key}")
async def put_value(key: str, request: Request):
    value = await request.body()
    value = value.decode()
    if len(memtable) >= MEMTABLE_LIMIT:
        flush_memtable()
    memtable[key] = value
    return

def get_next_sst_file_id():
    with open("manifest.txt", "r") as manifest_file:
        lines = manifest_file.read().splitlines()
        return len(lines) +  1

def flush_memtable():
    filename = f"sst-{get_next_sst_file_id()}.json"
    with open(filename, "w") as file:
        result = [{"key": k, "value": v} for k, v in memtable.items()]
        file.write(json.dumps(result))
    with open("manifest.txt", "a") as manifest_file:
        manifest_file.write(filename + "\n")
    memtable.clear()