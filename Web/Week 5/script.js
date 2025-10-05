// Functions
function greetUser(name) {
  return `Hello, ${name}! Welcome to JavaScript.`;
}
console.log(greetUser("Alice"));

// Part 2: Control Structures

// 4. If Statement: Check Voting Eligibility
let userAge = parseInt(prompt("Enter your age:"));
if (userAge >= 18) {
  document.body.innerHTML += "<p>You are eligible to vote.</p>";
} else {
  document.body.innerHTML += "<p>You are not eligible to vote yet.</p>";
}

// 5. Loops: Display Numbers 1-10
const numbersList = document.getElementById("numbers");
for (let i = 1; i <= 10; i++) {
  const listItem = document.createElement("li");
  listItem.textContent = i;
  numbersList.appendChild(listItem);
}

// Part 3: DOM Manipulation

// Changing HTML Elements
const title = document.querySelector("h1");
title.textContent = "JavaScript in Action!";

const dynamicDiv = document.getElementById("dynamic-content");
dynamicDiv.innerHTML = "<p>This content was added dynamically using JavaScript.</p>";

// Bonus: Interactive Features
const button = document.getElementById("click-me");
const dateTimeParagraph = document.getElementById("date-time");

button.addEventListener("click", () => {
  document.body.style.backgroundColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  dateTimeParagraph.textContent = `Current Date & Time: ${new Date().toLocaleString()}`;
});
