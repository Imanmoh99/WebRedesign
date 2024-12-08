import Swiper, { Navigation } from "swiper";
import "swiper/css";
import "swiper/css/navigation";

export const inilializeSwiper = () => {
  const blogSwiper = new Swiper(".publications-cards", {
    modules: [Navigation],
    navigation: {
      nextEl: ".blog-right-arrow",
      prevEl: ".blog-left-arrow",
    },
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
  });
  const interviewSwiper = new Swiper(".interview-cards", {
    modules: [Navigation],
    navigation: {
      nextEl: ".right-arrow",
      prevEl: ".left-arrow",
    },
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
  });
  const academicSwiper = new Swiper(".academic-cards", {
    modules: [Navigation],
    navigation: {
      nextEl: ".right-arrow",
      prevEl: ".left-arrow",
    },
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
  });

  blogSwiper.update();
  academicSwiper.update();
  interviewSwiper.update();
};
