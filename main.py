from fastapi import FastAPI
from pydantic import BaseModel
import argostranslate.package
import argostranslate.translate
import os

# Inicializa app
app = FastAPI()

# Instala modelo se não existir
def instalar_modelo_padrao():
    pt_en_url = "https://www.argosopentech.com/argospm/index/pt_en.argosmodel"
    output_file = "pt_en.argosmodel"
    if not os.path.exists(output_file):
        os.system(f"wget {pt_en_url}")
        argostranslate.package.install_from_path(output_file)

instalar_modelo_padrao()

class TraducaoRequest(BaseModel):
    text: str

@app.post("/traduzir")
def traduzir(data: TraducaoRequest):
    try:
        traduzir = argostranslate.translate.translate
        resultado = traduzir(data.text, from_code="pt", to_code="en")
        return {"status": "ok", "original": data.text, "traduzido": resultado}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
