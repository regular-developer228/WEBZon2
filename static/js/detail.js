/**
 * detail.js
 * Рендер звёзд для product_detail и category_detail
 */
(function () {
  'use strict';

  function starsHTML(avg) {
    var full  = Math.floor(avg);
    var half  = (avg - full) >= 0.5 ? 1 : 0;
    var empty = 5 - full - half;
    return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
  }

  // product_detail: одиночный средний рейтинг
  document.querySelectorAll('.pd-rating__stars[data-avg]').forEach(function (el) {
    var avg = parseFloat(el.getAttribute('data-avg'));
    if (!isNaN(avg)) el.textContent = starsHTML(avg);
  });

  // product_detail: рейтинг каждого отзыва (1–5)
  document.querySelectorAll('.review-card__stars[data-rating]').forEach(function (el) {
    var r = parseInt(el.getAttribute('data-rating'), 10);
    if (!isNaN(r)) el.textContent = '★'.repeat(r) + '☆'.repeat(5 - r);
  });

  // category_detail: средний из массива
  document.querySelectorAll('.cat-card__stars[data-reviews]').forEach(function (el) {
    try {
      var ratings = JSON.parse(el.getAttribute('data-reviews'));
      if (!ratings.length) { el.textContent = ''; return; }
      var avg = ratings.reduce(function (a, b) { return a + b; }, 0) / ratings.length;
      el.textContent = starsHTML(avg);
      el.title = 'Рейтинг: ' + avg.toFixed(1) + ' / 5';
    } catch (e) {
      el.textContent = '';
    }
  });

})();