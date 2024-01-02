#%%
import numpy as np
from scipy.optimize import minimize
from jax import config
config.update("jax_enable_x64", True)
import jax

def parse_input(fname):
    pos_data = []
    v_data = []
    with open(fname) as f:
        for line in f:
            pos, v = line.strip().split('@')
            pos_data.append([int(x) for x in pos.split(',')])
            v_data.append([int(x) for x in v.split(',')])
    return np.array(pos_data), np.array(v_data)

pos, v = parse_input("/home/mscherbela/develop/advent_of_code/2023/24/input.txt")

def loss_func(params):
    p0 = params[:3]
    v0 = params[3:6]
    t = params[6:]
    error = (p0 - pos) + t[:, None] * (v0 - v)
    # error /= 1e9
    return np.sum(error**2)

grad_func = jax.jit(jax.grad(loss_func))
loss_func = jax.jit(loss_func)
hessian_func = jax.jit(jax.hessian(loss_func))
x0 = np.zeros(len(pos) + 6)

# First round: Optimize non-linear function to find approximate solution
result = minimize(loss_func, 
    method="powell",
    jac=grad_func,
    hess=hessian_func,
    x0=x0,
    options=dict(maxiter=500, disp=True))

x = np.round(result.x).astype(int)
p0_guess, v0_guess, t_guess = x[:3], x[3:6], x[6:]

# Second round: Assume v and t are correct to find p0
rough_error = pos - p0_guess + (v - v0_guess) * t_guess[:, None]
print("Initial rough error:", np.sum(np.abs(rough_error)))

mean_error = np.mean(rough_error, axis=0)
p0_guess = p0_guess + mean_error.round().astype(int)
rough_error = pos - p0_guess + (v - v0_guess) * t_guess[:, None]
print("Refined rough error:", np.sum(np.abs(rough_error)))
print("Part 2:", p0_guess.sum())


