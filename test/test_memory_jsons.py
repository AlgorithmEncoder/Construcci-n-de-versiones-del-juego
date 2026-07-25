from pathlib import Path
import json
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORIES_DIR = PROJECT_ROOT / "data" / "memories"

TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

def load_json(path, errors):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        errors.append(f"Missing file: {path}")
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {path} ({e})")
    return None

def req(data, fields, where, errors):
    for f in fields:
        if f not in data:
            errors.append(f"{where}: missing '{f}'")

def valid_time(t): return isinstance(t,str) and TIME_RE.match(t)

def validate_metadata(d,e):
    if d is None:return
    req(d,["id","name","author","version","resolution"],"metadata.json",e)

def validate_story(d,rooms,e):
    if d is None:return
    req(d,["title","objective","time_limit","initial_room","intro","ending"],"story.json",e)
    if "initial_room" in d and rooms and d["initial_room"] not in rooms:
        e.append("story.json: initial_room does not exist")

def validate_rooms(rooms,objects,e):
    if rooms is None:return
    for rid,r in rooms.items():
        req(r,["name","background","connections","objects"],f"rooms:{rid}",e)
        for c in r.get("connections",[]):
            if c not in rooms:
                e.append(f"rooms:{rid}: connection '{c}' not found")
        if objects:
            for o in r.get("objects",[]):
                if o not in objects:
                    e.append(f"rooms:{rid}: object '{o}' not found")

def validate_objects(objs,docs,pcs,rooms,e):
    if objs is None:return
    for oid,o in objs.items():
        req(o,["type","position","polygon"],f"objects:{oid}",e)
        if len(o.get("polygon",[]))<3:
            e.append(f"objects:{oid}: polygon must have >=3 points")
        t=o.get("type")
        if t=="document":
            if o.get("document_id") not in (docs or {}):
                e.append(f"objects:{oid}: invalid document_id")
        elif t=="computer":
            if o.get("computer_id") not in (pcs or {}):
                e.append(f"objects:{oid}: invalid computer_id")
        elif t=="door":
            if o.get("destination") not in (rooms or {}):
                e.append(f"objects:{oid}: invalid destination")

def validate_computers(c,e):
    if c is None:return
    for k,v in c.items():
        req(v,["emails","chats","files"],f"computers:{k}",e)

def validate_documents(d,e):
    if d is None:return
    for k,v in d.items():
        req(v,["title"],f"documents:{k}",e)
        if ("pages" in v)==("text" in v):
            e.append(f"documents:{k}: require pages XOR text")

def validate_dialogues(d,e):
    if d is None:return
    for k,v in d.items():
        if not isinstance(v,list):
            e.append(f"dialogues:{k}: must be list")

def validate_npcs(n,rooms,dialogs,e):
    if n is None:return
    for k,v in n.items():
        req(v,["name","sprite","schedule","dialogue","room", "positions"],f"npcs:{k}",e)
        if v.get("room") not in (rooms or {}):
            e.append(f"npcs:{k}: invalid room")
        if v.get("dialogue") not in (dialogs or {}):
            e.append(f"npcs:{k}: invalid dialogue")
        for s in v.get("schedule",[]):
            if not valid_time(s.get("time","")):
                e.append(f"npcs:{k}: invalid time")
            if s.get("room") not in (rooms or {}):
                e.append(f"npcs:{k}: invalid schedule room")

def validate_events(ev,npcs,rooms,e):
    if ev is None:return
    if not isinstance(ev,list):
        e.append("events.json must be list");return
    for i,v in enumerate(ev):
        req(v,["time","action"],f"events[{i}]",e)
        if not valid_time(v.get("time","")):
            e.append(f"events[{i}]: invalid time")
        a=v.get("action")
        if a=="npc_move":
            if v.get("npc") not in (npcs or {}): e.append(f"events[{i}]: invalid npc")
            if v.get("room") not in (rooms or {}): e.append(f"events[{i}]: invalid room")
        elif a=="sound":
            if "sound" not in v: e.append(f"events[{i}]: missing sound")

def main():
    total=0
    for mem in sorted(MEMORIES_DIR.glob("memory_*")):
        print(f"\n== {mem.name} ==")
        err=[]
        md=load_json(mem/"metadata.json",err)
        st=load_json(mem/"story.json",err)
        rooms=load_json(mem/"rooms.json",err)
        objs=load_json(mem/"objects.json",err)
        pcs=load_json(mem/"computers.json",err)
        docs=load_json(mem/"documents.json",err)
        npcs=load_json(mem/"npcs.json",err)
        di=load_json(mem/"dialogues.json",err)
        ev=load_json(mem/"events.json",err)
        validate_metadata(md,err)
        validate_story(st,rooms,err)
        validate_rooms(rooms,objs,err)
        validate_objects(objs,docs,pcs,rooms,err)
        validate_computers(pcs,err)
        validate_documents(docs,err)
        validate_dialogues(di,err)
        validate_npcs(npcs,rooms,di,err)
        validate_events(ev,npcs,rooms,err)
        if err:
            total+=len(err)
            for x in err: print(" -",x)
        else:
            print(" OK")
    print(f"\nTotal errors: {total}")
    sys.exit(1 if total else 0)

if __name__=="__main__":
    main()