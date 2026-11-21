# v19: unseen-fault closure of the two-channel system. Pre-registration
Written 21 Nov 2026, 14:45 IST, before any v19 code ran. Kaggle only.

**Why.** U1 (closure of faults the per-query attributor never saw) is 0.36 to 0.41 on every seed, below its 0.50 bar, and the ceiling analysis showed that the per-query flagger alone can reach at most about 0.51 to 0.54. The deployed system now has a second channel: the diagnostic self-test, confirmed on held-out seeds (v15). U1 of the system that actually runs both channels has not been measured.

**What is measured** (script `v19_two_channel_u1.py`, frozen-v6 harness, no new parameters). For each of the 25 LOFO faults and each of its 50 held-out episodes: if the fault is one of the 12 system faults among them (K04, R01, R03, R05, R06, R07, R10, R11, R13, R19, R22, R24), the v15 self-test runs on the faulted configuration with a dictionary that **does not contain that fault** (random probes only, as for unseen faults in v15); if a probe fails, its verified repair (or rollback) is applied to the episode; if no probe fails, the stored per-query outcome stands. The other 13 faults keep the stored per-query outcome. The per-query U1 is reproduced from the stored rows.

**Rule (held-out seeds 71, 72, 73; fixed now; no development step, because nothing is tuned):** U-1 the mean over the three seeds of the two-channel U1 is >= 0.50; U-2 on the clean system the self-test detects no fault on every seed (no false alarm, so no repair runs on healthy traffic). Reported: per-seed values, the paired difference to the per-query U1 with a bootstrap interval over faults, system and other faults separately. A trial on seed 55 checks the code; its numbers are not results.

**Caveat fixed now.** The gain can only come from system faults; query and content faults (13 of 25) keep the per-query outcome. The two-channel U1 is a property of the deployed system, not of the attributor, and the per-query U1 is reported next to it.
