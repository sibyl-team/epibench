"""
Library for loading instances in the benchmark repository
Only the "binary" versions are loaded here

Copyright 2020 Fabio Mazza "fab4mazz@gmail.com"

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import numpy as np
import pandas as pd

import json
import bz2
import tarfile
from pathlib import Path

def save_json(obj,file_,indent=1):
    f = open(file_,"w")
    json.dump(obj,f,indent=indent)
    f.close()


CONTACTS_FNAME = "contacts.csv.bz2"
EPI_NAME = "epidemy"
OBS_NAME = "observ"
OBS_JSON_FNAME = "obs.json"
PARAMS_FNAME = "parameters.json"
ALL_OBS_FILE= "all_obs.json.bz2"
ALL_EPI = "all_epidemies"

NAMES_COLS_CONTACTS = ["t","i","j","lambda"]
CONTACTS_DTYPES = dict(zip(NAMES_COLS_CONTACTS,(np.int,np.int,np.int,np.float) ))

STATE_MAP = {"S":0,"I":1,"R":2}
STATE_INVERSE_MAP =  {v: k for k, v in STATE_MAP.items()}


def load_exported_data(folder_path,epidemies_with_name=False,pandas_df=True):
    """
    Load only the binary formatted files from folder "folder_path"
    """
    fold = Path(folder_path)
    if not fold.exists():
        raise ValueError("Folder doesn't exists")

    with open(fold / PARAMS_FNAME) as f:
        params = json.load(f)

    with bz2.open(fold/(CONTACTS_FNAME),"r") as f:
        if pandas_df:
            contacts = pd.read_csv(f,names=NAMES_COLS_CONTACTS,dtype=CONTACTS_DTYPES)
        else:
            contacts = np.loadtxt(f,delimiter=",")

    file_all_obs = fold / ALL_OBS_FILE
    if file_all_obs.exists():
        with bz2.open(file_all_obs,"rt") as f:
            observ = json.load(f)
    else:
        print("No observations found")
        observ = None
    
    all_epi = np.load(fold/(ALL_EPI+".npz"))
    epids = all_epi.files
    indc  = [int(n.split("_")[1]) for n in epids]
    r = list(zip(indc,epids))
    r.sort()    
    epid_stacked = np.stack([all_epi[name] for i,name in r])

    return params,contacts,observ,epid_stacked

def convert_obs_to_df(globs,columns=["st","i","t"]):
    """
    Transform observations from dictionaries to DataFrames
    """
    import itertools

    all_dfs = []
    for state,obse in globs.items():
        v = STATE_MAP[state]
        for t, nodes in obse.items():
            data_iter = itertools.product([v],nodes,[int(t)])
            all_dfs.append(pd.DataFrame(data_iter,columns=columns))
    return pd.concat(all_dfs)

def save_data_exported(base_path,name_instance,pars,num_inst,contacts,
                       full_epidemies,obs_all_json=None,obs_all_df=None):
    """
    Export inference problem instance, complete with observations and epidemies
    """
    if obs_all_json is None and obs_all_df is None:
        raise ValueError("Give the observations both in ")
    if obs_all_df is None:
        obs_all_df = convert_obs_to_df(obs_all_json)
    elif obs_all_json is None:
        pass

    num_nodes = pars["n"]

    folder = Path(base_path) / name_instance
    
    if not folder.exists():
        folder.mkdir(parents=True)

    save_json(pars,folder/PARAMS_FNAME)

    with bz2.open(folder/(CONTACTS_FNAME),"w") as f:
        np.savetxt(f,contacts,delimiter=",")

    if obs_all_json is not None:
        with bz2.open(folder/(ALL_OBS_FILE),"wt") as f:
            json.dump(obs_all_json,f,indent=1)

    title_epi = " ,".join(["{}".format(i) for i in range(num_nodes)])


    for  i in range(num_inst):
        epi = full_epidemies[i]
        
        tf = tarfile.open(folder/"instance_{:03d}.tar.bz2".format(i),"w:bz2")
        epidemy_name = EPI_NAME+"_{:02d}.csv".format(i)
        observ_name = OBS_NAME + "_{:02d}.csv".format(i)

        np.savetxt(epidemy_name,epi,"%d",delimiter=",",header=title_epi)
        tf.add(epidemy_name)

        if obs_all_df is not None:
            observ = obs_all_df[i]
            observ.to_csv(observ_name,index=False)
            tf.add(observ_name)
            tf.close()
            # delete files
            f = Path(observ_name)
            f.unlink()
        else:
            tf.close()        
        
        f = Path(epidemy_name)
        f.unlink()
    
    d_epid = dict(zip(["epi_{}".format(v) for v in range(num_inst)],full_epidemies))
    np.savez_compressed(folder/"all_epidemies",**d_epid)
    print("Saved on "+folder.as_posix())

    