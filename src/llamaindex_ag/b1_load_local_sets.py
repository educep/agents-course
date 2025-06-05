# Standard imports
from pathlib import Path

# Third party imports
from datasets import load_dataset
from huggingface_hub import login

# Internal imports
from config.settings import settings

# necesitamos el token de huggingface HF_TOKEN en el .envpara poder descargar los modelos
login(token=settings.hf_token)

this_path = Path(settings.project_path / "src" / "llamaindex_ag" / "data")
this_path.mkdir(parents=True, exist_ok=True)


def load_local_sets() -> None:
    # Cargamos el dataset y lo almacenamos como archivos en el directorio data
    dataset = load_dataset(path="dvilasuero/finepersonas-v0.1-tiny", split="train")

    for i, persona in enumerate(dataset):
        with open(this_path / f"persona_{i}.txt", "w", encoding="utf-8") as f:
            f.write(persona["persona"])

    return
