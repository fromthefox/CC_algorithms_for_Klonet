#!/bin/bash
set -e

# Path
SCRIPT_DIR=$(dirname "$(realpath $0)")
ASTRA_SIM=${SCRIPT_DIR}/../../build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware
TARGET_WORKLOAD=$1  # 通过参数接收工作负载

# Run ASTRA-sim
(
${ASTRA_SIM} \
    --workload-configuration=${SCRIPT_DIR}/workload/${TARGET_WORKLOAD} \
    --system-configuration=${SCRIPT_DIR}/inputs/system.json \
    --network-configuration=${SCRIPT_DIR}/inputs/network.yml \
    --remote-memory-configuration=${SCRIPT_DIR}/inputs/RemoteMemory.json
)