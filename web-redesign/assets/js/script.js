document.addEventListener("DOMContentLoaded", () => {
  const wrapper = document.getElementById("partner-wrapper");

  // Check if wrapper has content before accessing scrollWidth
  if (wrapper.scrollWidth > 0) {
    const content = wrapper.innerHTML;
    wrapper.innerHTML = content.repeat(10);

    const contentWidth = wrapper.scrollWidth; // Access scrollWidth after content is added
    const animationDuration = contentWidth / 100; // Adjust divisor for desired speed

    wrapper.style.setProperty("--animation-duration", `${animationDuration}s`);
    wrapper.style.animation = `scroll var(--animation-duration) linear infinite`;
  } else {
    console.warn("Partner wrapper has no content. Animation not applied.");
  }
});

// theam changer
// Check for saved user preference
const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
  document.body.classList.add(savedTheme);
}

document.getElementById("theme-toggle").addEventListener("click", function () {
  document.body.classList.toggle("dark-theme");
  let theme = "light-theme";

  if (document.body.classList.contains("dark-theme")) {
    theme = "dark-theme";
  }

  // Save the user's preference
  localStorage.setItem("theme", theme);
});
// JavaScript for toggling the sidebar
document
  .getElementById("hamburger-menu")
  .addEventListener("click", function () {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("active");
  });

// JavaScript for closing the sidebar
document.getElementById("close-btn").addEventListener("click", function () {
  var sidebar = document.getElementById("sidebar");
  sidebar.classList.remove("active");
});
//functionality for the FAQ SECTION 
function toggleFAQ(element) {
  const faqItem = element.parentElement;
  const icon = element.querySelector(".faq-icon");

  if (faqItem.classList.contains("active")) {
    faqItem.classList.remove("active");
    icon.textContent = "+";
  } else {
    faqItem.classList.add("active");
    icon.textContent = "_";
  }
}

