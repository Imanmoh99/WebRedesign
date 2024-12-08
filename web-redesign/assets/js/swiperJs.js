// Import Swiper and required modules
import Swiper, { Navigation } from "swiper";
import "swiper/css";
import "swiper/css/navigation";

// Initialize Swiper
const swiper = new Swiper(".swiper", {
  modules: [Navigation], // Include required modules
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  slidesPerView: 3,
  spaceBetween: 20,
});
