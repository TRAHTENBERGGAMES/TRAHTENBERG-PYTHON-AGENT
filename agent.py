#!/usr/bin/env python3
import json, shutil, os, platform
from pathlib import Path

def status():
    mem={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        k,_,v=line.partition(':')
        if k in ('MemTotal','MemAvailable'): mem[k+'_MiB']=int(v.split()[0])//1024
    d=shutil.disk_usage(Path.home())
    return {'agent':'TRAHTENBERG Python Agent','version':'0.2.0','platform':platform.machine(),'cpu_threads':os.cpu_count(),'memory':mem,'storage_free_GiB':round(d.free/1024**3,2),'python':platform.python_version(),'ffmpeg_available':bool(shutil.which('ffmpeg')),'remote_control':False,'renderer_connected':False}

def workspace():
    root=Path.home()/'TRAHTENBERG_WORKSPACE'
    root.mkdir(exist_ok=True)
    for name in ('music','video','projects','renders','logs','temp'):
        (root/name).mkdir(exist_ok=True)
    return root

def report():
    result=status()
    root=workspace()
    result['workspace']=str(root)
    result['clamav_available']=bool(shutil.which('clamscan'))
    result['freshclam_available']=bool(shutil.which('freshclam'))
    result['directories']=[p.name for p in root.iterdir() if p.is_dir() and not p.is_symlink()]
    return result

if __name__=='__main__':
    print(json.dumps(report(),indent=2,ensure_ascii=False))
