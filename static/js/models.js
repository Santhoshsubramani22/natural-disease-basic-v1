let rocChart = null;

function loadModelMetrics() {
    const disaster = document.getElementById("modelDisasterSelect").value;
    fetch("/api/model-metrics")
        .then(res => res.json())
        .then(metrics => {
            const disasterMetrics = metrics[disaster] || {};
            const tbody = document.getElementById("metricsTableBody");
            tbody.innerHTML = "";

            const algos = ["random_forest", "xgboost", "decision_tree", "logistic_regression"];
            const rocDatasets = [];

            algos.forEach((algo, idx) => {
                const m = disasterMetrics[algo] || { accuracy: 0, precision: 0, recall: 0, f1_score: 0, roc_auc: 0 };
                const isPrimary = algo === "random_forest" ? '<span class="badge badge-green">Primary</span>' : 'Comparison';
                
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${algo.replace('_', ' ').toUpperCase()}</strong></td>
                        <td>${m.accuracy}</td>
                        <td>${m.precision}</td>
                        <td>${m.recall}</td>
                        <td>${m.f1_score}</td>
                        <td>${m.roc_auc}</td>
                        <td>${isPrimary}</td>
                    </tr>`;

                if (m.roc_curve) {
                    rocDatasets.push({
                        label: algo,
                        data: m.roc_curve.fpr.map((x, i) => ({ x: x, y: m.roc_curve.tpr[i] })),
                        borderColor: ['#0d6efd', '#198754', '#ffc107', '#dc3545'][idx],
                        showLine: true,
                        fill: false
                    });
                }
            });

            renderRocCurve(rocDatasets);
            renderConfusionMatrix(disasterMetrics["random_forest"]?.confusion_matrix || [[0,0],[0,0]]);
        });
}

function renderRocCurve(datasets) {
    const ctx = document.getElementById("rocCurveChart").getContext("2d");
    if (rocChart) rocChart.destroy();

    rocChart = new Chart(ctx, {
        type: 'scatter',
        data: { datasets: datasets },
        options: {
            scales: {
                x: { title: { display: true, text: 'False Positive Rate' }, min: 0, max: 1 },
                y: { title: { display: true, text: 'True Positive Rate' }, min: 0, max: 1 }
            }
        }
    });
}

function renderConfusionMatrix(cm) {
    const container = document.getElementById("confusionMatrixContainer");
    container.innerHTML = `
        <table class="data-table" style="text-align:center;">
            <tr><th></th><th>Pred NO</th><th>Pred YES</th></tr>
            <tr><th>Actual NO</th><td style="background:#d1e7dd">${cm[0][0]} (TN)</td><td style="background:#f8d7da">${cm[0][1]} (FP)</td></tr>
            <tr><th>Actual YES</th><td style="background:#f8d7da">${cm[1][0]} (FN)</td><td style="background:#d1e7dd">${cm[1][1]} (TP)</td></tr>
        </table>`;
}

document.addEventListener("DOMContentLoaded", loadModelMetrics);