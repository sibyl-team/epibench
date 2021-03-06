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
import os


import json
import bz2
import tarfile
from pathlib import Path


def save_json(obj, file_, indent=1):
    f = open(file_, "w")
    json.dump(obj, f, indent=indent)
    f.close()


CONTACTS_FNAME = "contacts.gz"
EPI_NAME = "epidemy"
OBS_NAME = "observ"
OBS_JSON_FNAME = "obs.json"
PARAMS_FNAME = "parameters.json"
ALL_OBS_FILE = "all_obs.json.bz2"
ALL_EPI = "all_epidemies"

NAMES_COLS_CONTACTS = ["t", "i", "j", "lambda"]
CONTACTS_DTYPES = dict(
    zip(NAMES_COLS_CONTACTS, (np.int, np.int, np.int, np.float)))

STATE_MAP = {"S": 0, "I": 1, "R": 2}
STATE_INVERSE_MAP = {v: k for k, v in STATE_MAP.items()}


class FileDecoder(json.JSONDecoder):
    # thanks to https://stackoverflow.com/questions/45068797/how-to-convert-string-int-json-into-real-int-with-json-loads
    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            out_d = {}
            for k, v in o.items():
                try:
                    c = int(k)
                except ValueError:
                    c = k
                out_d[c] = self._decode(v)
            return out_d
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def convert_obs_to_df(globs, column_names=["st", "i", "t"]):
    """
    Transform observations from a dictionary to a DataFrame
    Column names are for, in order, the state, the node index, and the time of the observation
    """
    import itertools

    all_dfs = []
    for state, obse in globs.items():
        v = STATE_MAP[state]
        for t, nodes in obse.items():
            data_iter = itertools.product([v], nodes, [int(t)])
            all_dfs.append(pd.DataFrame(data_iter, columns=column_names))
    return pd.concat(all_dfs, ignore_index=True)


def convert_obs_to_json(df, name_state="st", name_t="t", name_node="i"):
    d = {k: {} for k in STATE_MAP.keys()}
    for si, grs in df.groupby(name_state):
        sname = STATE_INVERSE_MAP[si]
        for ti, grouptime in grs.groupby(name_t):
            d[sname][ti] = list(grouptime[name_node])
    return d

def convert_obs_to_json(df, name_state="st", name_t="t", name_node="i"):
    d = {k: {} for k in STATE_MAP.keys()}
    for si, grs in df.groupby(name_state):
        sname = STATE_INVERSE_MAP[si]
        for ti, grouptime in grs.groupby(name_t):
            d[sname][ti] = list(grouptime[name_node])
    return d

def load_exported_data(folder_path, epidemies_with_name=False, obs_dataframe=True):
    """
    Load only the binary formatted files from folder "folder_path"
    """
    fold = Path(folder_path)
    if not fold.exists():
        raise ValueError("Folder doesn't exists")

    with open(fold / PARAMS_FNAME) as f:
        params = json.load(f)

    with bz2.open(fold/(CONTACTS_FNAME), "r") as f:
        if obs_dataframe:
            contacts = pd.read_csv(
                f, names=NAMES_COLS_CONTACTS, dtype=CONTACTS_DTYPES)
        else:
            contacts = np.loadtxt(f, delimiter=",")

    file_all_obs = fold / ALL_OBS_FILE
    if file_all_obs.exists():
        with bz2.open(file_all_obs, "rt") as f:
            observ = json.load(f, cls=FileDecoder)
    else:
        print("No observations found")
        observ = None
    if obs_dataframe:
        obs_out = [convert_obs_to_df(o) for o in observ]
    else:
        obs_out = observ

    all_epi = np.load(fold/(ALL_EPI+".npz"), allow_pickle=True)
    epids = all_epi.files
    indc = [int(n.split("_")[1]) for n in epids]
    r = list(zip(indc, epids))
    r.sort()
    epid_stacked = np.stack([all_epi[name] for i, name in r])

    return params, contacts, obs_out, epid_stacked

def load_instance(folder_path):
    """
    Load only the binary formatted files from folder "folder_path"
    """
    fold = Path(folder_path)
    if not fold.exists():
        raise ValueError("Folder doesn't exists")

    with open(fold / PARAMS_FNAME) as f:
        params = json.load(f)

    contacts = pd.read_csv(fold/(CONTACTS_FNAME))
    
    name_epi = EPI_NAME+".gz"
    epidemy_name = fold/name_epi
    epi = np.loadtxt(epidemy_name, dtype=np.int, delimiter="," )
    
    obs_list = []
    count_num_obs = len([1 for filename in os.listdir(fold) if filename.startswith("observ")])
    
    for i_obs in range(count_num_obs):
        name_file = f"observ{i_obs}.gz"
        obs_list.append(pd.read_csv(fold/name_file))
    return params, contacts, epi, obs_list


def save_instance(base_path, name_instance, pars, contacts_df, full_epidemy, obs_df_list):
    '''
    - contatcs DataFrame
    - full_epidemy: numpy array
    '''
    
    folder = Path(base_path) / name_instance
    if not folder.exists():
        folder.mkdir(parents=True)
    
    num_nodes = pars["n"]
    
    epi = full_epidemy
    name_epi = EPI_NAME+".gz"
    epidemy_name = folder/name_epi
    title_epi = " ,".join(["{}".format(i) for i in range(num_nodes)])
    np.savetxt(epidemy_name, epi, "%d", delimiter=",", header=title_epi)

    save_json(pars, folder/PARAMS_FNAME)
    
    contacts_df.to_csv(folder/(CONTACTS_FNAME), 
                       compression="gzip",
                      index=False)
    for i, o in enumerate(obs_df_list):
        obs_name = OBS_NAME + f"{i}.gz"
        o.to_csv(folder/obs_name,
                          compression="gzip",
                          index=False)
    
    print("contacts saved")
    

    
def save_data_exported(base_path, name_instance, pars, contacts,
                       full_epidemies, obs_all_json=None, obs_all_df=None,              
                       num_inst=None,
                       name_state_obs="st", name_t_obs="t", name_node_obs="i"):
    """
    Export inference problem instance, complete with observations and epidemies

    the data is saved in the folder "base_path/name_instance", so watch out to avoid 
    overwriting previously saved data!

    num_inst is the number of instances present in the data that will be saved

    the name_* parameters are used when the observations are converted from a dataframe 
    into a dictionary, they indicate the name of the columns to use for the conversion 
    (see convert_obs_to_df)

    """
    print("starting...")
    if obs_all_json is None and obs_all_df is None:
        raise ValueError("Give the observations in JSON or DataFrame format")
    if obs_all_df is None:
        obs_all_df = [convert_obs_to_df(o) for o in obs_all_json]
    elif obs_all_json is None:
        obs_all_json = [convert_obs_to_json(
            df, name_state_obs, name_t_obs, name_node_obs) for df in obs_all_df]

    if num_inst is None:
        num_inst = len(obs_all_json)

    num_nodes = pars["n"]

    folder = Path(base_path) / name_instance

    if not folder.exists():
        folder.mkdir(parents=True)

    save_json(pars, folder/PARAMS_FNAME)

    with bz2.open(folder/(CONTACTS_FNAME), "w") as f:
        np.savetxt(f, contacts, delimiter=",")
    if obs_all_json is not None:
        with bz2.open(folder/(ALL_OBS_FILE), "wt") as f:
            json.dump(obs_all_json, f, indent=1)

    title_epi = " ,".join(["{}".format(i) for i in range(num_nodes)])

    for i in range(num_inst):
        epi = full_epidemies[i]

        tf = tarfile.open(folder/"instance_{:03d}.tar.bz2".format(i), "w:bz2")
        epidemy_name = EPI_NAME+"_{:02d}.csv".format(i)
        observ_name = OBS_NAME + "_{:02d}.csv".format(i)

        np.savetxt(epidemy_name, epi, "%d", delimiter=",", header=title_epi)
        tf.add(epidemy_name)

        if obs_all_df is not None:
            observ = obs_all_df[i]
            observ.to_csv(observ_name, index=False)
            tf.add(observ_name)
            tf.close()
            # delete files
            f = Path(observ_name)
            f.unlink()
        else:
            tf.close()

        f = Path(epidemy_name)
        f.unlink()

    d_epid = dict(zip(["epi_{}".format(v)
                       for v in range(num_inst)], full_epidemies))
    np.savez_compressed(folder/"all_epidemies", **d_epid)
    print("Saved on "+folder.as_posix())
