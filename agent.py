#!/usr/bin/env python3
import json, shutil, os, platform
from pathlib import Path

def status():
    mem={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        k,_,v=line.partition(':')
        if k in ('MemTotal','MemAvailable'): mem[k+'_MiB']=int(v.split()[0])//1024
    d=shutil.disk_usage(Path.home())
    return {'agent':'TRAHTENBERG Python Agent','version':'0.1.0','platform':platform.machine(),'cpu_threads':os.cpu_count(),'memory':mem,'storage_free_GiB':round(d.free/1024**3,2),'python':platform.python_version(),'ffmpeg_available':bool(shutil.which('ffmpeg')),'remote_control':False,'renderer_connected':False}

if __name__=='__main__':
    print(json.dumps(status(),indent=2,ensure_ascii=False))
