import os, sys, urllib.parse, subprocess

def get_params():
    method = os.environ.get("REQUEST_METHOD", "GET")
    if method == "GET":
        qs = os.environ.get("QUERY_STRING", "")
    else:
        length = int(os.environ.get("CONTENT_LENGTH", "0") or 0)
        qs = sys.stdin.read(length)
    return {k: v[0] for k, v in urllib.parse.parse_qs(qs).items()}

CLIENT = "/usr/local/JSBach/scripts/client_srv_cli"

def send_to_srv_cli(cmd):
    if not cmd:
        return ""
    try:
        args = [CLIENT] + cmd.split()
        p = subprocess.run(args, capture_output=True, text=True, timeout=6)
        out = p.stdout
        if p.stderr:
            out += "\n[stderr]\n" + p.stderr
        return out.strip()
    except Exception as e:
        return f"ERROR: {e}"

def parse_interfaces(raw):
    import re
    lst = []
    for line in raw.splitlines():
        m = re.match(r'^\s*\d+\s*-\s*([A-Za-z0-9._-]+)', line)
        if m:
            lst.append(m.group(1))
    return lst

def load_interfaces_conf(path="/usr/local/JSBach/conf/interfaces.conf"):
    """Lee interfaces.conf y devuelve una lista de interfaces válidas"""
    interfaces = []
    if not os.path.exists(path):
        return interfaces

    with open(path, "r") as f:
        for line in f:
            # Buscar líneas tipo "1 - eno1"
            m = re.match(r"\s*\d+\s*-\s*([A-Za-z0-9._-]+)", line)
            if m:
                interfaces.append(m.group(1))

    return interfaces
