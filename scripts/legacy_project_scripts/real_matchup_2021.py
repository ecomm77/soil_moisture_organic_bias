#!/usr/bin/env python3
# Real 2021 overpass-matched, per-sensor-family SMAP L3 validation.
# Data: ISMN *.stm hourly (real) + SMAP L3 SM_P daily HDF5 (real).
# NO synthetic data. Scoped to 2021, SMAP AM (descending, 6am) overpass,
# recommended-quality retrievals, in-situ QC flag 'G', depth_from <= 0.15 m.
import argparse, os, re, sys, glob
import numpy as np, pandas as pd

FAMS = {
    'HydraProbe': ['hydraprobe', 'stevens'],
    'Decagon/METER TDR': ['5te', 'ec-tm', 'ec-5', 'gs1', 'gs3', 'decagon', 'meter', 'teros', '5tm'],
    'Campbell CS6xx': ['cs616', 'cs650', 'cs655', 'cs61'],
    'ThetaProbe': ['thetaprobe', 'ml2', 'ml3'],
    'TRIME': ['trime'],
}
def family(sensor):
    s = sensor.lower()
    for f, keys in FAMS.items():
        if any(k in s for k in keys):
            return f
    return 'other'

FN = re.compile(r'(.+?)_(.+?)_(.+)_sm_([0-9.]+)_([0-9.]+)_(.+?)_(\d{8})_(\d{8})\.stm$')

def parse_name(path):
    b = os.path.basename(path)
    m = FN.match(b)
    if not m:
        return None
    net, net2, station, dfrom, dto, sensor, d0, d1 = m.groups()
    return dict(network=net, station=station, sensor=sensor,
                depth_from=float(dfrom), family=family(sensor))


# ---------------------------------------------------------------- in-situ
def cmd_insitu(args):
    files = [l.strip() for l in open(args.list) if l.strip()]
    rows, meta = [], []
    kept = 0
    for path in files:
        info = parse_name(path)
        if info is None or info['depth_from'] > 0.15:
            continue
        skey = f"{info['network']}|{info['station']}|{info['sensor']}|{info['depth_from']}"
        daily = {}   # date -> [sum, n]
        lat = lon = None
        try:
            with open(path, errors='ignore') as fh:
                for ln in fh:
                    p = ln.split()
                    if len(p) < 14:
                        continue
                    flag = p[13]
                    if not flag.startswith('G'):      # ISMN good-quality only
                        continue
                    try:
                        sm = float(p[12])
                    except ValueError:
                        continue
                    if not (0.0 < sm < 1.0):
                        continue
                    if lat is None:
                        try: lat, lon = float(p[7]), float(p[8])
                        except ValueError: pass
                    d = p[0].replace('/', '-')
                    a = daily.setdefault(d, [0.0, 0])
                    a[0] += sm; a[1] += 1
        except OSError:
            continue
        if len(daily) < args.min_days or lat is None:
            continue
        kept += 1
        meta.append(dict(skey=skey, network=info['network'], family=info['family'],
                         lat=lat, lon=lon, sensor=info['sensor']))
        for d, (s, n) in daily.items():
            rows.append((skey, d, s / n))
    os.makedirs(args.outdir, exist_ok=True)
    pd.DataFrame(rows, columns=['skey', 'date', 'insitu']).to_csv(
        os.path.join(args.outdir, 'insitu_2021_daily.csv'), index=False)
    md = pd.DataFrame(meta)
    md.to_csv(os.path.join(args.outdir, 'stations_2021.csv'), index=False)
    print(f"kept {kept} station-sensors; {len(rows)} daily obs")
    print(md['family'].value_counts().to_string())


# ------------------------------------------------------------------- SMAP
def _granules_by_date(smapdir):
    """One granule per date (keep the highest R reprocessing number)."""
    best = {}
    for p in glob.glob(os.path.join(smapdir, '*.h5')):
        b = os.path.basename(p)
        m = re.search(r'_(\d{8})_R(\d+)_', b)
        if not m:
            continue
        d, r = m.group(1), int(m.group(2))
        if d not in best or r > best[d][0]:
            best[d] = (r, p)
    return {d: p for d, (r, p) in best.items()}

def cmd_smap(args):
    import h5py
    md = pd.read_csv(os.path.join(args.outdir, 'stations_2021.csv'))
    slat = md['lat'].values; slon = md['lon'].values; skeys = md['skey'].values
    cellmap_path = os.path.join(args.outdir, 'cellmap.npy')
    grans = _granules_by_date(args.smapdir)
    dates = sorted(d for d in grans if d.startswith('2021') and
                   args.m0 <= int(d[4:6]) <= args.m1)
    if not dates:
        sys.exit("no granules in month range")
    # station -> flat EASE cell index (compute once, cache)
    if os.path.exists(cellmap_path):
        flat = np.load(cellmap_path)
    else:
        with h5py.File(grans[dates[0]], 'r') as f:
            g = f['Soil_Moisture_Retrieval_Data_AM']
            lat = g['latitude'][:].ravel(); lon = g['longitude'][:].ravel()
        ok = np.isfinite(lat) & np.isfinite(lon) & (np.abs(lat) <= 90) & (np.abs(lon) <= 180)
        vidx = np.where(ok)[0]; vlat = lat[vidx]; vlon = lon[vidx]
        flat = np.empty(len(slat), dtype=np.int64)
        for i in range(len(slat)):
            d2 = (vlat - slat[i]) ** 2 + (vlon - slon[i]) ** 2
            flat[i] = vidx[int(np.argmin(d2))]
        np.save(cellmap_path, flat)
        print(f"built cell map for {len(flat)} stations")
    out = os.path.join(args.outdir, 'smap_2021_at_stations.csv')
    write_header = not os.path.exists(out)
    fout = open(out, 'a')
    if write_header:
        fout.write('skey,date,smap\n')
    n_written = 0
    for k, d in enumerate(dates):
        with h5py.File(grans[d], 'r') as f:
            g = f['Soil_Moisture_Retrieval_Data_AM']
            sm = g['soil_moisture'][:].ravel()
            qf = g['retrieval_qual_flag'][:].ravel()
        vals = sm[flat]; q = qf[flat]
        good = (vals > 0) & (vals < 1) & ((q.astype(int) & 1) == 0)  # bit0=0 -> recommended
        iso = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        for i in np.where(good)[0]:
            fout.write(f"{skeys[i]},{iso},{vals[i]:.4f}\n"); n_written += 1
        if k % 40 == 0:
            print(f"  {d} ({k+1}/{len(dates)})")
    fout.close()
    print(f"appended {n_written} SMAP obs for months {args.m0}-{args.m1}")


# ---------------------------------------------------------------- metrics
def _anom(s, window=31):
    s = s.sort_index()
    return s - s.rolling(f"{window}D", center=True, min_periods=7).mean()

def cmd_metrics(args):
    ins = pd.read_csv(os.path.join(args.outdir, 'insitu_2021_daily.csv'))
    # smap CSV is hand-written and some skey values contain commas -> split from right
    srecs = []
    with open(os.path.join(args.outdir, 'smap_2021_at_stations.csv')) as fh:
        next(fh)
        for ln in fh:
            ln = ln.rstrip('\n')
            if not ln:
                continue
            try:
                sk, d, v = ln.rsplit(',', 2)
                srecs.append((sk, d, float(v)))
            except ValueError:
                continue
    sat = pd.DataFrame(srecs, columns=['skey', 'date', 'smap'])
    md = pd.read_csv(os.path.join(args.outdir, 'stations_2021.csv'))[['skey', 'network', 'family']]
    df = ins.merge(sat, on=['skey', 'date']).merge(md, on='skey')
    df['date'] = pd.to_datetime(df['date'])
    rows = []
    for (sk, net, fam), g in df.groupby(['skey', 'network', 'family']):
        g = g.set_index('date').sort_index()
        d = g[['insitu', 'smap']].dropna()
        if len(d) < args.min_matches:
            continue
        err = d['smap'].values - d['insitu'].values
        bias = float(err.mean()); ub = float(err.std(ddof=0))
        R = float(np.corrcoef(d['smap'], d['insitu'])[0, 1]) if d['insitu'].std() > 1e-9 and d['smap'].std() > 1e-9 else np.nan
        ad = pd.concat([_anom(d['insitu']), _anom(d['smap'])], axis=1).dropna()
        Ra = float(np.corrcoef(ad.iloc[:, 1], ad.iloc[:, 0])[0, 1]) if len(ad) >= args.min_matches and ad.iloc[:, 0].std() > 1e-9 and ad.iloc[:, 1].std() > 1e-9 else np.nan
        rows.append(dict(skey=sk, network=net, family=fam, n=len(d),
                         bias=bias, ubrmse=ub, R=R, Ranom=Ra))
    ps = pd.DataFrame(rows)
    ps.to_csv(os.path.join(args.outdir, 'per_station_metrics.csv'), index=False)

    rng = np.random.default_rng(20260708)
    def cluster_ci(vals, clus, stat=np.nanmedian, nb=5000):
        vals = np.asarray(vals, float); clus = np.asarray(clus)
        keep = ~np.isnan(vals); vals, clus = vals[keep], clus[keep]
        if len(vals) == 0: return (np.nan, np.nan, np.nan)
        uniq = np.unique(clus); idxby = {c: np.where(clus == c)[0] for c in uniq}
        bs = np.empty(nb)
        for b in range(nb):
            ch = rng.choice(uniq, len(uniq), replace=True)
            bs[b] = stat(vals[np.concatenate([idxby[c] for c in ch])])
        return (float(stat(vals)), float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5)))

    fam_rows = []
    for fam, g in ps.groupby('family'):
        rec = dict(family=fam, n_stations=len(g))
        for m in ['bias', 'ubrmse', 'R', 'Ranom']:
            pt, lo, hi = cluster_ci(g[m].values, g['network'].values)
            rec[f'{m}_med'], rec[f'{m}_lo'], rec[f'{m}_hi'] = pt, lo, hi
        fam_rows.append(rec)
    pf = pd.DataFrame(fam_rows).sort_values('n_stations', ascending=False)
    pf.to_csv(os.path.join(args.outdir, 'per_family_metrics.csv'), index=False)

    # HydraProbe vs non-HydraProbe
    hp = ps[ps['family'] == 'HydraProbe']; nh = ps[ps['family'] != 'HydraProbe']
    con = []
    for m in ['bias', 'ubrmse', 'R', 'Ranom']:
        a = hp[m].dropna().values; b = nh[m].dropna().values
        t = p = np.nan
        if len(a) > 1 and len(b) > 1:
            va, vb = a.var(ddof=1), b.var(ddof=1)
            se = np.sqrt(va/len(a) + vb/len(b))
            if se > 0:
                t = (a.mean()-b.mean())/se
                dof = (va/len(a)+vb/len(b))**2/((va/len(a))**2/(len(a)-1)+(vb/len(b))**2/(len(b)-1))
                import math
                try:
                    from scipy import stats; p = float(2*stats.t.sf(abs(t), dof))
                except Exception:
                    p = float(math.erfc(abs(t)/math.sqrt(2)))
        con.append(dict(metric=m, HP_median=float(np.nanmedian(hp[m])),
                        nonHP_median=float(np.nanmedian(nh[m])),
                        welch_t=float(t) if t==t else np.nan,
                        welch_p=float(p) if p==p else np.nan))
    pc = pd.DataFrame(con)
    pc.to_csv(os.path.join(args.outdir, 'hp_vs_nonhp.csv'), index=False)

    print("\n=== REAL per-family temporal metrics vs SMAP L3 SM_P AM (2021) ===")
    print(pf.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    print("\n=== HydraProbe vs non-HydraProbe ===")
    print(pc.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    _plot(pf, args.outdir)

def _plot(pf, outdir):
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    except Exception:
        return
    fam = pf.sort_values('ubrmse_med')
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.4))
    for a, (m, lab) in zip(ax, [('bias', 'bias'), ('ubrmse', 'ubRMSE'), ('R', 'R'), ('Ranom', 'anomaly R')]):
        y = fam[f'{m}_med'].values
        yerr = [y - fam[f'{m}_lo'].values, fam[f'{m}_hi'].values - y]
        cols = ['#c0392b' if f == 'HydraProbe' else '#2c7fb8' for f in fam['family']]
        a.bar(range(len(fam)), y, yerr=yerr, color=cols, capsize=3)
        a.set_xticks(range(len(fam))); a.set_xticklabels(
            [f.replace(' family', '').replace('/METER TDR', '') for f in fam['family']],
            rotation=45, ha='right', fontsize=7)
        a.set_ylabel(lab, fontsize=8); a.axhline(0, color='k', lw=0.6)
    fig.suptitle('REAL 2021 SMAP L3 SM_P (AM) temporal validation by sensor family '
                 '(red=HydraProbe; bars=network-cluster 95% CI)', fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(os.path.join(outdir, 'family_temporal_real2021.png'), dpi=200)
    print("figure ->", os.path.join(outdir, 'family_temporal_real2021.png'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('insitu'); a.add_argument('--list', required=True)
    a.add_argument('--outdir', default='real2021'); a.add_argument('--min-days', type=int, default=40)
    a.set_defaults(func=cmd_insitu)
    b = sub.add_parser('smap'); b.add_argument('--smapdir', required=True)
    b.add_argument('--outdir', default='real2021'); b.add_argument('--m0', type=int, default=1); b.add_argument('--m1', type=int, default=12)
    b.set_defaults(func=cmd_smap)
    c = sub.add_parser('metrics'); c.add_argument('--outdir', default='real2021'); c.add_argument('--min-matches', type=int, default=20)
    c.set_defaults(func=cmd_metrics)
    args = ap.parse_args(); args.func(args)
