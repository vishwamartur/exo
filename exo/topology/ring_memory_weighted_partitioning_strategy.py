from typing import List
from .partitioning_strategy import PartitioningStrategy
from .topology import Topology
from .partitioning_strategy import Partition


class RingMemoryWeightedPartitioningStrategy(PartitioningStrategy):
  def partition(self, topology: Topology) -> List[Partition]:
    nodes = list(topology.all_nodes())
    nodes.sort(key=lambda x: (x[1].memory, x[0]), reverse=True)
    total_memory = sum(node[1].memory for node in nodes)
    total_flops = sum(node[1].flops.fp32 for node in nodes)
    partitions = []
    start = 0
    for node in nodes:
      memory_weight = node[1].memory / total_memory
      flops_weight = node[1].flops.fp32 / total_flops
      weight = (memory_weight + flops_weight) / 2
      end = round(start + weight, 5)
      partitions.append(Partition(node[0], start, end))
      start = end
    if partitions[-1].end != 1.0:
      partitions[-1] = Partition(partitions[-1].node_id, partitions[-1].start, 1.0)
    return partitions
