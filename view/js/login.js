const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginMessage.textContent = "";

  try {
    const user = await api.login(loginForm.username.value, loginForm.password.value);
    saveLoggedUser(user);
    window.location.href = "profile.html";
  } catch (error) {
    loginMessage.textContent = error.message;
  }
});
