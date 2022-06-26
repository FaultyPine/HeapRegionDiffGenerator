### diff_generator.py
A python script that takes in memory dumps from the dolphin emulator, parses differences in the binary files, and gives the user
a list of changed addresses sorted by "heap region" (see heap_regions.txt)  
  
  
The purpose of this is to research which areas of memory are changing across frames for some game. Useful when implementing Rollback Netcode.  
  

An example output of this script might look like:

```
// System FW
{ 0x805b6cf0, 0x805b6dc0, nullptr, "System FW" },
...

// MenuInstance
{ 0x81734d60, 0x81734e10, nullptr, "MenuInstance" },
...

// Replay
{ 0x91301be0, 0x91301c40, nullptr, "Replay" },
...

// CopyFB
{ 0x9134cc00, 0x9134cc10, nullptr, "CopyFB" },
...

// Fighter1Resource
{ 0x9151fa00, 0x9151fab0, nullptr, "Fighter1Resource" },
.....

// Fighter2Resource
{ 0x91b04c80, 0x91b04d30, nullptr, "Fighter2Resource" },
...

// Fighter3Instance
{ 0x812deb60, 0x812deb80, nullptr, "Fighter3Instance" },
...
```

(... means truncated text)

### unchanged_regions.py

Script to output regions of memory that are unchanged across all memory dump frames

sample output:

```
MEM1 Unchanged Regions-------:

0x80c23a46 size: 4428698
0x807824d8 size: 4205107
0x812dde12 size: 2339067
0x810602be size: 2078074
0x806729bc size: 1112859
0x81734830 size: 833488

MEM2 Unchanged Regions-------:

0x91b67654 size: 20761996
0x935f0b39 size: 10548423
0x90432344 size: 10185604
0x91546347 size: 6345997
0x92fca410 size: 6343988
0x90ff5196 size: 3197552
0x9134c9d8 size: 1988791
0x90e6f7b0 size: 1500261
```
