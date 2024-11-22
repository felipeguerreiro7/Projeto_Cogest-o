from flask import Flask, render_template, request, jsonify
from calculations import ( # type: ignore
    calcular_vpl, 
    calcular_tir, 
    calcular_payback, 
    calcular_ponto_equilibrio, 
    fluxo_caixa_descontado
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.json

    investimento_inicial = float(data["investimento_inicial"])
    receita_anual = float(data["receita_anual"])
    custo_anual = float(data["custo_anual"])
    taxa_crescimento = float(data["taxa_crescimento"])
    taxa_desconto = float(data["taxa_desconto"])
    anos = int(data["anos"])

    fluxo_de_caixa = [receita_anual - custo_anual]
    for _ in range(1, anos):
        fluxo_de_caixa.append(fluxo_de_caixa[-1] * (1 + taxa_crescimento))
    fluxo_de_caixa[0] -= investimento_inicial

    vpl = calcular_vpl(fluxo_de_caixa, taxa_desconto)
    tir = calcular_tir(fluxo_de_caixa)
    payback = calcular_payback(fluxo_de_caixa)
    breakeven = calcular_ponto_equilibrio(investimento_inicial, receita_anual, custo_anual)
    valuation = fluxo_caixa_descontado(fluxo_de_caixa, taxa_desconto)

    resultado = {
        "vpl": vpl,
        "tir": tir,
        "payback": payback,
        "breakeven": breakeven,
        "valuation": valuation,
        "fluxos": fluxo_de_caixa
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
