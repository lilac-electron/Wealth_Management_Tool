"use strict";

const form1 = document.getElementById("form1");
const form2 = document.getElementById("form2");
const form3 = document.getElementById("form3");
const progressEl = document.getElementById("progress");
const circles = document.querySelectorAll(".circle");
let currectActive = 1;
//============== Next Form===============
function nextOne() {
  form1.style.left = "-450px";
  form2.style.left = "25px";
  //next slide
  increamentNumber();
  // update progress bar
  update();
}
//=============== Back One==================
function backOne() {
  form1.style.left = "25px";
  form2.style.left = "450px";
  // back slide
  decreametNumber();
  // update progress bar
  update();
}
//============ Second Form=============
function nextTwo() {
  form2.style.left = "-450px";
  form3.style.left = "25px";
  //next slide
  increamentNumber();
  // update progress bar
  update();
}
//=============== Back One==================
function backTwo() {
  form2.style.left = "25px";
  form3.style.left = "450px";
  // back slide
  decreametNumber();
  // update progress bar
  update();
}
//============= Progress update====================
function update() {
  circles.forEach((circle, indx) => {
    if (indx < currectActive) {
      circle.classList.add("active");
    } else {
      circle.classList.remove("active");
    }
    // get all of active classes
    const actives = document.querySelectorAll(".active");
    progressEl.style.width =
      ((actives.length - 1) / (circles.length - 1)) * 100 + "%";
  });
}
//================== Increament Number===============
function increamentNumber() {
  // next progress number
  currectActive++;
  if (currectActive > circles.length) {
    currectActive = circles.length;
  }
}
//================ Decreament Number=================
function decreametNumber() {
  currectActive--;
  if (currectActive < 1) {
    currectActive = 1;
  }
}
//================= btn Events===================
const btnsEvents = () => {
  const next1 = document.getElementById("next1");
  const next2 = document.getElementById("next2");
  const back1 = document.getElementById("back1");
  const back2 = document.getElementById("back2");
  //next1
  next1.addEventListener("click", nextOne);
  // back1
  back1.addEventListener("click", backOne);
  //next 2
  next2.addEventListener("click", nextTwo);
  // back 2
  back2.addEventListener("click", backTwo);
};
document.addEventListener("DOMContentLoaded", btnsEvents);