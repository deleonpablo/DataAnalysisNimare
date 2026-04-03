# Familiarizandonos con Nimare especificamente en StudySets. 

# Importamos las librerias necesarias
from pprint import pprint 
from requests import request

from nimare.meta.cbma.ale import ALE
from nimare.nimads import Studyset

def download_file(url):
    response = request("GET", url)
    return response.json()

nimads_studyset = download_file("https://neurostore.org/api/studysets/Cv2LLUqG76W9?nested=true")
nimads_annotation = download_file("https://neurostore.org/api/annotations/76PyNqoTNEsE")

studyset = Studyset(nimads_studyset, annotations=nimads_annotation)


print("\nStudyset Information:")
print("chismoseando estudios")
print("-" * 50)
print(studyset.to_nimads("nidm_pain_studyset.json"))

# Primero aqui es como poder chismosear en analisis que tengan ciertos tipos de cordenadas en cierto rango del material de estudio 
'''
example_coord = [-42, -58, -15]  # MNI coordinates
print("\nCoordinate Search Results:")
print("-" * 50)
print(f"Searching near coordinate: {example_coord}")

# Find analyses with coordinates within 10mm
nearby_analyses = studyset.get_analyses_by_coordinates(example_coord, r=10)
print(f"\nFound {len(nearby_analyses)} analyses within 10mm")

closest_analyses = studyset.get_analyses_by_coordinates(example_coord, n=5)
print(f"\nClosest 5 analyses: {closest_analyses}")
'''

# Segundo ------- aqui se hacen queries {me va a servir para cuando este separando la info de funcional vs estrucutral y depresion vs bipolaridad}
'''
# Get all analyses that have a specific metadata field
metadata_results = studyset.get_analyses_by_metadata("contrast_type")
print("\nAnalyses with contrast_type metadata:")
print("-" * 50)
pprint(metadata_results)

# -------------- Cambiar de study set a dataset por conveniencia. ------------------------------------------------------------------------------------------
nimare_dset = studyset.to_dataset()
print("\nLegacy Dataset coordinates preview:")
print("-" * 50)
print(nimare_dset.coordinates.head())

# Tercero - aqui uso 
results = ALE(null_method="approximate").fit(nimare_dset)
print("\nMeta-analysis output maps:")
print("-" * 50)
print(sorted(results.maps))
'''
'''
print(f"ID: {studyset.id}")
print(f"Name: {studyset.name}")
print(f"Number of studies: {len(studyset.studies)}")
print(f"Number of annotations: {len(studyset.annotations)}")
'''


'''first_study = studyset.studies[0]
print("\nFirst Study Details:")
print("\n", "-" * 50)
print("chismoseando", first_study)
print("-" * 50)

print(f"Study ID: {first_study.id}")
print(f"Title: {first_study.name}")
print(f"Authors: {first_study.authors}")
print(f"Publication: {first_study.publication}")
print(f"Number of analyses: {len(first_study.analyses)}")
'''

    