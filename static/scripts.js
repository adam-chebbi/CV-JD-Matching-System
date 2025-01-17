// Confirmation prompt for deletion of JDs and CVs
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("button[data-delete]");
    
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const message = button.dataset.delete;
            const confirmDelete = confirm(`Are you sure you want to ${message}?`);
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });
});

// Smooth scrolling to sections
const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
smoothScrollLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
        event.preventDefault();
        const targetId = link.getAttribute("href").substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: "smooth" });
        }
    });
});

// Dynamic filtering of CVs by similarity score
const filterInput = document.getElementById("filter-input");
const cvRows = document.querySelectorAll(".cv-row");

if (filterInput) {
    filterInput.addEventListener("input", () => {
        const minScore = parseFloat(filterInput.value) || 0;
        cvRows.forEach((row) => {
            const score = parseFloat(row.dataset.score);
            if (score >= minScore) {
                row.style.display = ""; // Show the row
            } else {
                row.style.display = "none"; // Hide the row
            }
        });
    });
}

// Responsive navigation toggle
const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("nav-menu");

if (navToggle) {
    navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("open");
    });
}
