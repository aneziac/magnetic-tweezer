import time
import magnetic_tweezer.T as T
import UI
import numpy as np
import magnetic_tweezer.micro_manager as micro_manager
import utils
import magnetic_tweezer.acs as acs
import matplotlib.pyplot as plt

acs.magnet_height_to(39)
z0 = micro_manager.GetZ()

beads = UI.SelectBeads(T, micro_manager.Get)

UI.Calibrate(beads, T, micro_manager.Get, micro_manager.GetZ, micro_manager.SetZ)

for i in range(1, len(beads)):
    beads[i].rf = 14  # reference beads
T.ComputeCalibration(beads)

for i in range(len(beads)):
    utils.PlotCalibration(beads[i])

δz = 4000
micro_manager.SetZ(z0 + δz)

trace = UI.Track(beads, T, micro_manager.Get, 500)
utils.PlotXY(trace[0])
plt.plot(utils.TraceAxis(trace[0]) - utils.TraceAxis(trace[1]))
plt.xlabel("Z(nm)")
plt.title("Z Position")
plt.grid()
plt.show()

data = []
for magneticHeight in np.arange(39, 25, -0.5):
    acs.magnet_height_to(magneticHeight)
    micro_manager.SetZ(z0 + δz)
    print(magneticHeight)
    time.sleep(1)
    micro_manager.Get()
    trace = UI.Track(beads, T, micro_manager.Get, 500)
    data.append(trace)
allTrace = []
for h in range(len(data)):
    trace = data[h]
    for j in range(len(trace[0])):
        one = []
        for i in range(len(trace)):
            one.append(trace[i][j][0])
            one.append(trace[i][j][1])
            one.append(trace[i][j][2])
        allTrace.append(one)
allTrace = np.array(allTrace)
acs.magnet_height_to(39)

plt.plot((allTrace[:, 2] - allTrace[:, 5])[:])
plt.show()

f = open("./data/trace3.dat", "w")
for t in allTrace:
    for d in t:
        f.write(str(d) + ",")
    f.write("\n")
f.close()
