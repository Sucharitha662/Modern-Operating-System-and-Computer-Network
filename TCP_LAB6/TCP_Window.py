import numpy as np
import random
import matplotlib.pyplot as plt

# Simulation parameters
RTT = 0.05             # 50 ms
SIM_TIME = 20.0        # simulate for 20 sec
MSS = 1.0              # normalized MSS
ALGO = "reno"          # TCP Reno
INITIAL_CWND = 1.0
INITIAL_SSTHRESH = 64.0

LOSS_RATES = [0.001, 0.01, 0.02]  # 0.1%, 1%, 2%


def run_simulation(loss_prob):

    t = 0.0
    cwnd = INITIAL_CWND
    ssthresh = INITIAL_SSTHRESH

    time_steps = []
    cwnd_trace = []
    bytes_acked = 0.0

    # Helper function
    def send_window(cwnd):
        segs = int(max(1, round(cwnd / MSS)))
        lost = False
        acks = 0

        for _ in range(segs):
            if random.random() < loss_prob:
                lost = True
            else:
                acks += 1
        return lost, acks

    # Main simulation loop
    while t < SIM_TIME:

        time_steps.append(t)
        cwnd_trace.append(cwnd)

        in_slow_start = (cwnd < ssthresh)

        lost, acks = send_window(cwnd)

        bytes_acked += acks * MSS

        if lost:
            # multiplicative decrease
            ssthresh = max(cwnd / 2, 2.0)
            cwnd = max(cwnd / 2, 1.0)

        else:
            if in_slow_start:
                cwnd = cwnd * 2.0     # exponential
            else:
                cwnd = cwnd + 1.0     # additive

        cwnd = min(cwnd, 1000.0)
        t += RTT

    throughput = bytes_acked / SIM_TIME
    return time_steps, cwnd_trace, throughput


# ----------------------------------------------------------
# Run for each loss rate
# ----------------------------------------------------------

for loss in LOSS_RATES:
    steps, cwnds, thr = run_simulation(loss)

    plt.figure(figsize=(10, 4))
    plt.step(steps, cwnds, where="post")
    plt.xlabel("Time (s)")
    plt.ylabel("Congestion Window (cwnd)")
    plt.title(f"TCP Reno: Loss={loss*100:.2f}%, RTT={RTT}s\nThroughput={thr:.2f} MSS/s")
    plt.grid()
    plt.show()

    print(f"Loss Rate = {loss*100:.2f}%  -->  Throughput = {thr:.2f} MSS/s")
