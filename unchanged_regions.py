from audioop import add
from enum import unique
import os, sys
import numpy as np
import time
from dataclasses import dataclass

REGION_SIZE_CUTOFF = 1000

def mem1FilenameFromNum(dump_num):
  return MEMDUMP_DIR_BASE + "/dump" + str(dump_num) + "/mem1_" + str(dump_num) + ".raw"
def mem2FilenameFromNum(dump_num):
  return MEMDUMP_DIR_BASE + "/dump" + str(dump_num) + "/mem2_" + str(dump_num) + ".raw"

if (len(sys.argv) < 2):
    print("Missing memdump directory argument. The cmd should look something like: unchanged_regions.py C:/PATH_TO_MEMDUMPS/memdumps")
    quit()
MEMDUMP_DIR_BASE = sys.argv[1]
print("Memdump directory: " + MEMDUMP_DIR_BASE)

initial_dump_dir = MEMDUMP_DIR_BASE + "/dump0"

with open(initial_dump_dir + '/mem1_0.raw', 'rb') as f:
  prev_mem1 = np.frombuffer(f.read(), dtype='byte')
with open(initial_dump_dir + '/mem2_0.raw', 'rb') as f:
  prev_mem2 = np.frombuffer(f.read(), dtype='byte')


MEM1_TOTAL_SIZE = prev_mem1.size
MEM2_TOTAL_SIZE = prev_mem2.size

mem_1_changed_addresses = np.array([],dtype=np.int64)
mem_2_changed_addresses = np.array([],dtype=np.int64)

dump_num = 1
prev_mem1_dump = mem1FilenameFromNum(dump_num)
prev_mem2_dump = mem2FilenameFromNum(dump_num)
while os.path.exists(prev_mem1_dump) and os.path.exists(prev_mem2_dump):

  with open(prev_mem1_dump, 'rb') as f:
    curr_mem1 = np.frombuffer(f.read(), dtype='byte')

  with open(prev_mem2_dump, 'rb') as f:
    curr_mem2 = np.frombuffer(f.read(), dtype='byte')

  curr_mem_1_changed_addresses = (prev_mem1 != curr_mem1).nonzero()
  mem_1_changed_addresses = np.append(mem_1_changed_addresses, curr_mem_1_changed_addresses[0])
  mem_1_changed_addresses = np.unique(mem_1_changed_addresses)

  curr_mem_2_changed_addresses = (prev_mem2 != curr_mem2).nonzero()
  mem_2_changed_addresses = np.append(mem_2_changed_addresses, curr_mem_2_changed_addresses[0])
  mem_2_changed_addresses = np.unique(mem_2_changed_addresses)

  dump_num += 1
  prev_mem1_dump = mem1FilenameFromNum(dump_num)
  prev_mem1 = curr_mem1

  prev_mem2_dump = mem2FilenameFromNum(dump_num)
  prev_mem2 = curr_mem2


@dataclass
class Region:
  start: np.int64
  size: np.int64

def getUnchangedRegions(changed_addresses, total_size):

  unchanged_regions = []

  changed_addresses_iter = iter(changed_addresses)
  prev_address = next(changed_addresses_iter)

  # look for large gaps in changed addresses
  for address in changed_addresses_iter:
    region_size = address - prev_address - 1
    if region_size >= REGION_SIZE_CUTOFF:
      unchanged_regions.append(Region(prev_address + 1, region_size))
    prev_address = address

  # check for end of memory region
  region_size = total_size - prev_address - 1
  if region_size >= REGION_SIZE_CUTOFF:
    unchanged_regions.append(Region(prev_address + 1, region_size))

  unchanged_regions.sort(key=lambda x: x.size, reverse=True)
  return unchanged_regions

mem1_unchanged_regions = getUnchangedRegions(mem_1_changed_addresses, MEM1_TOTAL_SIZE)

print("\nMEM1 Unchanged Regions-------:\n")
for region in mem1_unchanged_regions:
  start_val = 0x80000000 + region.start
  print(f"0x{start_val:x} size: {region.size}")

mem2_unchanged_regions = getUnchangedRegions(mem_2_changed_addresses, MEM2_TOTAL_SIZE)

print("\nMEM2 Unchanged Regions-------:\n")
for region in mem2_unchanged_regions:
  start_val = 0x90000000 + region.start
  print(f"0x{start_val:x} size: {region.size}")

