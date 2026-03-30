const algoOptions = document.querySelectorAll('.algo-option');
const badge = document.getElementById('selectedAlgoBadge');
const desc = document.getElementById("algoDescription");
const icon = document.getElementById("algoIcon");
const text = document.getElementById("algoText");

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
    if (!data) return;

    if (text) text.textContent = value;
    if (icon) icon.className = "bi " + data.icon + " me-2";
    if (desc) desc.textContent = data.desc;
    if (badge) {
        badge.classList.remove("algo-bfs", "algo-dfs", "algo-ucs", "algo-astar");
        badge.classList.add(data.class);
        badge.style.transform = "scale(1.08)";
        setTimeout(() => badge.style.transform = "scale(1)", 180);
    }
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

// --- SWAP BUTTON ---
const swapBtn = document.getElementById('swapBtn');
const startSelect = document.getElementById('startSelect');
const goalSelect = document.getElementById('goalSelect');

if (swapBtn && startSelect && goalSelect) {
    swapBtn.addEventListener('click', function() {
        const temp = startSelect.value;
        startSelect.value = goalSelect.value;
        goalSelect.value = temp;
        startSelect.classList.add('swap-highlight');
        goalSelect.classList.add('swap-highlight');
        setTimeout(() => {
            startSelect.classList.remove('swap-highlight');
            goalSelect.classList.remove('swap-highlight');
        }, 300);
    });
}