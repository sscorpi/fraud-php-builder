import { scroll_to_top_array } from "./exports/scroll_top.js";

// SCROLL HANDLER

// Get the current scroll position and store it in local storage

const pos = parseInt(sessionStorage.getItem("pos"));
$(window).on("beforeunload", function () {
  sessionStorage.setItem("pos", window.scrollY.toString());
});
$(window).on("load", function () {
  if (!isNaN(pos)) {
    window.scrollTo(0, pos);
    sessionStorage.removeItem("pos");
  }
});
function getCurrentPage() {
  let mypage = window.location.pathname.split("/");
  return mypage[mypage.length - 1].split(".")[0];
}

if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
} else if (
  performance.navigation.type === performance.navigation.TYPE_NAVIGATE
) {
  if (scroll_to_top_array.includes(getCurrentPage())) {
    $(window).on("load", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
}
// SCROLL HANDLER

// ROUTE HANDLER

// Get the current path without the domain and query parameters
const currentPath = window.location.href;

// Get all the anchor elements on the page
const anchors = document.querySelectorAll("a");

// Add a click event listener to each anchor element
anchors.forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    // Get the path of the target URL without the domain and query parameters
    const targetPath = anchor.href;
    // Check if the target URL path matches the current page path
    if (targetPath === currentPath) {
      // Prevent the default behavior of the link
      e.preventDefault();
    }
  });
});

// ROUTE HANDLER
