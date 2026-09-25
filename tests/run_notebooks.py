from pathlib import Path
import json, tempfile, traceback, time, concurrent.futures, os
import nbformat
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'outputs'/'validation';REPORT.mkdir(parents=True,exist_ok=True)
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',MPLBACKEND='Agg')
cases=[(str(p.relative_to(ROOT)),{},'default') for p in sorted(ROOT.glob('notebooks/*/*.ipynb'))]
cases += [
('notebooks/01_tabular/02_supervised.ipynb',{'TASK':'regression','METRIC':'rmse'},'regression'),
('notebooks/01_tabular/02_supervised.ipynb',{'PREDICTION_KIND':'probability','CLASS_ORDER':[1,0],'TARGET_COLUMNS':['p1','p0'],'METRIC':'log_loss'},'probability'),
('notebooks/01_tabular/03_anomaly_clustering.ipynb',{'MODE':'clustering'},'clustering'),
('notebooks/02_time_series/03_sensor_windows.ipynb',{'TASK':'regression','METRIC':'rmse'},'regression'),
('notebooks/02_time_series/03_sensor_windows.ipynb',{'TASK':'anomaly'},'anomaly'),
('notebooks/03_text/02_supervised.ipynb',{'TASK':'regression','METRIC':'mae'},'regression'),
('notebooks/03_text/02_supervised.ipynb',{'ANALYZER':'word'},'word'),
('notebooks/03_text/02_supervised.ipynb',{'PREDICTION_KIND':'positive_probability','POSITIVE_CLASS':1,'METRIC':'roc_auc'},'probability'),
('notebooks/04_image/02_classification.ipynb',{'FEATURE':'color_hist'},'histogram'),
('notebooks/04_image/02_classification.ipynb',{'FEATURE':'gradient'},'gradient'),
]
def run(case):
    rel,override,label=case;key=rel.replace('/','__')+'__'+label;t=time.monotonic()
    try:
        notebook=nbformat.read(ROOT/rel,as_version=4);nbformat.validate(notebook)
        # 각 사례의 설정을 해당 대입 직후에 덮어써서 분기를 검증합니다.
        for name,value in override.items():
            found=False
            import re
            for cell in notebook.cells:
                if cell.cell_type!='code':continue
                pattern=rf'(?m)^{name}=.*$'
                if re.search(pattern,cell.source):
                    # 같은 줄의 다른 설정을 유지한 채 다음 줄에서 덮어씁니다.
                    cell.source=re.sub(pattern,lambda m:m.group(0)+'\n'+name+'='+repr(value),cell.source,count=1);found=True;break
                # semicolon-separated config, patch at end of first config cell
            if not found:
                config=next(c for c in notebook.cells if c.cell_type=='code');config.source+='\n'+name+'='+repr(value)+'\n'
        with tempfile.TemporaryDirectory(prefix='maicon-nb-') as work:
            source='\n\n'.join(c.source for c in notebook.cells if c.cell_type=='code')
            result=subprocess.run([sys.executable,'-c',source],cwd=work,env=os.environ.copy(),capture_output=True,text=True,timeout=180)
            (REPORT/(key+'.log.txt')).write_text(result.stdout+result.stderr)
            if result.returncode: raise RuntimeError(result.stderr[-6000:])
        nbformat.write(notebook,REPORT/(key+'.ipynb'))
        result={'notebook':rel,'case':label,'status':'passed','seconds':round(time.monotonic()-t,2)}
    except Exception:
        (REPORT/(key+'.error.txt')).write_text(traceback.format_exc())
        result={'notebook':rel,'case':label,'status':'failed','seconds':round(time.monotonic()-t,2),'error_file':key+'.error.txt'}
    print(json.dumps(result),flush=True);return result
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,cases))
    (REPORT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    failures=sum(r['status']=='failed' for r in results)
    print('TOTAL',len(results),'FAILED',failures,flush=True)
    raise SystemExit(bool(failures))
