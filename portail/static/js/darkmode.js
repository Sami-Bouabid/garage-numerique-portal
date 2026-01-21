document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.body.classList.add(`${savedTheme}-mode`);
    updateButtonText(savedTheme);
    updateLogo(savedTheme);

    const toggleBtn = document.getElementById("toggleDarkMode");
    if (!toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
        const isDark = document.body.classList.contains("dark-mode");
        document.body.classList.toggle("dark-mode", !isDark);
        document.body.classList.toggle("light-mode", isDark);

        const newTheme = isDark ? "light" : "dark";
        localStorage.setItem("theme", newTheme);
        updateButtonText(newTheme);
        updateLogo(newTheme);
    });
});

function updateButtonText(theme) {
    const toggleBtn = document.getElementById("toggleDarkMode");
    if (toggleBtn) {
        toggleBtn.textContent = theme === "dark" ? "☀️" : "🌙";
    }
}

function updateLogo(theme) {
    const logo = document.getElementById("logo");
    if (logo) {
        const lightSrc = logo.getAttribute("data-light-src");
        const darkSrc = logo.getAttribute("data-dark-src");
        logo.src = theme === "dark" ? darkSrc : lightSrc;
    }
}
