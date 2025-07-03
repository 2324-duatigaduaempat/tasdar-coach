document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const input = document.querySelector("input");
    const output = document.getElementById("output");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = input.value;
        if (!message) return;

        output.innerHTML += `<div><b>🧑:</b> ${message}</div>`;

        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });
            const data = await res.json();
            if (data.reply) {
                output.innerHTML += `<div><b>🤖:</b> ${data.reply}</div>`;
            } else {
                output.innerHTML += `<div style="color:red;">❌ Ralat: ${data.error || 'Tiada jawapan.'}</div>`;
            }
        } catch (err) {
            output.innerHTML += `<div style="color:red;">❌ Sambungan gagal: ${err.message}</div>`;
        }

        input.value = "";
    });
});
