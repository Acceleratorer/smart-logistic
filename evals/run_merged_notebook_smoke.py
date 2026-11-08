"""Static and JavaScript smoke gate for the merged five-robot notebook.

This is intentionally a smoke gate, not a claim that the full Colab/Three.js
runtime is proven. Known gaps stay listed in logs/known_issues.md.
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "output" / "jupyter-notebook" / "Warehouse_AGV_5Robot_AStar.ipynb"
RESULT = ROOT / "logs" / "merged_notebook_smoke.json"


def load_html_template() -> tuple[dict, str]:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4:
        raise AssertionError("notebook must use nbformat 4")
    source_parts = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if source.lstrip().startswith("%pip"):
            continue
        ast.parse(source)
        source_parts.append(source)
    source = "\n".join(source_parts)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "html_template" for target in node.targets):
            return notebook, ast.literal_eval(node.value)
    raise AssertionError("html_template assignment not found")


def extract_between(html: str, start: str, end: str) -> str:
    left = html.find(start)
    right = html.find(end, left + len(start))
    if left < 0 or right <= left:
        raise AssertionError(f"missing JS block: {start}")
    return html[left:right]


def run_node(source: str) -> str:
    node = shutil.which("node") or r"C:\Program Files\nodejs\node.exe"
    if not Path(node).exists() and shutil.which(node) is None:
        raise RuntimeError("Node.js is required for the JS smoke check")
    with tempfile.TemporaryDirectory() as temp_dir:
        script = Path(temp_dir) / "merged_smoke.js"
        script.write_text(source, encoding="utf-8")
        result = subprocess.run([node, str(script)], capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def check_node_syntax(source: str) -> None:
    node = shutil.which("node") or r"C:\Program Files\nodejs\node.exe"
    if not Path(node).exists() and shutil.which(node) is None:
        raise RuntimeError("Node.js is required for the JS syntax check")
    with tempfile.TemporaryDirectory() as temp_dir:
        script = Path(temp_dir) / "warehouse.js"
        script.write_text(source, encoding="utf-8")
        result = subprocess.run([node, "--check", str(script)], capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stderr.strip() or result.stdout.strip())


def main() -> int:
    _, html = load_html_template()
    checks = {
        "robot_count": html.count("const ROBOT_COUNT=5;") == 1,
        "five_bays": html.count("{x:1.25,z:") >= 5 and "{x:1.25,z:25.45}" not in html,
        "astar_route": "function findPathAStar" in html and "findPathDijkstra" not in html,
        "cpa_controller": "function f5PredictiveControl" in html,
        "swept_gap": "function f5AllowedMove" in html,
        "single_fleet_controller": "function updateAGVBehavior" not in html and "function dispatchAGV(" not in html,
    }
    scripts = re.findall(r"<script(?:[^>]*)>(.*?)</script>", html, re.IGNORECASE | re.DOTALL)
    inline_js = "\n".join(script for script in scripts if script.strip())
    inline_js = inline_js.replace("__INVENTORY_JSON_DATA__", "[]").replace("__OPERATION_DATE__", "01/01/2026")
    check_node_syntax(inline_js)

    astar = re.search(r"        function findPathAStar\(startPos, targetPos\) \{.*?\n        \}\n", html, re.DOTALL)
    if not astar:
        raise AssertionError("A* function body not found")
    other_positions = extract_between(html, "function f5OtherPositions", "function f5Dist")
    allowed_move = extract_between(html, "function f5AllowedMove", "function f5Advance")
    smoke_js = f"""
const GRID_DIM=10, GRID_RES=0.5;
const gridMap=Array.from({{length:GRID_DIM}},()=>Array.from({{length:GRID_DIM}},()=>({{walkable:true}})));
for(let z=0;z<9;z++) gridMap[4][z].walkable=false;
function getNearestWalkableNode(x,z){{const gx=Math.max(0,Math.min(GRID_DIM-1,Math.floor(x/GRID_RES)));const gz=Math.max(0,Math.min(GRID_DIM-1,Math.floor(z/GRID_RES)));if(gridMap[gx][gz].walkable)return{{x:gx,z:gz}};for(let r=1;r<GRID_DIM;r++)for(let dx=-r;dx<=r;dx++)for(let dz=-r;dz<=r;dz++){{const nx=gx+dx,nz=gz+dz;if(nx>=0&&nz>=0&&nx<GRID_DIM&&nz<GRID_DIM&&gridMap[nx][nz].walkable)return{{x:nx,z:nz}};}}return{{x:gx,z:gz}};}}
const THREE={{Vector3:class{{constructor(x,y,z){{this.x=x;this.y=y;this.z=z;}}}}}};
{astar.group(0)}
const SAFE_GAP=0.98;
const f5Dist=(a,b)=>Math.hypot(a.x-b.x,a.z-b.z);
let fleet5=[{{id:0,mesh:{{position:{{x:0,z:0}}}}}},{{id:1,mesh:{{position:{{x:.5,z:0}}}}}}];
{other_positions}{allowed_move}
const path=findPathAStar({{x:0,z:0}},{{x:4.75,z:4.75}});
if(!path.length||path.some(p=>p.x===2.25&&p.z<4.5))throw new Error('A* wall check failed');
if(f5AllowedMove({{x:0,z:0}},{{x:1,z:0}},0))throw new Error('swept-gap failed to block');
fleet5[1].mesh.position={{x:.5,z:2}};
if(!f5AllowedMove({{x:0,z:0}},{{x:1,z:0}},0,0.4))throw new Error('clearance check failed');
console.log(JSON.stringify({{astar_nodes:path.length,blocked_move:true,clearance_check:true}}));
"""
    node_output = run_node(smoke_js)
    checks["astar_wall_and_swept_gap"] = True
    RESULT.write_text(json.dumps({"checks": checks, "node_output": node_output}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not all(checks.values()):
        print(json.dumps(checks, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"checks": checks, "node_output": node_output}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
