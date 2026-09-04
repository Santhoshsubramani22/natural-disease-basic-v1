document.addEventListener("DOMContentLoaded", () => {
    // Inject navigation dynamically across subpages
    const navPlaceholder = document.getElementById("nav-placeholder");
    if (navPlaceholder) {
        navPlaceholder.innerHTML = `
        <nav class="navbar">
            <div class="logo"><a href="/" style="color:#4dabf7;text-decoration:none;"><i class="fa-solid fa-shield-halved"></i> DisasterAI</a></div>
            <div class="nav-links">
                <a href="/"><i class="fa-solid fa-house"></i> Home</a>
                <a href="/dashboard"><i class="fa-solid fa-chart-line"></i> Dashboard</a>
                <a href="/prediction"><i class="fa-solid fa-bolt"></i> Predict Risk</a>
                <a href="/map"><i class="fa-solid fa-map-location-dot"></i> Risk Map</a>
                <a href="/analytics"><i class="fa-solid fa-chart-pie"></i> Analytics</a>
                <a href="/models"><i class="fa-solid fa-microchip"></i> Models</a>
                <a href="/alerts"><i class="fa-solid fa-bell"></i> Alerts</a>
                <a href="/history"><i class="fa-solid fa-clock-rotate-left"></i> History</a>
            </div>
            <div class="lang-selector">
                <select id="languageSelect" onchange="changeLanguage(this.value)">
                    <option value="en">English</option>
                    <option value="ta">தமிழ்</option>
                    <option value="hi">हिन्दी</option>
                    <option value="te">తెలుగు</option>
                    <option value="ml">മലയാളം</option>
                    <option value="kn">ಕನ್ನಡ</option>
                    <option value="bn">বাংলা</option>
                </select>
            </div>
        </nav>`;
    }

    // Set saved language preference
    const savedLang = localStorage.getItem("selected_lang") || "en";
    const langSelect = document.getElementById("languageSelect");
    if (langSelect) langSelect.value = savedLang;
});

function changeLanguage(lang) {
    localStorage.setItem("selected_lang", lang);
    fetch(`/api/translations/${lang}`)
        .then(res => res.json())
        .then(data => {
            document.querySelectorAll("[data-i18n]").forEach(el => {
                const key = el.getAttribute("data-i18n");
                if (data[key]) el.innerText = data[key];
            });
        });
}