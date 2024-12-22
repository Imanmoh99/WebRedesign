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

// for work with us
function populateTop() {
  let Outtarget = document.getElementsByClassName("register-top")[0];

  for (let i = 0; i < 5; i++) {
    let target = document.createElement("div");
    target.className = "register-top-card";

    let top_div = document.createElement("div");
    top_div.className = "register-top-div";

    let top_divimg = document.createElement("img");
    top_divimg.src = "assets/img/head.png";
    top_divimg.className = "top-div-img";
    top_div.appendChild(top_divimg);

    let cardType = document.createElement("p");
    cardType.className = "card-type";
    cardType.textContent = "[Course Name]";
    top_div.appendChild(cardType);

    target.appendChild(top_div);

    let middleDiv = document.createElement("div");
    middleDiv.className = "middle-div";
    middleDiv.textContent =
      "In this course, we will teach you the basics of [Course Name]. You will learn [Skill list].";

    target.appendChild(middleDiv);

    let cardBut = document.createElement("button");
    cardBut.className = "hero-button";
    cardBut.textContent = "Register";
    target.appendChild(cardBut);

    Outtarget.appendChild(target);
  }
  let left = document.createElement("img");
  left.src = "assets/img/left.png";

  let right = document.createElement("img");
  right.src = "assets/img/right.png";

  left.className = "left-arrow";
  right.className = "right-arrow";

  Outtarget.appendChild(left);
  Outtarget.appendChild(right);
}

function populateSecondCard(target) {
  let secondTarget = document.getElementsByClassName(`${target}`)[0];

  for (let i = 0; i < 6; i++) {
    secondCard = document.createElement("div");
    secondCard.className = "second-card";

    let secondImg = document.createElement("img");
    secondImg.src = "assets/img/middleimg.png";
    secondImg.className = "second-img";
    secondCard.appendChild(secondImg);

    let secondMiddle = document.createElement("div");
    secondMiddle.className = "second-middle";
    secondMiddle.textContent =
      "“I really enjoyed my stay at Ethioware. I learned a lot of valuable lessons.”";
    secondCard.appendChild(secondMiddle);

    let secondLast = document.createElement("div");
    secondLast.className = "second-last";
    secondLast.textContent = "- John Doe";
    secondCard.appendChild(secondLast);
    secondTarget.appendChild(secondCard);
  }
  let left = document.createElement("img");
  left.src = "assets/img/left.png";

  let right = document.createElement("img");
  right.src = "assets/img/right.png";

  left.className = "left-arrow";
  right.className = "right-arrow";

  secondTarget.appendChild(left);
  secondTarget.appendChild(right);
}

populateTop();
populateSecondCard("work-pandas");
populateSecondCard("work-pandas-two");
populateSecondCard("work-pandas-three");

function populateSecondSecond(target) {
  let Outtarget = document.getElementsByClassName(`${target}`)[0];

  for (let i = 0; i < 6; i++) {
    let target = document.createElement("div");
    target.className = "register-top-card";

    let top_div = document.createElement("div");
    top_div.className = "register-top-div";

    let top_divimg = document.createElement("img");
    top_divimg.src = "assets/img/head.png";
    top_divimg.className = "top-div-img";
    top_div.appendChild(top_divimg);

    let cardType = document.createElement("p");
    cardType.className = "card-type";
    cardType.textContent = "[Department Name]";
    top_div.appendChild(cardType);

    target.appendChild(top_div);

    let middleDiv = document.createElement("div");
    middleDiv.className = "middle-div";
    middleDiv.textContent =
      "In this department, you will work on [Focus Areas] where you can gain practical skills in [Skill lists].";

    target.appendChild(middleDiv);

    let cardBut = document.createElement("button");
    cardBut.className = "hero-button";
    cardBut.textContent = "Register";
    target.appendChild(cardBut);

    Outtarget.appendChild(target);
  }

  let left = document.createElement("img");
  left.src = "assets/img/left.png";

  let right = document.createElement("img");
  right.src = "assets/img/right.png";
  left.className = "left-arrow";
  right.className = "right-arrow";
  Outtarget.appendChild(left);
  Outtarget.appendChild(right);
}

populateSecondSecond("register-second");

function populateHead(target) {
  let taregtNode = document.getElementsByClassName(`${target}`)[0];
  if (taregtNode) console.log("targetNode", target);

  for (let i = 0; i < 7; i++) {
    let headcard = document.createElement("div");
    headcard.className = "head-card";

    let headimg = document.createElement("img");
    headimg.src = "assets/img/head.png";

    headcard.appendChild(headimg);
    taregtNode.appendChild(headcard);
  }

  let left = document.createElement("img");
  left.src = "assets/img/left.png";

  let right = document.createElement("img");
  right.src = "assets/img/right.png";
  left.className = "left-arrow";
  right.className = "right-arrow";

  taregtNode.appendChild(left);
  taregtNode.appendChild(right);
}

populateHead("register-third");
populateHead("register-fourth");
