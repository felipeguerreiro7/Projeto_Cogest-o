document.getElementById("analise-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
        investimento_inicial: document.getElementById("investimento_inicial").value,
        receita_anual: document.getElementById("receita_anual").value,
        custo_anual: document.getElementById("custo_anual").value,
        taxa_crescimento: document.getElementById("taxa_crescimento").value / 100,
        taxa_desconto: document.getElementById("taxa_desconto").value / 100,
        anos: document.getElementById("anos").value,
    };

    fetch("/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((result) => {
            const resultadosDiv = document.getElementById("resultados");
            resultadosDiv.innerHTML = `
                <h3>Resultados:</h3>
                <p>VPL: R$ ${result.vpl.toFixed(2)}</p>
                <p>TIR: ${(result.tir * 100).toFixed(2)}%</p>
                <p>Payback: ${result.payback ? result.payback.toFixed(2) + " anos" : "Não atingido"}</p>
                <p>Ponto de Equilíbrio: R$ ${result.breakeven.toFixed(2)}</p>
                <p>Valuation: R$ ${result.valuation.toFixed(2)}</p>
            `;
        })
        .catch((error) => console.error("Erro:", error));
});
