(() => {
  const clear__inputs = (inputs) => {
    if(!inputs.length) return;
    inputs.map((item, idx) => {
      item.value = ''
    });
  }
  //S: 모달 밖 클릭 시 모달 닫기
  $(document).on("click", ".modal-bg.show", (e) => {
    e.target.classList.remove("show");
  });

  //S: 모달 푸터 취소 박스 클릭 시 모달 닫기
  $(document).on("click", ".js-close", (e) => {
    e.target.closest(".modal-bg").classList.remove("show");
    const target = $(e.target).parent().siblings().closest('.modal-body');
    const inputs = Array.from(target.find('input'))
    const texts = Array.from(target.find('textarea'))
    clear__inputs(inputs)
    clear__inputs(texts)
    if($('.file-badge')) $('.file-badge').remove();
  });

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

    modal_closeLogin.addEventListener("click", () => {
      login_background.classList.remove("show");
      const inputs = Array.from(
        document.querySelectorAll(".modal-login .form  input")
        );
        clear__inputs(inputs);
      }
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

    modal_closeSignup.addEventListener("click", () => {
      signup_background.classList.remove("show");
      const inputs = Array.from(
        document.querySelectorAll(".modal-signup .form  input")
      );
      clear__inputs(inputs);
    });

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
    const inputs = document.querySelector(
      '.modal-addpost .form  input[type="file"]'
    );

    addPost.addEventListener("click", () => {
      addPost_background.classList.toggle("show");
    });

    modal_closeAddPost.addEventListener("click", () => {
      addPost_background.classList.remove("show");
      const inputs = Array.from($(".modal-addpost").find('input'));
      const options = document.querySelector(".modal-addpost select")
      const texts = document.querySelector(".modal-addpost textarea")
      texts.value = ''
      $('.file-badge').remove();
      clear__inputs(inputs);
    });

    AddPost_formcheck.addEventListener("click", () => {
      const inputs = Array.from(
        document.querySelectorAll(".modal-addpost input")
      );
      empty__inputs(inputs);
    });

    //첨부파일 뱃지 추가
    inputs.addEventListener("change", () => {
      const file = inputs.value.split("\\"); //경로
      if (!file[0].length) return;
      $(".file-badge").length > 0 && $(".file-badge").remove(); // 사진 첨부되었는데 또 했을 경우 새로 추가한 사진만 남기기

      const fileBadge_element =
        '<span class="file-badge ellipse"><a href="#">' +
        file[file.length - 1] +
        "</a></span >";
      $(".js-form-file").append(fileBadge_element);
      $(".empty-input").removeClass("empty-input");
      //formData에 저장된 이미지 경로는 백엔드에서만 확인 가능
      const formData = new FormData();
      formData.set("file_", file);
    });

    //첨부 파일 삭제
    $(document).on("click", ".file-badge", function(e) {
      e.target.classList.contains("file-badge") === true
        ? e.target.remove()
        : e.target.closest(".file-badge").remove();
    });
  };

  //S:게시물 보기 모달
  const onPostDetailHandler = () => {
    if (document.querySelector("#postDetail") === null) return;

    const detailPost = document.querySelector(".js-postDetail");
    const detailPost_background = document.querySelector(
      "#postDetail.modal-bg"
    );
    const modal_closeAddPost = document.querySelector("#postDetail .btn-close");
    const detailPost_formcheck = document.querySelector(
      "#postDetail .btn.formcheck"
    );

    detailPost.addEventListener("click", () => {
      detailPost_background.classList.toggle("show");
    });

    modal_closeAddPost.addEventListener("click", () => {
      detailPost_background.classList.remove("show");
    });
  };

  onPostDetailHandler();
  onAddPostHandler();
  onLoginHandler();
  onSignupHandler();
})();
