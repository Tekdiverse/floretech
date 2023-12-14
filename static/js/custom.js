(function ($) {
  "use strict";

  $(document).ready(function () {
    var $window = $(window);
    var didScroll,
      lastScrollTop = 0,
      delta = 5,
      $mainNav = $("#sticky"),
      $mainNavHeight = $mainNav.outerHeight(),
      scrollTop;

    $window.on("scroll", function () {
      didScroll = true;
      scrollTop = $(this).scrollTop();
    });

    setInterval(function () {
      if (didScroll) {
        hasScrolled();
        didScroll = false;
      }
    }, 200);

    function hasScrolled() {
      if (Math.abs(lastScrollTop - scrollTop) <= delta) {
        return;
      }
      if (scrollTop > lastScrollTop && scrollTop > $mainNavHeight) {
        $mainNav.css("top", -$mainNavHeight);
      } else {
        if (scrollTop + $(window).height() < $(document).height()) {
          $mainNav.css("top", 0);
        }
      }
      lastScrollTop = scrollTop;
    }

    //sticky header
    function navbarFixed() {
      if ($("#sticky").length) {
        $(window).scroll(function () {
          var scroll = $(window).scrollTop();
          if (scroll) {
            $("#sticky").addClass("navbar_fixed");
          } else {
            $("#sticky").removeClass("navbar_fixed");
          }
        });
      }
    }
    navbarFixed();

    $(".navbar-nav > li .mobile_dropdown_icon").on("click", function (e) {
      $(this).parent().find("ul").first().toggle(300);
      $(this).parent().siblings().find("ul").hide(300);
    });

    if ($(".submenu").length) {
      $(".submenu > .dropdown-toggle").on("click", function () {
        var location = $(this).attr("href");
        window.location.href = location;
        return false;
      });
    }

    //initialize smmothscroll
    if ($("header").length) {
      $("header").smoothScroll();
    }

    if ($("#banner_animation").length > 0) {
      $("#banner_animation").parallax({
        scalarX: 10.0,
        scalarY: 7.0,
      });
    }
    if ($("#banner_animation2").length > 0) {
      $("#banner_animation2").parallax({
        scalarX: 10.0,
        scalarY: 0.0,
      });
    }
    if ($("#card_area_animation").length > 0) {
      $("#card_area_animation").parallax({
        scalarX: 10.0,
        scalarY: 0.0,
      });
    }
    if ($("#MouseMoveAnimation").length > 0) {
      $("#MouseMoveAnimation").parallax({
        scalarX: 5.0,
        scalarY: 10.0,
      });
    }

    if ($("#readOnlyClose").length) {
      $("#readOnlyClose").on("click", function () {
        $("#locationSelect").val("");
        $("#locationSelect").focus();
      });
    }

    // === Back to Top Button
    var back_top_btn = $("#back-to-top");

    $(window).scroll(function () {
      if ($(window).scrollTop() > 300) {
        back_top_btn.addClass("show");
      } else {
        back_top_btn.removeClass("show");
      }
    });

    back_top_btn.on("click", function (e) {
      e.preventDefault();
      $("html, body").animate({ scrollTop: 0 }, "300");
    });

    //initialize wow js
    new WOW({}).init();

    //initialize counterUp
    if ($(".counter span").length) {
      $(".counter span").counterUp();
    }
    if ($(".stat-counter").length) {
      $(".stat-counter").counterUp();
    }

    //initialize niceselect
    if ($("#select-lang").length) {
      $("#select-lang").niceSelect();
    }
    if ($("#select-loan-type").length) {
      $("#select-loan-type").niceSelect();
    }
    if ($("#loandetails01").length) {
      $("#loandetails01").niceSelect();
    }
    if ($("#loandetails02").length) {
      $("#loandetails02").niceSelect();
    }
    if ($("#dob-d").length) {
      $("#dob-d").niceSelect();
    }
    if ($("#dob-m").length) {
      $("#dob-m").niceSelect();
    }
    if ($("#dob-y").length) {
      $("#dob-y").niceSelect();
    }
    if ($("#sort-select").length) {
      $("#sort-select").niceSelect();
    }

    //ediatable location select
    if ($("#locationSelect").length) {
      $("#locationSelect").editableSelect();
    }

    //initialize fencybox
    if ($("[data-fancybox]").length) {
      $("[data-fancybox]").fancybox({
        animationEffect: "zoom-in-out",
      });
    }

    //initialize slick slider
    if ($(".testimonial-slider").length) {
      $(".testimonial-slider").slick({
        dots: false,
        arrows: true,
        prevArrow:
          '<button type="button" class="slick-prev"><i class="arrow_carrot-left"></i></button>',
        nextArrow:
          '<button type="button" class="slick-next"><i class="arrow_carrot-right"></i></button>',
        slidesToShow: 1,
        centerMode: true,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 7000,
        slidesToScroll: 1,
        variableWidth: true,
        responsive: [
          {
            breakpoint: 576,
            settings: {
              centerMode: false,
              variableWidth: false,
            },
          },
        ],
      });
    }

    if ($(".testimonial-slider-2").length) {
      $(".testimonial-slider-2").slick({
        dots: false,
        arrows: true,
        prevArrow:
          '<button type="button" class="slick-prev"><i class="arrow_left"></i></button>',
        nextArrow:
          '<button type="button" class="slick-next"><i class="arrow_right"></i></button>',
        slidesToShow: 3,
        centerMode: false,
        autoplay: false,
        infinite: true,
        autoplaySpeed: 7000,
        slidesToScroll: 1,
        asNavFor: ".testimonial-slider-3",
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 2,
            },
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 2,
            },
          },
        ],
      });
    }

    if ($(".testimonial-slider-3").length) {
      $(".testimonial-slider-3").slick({
        dots: false,
        asNavFor: ".testimonial-slider-2",
        arrows: false,
        slidesToShow: 1,
        centerMode: false,
        autoplay: false,
        infinite: true,
        slidesToScroll: 1,
        fade: true,
      });
    }
    if ($(".feature-slider").length) {
      $(".feature-slider").slick({
        dots: true,
        arrows: false,
        slidesToShow: 3,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 5000,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
    }
    if ($(".statistics-slider").length) {
      $(".statistics-slider").slick({
        dots: true,
        arrows: false,
        slidesToShow: 1,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 3000,
        slidesToScroll: 1,
      });
    }
    if ($(".client-slider").length) {
      $(".client-slider").slick({
        dots: true,
        arrows: false,
        centerMode: false,
        slidesToShow: 3,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 5000,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 1200,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
            },
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
    }
    /* new version */
    if ($(".client-slider-2").length) {
      $(".client-slider-2").slick({
        dots: true,
        arrows: true,
        prevArrow:
          '<button type="button" class="slick-prev"><i class="arrow_left"></i></button>',
        nextArrow:
          '<button type="button" class="slick-next"><i class="arrow_right"></i></button>',
        centerMode: false,
        slidesToShow: 3,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 5000,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 1200,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
            },
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
    }
    if ($(".loan-slider").length) {
      $(".loan-slider").slick({
        dots: true,
        arrows: true,
        prevArrow:
          '<button type="button" class="slick-prev"><i class="arrow_left"></i></button>',
        nextArrow:
          '<button type="button" class="slick-next"><i class="arrow_right"></i></button>',
        centerMode: false,
        slidesToShow: 3,
        autoplay: true,
        infinite: true,
        autoplaySpeed: 5000,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 1200,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
            },
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
    }
    if ($(".news-slider").length) {
      $(".news-slider").slick({
        dots: true,
        arrows: false,
        centerMode: false,
        slidesToShow: 3,
        autoplay: false,
        infinite: true,
        autoplaySpeed: 7500,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
            },
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
    }

    //initilalize Telephone Input Country
    if ($("#inputPhoneNumber").length) {
      $("#inputPhoneNumber").intlTelInput({
        separateDialCode: false,
        utilsScript: "js/utils.js",
      });
    }

    //initilalize DropeZone
    if ($("#dropzone").length) {
      $("#dropzone").dropzone({
        paramName: "file",
        url: "upload-target",
      });
    }

    // ------- Emi Calculator --------- //
    var SelectedAmount,
      selectedTime = {},
      RateOfInterestTime,
      RateOfInterestAmount,
      SelectedRoi;

    if (typeof wNumb !== "undefined") {
      var AmountFormat = wNumb({
        decimals: 0,
        thousand: ",",
        prefix: "$",
      });
      var AmountFormatNoMerge = wNumb({
        decimals: 0,
        thousand: ",",
      });

      var TimeFormatMonths = wNumb({
        suffix: " months",
      });
      var TimeFormatYears = wNumb({
        suffix: " years",
      });
      var TimeFormatWeeks = wNumb({
        suffix: " weeks",
      });
      var RoiFormat = wNumb({
        suffix: " %",
      });
    }

    //Slider Elements
    var mySlider = document.getElementById("RangeSlider");
    var mySliderMonth = document.getElementById("MonthRangeSlider");
    var mySliderWeekly = document.getElementById("WeekRangeSlider");
    var mySliderYear = document.getElementById("YearRangeSlider");
    var mySliderROI = document.getElementById("RoiRangeSlider");
    //-----home page 1
    var SliderAmount = document.getElementById("SliderAmount");
    var SliderPeriod = document.getElementById("SliderPeriod");

    function clickOnPip(sliderName, This) {
      var value = Number(This.getAttribute("data-value"));
      sliderName.noUiSlider.set(value);
    }

    function SetPipsOnSlider(PipsName, sliderName) {
      for (var i = 0; i < PipsName.length; i++) {
        PipsName[i].style.cursor = "pointer";
        PipsName[i].addEventListener("click", function () {
          clickOnPip(sliderName, this);
        });
      }
    }

    //   Activate Range Sliders

    if (mySlider && mySliderMonth && mySliderYear) {
      noUiSlider.create(mySlider, {
        start: [15000],
        connect: "lower",
        range: {
          min: 5000,
          max: 150000,
        },
        format: wNumb({
          decimals: 0,
        }),
        pips: {
          mode: "values",
          density: 100,

          values: [5000, 25000, 50000, 75000, 100000, 125000, 150000],
          stepped: true,
          format: wNumb({
            encoder: function (a) {
              return a / 1000;
            },
            decimals: 0,
            prefix: "$",
            suffix: "k",
          }),
        },
      });
      noUiSlider.create(mySliderMonth, {
        start: [18],
        connect: "lower",
        range: {
          min: 12,
          max: 48,
        },
        format: wNumb({
          decimals: 0,
        }),
        pips: {
          mode: "values",
          density: 100,

          values: [12, 18, 24, 30, 36, 42, 48],
          stepped: true,
          format: wNumb({
            decimals: 0,
          }),
        },
      });
      noUiSlider.create(mySliderYear, {
        start: [5],
        connect: "lower",
        range: {
          min: 2,
          max: 8,
        },
        format: wNumb({
          decimals: 0,
        }),
        pips: {
          mode: "values",
          density: 100,

          values: [2, 3, 4, 5, 6, 7, 8],
          stepped: true,
          format: wNumb({
            decimals: 0,
          }),
        },
      });
      noUiSlider.create(mySliderWeekly, {
        start: [5],
        connect: "lower",
        range: {
          min: 2,
          max: 40,
        },
        format: wNumb({
          decimals: 0,
        }),
      });
      //Slider Pips
      var pips = mySlider.querySelectorAll(".noUi-value");
      var pipsMonth = mySliderMonth.querySelectorAll(".noUi-value");
      var pipsYear = mySliderYear.querySelectorAll(".noUi-value");

      //Slider Input Element
      var inputMonthFormat = document.getElementById("SetMonthRange");
      var inputFormat = document.getElementById("SetRange");

      SetPipsOnSlider(pips, mySlider);
      SetPipsOnSlider(pipsMonth, mySliderMonth);
      SetPipsOnSlider(pipsYear, mySliderYear);
      mySlider.noUiSlider.on("update", function (values, handle) {
        SelectedAmount = AmountFormat.from(values[handle]);
        CalculateAmount();
      });

      inputFormat.addEventListener("change", function () {
        mySlider.noUiSlider.set(this.value);
      });
      mySliderMonth.noUiSlider.on("update", function (values, handle) {
        selectedTime = {
          type: "month",
          value: TimeFormatMonths.from(values[handle]),
        };

        CalculateAmount();
      });

      mySliderWeekly.noUiSlider.on("update", function (values, handle) {
        selectedTime = {
          type: "week",
          value: TimeFormatWeeks.from(values[handle]),
        };

        CalculateAmount();
      });
      mySliderYear.noUiSlider.on("update", function (values, handle) {
        selectedTime = {
          type: "year",
          value: TimeFormatYears.from(values[handle]),
        };
        CalculateAmount();
      });
      inputMonthFormat.addEventListener("change", function () {
        if ($("#monthTab.active").length > 0) {
          mySliderMonth.noUiSlider.set(this.value);
        } else if ($("#yearTab.active").length > 0) {
          mySliderYear.noUiSlider.set(this.value);
        } else if ($("#weekTab.active").length > 0) {
          mySliderWeekly.noUiSlider.set(this.value);
        } else {
          mySliderMonth.noUiSlider.set(this.value);
        }
      });

      $("#yearTab-tab").on("click", function () {
        $(".active_bar").removeClass("left");
        mySliderYear.noUiSlider.on("update", function (values, handle) {
          selectedTime = {
            type: "year",
            value: TimeFormatYears.from(values[handle]),
          };
          CalculateAmount();
        });
      });
      $("#monthTab-tab").on("click", function () {
        $(".active_bar").addClass("left");
        mySliderMonth.noUiSlider.on("update", function (values, handle) {
          selectedTime = {
            type: "month",
            value: TimeFormatMonths.from(values[handle]),
          };
          CalculateAmount();
        });
      });
      $("#weekTab-tab").on("click", function () {
        mySliderWeekly.noUiSlider.on("update", function (values, handle) {
          selectedTime = {
            type: "week",
            value: TimeFormatWeeks.from(values[handle]),
          };
          CalculateAmount();
        });
      });
    }
    if (SliderAmount && SliderPeriod) {
      noUiSlider.create(SliderAmount, {
        start: [100000],
        connect: "lower",
        range: {
          min: 5000,
          max: 250000,
        },
        format: wNumb({
          decimals: 0,
          thousand: ",",
          prefix: "$ ",
        }),
      });
      noUiSlider.create(SliderPeriod, {
        start: [3],
        connect: "lower",
        range: {
          min: 1,
          max: 5,
        },
        format: wNumb({
          decimals: 0,
          suffix: " year",
        }),
      });

      var SliderAmountFormat = document.getElementById("SetSliderAmount");
      var SliderPeriodFormat = document.getElementById("SetSliderPeriod");

      SliderAmount.noUiSlider.on("update", function (values, handle) {
        SliderAmountFormat.value = values[handle];
      });
      SliderPeriod.noUiSlider.on("update", function (values, handle) {
        SliderPeriodFormat.value = values[handle];
      });

      SliderAmountFormat.addEventListener("change", function () {
        SliderAmount.noUiSlider.set(this.value);
      });
      SliderPeriodFormat.addEventListener("change", function () {
        SliderPeriod.noUiSlider.set(this.value);
      });
    }

    if (mySliderROI) {
      noUiSlider.create(mySliderROI, {
        start: [8],
        connect: "lower",
        range: {
          min: 5,
          max: 30,
        },
        format: wNumb({
          decimals: 0,
        }),
      });

      var inputRoiFormat = document.getElementById("SetRoiRange");

      mySliderROI.noUiSlider.on("update", function (values, handle) {
        inputRoiFormat.value = values[handle];
        SelectedRoi = RoiFormat.from(values[handle]);
        CalculateAmount();
      });

      inputRoiFormat.addEventListener("change", function () {
        mySliderROI.noUiSlider.set(this.value);
      });
    }

    function CalculateAmount() {
      if (selectedTime.type === "month") {
        var LoanTime = selectedTime.value;
        switch (true) {
          case LoanTime >= 48:
            RateOfInterestTime = 2.4;
            break;
          case LoanTime >= 42:
            RateOfInterestTime = 2.55;
            break;
          case LoanTime >= 32:
            RateOfInterestTime = 2.7;
            break;
          case LoanTime >= 25:
            RateOfInterestTime = 2.9;
            break;
          case LoanTime >= 20:
            RateOfInterestTime = 3;
            break;
          case LoanTime >= 12:
            RateOfInterestTime = 3.15;
            break;
          default:
            RateOfInterestTime = 0;
        }
      }
      if (selectedTime.type === "year") {
        var LoanTime = selectedTime.value;
        switch (true) {
          case LoanTime >= 8:
            RateOfInterestTime = 2;
            break;
          case LoanTime >= 7:
            RateOfInterestTime = 2.2;
            break;
          case LoanTime >= 6:
            RateOfInterestTime = 2.3;
            break;
          case LoanTime >= 5:
            RateOfInterestTime = 2.5;
            break;
          case LoanTime >= 4:
            RateOfInterestTime = 2.7;
            break;
          case LoanTime >= 3:
            RateOfInterestTime = 2.9;
            break;
          case LoanTime >= 2:
            RateOfInterestTime = 3.1;
            break;

          default:
            RateOfInterestTime = 0;
        }
      }
      if (typeof SelectedAmount === "number") {
        var LoanAmount = SelectedAmount;
        switch (true) {
          case LoanAmount >= 13e4:
            RateOfInterestAmount = 2.9;
            break;
          case LoanAmount >= 115e3:
            RateOfInterestAmount = 3.1;
            break;
          case LoanAmount >= 1e5:
            RateOfInterestAmount = 3.3;
            break;
          case LoanAmount >= 8e4:
            RateOfInterestAmount = 3.5;
            break;
          case LoanAmount >= 65e3:
            RateOfInterestAmount = 3.7;
            break;
          case LoanAmount >= 5e4:
            RateOfInterestAmount = 3.8;
            break;
          case LoanAmount >= 25e3:
            RateOfInterestAmount = 3.95;
            break;
          case LoanAmount >= 1e4:
            RateOfInterestAmount = 4;
            break;
          default:
            RateOfInterestAmount = 4.09;
        }
      }

      var TotalRateOfInterest = SelectedRoi
        ? SelectedRoi / 100
        : (RateOfInterestAmount + RateOfInterestTime) / 100;

      var TotalInterest = SelectedAmount * TotalRateOfInterest;
      var InterestAndPrincipal = TotalInterest + SelectedAmount;

      if ($(inputFormat).hasClass("noTextMerge")) {
        inputFormat.value = AmountFormatNoMerge.to(SelectedAmount);
      } else {
        inputFormat.value = AmountFormat.to(SelectedAmount);
      }

      $(".LoanTotalAmount").text(AmountFormat.to(InterestAndPrincipal) + "*");

      if ($(inputMonthFormat).hasClass("noTextMerge")) {
        inputMonthFormat.value = selectedTime.value;
      } else {
        inputMonthFormat.value = selectedTime.value + " " + selectedTime.type;
      }

      if ($(".LoanTotalDuration").length) {
        $(".LoanTotalDuration").text(
          selectedTime.value + " " + selectedTime.type
        );
        if (selectedTime.type) {
          $(".loanTermIndicator").text(selectedTime.type.charAt(0));
        }
      }

      $("#emiAmount").text(
        AmountFormat.to(InterestAndPrincipal / selectedTime.value) + "*"
      );
      $("#InterestPayable").text(AmountFormat.to(TotalInterest) + "*");
      $("#InterestAmount").text((TotalRateOfInterest * 100).toFixed(2));

      var loanGraphEl = $("#loan_graph_circle");
      var percent = (100 * TotalInterest) / InterestAndPrincipal;
      loanGraphEl
        .find($(".left-side"))
        .css({ transform: "rotate(" + percent * 3.6 + "deg)" });

      if (percent <= 50) {
        loanGraphEl.find($(".right-side")).css({ display: "none" });
      } else if (percent > 50) {
        loanGraphEl.find($(".right-side")).css({ transform: "rotate(180deg)" });
        loanGraphEl
          .find($(".pie"))
          .css({ clip: "rect(auto, auto, auto, auto)" });
      }
    }

    if ($("#loanStartDate").length) {
      $("#loanStartDate").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
      });
      $("#loanEndDate").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
      });
    } // End of Calculator

    /*------------ Added Dark Mode ------------*/
    function createCookie(name, value, days) {
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + value + expires + "; path=/";
    }

    function readCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
      }
      return null;
    }

    var prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    var selectedNightTheme = readCookie("body_dark");

    if (
      selectedNightTheme == "true" ||
      (selectedNightTheme === null && prefersDark)
    ) {
      applyNight();
      $(".dark_mode_switcher").prop("checked", true);
    } else {
      applyDay();
      $(".dark_mode_switcher").prop("checked", false);
    }

    function applyNight() {
      if ($(".js-darkmode-btn .ball").length) {
        $(".js-darkmode-btn .ball").css("left", "26px");
      }
      $("body").addClass("body_dark");
    }

    function applyDay() {
      if ($(".js-darkmode-btn .ball").length) {
        $(".js-darkmode-btn .ball").css("left", "3px");
      }
      $("body").removeClass("body_dark");
    }

    $(".dark_mode_switcher").change(function () {
      if ($(this).is(":checked")) {
        applyNight();

        createCookie("body_dark", true, 999);
      } else {
        applyDay();
        createCookie("body_dark", false, 999);
      }
    });
    // End of Dark Mode
  });

  /*--------------- Start price js--------*/
  if ($(".pricing_tab_btn .toggle").length) {
    $(".pricing_tab_btn .toggle").on("click", function () {
      $(this).toggleClass("clicked");
      $(".pricing_inner").toggleClass("active");
      $(".pricing_tab_btn").toggleClass("active");
    });
  }

  if ($(".map_list").length) {
    setInterval(function () {
      var active = $(".map_list li.active");
      active.removeClass("active");
      if (active.next("li").length == 0) {
        active.parent(".map_list").find("li:first-child").addClass("active");
      } else {
        active.next("li").addClass("active");
      }
    }, 3000);
  }
})(jQuery);
