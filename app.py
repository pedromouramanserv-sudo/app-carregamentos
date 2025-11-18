# Vamos importar nossas bibliotecas
from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Caminho do arquivo excel

FILE_PATH = "carregamentos.xlsx"

# Se não existir, cria o arquivo com colunas
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=[
                      "ID", "Placa", "Deposito", "Tipo", "Doca", "Inicio", "Fim", "Status"
                      ])
    df.to_excel(FILE_PATH, index=False)

def ler_dados():
    return pd.read_excel(FILE_PATH)

def salvar_dados(df):
    df.to_excel(FILE_PATH, index=False)

@app.route("/")
def home():
    df = ler_dados()
    abertos = df[df["Status"] == "Aberto"].to_dict(orient="records")
    return render_template("home.html", carregamentos=abertos)
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        df = ler_dados()
        novo_id = len(df) + 1
        placa = request.form["placa"]
        deposito = request.form["deposito"]
        tipo = request.form["tipo"]
        doca = request.form["doca"]
        inicio = datetime.now().strftime("%d/%m/%Y %H:%M")
        df.loc[len(df)] = [novo_id, placa, deposito, tipo, doca, inicio, "", "Aberto"]
        salvar_dados(df)
        return redirect("/")
    return render_template("novo.html")

@app.route("/finalizar/<int:id>", methods=["GET", "POST"])
def finalizar(id):
    df = ler_dados()
    if request.method == "POST":
        fim = datetime.now().strftime("%d/%m/%Y %H:%M")
        df.loc[df["ID"] == id, "Fim"] = fim
        df.loc[df["ID"] == id, "Status"] = "Finalizado"
        salvar_dados(df)
        return redirect("/")
    carregamento = df[df["ID"] == id].to_dict(orient="records")[0]
    return render_template("finalizar.html", carregamento=carregamento)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    