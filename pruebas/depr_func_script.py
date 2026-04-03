# Primero importar todo lo necesario 
# AL ser funcional se tiene que hacer 

import os
from pprint import pprint

from nilearn.plotting import plot_stat_map

from nimare.correct import FWECorrector
from nimare.nimads import Studyset
from nimare.utils import get_resource_path
import matplotlib.pyplot as plt
from nimare.meta.cbma.mkda import MKDADensity

# ALE
from nimare.meta.cbma.ale import ALE


studyset_file = "depresion_funcional_mkDA.json"
studyset = Studyset(studyset_file, target="mni152_2mm")

print("\nStudyset Information:")
print("-" * 50)
print(f"ID: {studyset.id}")
print(f"Name: {studyset.name}")
print(f"Number of studies: {len(studyset.studies)}")
print(f"Number of annotations: {len(studyset.annotations)}")

#cambiar a dataset
nimare_dset = studyset.to_dataset()
print("\nLegacy Dataset coordinates preview:")
print("-" * 50)
print(nimare_dset.coordinates.head())

## Primero es MKDA, multilevel kernel density analysis
meta = MKDADensity()
results = meta.fit(nimare_dset)

corr = FWECorrector(method="montecarlo", n_iters=10, n_cores=1)
cres = corr.transform(results)

plot_stat_map(
    results.get_map("z"),
    cut_coords=[4, 0, -8],
    draw_cross=False,
    cmap="RdBu_r",
    symmetric_cbar=True,
    threshold=0.1,
)
plot_stat_map(
    cres.get_map("z_level-voxel_corr-FWE_method-montecarlo"),
    cut_coords=[0, 0, -8],
    draw_cross=False,
    cmap="RdBu_r",
    symmetric_cbar=True,
    threshold=0.1,
)


print("Description:")
pprint(results.description_)
print("References:")
pprint(results.bibtex_)
plt.show()
