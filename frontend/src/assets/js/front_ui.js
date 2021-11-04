(() => {
  //S: 모달 밖 클릭 시 모달 닫기
  $(document).on("click", ".modal-bg.show", (e) =>
    e.target.classList.remove("show")
  );

  //S: 공통 form 검증 함수
  const empty__inputs = (inputs) => {
    inputs.map((item, idx) => {
      item.value.length === 0
        ? item.parentNode.classList.add("empty-input")
        : item.parentNode.classList.remove("empty-input");
    });
  };

  //S: scroll-top
  const scrollTop = document.querySelector(".scrolltop");
  scrollTop.addEventListener("click", () => {
    window.scroll({
      behavior: "smooth",
      left: 0,
      top: 0,
    });
  });

  //S:로그인 모달
  const onLoginHandler = () => {
    if (document.querySelector("#loginModal") === null) return;

    const login = document.querySelector(".js-login");
    const login_background = document.querySelector("#loginModal.modal-bg");
    const modal_closeLogin = document.querySelector("#loginModal .btn-close");
    const login_formcheck = document.querySelector(
      "#loginModal .btn.formcheck"
    );
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
  };

  //S:회원가입 모달
  const onSignupHandler = () => {
    if (document.querySelector("#signupModal") === null) return;

    const signup = document.querySelector(".js-signup");
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
    });
  };

  //S:게시물 추가 모달
  const onAddPostHandler = () => {
    if (document.querySelector("#addPost") === null) return;

    const addPost = document.querySelector(".js-addPost");
    const addPost_background = document.querySelector("#addPost.modal-bg");
    const modal_closeAddPost = document.querySelector("#addPost .btn-close");
    const AddPost_formcheck = document.querySelector("#addPost .btn.formcheck");

    addPost.addEventListener("click", () => {
      addPost_background.classList.toggle("show");
    });

    modal_closeAddPost.addEventListener("click", () => {
      addPost_background.classList.remove("show");
    });
  };

  onAddPostHandler();
  onLoginHandler();
  onSignupHandler();
})();
