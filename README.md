# Remembrall

This repository contains artifacts (e.g., source code, ransomware sample executables, corresponding ETW events log files) for the paper [***Preventing Disruption of System Backup Against Ransomware Attacks*** published in ISSTA'25](https://doi.org/10.1145/3728880).

## Overview

Remembrall presents a new anti-ransomware perspective that focuses on defending against ransomware by monitoring and preventing system backup disruptions.

**Basic idea**:
For ransomware attacks, deleting data backups and system copies to prevent system rollback is a step that cannot be skipped and hidden.
Ransomware has to ensure that the victim host's data is completely disrupted and cannot be recovered on its own, i.e., it causes a complete loss of data accessibility and usability to facilitate the success of the ransom. 
Thus, Remembrall maintains a single, core invariant: 
*malicious rollback prevention actions signal the existence of ransomware and cannot be bypassed.*

**Implementation**:
Focusing on VSC deletion actions, Remembrall captures related malicious events and identifies all ransomware traces as a real-time defending tool. 
We comprehensively investigate the VSS mechanism and classify all attack actions that one can use to delete VSC backups throughout the application layer, OS layer, and hardware layer.
Based on the above investigation, we design and implement Remembrall to identify VSC deletions and further verify the presence of ransomware.

## Environment

Remembrall can run on any operating system that (1) is part of the Windows series, (2) the version is higher than Windows 8, and (3) x64 platform. 

We tested Remembrall on Windows 11 22H2 version.

## Configuration and Usage of Remembrall
<!-- ### 0. TL;DR
```
cd Remembrall
python Remembrall_detect.py C:/Windows/Remembrall_events.jsonl
``` -->


### 1. Select Which ETW Providers to Use
In the `info_providers` folder, there are scripts and txt files to record all useful ETW providers in the target system.

For the Windows 11 22H2 system, we manually investigate all of the 1,121 providers and focus on the following perspectives: 
(1) the associated information they provide, for example, VSS interaction, process execution, file I/O, disk I/O, etc; 
(2) whether they have high events count, which indicates the higher probability to contain interesting events; 
(3) the coverage of the application layer, the OS layer, and the hardware layer.

We ultimately select 15 providers to generate ETW events in both the OS’s user mode and kernel
mode, as shown in `selected_providers_v2.txt`.
Feel free to modify it if there are other ETW providers that you want to monitor in your task.

### 2. Configure Session Controlling 

Run `set_providers_config_tracing.py` to get an initial version of `config.json`.
```
cd Remembrall
python set_providers_config_tracing.py
```

In `config.json` file, the configuration defines that the events will be logged in `C:/Windows/Remembrall_events.json`.
You can also configure event filtering and buffering strategy here.

### 3. Start Event Generation
We customized code from `sealighter` and compile our version called `Remembrall_generator.exe` to get ETW events captured.

Run `Remembrall_generator.exe` as the Administrator, and pass in `config.json` which defines User Trace providers and Kernel Trace providers to generate ETW events.  

```
[run cmd or PowerShell with the admin privilege]
cd Remembrall
./Remembrall_generator.exe ./config.json
```

The events output will be stored in `C:/Windows/Remembrall_events_ini.json`, which contains entries of JSON object record.
Then start events parsing and structuring, to get a standard JSON output as `C:/Windows/Remembrall_events.json` which facilitates later process:

```
cd Remembrall

python output2json_arg.py C:/Windows/Remembrall_events_ini.json C:/Windows/Remembrall_events.json
```

For its data structure, please refer to `Remembrall_events_example.json`.

### 4. VSC Deletion Monitoring

```
cd Remembrall
python Remembrall_detect.py C:/Windows/Remembrall_events.json

# for artifact evaluation
python Remembrall_detect.py Remembrall_events_example.jsonl
```



Besides, the YARA rule we use can be found in the `Yara_rules` folder.


### 5. Overhead Evaluation
When Remembrall is running on the machine, run `collect_overhead.py` to analyze CPU and memory usage:

```
python collect_overhead.py
```
The results are shown in `overhead_data.txt`.


## Materials Used in the Experiment
***NOTE: These ransomware samples were collected for research purposes only.***

***NOTE-2: Be careful or these samples will operate to disrupt data after a simple double-click.***

### Ransomware Samples

Through test running and filtering process, we build a real-world dataset with 178 active samples from 60 ransomware families.
These samples were collected over a period ranging from November 2023 to March 2024. 
Regarding the first-seen timestamp distribution of the samples, 7 samples (3.9%) were reported before 2021, while the remaining 171 samples (96.1%) were first reported between 2021 and 2024.

In the experiment, Remembrall also identified eight samples that we see as zero-day ransomware variants in early July 2024. 

The compression password of each sample is *infected*.

Please refer to the `ransomware_samples` folder for more information.

### Corresponding ETW Events Log Files

Due to the space limit, the full record of ~6.5 GiB cannot be uploaded. We will find other ways to share these traces.


## Acknowledgement

We customize / reuse code from [Sealighter](https://github.com/pathtofile/Sealighter) and [KrabsETW](https://github.com/microsoft/krabsetw) for part of event filtering and parsing.
