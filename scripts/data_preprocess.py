import csv, ast, json, re
from datetime import datetime
from dateutil import parser as dparser

INPUT = "resumes.csv"
OUTPUT = "dataset_clean.jsonl"

def safe_ast(text):
    """Convert Python-literal dict/list → Python object; else return None."""
    if not text or text.strip() == "":
        return None
    try:
        return ast.literal_eval(text)
    except:
        # extract first {...} or [...]
        m = re.search(r'(\{.*\}|\[.*\])', text, re.S)
        if m:
            try:
                return ast.literal_eval(m.group(1))
            except:
                return None
        return None

def years_between(s, e):
    import math
    from datetime import datetime
    from dateutil import parser as dparser

    try:
        start = dparser.parse(str(s), fuzzy=True)
    except:
        return None

    if not e or "present" in str(e).lower():
        end = datetime.now()
    else:
        try:
            end = dparser.parse(str(e), fuzzy=True)
        except:
            return None

    # total months difference
    total_months = (end.year - start.year) * 12 + (end.month - start.month)

    if total_months < 0:
        return None

    # convert to years with allowed increments: 0, 0.5, 1, 1.5 ...
    full_years = total_months // 12
    leftover_months = total_months % 12

    if leftover_months >= 9:
        return int(full_years + 1)
    elif leftover_months >= 3:
        return float(full_years) + 0.5
    else:
        return int(full_years)


def norm_exp(data):
    out = []
    if not data: return []
    # Cases: {'Companies': [...] }
    if isinstance(data, dict) and "Companies" in data:
        items = data["Companies"]
    else:
        items = data if isinstance(data, list) else [data]

    for it in items:
        if not isinstance(it, dict):
            continue

        role = it.get("Role") or ""
        comp = it.get("Company Name") or ""
        sd = it.get("Start Date") or ""
        ed = it.get("End Date") or ""
        if (not ed) and it.get("Current_Flag") == 1:
            ed = "Present"

        yrs = years_between(sd, ed) if sd else None

        out.append({
            "role": role,
            "company": comp,
            "start_date": sd,
            "end_date": ed,
            "years_worked": yrs
        })

    return out

def norm_edu(data):
    out = []
    if not data: return []
    items = data if isinstance(data, list) else [data]
    for it in items:
        if not isinstance(it, dict):
            continue
        degree = it.get("Degree") or ""
        college = it.get("College Name") or ""
        sy = it.get("Start Date") or ""
        ey = it.get("End Date") or ""

        try: sy_i = int(str(sy))
        except: sy_i = None
        try: ey_i = int(str(ey))
        except: ey_i = None

        out.append({
            "degree": degree,
            "college": college,
            "start_year": sy_i,
            "end_year": ey_i
        })
    return out

def make_prompt(text):
    return (
        "Extract 'experience' and 'education' as strict JSON.\n\nResume:\n"
        + text +
        "\n\nReturn only valid JSON."
    )

count_written = 0

with open(INPUT, encoding="utf-8", newline="") as fin, open(OUTPUT, "w", encoding="utf-8") as fout:
    # Proper CSV reader supporting multiline cells:
    reader = csv.reader(fin)

    header = next(reader, None)  # skip header
    for i, row in enumerate(reader, 1):
        if len(row) < 3:
            continue

        resume = row[0]
        raw_exp = row[1]
        raw_edu = row[2]

        parsed_exp = safe_ast(raw_exp)
        parsed_edu = safe_ast(raw_edu)

        normed_exp = norm_exp(parsed_exp)
        normed_edu = norm_edu(parsed_edu)

        # ⚠️ Skip rows with empty experience (your request)
        if not normed_exp:
            continue

        final = {
            "experience": normed_exp,
            "education": normed_edu
        }

        entry = {
            "prompt": make_prompt(resume),
            "response": json.dumps(final, ensure_ascii=False)
        }

        fout.write(json.dumps(entry, ensure_ascii=False) + "\n")
        count_written += 1

print("✅ Finished.")
print("Rows written:", count_written)
