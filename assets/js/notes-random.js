/**
 * Random note picker for the notes toolbar.
 */
(function () {
  var randomBtn = document.querySelector("[data-notes-random]");
  var randomData = document.querySelector(".notes-random-data");
  if (!randomBtn || !randomData) return;

  var pool;
  try {
    pool = JSON.parse(randomData.textContent);
  } catch (e) {
    pool = [];
  }

  randomBtn.addEventListener("click", function () {
    if (!pool.length) return;
    var pick = pool[Math.floor(Math.random() * pool.length)];
    if (pick && pick.url) {
      window.location.href = pick.url;
    }
  });
})();
