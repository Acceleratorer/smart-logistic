# Notebook inventory and merge direction

## Scope

This inventory compares the three notebooks before implementation. The target is a single warehouse simulation with the full FEFO/WMS warehouse experience and five AGVs that accept pick-and-deliver tasks, avoid static obstacles, and resolve robot-to-robot conflicts without collisions.

## Source comparison

| Source | Main value | Current fleet | Routing / conflict logic | Warehouse / WMS | Recommendation |
|---|---|---:|---|---|---|
| `Draft_simul.ipynb` | Small, readable multi-AGV proof of concept | **5** AGVs | Time-expanded A* (`findPathST`) with node and reverse-edge reservations; fixed plan computed before animation | Simplified warehouse, shelves, doors, minimap, FPS view | Keep the reservation ideas as a reference; do not use as the visual base |
| `Warehouse_AGV_3D.ipynb` | Most complete 3D warehouse presentation | **1** AGV | Grid Dijkstra for one route; no fleet coordination | Photorealistic warehouse, FEFO inventory from Kaggle, racks, doors, charging station, tablet, search, relocation, metrics | Use as the visual/WMS base |
| `NHÓM_1_SMART_LOG.ipynb` | Closest existing integration | **6** AGVs in the current code | Shared fleet planner (`f5PlanCost`), predictive CPA checks, swept movement check, replanning, cooperative detour, deadlock scan, per-robot queues | Reuses the FEFO/3D warehouse and adds fleet UI, task history, speed CSV | Use as the integration base, then normalize it to exactly five AGVs and remove legacy single-robot paths |

`IDEA.md` is not present in the repository root at the time of inspection.

## Reusable pieces

### From `Warehouse_AGV_3D.ipynb`

- FEFO dataset loading through `kagglehub.dataset_download("willianoliveiragibin/grocery-inventory")`.
- Date parsing and FEFO grouping for real inventory records.
- Continuous rack generation with empty slots and location codes.
- Photorealistic scene construction: floor/walls, doors, rack geometry, hazard stripes, pipes/trusses, lighting, FPS and Orbit views.
- Charging-station geometry and the single-robot task lifecycle (`pick -> drop -> charge`).
- Tablet/WMS functions: product search, route preview, inspect slot, relocate stock, task metrics, and FEFO navigation.

### From `Draft_simul.ipynb`

- 0.5 m grid model over a 28 m square warehouse.
- Static obstacle marking with `markUnwalkable`.
- Time-expanded A* state `(x, z, t)` with wait actions.
- Node reservations, reverse-edge reservations, and temporary occupancy of the previous cell during movement.
- Five-robot initialization and batch dispatch.
- Min-heap priority queue and a deterministic animated interpolation over the planned time path.

The Draft model is useful for explaining reservation-based multi-agent planning, but it is a preplanned animation. It does not replan from live robot state after a sensor event, and it does not share the FEFO/WMS object model from the photorealistic notebook.

### From `NHÓM_1_SMART_LOG.ipynb`

- `initFiveFleet` and a common per-robot state machine (`PICK`, `DROP`, `RETURN`, `DOCK_TURN`, `CHARGE`, `WAIT_NEXT`, `SCAN_360`).
- Shared occupancy-aware planner `f5PlanCost` plus route wrappers for normal and charging returns.
- Predictive controller `f5PredictiveControl` using forward/side sensing and closest point of approach (CPA) over `CONFLICT_HORIZON`.
- Continuous swept-segment guard `f5AllowedMove`, which prevents a frame from moving a robot through another robot.
- Replanning (`f5TryRouteOnce`), local cooperative detours (`f5TryCooperativeDetour`), and a rate-limited 360-degree scan after a sustained no-route condition.
- Per-robot queues, reserved slot IDs, conflict/collision counters, task history, speed history, and CSV export.
- Direct handoff from WMS actions to the fleet (`f5Assign`, `dispatchPendingQueue`, `dispatchInspectedFleetItem`).

## Required corrections before adopting the integration

1. **Normalize fleet size to five.** The current `NHÓM_1_SMART_LOG.ipynb` declares six charging bays and six fleet colors, and `initFiveFleet` creates one robot per bay. The target specification says five robots. Set one authoritative `ROBOT_COUNT = 5`, create five bays, and derive colors/UI rows/CSV columns from that count.
2. **Remove or isolate the legacy Robot 1 path.** The integrated notebook still contains `agvRobotGroup`, `createAGVRobot3D`, `dispatchAGV`, `updateAGVBehavior`, `planRobot1Return`, and related single-robot state. `initFiveFleet` removes the legacy mesh, and `animate` drives `updateFiveFleet`, so this is dead/duplicate control logic that makes the notebook hard to reason about. Keep only shared fleet code for the final notebook; retain the old functions only in the source notebook for history.
3. **Use one route representation.** The fleet planner returns `{x, z}` world points while the old Robot 1 path uses `THREE.Vector3`. Keep fleet routes as plain `{x, z}` points and convert only at rendering boundaries.
4. **Make five-robot dispatch the only task entry point.** WMS buttons should call `f5Assign`/queue functions. Avoid exposing both `dispatchAGV` and fleet dispatch controls, because they can reserve the same slot through different state stores.
5. **Keep one occupancy policy.** The final controller should use the same `SAFE_GAP`, static obstacle map, reservation/occupancy check, and route-replan cadence for every robot, including returns to charging.
6. **Make the five-bay station match the scene.** The current six-bay layout, labels, and CSV filename (`lich_su_toc_do_robot_1_den_6.csv`) must be generated from the fleet count so they cannot drift from the simulation state.
7. **Validate the boot order.** The integrated notebook builds the environment, racks, charging station, legacy AGV, then the fleet. After removing the legacy robot, verify that the scene still initializes, FEFO slot meshes carry the expected `userData`, and all fleet UI callbacks are bound.

## Proposed final notebook structure

1. **Setup and data** — imports, Kaggle dataset loading, date selection, FEFO classification, reproducible inventory JSON.
2. **Simulation constants** — one `ROBOT_COUNT = 5`, world/grid dimensions, safety gap, speed/acceleration/braking, replanning and scan thresholds.
3. **Warehouse model** — scene, doors, racks, slots, obstacle boxes, five-bay charging station.
4. **Fleet model** — robot meshes, per-robot state, task queues, reserved slots, task history.
5. **Planning and safety** — occupancy-aware path cost, route wrappers, predictive CPA controller, swept-motion guard, detours and deadlock handling.
6. **Operations** — assign, queue, pick, drop, return, dock turn, charge, reset, CSV exports.
7. **WMS UI** — tablet, FEFO search, inspection, relocation, minimap, fleet status and history.
8. **Runtime** — Three.js boot, animation loop, FPS/Orbit controls, error panel.
9. **Validation cell** — assertions for fleet length, charging-bay length, unique robot IDs, non-overlapping initial bays, and route/collision counters.

## Acceptance checks for the merged model

- Exactly five robots are created and displayed.
- Every occupied slot can be assigned once; queued and active reservations cannot duplicate a slot.
- A pick/drop/return cycle completes without static-obstacle intersection.
- Two robots approaching the same aisle slow or replan; they never cross inside `SAFE_GAP`.
- A sustained blocked state triggers a bounded detour attempt and only then a rate-limited scan.
- Each robot can return to a distinct charging bay and charge independently.
- FEFO ordering, product inspection, relocation, task history, and speed CSV remain available.
- The notebook runs top-to-bottom in Colab after the Kaggle dataset is available.

## Recommended merge decision

Use `NHÓM_1_SMART_LOG.ipynb` as the starting point because it already contains the warehouse/WMS stack and the reactive five-or-more robot controller. Port the reservation semantics from `Draft_simul.ipynb` only if deterministic time-slot planning is needed for a benchmark mode; do not combine both planners into the live controller. First reduce the integrated fleet to five and delete the legacy Robot 1 execution path, then run a five-robot smoke scenario with overlapping aisle routes.
