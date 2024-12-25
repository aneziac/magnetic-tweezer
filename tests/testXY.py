import numpy as np
import time
import magnetic_tweezer.micro_manager as micro_manager
import magnetic_tweezer.utils as utils
import magnetic_tweezer.gpu_tracker as gpu_tracker
import magnetic_tweezer.UI as UI

beads = []
traces = []

beads = UI.SelectBeads(gpu_tracker, micro_manager.Get)
print(beads)
n = len(beads)
for i in range(n):
    traces.append([])

gpu_tracker.XY(beads, [micro_manager.Get()])

ts = []
start = time.time()
for loop in range(1000):
    img = micro_manager.Get()
    time.sleep(0.02)
    ts.append(time.time() - start)
    gpu_tracker.XY(beads, [img])
    for i in range(n):
        b = beads[i]
        traces[i].append([b.x, b.y])

traces = np.array(traces)
print("time:", time.time() - start)
Δt = traces[0] - traces[1]
print("X STD =", np.std(utils.TraceAxis(Δt, 0)))
print("Y STD =", np.std(utils.TraceAxis(Δt, 1)))
utils.PlotXY(Δt)
