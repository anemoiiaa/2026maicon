"""Notebook 공통 함수의 누수 방지·제출 계약을 검증합니다."""
from pathlib import Path
import json, tempfile, unittest, contextlib, io, os
os.environ.setdefault('MPLBACKEND','Agg')
ROOT=Path(__file__).resolve().parents[1]
notebook=json.loads((ROOT/'notebooks/01_tabular/02_supervised.ipynb').read_text())
common=next(c['source'] for c in notebook['cells'] if c['cell_type']=='code' and 'def write_submission' in c['source'])
ns={};exec(compile(common,'notebook_common','exec'),ns)
pd=ns['pd'];np=ns['np']

class Contracts(unittest.TestCase):
    def test_train_only_imputation(self):
        X=pd.DataFrame({'x':[1.,3.,np.nan]})
        prep=ns['tabular_preprocessor'](X).fit(X)
        median=prep.named_transformers_['num'][0].statistics_.copy()
        prep.transform(pd.DataFrame({'x':[1e9,np.nan]}))
        np.testing.assert_equal(prep.named_transformers_['num'][0].statistics_,median)
        self.assertEqual(median[0],2.)

    def test_unseen_and_all_missing_features(self):
        X=pd.DataFrame({'n':[np.nan]*3,'cat':['a','a','b']})
        prep=ns['tabular_preprocessor'](X).fit(X)
        value=prep.transform(pd.DataFrame({'n':[np.nan],'cat':['new']}))
        if hasattr(value,'toarray'):value=value.toarray()
        self.assertTrue(np.isfinite(value).all())

    def test_group_disjoint(self):
        df=pd.DataFrame({'g':np.repeat(range(10),4),'y':np.tile([0,1],20)})
        a,b=ns['split_rows'](df,'y',strategy='group',group='g')
        self.assertFalse(set(df.iloc[a].g)&set(df.iloc[b].g))

    def test_time_gap_with_duplicate_timestamps(self):
        df=pd.DataFrame({'t':np.repeat(pd.date_range('2025-01-01',periods=20),2)})
        a,b=ns['split_rows'](df,task='regression',strategy='time',time_col='t',gap=2)
        self.assertGreater((df.iloc[b].t.min()-df.iloc[a].t.max()).days,2)

    def test_submission_reorders_by_sample(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            sample=Path(d)/'sample.csv';out=Path(d)/'out.csv'
            pd.DataFrame({'id':['c','a','b'],'label':[0]*3}).to_csv(sample,index=False)
            result=ns['write_submission'](['a','b','c'],[10,20,30],'id',['label'],out,sample)
            self.assertEqual(result.label.tolist(),[30,10,20])

    def test_submission_rejects_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'out.csv'
            for ids,pred in [(['a','a'],[0,1]),(['a'],[np.nan]),(['a'],[np.inf])]:
                with self.assertRaises(ValueError):ns['write_submission'](ids,pred,'id',['label'],path)
            with self.assertRaises(ValueError):ns['write_submission'](['a'],[[.3,.3]],'id',['p0','p1'],path,probabilities=True)

    def test_probability_class_order(self):
        model=ns['LogisticRegression']().fit([[0],[1],[2],[3]],['a','a','b','b'])
        expected=model.predict_proba([[1.5]])[:,::-1]
        result=ns['classification_output'](model,[[1.5]],'probability',['b','a'])
        np.testing.assert_allclose(result,expected)
        with self.assertRaises(ValueError):ns['classification_output'](model,[[1.5]],'probability',['a','a'])

    def test_real_csv_mode(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            directory=Path(d)
            train=pd.DataFrame({'id':[f't{i}' for i in range(80)],'x':np.arange(80)%2,'category':['a','b']*40,'target':[0,1]*40})
            test=pd.DataFrame({'id':['z','x','y'],'x':[0,1,0],'category':['unknown','a','b']})
            train.to_csv(directory/'train.csv',index=False);test.to_csv(directory/'test.csv',index=False)
            pd.DataFrame({'id':['x','y','z'],'target':[0]*3}).to_csv(directory/'sample.csv',index=False)
            overrides={'DEMO':False,'TRAIN_PATH':str(directory/'train.csv'),'TEST_PATH':str(directory/'test.csv'),'SAMPLE_PATH':str(directory/'sample.csv'),'OUTPUT':str(directory/'out.csv')}
            scope={};configured=False
            for cell in notebook['cells']:
                if cell['cell_type']!='code':continue
                source=cell['source']
                if not configured:source+='\n'+ '\n'.join(f'{k}={v!r}' for k,v in overrides.items());configured=True
                exec(compile(source,'real_csv_cell','exec'),scope)
            self.assertEqual(pd.read_csv(directory/'out.csv').id.tolist(),['x','y','z'])
            # 라벨 없는 실제 CSV: 정형 이상탐지와 텍스트 군집 모두 target 없이 실행
            for relative,is_text in [('notebooks/01_tabular/03_anomaly_clustering.ipynb',False),('notebooks/03_text/03_clustering.ipynb',True)]:
                unlabeled=train.drop(columns='target').copy();future=test.copy()
                if is_text:
                    unlabeled['text']=['normal equipment' if i%2 else 'maintenance warning' for i in range(len(unlabeled))]
                    future['text']=['equipment normal','warning repair','maintenance']
                unlabeled.to_csv(directory/'train.csv',index=False);future.to_csv(directory/'test.csv',index=False)
                workflow=json.loads((ROOT/relative).read_text());scope={};configured=False
                for cell in workflow['cells']:
                    if cell['cell_type']!='code':continue
                    source=cell['source']
                    if not configured:
                        source+='\n'+ '\n'.join(f'{k}={v!r}' for k,v in {**overrides,'SAMPLE_PATH':None}.items());configured=True
                    exec(compile(source,'unlabeled_csv_cell','exec'),scope)
                self.assertEqual(len(pd.read_csv(directory/'out.csv')),3)


    def test_forecast_never_uses_future_truth(self):
        forecast=json.loads((ROOT/'notebooks/02_time_series/02_forecasting.ipynb').read_text())
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            scope={};configured=False
            for cell in forecast['cells']:
                if cell['cell_type']!='code':continue
                source=cell['source']
                if not configured:source+='\nOUTPUT='+repr(str(Path(d)/'out.csv'));configured=True
                exec(compile(source,'forecast_cell','exec'),scope)
            model=scope['models']['ridge'];history=scope['history'];future=scope['valid']
            expected=scope['recursive_predict'](model,history,future)
            changed=future.copy();changed[scope['VALUE']]=1e12
            actual=scope['recursive_predict'](model,history,changed)
            np.testing.assert_allclose(actual,expected)

if __name__=='__main__':unittest.main()
