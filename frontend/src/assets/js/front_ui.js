(() => {
  //S: scroll-top
  const scrollTop = document.querySelector(".scrolltop");
  scrollTop.addEventListener("click", () => {
    window.scroll({
      behavior: "smooth",
      left: 0,
      top: 0,
    });
  });

  //S:공통 form 검증 함수
  const empty__inputs = (inputs) =>
    inputs.map((item, idx) => {
      item.value.length === 0
        ? item.parentNode.classList.add("empty-input")
        : item.parentNode.classList.remove("empty-input");
    });

  //S:로그인 모달
/*   const login = document.querySelector(".js-login");
  const login_background = document.querySelector("#loginModal.modal-bg");
  const modal_closeLogin = document.querySelector("#loginModal .btn-close");
  const login_formcheck = document.querySelector("#loginModal .btn.formcheck"); // 사용시 querySelectorAll 대신 querySelector로 적절하게 변경해서 사용해주세여!

  login.addEventListener("click", () =>
    login_background.classList.toggle("show")
  );

  modal_closeLogin.addEventListener("click", () =>
    login_background.classList.remove("show")
  );

  login_formcheck.addEventListener("click", () => {
    const inputs = Array.from(
      document.querySelectorAll(".modal-login .form  input")
    );
    empty__inputs(inputs);
  });
 */
  //S:회원가입 모달
 /*  const signup = document.querySelector(".js-signup");
  const signup_background = document.querySelector("#signupModal.modal-bg");
  const modal_closeSignup = document.querySelector("#signupModal .btn-close");
  const signup_formcheck = document.querySelector(
    "#signupModal .btn.formcheck"
  );

  signup.addEventListener("click", () =>
    signup_background.classList.toggle("show")
  );

  modal_closeSignup.addEventListener("click", () =>
    signup_background.classList.remove("show")
  );

  signup_formcheck.addEventListener("click", () => {
    const inputs = Array.from(
      document.querySelectorAll(".modal-signup .form  input")
    );
    empty__inputs(inputs);
  }); */
  //E:회원가입 모달
})();
