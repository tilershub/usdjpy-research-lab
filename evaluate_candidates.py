"""Offline candidate comparison. Never changes the production model.

CSV input: Date, Close; output includes all forecasts, coverage and costs.
Candidate selection uses development data only; the final chronological block
is evaluated once. Close-to-close fills are research proxies, not broker fills.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def dataset(price, horizon=5):
    p = price.dropna().sort_index()
    if p.index.has_duplicates or (p <= 0).any():
        raise ValueError('Price dates must be unique and prices positive')
    ret = p.pct_change()
    x = pd.DataFrame({f'return_{n}': p.pct_change(n) for n in (1, 5, 10, 20, 60)})
    x['vol20'] = ret.rolling(20).std()
    x['trend'] = p / p.ewm(span=50, adjust=False).mean() - 1
    x['range_position'] = (p-p.rolling(20).min()) / (p.rolling(20).max()-p.rolling(20).min()).replace(0,np.nan)
    # Features at close t, entry at close t+1, exit at close t+h+1.
    x['outcome'] = p.shift(-horizon-1) / p.shift(-1) - 1
    x['label_end'] = pd.Series(p.index,index=p.index).shift(-horizon-1)
    return x.replace([np.inf,-np.inf],np.nan).dropna()


def candidates():
    return {
        'logistic': make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1000,random_state=90)),
        'forest': RandomForestClassifier(n_estimators=150,max_depth=4,min_samples_leaf=30,random_state=90,n_jobs=1),
    }


def wilson(correct, n):
    if not n: return [None,None]
    z=1.96; p=correct/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [float(center-half),float(center+half)]


def metrics(frame, cost_bps, funding_bps_per_day, horizon):
    if frame.empty: return {'observations':0,'accuracy':None,'accuracy_95_interval':[None,None]}
    correct=int((frame.direction*frame.outcome>0).sum())
    costs=(cost_bps+funding_bps_per_day*horizon)/10000
    net=frame.direction*frame.outcome-costs
    equity=(1+net).cumprod()
    peak=equity.cummax().clip(lower=1)
    return {'observations':len(frame),'accuracy':correct/len(frame),'accuracy_95_interval':wilson(correct,len(frame)),
            'baseline_accuracy':float((frame.baseline*frame.outcome>0).mean()),
            'average_net_return':float(net.mean()),'total_net_return':float(equity.iloc[-1]-1),
            'max_drawdown':float((equity/peak-1).min())}


def evaluate(price,horizon=5,cost_bps=10,funding_bps_per_day=1):
    if horizon < 1 or cost_bps < 0 or funding_bps_per_day < 0: raise ValueError('Invalid horizon or costs')
    d=dataset(price,horizon)
    if len(d)<800: raise ValueError('At least 800 usable observations required; short histories cannot establish a 75% claim')
    a,b=int(len(d)*.60),int(len(d)*.80)
    features=[c for c in d if c not in ('outcome','label_end')]
    train=d.iloc[:a];train=train[train.label_end<d.index[a]]
    validation=d.iloc[a:b:horizon];validation=validation[validation.label_end<d.index[b]]
    scores={}
    for name,model in candidates().items():
        model.fit(train[features],(train.outcome>0).astype(int))
        pred=np.where(model.predict(validation[features])==1,1,-1)
        scores[name]=float(np.mean(pred*validation.outcome.to_numpy()>0))
    chosen=max(scores,key=scores.get)  # Never select on final test results.
    fit=d.iloc[:b];fit=fit[fit.label_end<d.index[b]]
    model=candidates()[chosen];model.fit(fit[features],(fit.outcome>0).astype(int))
    holdout=d.iloc[b::horizon].copy()
    probabilities=model.predict_proba(holdout[features])
    predictions=model.classes_[probabilities.argmax(axis=1)]
    holdout['direction']=np.where(predictions==1,1,-1)
    holdout['confidence']=probabilities.max(axis=1)
    holdout['baseline']=1 if (fit.outcome>0).mean()>=.5 else -1
    total=metrics(holdout,cost_bps,funding_bps_per_day,horizon)
    selective=holdout[holdout.confidence>=.75]
    selected=metrics(selective,cost_bps,funding_bps_per_day,horizon)
    selected['coverage']=len(selective)/len(holdout)
    # A high model probability alone never qualifies as demonstrated accuracy.
    qualified=bool(total['observations']>=100 and total['accuracy_95_interval'][0]>=.75 and total['accuracy']>total['baseline_accuracy'] and total['average_net_return']>0)
    report={'status':'offline candidate; not promoted','target':.75,'target_validated':qualified,
            'selection_scores':scores,'chosen':chosen,'all_forecasts':total,'confidence_75_subset':selected,
            'horizon_sessions':horizon,'round_trip_cost_bps':cost_bps,'daily_funding_bps':funding_bps_per_day,
            'train_end':str(fit.index[-1]),'test_start':str(holdout.index[0]),'test_end':str(holdout.index[-1]),
            'limitations':['Daily close execution proxy, not bid/ask or intraday stop simulation.','Costs are assumptions; funding charged per holding session, not exact calendar days.','A single chronological holdout is insufficient for a universal accuracy claim.','Probability scores are not independently calibrated; subset results and coverage are reported separately.','No revised macro data is used in this candidate.']}
    return report,holdout[['direction','confidence','baseline','outcome','label_end']]


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('csv');parser.add_argument('--output',required=True)
    parser.add_argument('--cost-bps',type=float,default=10);parser.add_argument('--funding-bps',type=float,default=1)
    args=parser.parse_args();df=pd.read_csv(args.csv,index_col=0,parse_dates=True)
    report,pred=evaluate(df.Close,cost_bps=args.cost_bps,funding_bps_per_day=args.funding_bps)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False));pred.to_csv(out.with_suffix('.forecasts.csv'))
    print(json.dumps(report,indent=2,allow_nan=False))
