import numpy as np
import sys

check_fn_I = lambda s: s==1
check_fn_IR = lambda s: s!=0
ranker_I = lambda x : x[1]
ranker_IR = lambda x : x[1]+x[2]

def events_list(t, observations, true_conf, check_fn = check_fn_I):
    '''
    Compute the list of node at time t not observed check positive
    
    - t: time of events.
    - observations: list of observations used in the inference.
    - true_conf: true configuration of the nodes at all times.
    - check_fn: [optional, default = check->I] function to check the correct node    
    '''
    N = len(true_conf[t])
    exclude = [False]*N
    for (i,s,t1) in observations:
        if t1 <= t and s!=-1 and check_fn(s):
            exclude[i] = True
    events = [(i,t,check_fn(true_conf[t][i])) for i in range(len(true_conf[t])) if exclude[i] == False]
    return events

def marginals_on_events(f, events):
    '''
    returns the marginals of nodes at fixed time 
    as listed in events
    
    - f: sib.f class function
    - events: list of events [[i, t_i, state_i], [j, t_j, state_j] ...]
    
    return: dict - probability to be {i : [prob_S, prob_I, prob_R]
    '''
    nodes = f.nodes
    M = {}
    for (i,t,state) in events:
        n = nodes[f.get_index(i)]
        ttrue = list(n.times).index(t)-1
        M[i] = n.marginal_t(ttrue)
    
    return M

def marginals_at_time(f, t):
    '''
    returns the marginals of nodes at fixed time 
    
    - f: sib.f class function
    - t: time
    
    return: dict - probability to be {i : [prob_S, prob_I, prob_R]
    '''
    M = {}
    for i in range(len(f.nodes)):
        n = f.nodes[f.get_index(i)]
        ttrue = list(n.times).index(t)-1
        M[i] = n.marginal_t(ttrue)
        #sib.marginal

    return M
    
def compute_roc(sortl):
    x = [0]
    y = [0]
    a = 0
    for (r,state) in sortl:
        if state:
            y.append(y[-1]+1)
            x.append(x[-1])
        else:
            a += y[-1]
            x.append(x[-1]+1)
            y.append(y[-1])
    a/=(y[-1]*x[-1])
    x = np.array(x)
    y = np.array(y)
    return x, y, a

#def order_checker(f, events, ranker = ranker_I):

def roc_curve(marginals, events, ranker = ranker_I):
    '''
    Generate the arrays for ROC curve
    
    - marginals: (dict) at time t
    - events: list of (i, t, state)
    - ranker: (optional = ranker_I) function to select the value to rank the node from marginals
    
    '''
    l = []
    for (i,t,state) in events:
        r = ranker(marginals[i])
        l.append([r,state])
    sortl = sorted(l, key=lambda kv: kv[0], reverse=True)
    x, y, a = compute_roc(sortl)
    return x,y,a,sortl

def roc(f, events, ranker = ranker_I):
    m_t = marginals_on_events(f, events)
    return roc_curve(m_t, events, ranker)

def roc_I(t, observations, true_conf, f):
    eventsI = events_list(
        t, 
        observations,
        true_conf,
        check_fn = check_fn_I)
    return roc(f, eventsI, ranker_I)
    
def roc_IR(t, observations, true_conf, f):
    eventsIR = events_list(
        t, 
        observations,
        true_conf,
        check_fn = check_fn_IR)
    return roc(f, eventsIR, ranker_IR)
