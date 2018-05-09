import numpy as np
import matplotlib.pyplot as plt

from tectosaur.mesh.mesh_gen import make_rect

import tde.fullspace

def gaussian(a, b, c, x):
    # return np.ones_like(x)
    return a * np.exp(-((x - b) ** 2) / (2 * c ** 2))

n = 20
gauss_params = (1.0, 0.0, 0.3)
sm = 1.0
nu = 0.25

m = make_rect(
    n, n,
    [[-1, 0, 1], [-1, 0, -1], [1, 0, -1], [1, 0, 1]]
)

n_tris = m[1].shape[0]
tri_pts = m[0][m[1]]
tri_centers = np.mean(tri_pts, axis = 1)

plt.triplot(m[0][:,0], m[0][:,2], m[1])
plt.plot(tri_centers[:, 0], tri_centers[:, 2], '*')
plt.show()

dist = np.linalg.norm(tri_centers, axis = 1)
strike_slip = gaussian(*gauss_params, dist)
slip = np.zeros((strike_slip.shape[0], 3))
slip[:,0] = strike_slip

def plot(m, field, name):
    plt.title(name)
    plt.tripcolor(m[0][:,0], m[0][:,2], m[1], field)
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('z')
    plt.show()


# plt.tricontourf(
#     m[0][:,0], m[0][:,2], m[1],
#     gaussian(*gauss_params, np.linalg.norm(m[0], axis = 1))
# )
# plt.triplot(m[0][:,0], m[0][:,2], m[1])
# plt.colorbar()
# plt.show()

# tiled_tris = np.tile(tri_pts[np.newaxis, :, :, :], (n_tris, 1, 1, 1)).reshape((-1,3,3))
# tiled_slip = np.tile(slip[np.newaxis, :, :], (n_tris, 1, 1)).reshape((-1,3))
# tiled_centers = np.tile(tri_centers[:, np.newaxis, :], (1, n_tris, 1)).reshape((-1,3))
# strain = tde.fullspace.clu_strain(tiled_centers, tiled_tris, tiled_slip, nu)
# stress = tde.fullspace.strain_to_stress(strain, sm, nu)
# strain = strain.reshape((n_tris, n_tris, 6))
# stress = stress.reshape((n_tris, n_tris, 6))
# stress_at_centers = np.sum(stress, axis = 1)

strain = np.empty((n_tris, 6))
for i in range(n_tris):
    obs_pts = np.tile(tri_centers[i,np.newaxis,:], (n_tris, 1))
    strain[i, :] = np.sum(
        tde.fullspace.clu_strain(obs_pts, tri_pts, slip, nu),
        axis = 0
    )
stress = tde.fullspace.strain_to_stress(strain, sm, nu)

plot(m, stress[:,3], 'sxy')
plot(m, stress[:,5], 'syz')
