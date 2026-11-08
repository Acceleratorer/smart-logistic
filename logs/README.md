# Log schema

The frame-level log should use one row per robot update.

| Field | Meaning |
|---|---|
| `timestamp` | Simulation time in seconds |
| `robot_id` | Robot identifier |
| `phase` | `PICK`, `DROP`, `RETURN`, `DOCK_TURN`, `CHARGE`, or wait state |
| `position` | Robot position `(x, z)` |
| `speed` | Actual speed in m/s |
| `event` | Move, wait, replan, detour, scan, or charge event |
| `conflict_count` | Conflicts accumulated by the active task |
| `collision_flag` | Independent geometry check result |
| `distance_to_nearest` | Nearest robot distance in metres |

The notebook already exports task history and speed history as CSV. A frame-level log remains required for continuous safety checks.
