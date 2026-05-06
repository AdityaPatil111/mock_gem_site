"""
Mock GeM Catalogue Site
- Hardcoded 10 items from BID NO: GEM/2026/B/7084813
- Item Title & Qty visible, Make/Model/HSN are EMPTY
- Automation tool fills those 3 fields via /update-item API
Run: uvicorn app:app --port 8001 --reload
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock GeM Catalogue")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Hardcoded 10 items from actual Excel (BID NO: GEM/2026/B/7084813) ──────
# item_no matches the Excel "Item Number" column — used for matching
CATALOGUE = [
    {"item_no": "1",  "item_title": "EK3000B-3627695", "qty": "142", "make": "", "model": "", "hsn_code": ""},
    {"item_no": "2",  "item_title": "EK3000B-3393301", "qty": "45",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "3",  "item_title": "EK3000B-3897787", "qty": "68",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "5",  "item_title": "EK3000B-3632028", "qty": "30",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "6",  "item_title": "EK3000B-3077793", "qty": "49",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "7",  "item_title": "EK3000B-145578",  "qty": "68",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "8",  "item_title": "EK3000B-3642342", "qty": "20",  "make": "", "model": "", "hsn_code": ""},
    {"item_no": "9",  "item_title": "EK3000B-3814695", "qty": "3",   "make": "", "model": "", "hsn_code": ""},
    {"item_no": "11", "item_title": "EK3000B-3175517", "qty": "9",   "make": "", "model": "", "hsn_code": ""},
    {"item_no": "14", "item_title": "EK3000B-3045047", "qty": "229", "make": "", "model": "", "hsn_code": ""},
]

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/items")
async def get_items():
    return JSONResponse(CATALOGUE)

@app.post("/update-item")
async def update_item(request: Request):
    """Called by Selenium automation to fill Make, Model, HSN Code"""
    data = await request.json()
    item_no = str(data.get("item_no", "")).strip()
    for item in CATALOGUE:
        if item["item_no"] == item_no:
            item["make"]     = data.get("make", "").strip()
            item["model"]    = data.get("model", "").strip()
            item["hsn_code"] = data.get("hsn_code", "").strip()
            return JSONResponse({"status": "updated", "item_no": item_no})
    return JSONResponse({"status": "not_found", "item_no": item_no}, status_code=404)

@app.get("/progress")
async def progress():
    total  = len(CATALOGUE)
    filled = sum(1 for i in CATALOGUE if i["make"] and i["model"] and i["hsn_code"])
    return JSONResponse({"total": total, "filled": filled, "pct": round(filled/total*100)})

@app.get("/reset")
async def reset():
    """Clear all Make/Model/HSN fields back to empty"""
    for item in CATALOGUE:
        item["make"]     = ""
        item["model"]    = ""
        item["hsn_code"] = ""
    return JSONResponse({"status": "reset", "message": "All fields cleared!"})
