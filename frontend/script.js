const scanBtn = document.getElementById("scanBtn");
const output = document.getElementById("output");

scanBtn.addEventListener("click", async () => {
    output.textContent = "Running scan...";
    try {
        const response = await fetch("http://127.0.0.1:5000/scan");
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 4);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
});
