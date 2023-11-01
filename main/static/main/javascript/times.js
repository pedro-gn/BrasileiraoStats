const searchInput = document.getElementById("search");
const timesTable = document.getElementById("timesTable");

searchInput.addEventListener("input", function() {
    const searchTerm = searchInput.value.toLowerCase();

    // Percorra as linhas da tabela e oculte aquelas que não correspondem à pesquisa
    const rows = timesTable.getElementsByTagName("tr");
    for (let i = 1; i < rows.length; i++) {
        const rowData = rows[i].getElementsByTagName("td");
        const nomeTime = rowData[0].textContent.toLowerCase();
        if (nomeTime.includes(searchTerm)) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
});