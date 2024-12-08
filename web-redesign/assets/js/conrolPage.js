const controlPage = (target) => {
  let home = document.getElementById("home-section");
  let about_us = document.getElementById("about-us-section");
  let publication = document.getElementById("publications-section");

  let all = [home, about_us, publication];

  all.forEach((element) => {
    if (element.id == target) {
      element.classList.remove("hidden");
    } else {
      element.classList.add("hidden");
    }
  });
};

let dates = [
  "August 26, 2024",
  "September 15, 2024",
  "November 03, 2024",
  "November 03, 2024",
  "November 03, 2024",
];

let fillBlog = (container, k, type) => {
  for (let i = 0; i < k; i++) {
    let card = document.createElement("div");
    card.className = "swiper-slide card";

    let image = document.createElement("img");
    image.src = "assets/img/card-panda.png";
    card.appendChild(image);

    carddesc = document.createElement("div");
    carddesc.className = "card-desc";

    let title = document.createElement("h2");
    title.textContent = "Title";
    carddesc.appendChild(title);

    content = document.createElement("p");
    content.textContent =
      "lorem ipsum dolor sit amet set max imose asjdnasd ajksdan kajsfd a kajs n aksjd kajsd naskjdan kajsdna ksajd kajssssssss kajsd";
    carddesc.appendChild(content);

    let date = document.createElement("h3");
    date.textContent = dates[i];
    carddesc.appendChild(date);
    card.appendChild(carddesc);

    if (type == 3) {
      let abstract = document.createElement("button");
      abstract.textContent = "+ Abstract";
      card.appendChild(abstract);
    }

    container.appendChild(card);
  }
};

let container = document.getElementById("first-cards");
fillBlog(container, 5, 1);

let secondContainer = document.getElementById("second-cards");
fillBlog(secondContainer, 3, 2);

let thirdContainer = document.getElementById("third-cards");
fillBlog(thirdContainer, 5, 3);

inilializeSwiper();
