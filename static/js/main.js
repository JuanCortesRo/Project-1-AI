const algoOptions = document.querySelectorAll('.algo-option');
const badge = document.getElementById('selectedAlgoBadge');
const desc = document.getElementById("algoDescription");
const icon = document.getElementById("algoIcon");
const text = document.getElementById("algoText");

/* 🔥 COLORES IGUALES AL BACKEND */
const algorithmsData = {
    "BFS": {
        desc: "Explora nivel por nivel.",
        icon: "bi-diagram-3",
        class: "algo-bfs"
    },
    "DFS": {
        desc: "Explora en profundidad.",
        icon: "bi-arrow-down-up",
        class: "algo-dfs"
    },
    "UCS": {
        desc: "Minimiza el costo.",
        icon: "bi-currency-dollar",
        class: "algo-ucs"
    },
    "A*": {
        desc: "Optimiza con heurística.",
        icon: "bi-stars",
        class: "algo-astar"
    }
};

function updateUI(value) {
    const data = algorithmsData[value];

    text.textContent = value;
    icon.className = "bi " + data.icon + " me-2";
    desc.textContent = data.desc;

    // quitar clases
    badge.classList.remove("algo-bfs", "algo-dfs", "algo-ucs", "algo-astar");

    // aplicar color
    badge.classList.add(data.class);

    // 🔥 animación pro
    badge.style.transform = "scale(1.08)";
    setTimeout(() => badge.style.transform = "scale(1)", 180);
}

/* inicial */
const selected = document.querySelector('.algo-option:checked');
if (selected) updateUI(selected.value);

/* cambio */
algoOptions.forEach(option => {
    option.addEventListener('change', function() {
        updateUI(this.value);
    });
});