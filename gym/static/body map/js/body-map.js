function getGender() {
    let gender = localStorage.getItem("sex") || "male";
    if (gender !== "male" && gender !== "female") {
      localStorage.setItem("sex", "male");
      gender = "male";
    }
    return gender;
  }
  
  function getAdvanced() {
    return localStorage.getItem("advancedMap") === "true";
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    let urlSegments = window.location.href.split("/");
    let sectionFromUrl = urlSegments[urlSegments.length - 2];
    
    Array.from(document.getElementsByClassName("js-section-button")).forEach((buttonElement) => {
      let buttonText = buttonElement.innerText.trim();
      if (buttonText.toUpperCase().includes(sectionFromUrl.toUpperCase())) {
        localStorage.setItem("section", buttonText.charAt(0) + buttonText.slice(1).toLowerCase());
      }
    });
  
    let defaultSection = localStorage.getItem("section") || "Exercises";
    setDisplayGender(getGender());
    
    $(".js-sex-option").on("click", (e) => {
      e.preventDefault();
      if ("male" === getGender()) {
        setDisplayGender("female");
      } else {
        setDisplayGender("male");
      }
    });
  
    const advancedToggle = $("#advanced-toggle");
    if (getAdvanced()) {
      advancedToggle.prop("checked", true);
    }
    
    advancedToggle.on("change", (e) => {
      e.preventDefault();
      localStorage.setItem("advancedMap", advancedToggle.prop("checked"));
      setDisplayGender(getGender());
    });
  
    $("#body-map").on("click", (e) => {
      const targetId = e.target.parentElement.id;
      const path = buildNavigationPath(targetId, defaultSection);
      if (path) {
        window.location = "/" + path; //+".html";
      }
    });
  
    $(".js-close-modal").on("click", () => {
      _hideModal();
    });
  
    $(`#sexchooser${getGender()}label`).click();
  
    document.onclick = () => {
      s.removeClass("more-menu--open");
      l.removeClass("mobile-menu--open");
    };
  
    let s = $(".js-more-menu");
    let l = $(".js-mobile-menu");
    let n = $(".js-mobile-menu-toggle");
    let d = $(".js-toggle-button-label");
    let i = $(".js-show-more-button");
    let r = $(".js-category-display");
    let c = false;
    
    defaultSection = defaultSection.toLowerCase();
    $(".section-selected").removeClass("section-selected");
    $(`[data-js-section="${defaultSection}"]`).addClass("section-selected");
    
    let menuText = $(".section-selected").first().text();
    d.text(menuText || "Featured");
    
    if ($(".section-selected").hasClass("more-menu-opt")) {
      i.addClass("section-selected");
      r.text(menuText);
    }
  
    n.on("click", (e) => {
      l.toggleClass("mobile-menu--open");
      e.stopPropagation();
    });
  
    $(".js-section-button").on("click", (e) => {
      let buttonElement = $(e.target);
      let currentSection = localStorage.getItem("section");
      let sectionAttribute = buttonElement.data("js-section");
      if (!getAdvanced() || (sectionAttribute !== "exercises" && currentSection !== sectionAttribute)) {
        c = false;
        r.text("More");
        n.addClass("mobile-menu-toggle--section-selected");
        $(".section-selected").removeClass("section-selected");
        localStorage.removeItem("section");
        d.text("Featured");
        if (sectionAttribute === currentSection) {
          c = true;
          i.removeClass("section-selected");
          n.removeClass("mobile-menu-toggle--section-selected");
        } else {
          d.text(buttonElement.text());
          buttonElement.addClass("section-selected");
          defaultSection = sectionAttribute;
          localStorage.setItem("section", sectionAttribute);
        }
      }
    });
  
    $(".js-more-menu-opt").on("click", (e) => {
      if (!c) {
        i.addClass("section-selected");
        r.text($(e.target).text());
      }
    });
  
    i.on("click", (e) => {
      if (getAdvanced()) {
        return false;
      }
      s.toggleClass("more-menu--open");
      e.stopPropagation();
    });
  });
  
  const checkModal = () => {
    const user = JSON.parse(localStorage.getItem("user"));
    const isPremium = user?.profile.premium || user?.profile.premium_cancelled;
    const hasShownModal = localStorage.getItem("ctaModalShown");
    const ctaCoupons = Number(JSON.parse(localStorage.getItem("ctaCoupons")));
    const shouldShowModal = !(isPremium || (hasShownModal && ctaCoupons && ctaCoupons > 0));
    
    localStorage.setItem("ctaCoupons", ctaCoupons ? ctaCoupons - 1 : 9);
    
    if (shouldShowModal) {
      localStorage.setItem("ctaModalShown", true);
      _showModal();
    }
  };
  
  function setDisplayGender(gender) {
    const bodyMap = $("#body-map");
    const maleBodyMaps = $("#male-body-maps");
    const femaleBodyMaps = $("#female-body-maps");
    const regularBody = $(".body-map__body").not(".body-map--advanced");
    const advancedBody = $(".body-map--advanced");
    const toggleMaleIcon = $(".js-toggle-male-icon");
    const toggleFemaleIcon = $(".js-toggle-female-icon");
    const genderToggleText = $(".js-gender-toggle-text");
  
    maleBodyMaps.hide();
    femaleBodyMaps.hide();
    advancedBody.hide();
    regularBody.hide();
    bodyMap.removeClass("invisible");
  
    if (getAdvanced()) {
      advancedBody.show();
      $(".js-featued-button").trigger("click");
      $(".js-nav").addClass("menu-disabled");
      checkModal();
    } else {
      regularBody.show();
      $(".js-nav").removeClass("menu-disabled");
    }
  
    genderToggleText.text(gender);
    localStorage.setItem("sex", gender);
  
    switch (gender) {
      case "female":
        toggleMaleIcon.addClass("tw-hidden");
        toggleFemaleIcon.removeClass("tw-hidden");
        femaleBodyMaps.fadeIn(500);
        break;
      case "male":
        toggleMaleIcon.removeClass("tw-hidden");
        toggleFemaleIcon.addClass("tw-hidden");
        maleBodyMaps.fadeIn(500);
        break;
      default:
        break;
    }
  }
  
  function buildNavigationPath(bodyPart, section) {
    if ([
      "calves","quads","traps","shoulders","biceps","triceps","forearms","lowerback","hamstrings",
      "obliques","chest","abdominals","quads","lats","glutes","traps-middle","upper-abdominals",
      "gastrocnemius","tibialis","soleus","outer-quadricep","rectus-femoris","inner-quadricep",
      "inner-thigh","lower-abdominals","wrist-flexors","wrist-extensors","short-head-bicep",
      "long-head-bicep","mid-lower-pectoralis","upper-pectoralis","lateral-deltoid","upper-trapezius",
      "hands","inner-thigh","anterior-deltoid","medial-hamstrings","lateral-hamstrings","gluteus-medius","gluteus-maximus","long-head-triceps",
      "lateral-head-triceps","posterior-deltoid","lateral-deltoid","lower-trapezius",
      "upper-trapezius","medial-head-triceps"].includes(bodyPart)) {
      return [section, localStorage.getItem("sex"), bodyPart].join("/");
    }
  }
  
  function _hideModal() {
    $(".js-cta-modal").addClass("tw-opacity-0");
    $(".js-cta-modal").addClass("tw-pointer-events-none");
  }
  
  function _showModal() {
    $(".js-cta-modal").removeClass("tw-opacity-0");
    $(".js-cta-modal").removeClass("tw-pointer-events-none");
  }
  
  // You can add more functions or continue the code as needed
  
  // End of code
  
  