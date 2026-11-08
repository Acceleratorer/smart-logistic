# Evaluation metrics

Report these metrics for every scenario and controller variant:

- completion rate and makespan;
- ETA error and total distance;
- blocked robot-seconds, replans, detours, scans, and rejected moves;
- minimum sampled distance (`dmin`) and independently measured collisions.

Keep implementation evidence separate from experimental evidence. A counter or guard in code proves that a mechanism exists; repeated controlled runs are required to claim that it improves performance or safety.
