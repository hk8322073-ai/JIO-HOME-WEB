const root = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
  root.classList.toggle("dark", savedTheme === "dark");
} else {
  // Use system preference
  root.classList.toggle(
    "dark",
    window.matchMedia("(prefers-color-scheme: dark)").matches,
  );
}

// Toggle theme
window.toggleTheme = function () {
  root.classList.toggle("dark");

  localStorage.setItem(
    "theme",
    root.classList.contains("dark") ? "dark" : "light",
  );
};
