# Coordinate-based meta analysis algorithms for neuroimaging data.
import os
from pprint import pprint

from nilearn.plotting import plot_stat_map

from nimare.correct import FWECorrector
from nimare.nimads import Studyset
from nimare.utils import get_resource_path
# Kernel density analysis
from nimare.meta.cbma.mkda import MKDADensity
import matplotlib.pyplot as plt



studyset_file = "nidm_pain_studyset.json"
studyset = Studyset(studyset_file, target="mni152_2mm")

print("\nStudyset Information:")
print("-" * 50)
print(f"ID: {studyset.id}")
print(f"Name: {studyset.name}")
print(f"Number of studies: {len(studyset.studies)}")
print(f"Number of annotations: {len(studyset.annotations)}")

'''
def subset_studies(studyset, start=None, stop=None):
    """Create a Studyset limited to a slice of studies."""
    source = studyset.to_dict()
    source["studies"] = source["studies"][start:stop]
    return Studyset(source, target=studyset.space)
    

# Some of the CBMA algorithms compare two collections,
# so we'll split this example Studyset in half.
studyset1 = subset_studies(studyset, None, 10)
studyset2 = subset_studies(studyset, 10, None)
'''
''' cambiar a dataset'''
nimare_dset = studyset.to_dataset()
print("\nLegacy Dataset coordinates preview:")
print("-" * 50)
print(nimare_dset.coordinates.head())

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
