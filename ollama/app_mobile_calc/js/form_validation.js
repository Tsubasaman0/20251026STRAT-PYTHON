const form = document.querySelector("form");

form.addEventListener("submit", (e) =>{
    const dataGb = Number(form.data_gb.value);
    if (dataGb > 30) {
        e.preventDefault();
        alert("30GB以上超える場合はこの料金診断は扱っておりません");
    }
});