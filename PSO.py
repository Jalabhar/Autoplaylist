import numpy as np
import benchmarks as bm
# rand_gen = np.random.default_rng()


def build_swarms(lim, n_swarms, n_parts, n_dims, step, starting):
    s, p, d = n_swarms, n_parts, n_dims
    shp = (s, p, d)
    Rng = np.subtract(lim[1], lim[0])
    if starting is None:
        swarms = np.random.uniform(lim[0], lim[1], shp)
    else:
        swarms = np.random.normal(starting, (0.02 * Rng), shp)
        swarms = np.where(lim[1] < swarms, np.random.uniform(
            lim[1] - 0.1 * Rng, lim[1]), swarms)
        swarms = np.where(lim[0] > swarms, np.random.uniform(
            lim[0], lim[0] + 0.1 * Rng), swarms)
    if step is not None:
        swarms = snap_to_grid(swarms, step)
    return swarms


def get_values(func, Swarm, *args):
    shp = Swarm.shape
    Swarm.shape = (shp[0] * shp[1], shp[2])
    vals = np.apply_along_axis(func, 1, Swarm, *args)
    Swarm.shape = shp
    vals.shape = (shp[0], shp[1], 1)
    return vals


def create_uniques(arr):
    # Get unique ones and the respective counts
    unq, c = np.unique(arr, return_counts=1)

    # Get mask of matches from the arr against the ones that have
    # respective counts > 1, i.e. the ones with duplicates
    m = np.isin(arr, unq[c > 1])

    # Get the ones that are absent in original array and shuffle it
    newvals = np.setdiff1d(np.arange(len(arr)), arr[~m])
    np.random.shuffle(newvals)

    # Assign the shuffled values into the duplicate places to get final o/p
    arr[m] = newvals
    return arr


def mtx_dif(Swarm, mtx):
    a = np.equal(Swarm, mtx).astype(int)
    b = np.not_equal(Swarm, mtx).astype(int)
    return (a * np.subtract(Swarm, mtx)
            + b * (Swarm))
    # + 0.01 *  np.random.uniform(np.min(Swarm), np.max(Swarm), Swarm.shape)


def history(cur_pos, cur_vals, hist_pos, hist_vals):

    K = np.less_equal(hist_vals, cur_vals)
    Keep = K.astype(int)
    C = np.greater(hist_vals, cur_vals)
    Change = C.astype(int)
    hist_vals = np.add(np.multiply(Keep, hist_vals),
                       np.multiply(Change, cur_vals))
    hist_pos = np.add(np.multiply(Keep, hist_pos),
                      np.multiply(Change, cur_pos))
    return hist_pos, hist_vals


def snap_to_grid(X, step):
    G = np.multiply(np.around(np.divide(X, step)), step)
    G[np.isnan(G)] = X[np.isnan(G)]
    return G


def set_position(i, progress, velocity, glob_best, B, S_D, L_D, G_D, S, lim, step, permut):
    W = .4 + progress
    r = 2. * np.random.uniform(0, 1, 3)
    t = np.random.uniform(-np.pi, np.pi, 3)
    h = np.random.uniform()
    Sp = S.shape
    if h < .5:
        C1 = np.sin(r[0] * t[0])
        C2 = np.sin(r[1] * t[1])
        C3 = np.sin(r[2] * t[2])
    if h > .5:
        C1 = np.cos(r[0] * t[0])
        C2 = np.cos(r[1] * t[1])
        C3 = np.cos(r[2] * t[2])
    Rng = np.subtract(lim[1], lim[0])
    slf_acc = np.multiply(C1, S_D)
    loc_acc = np.multiply(C2, L_D)
    shp = loc_acc.shape
    loc_acc.shape = (shp[0], 1, shp[1])
    glob_acc = np.multiply(C3, G_D)
    if loc_acc.any() != 0:
        glob_acc *= 0.1
    inertia = np.multiply(W, velocity)
    velocity = np.add(inertia, slf_acc)
    velocity = np.add(velocity, loc_acc)
    velocity = np.add(velocity, glob_acc)
    S = np.add(S, velocity)
    S = np.where(lim[1] < S, lim[1], S)
    S = np.where(lim[0] > S, lim[0], S)
    if step is not None:
        S = snap_to_grid(S, step)
    if permut:
        try:
            S = np.apply_along_axis(create_uniques, -1, S)
        except:
            pass
    return S


def run(f, n, lim, s, p, *args, passo=None, permut=False, starting=None):
    if passo is None:
        passo = np.zeros(len(lim[0]))
    Rng = np.subtract(lim[1], lim[0])
    n_swarms = s
    n_parts = p
    n_dims = len(lim[0])
    S = build_swarms(lim, n_swarms, n_parts, n_dims, passo, starting)
    slf_best = np.full((n_swarms, n_parts, 1), (10**9))
    slf_hist = np.full((n_swarms, n_parts, n_dims), 0.0)
    loc_best = np.full((n_swarms, 1), (10**9))
    loc_hist = np.full((n_swarms, n_dims), 0.0)
    if starting is None:
        glob_best = np.full((1), (10**9))
        glob_hist = np.full((n_dims), 0.0)
    else:
        glob_best = f(starting, *args)
        glob_hist = starting
    velocity = np.zeros((n_swarms, n_parts, n_dims))
    break_counter = 0
    All_pos = np.array([])
    All_vals = np.array([])
    for i in range(n):
        B = glob_best
        progress = 1 - (float(i) / n)
        R = get_values(f, S, *args)
        ind = np.argsort(R, axis=1)
        S = np.take_along_axis(S, ind, axis=1)
        R = np.take_along_axis(R, ind, axis=1)
        All_pos = np.append(All_pos, S)
        All_vals = np.append(All_vals, R)
        a = int(.5 + .2 * n_parts)
        S[:, -a:, :] = np.random.uniform(lim[0],
                                         lim[1], size=(n_swarms, a, len(lim[0])))
        loc_points = S[:, 0, :]
        loc_vals = R[:, 0, :]
        M = np.argmin(loc_vals)
        glob_val = loc_vals[M]
        glob_point = loc_points[M]
        slf_hist, slf_best = history(
            S, R, slf_hist, slf_best)
        loc_hist, loc_best = history(
            loc_points, loc_vals, loc_hist, loc_best)
        glob_hist, glob_best = history(
            glob_point, glob_val, glob_hist, glob_best)
        S_D = mtx_dif(S, slf_hist)
        L_D = mtx_dif(S[:, 0, :], loc_hist)
        G_D = mtx_dif(S, glob_hist)
        S = set_position(i, progress, velocity, glob_best, B, S_D,
                         L_D, G_D, S, lim, passo, permut)
        if glob_best < B:
            break_counter = 0
        else:
            break_counter += 1
        if break_counter > 0.2 * n and i > 0.5 * n:
            break
    return glob_hist, glob_best, All_pos, All_vals
