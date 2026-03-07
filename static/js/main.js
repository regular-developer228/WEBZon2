/**
 * METRO SHOP — main.js
 * AppBar, horizontal scroll controls, star ratings, mobile long-tap
 */

(function () {
  'use strict';

  /* -----------------------------------------------
     AppBar
  ----------------------------------------------- */
  const appbar = document.getElementById('appbar');

  function showAppBar() {
    appbar.classList.add('appbar--visible');
  }

  function hideAppBar() {
    appbar.classList.remove('appbar--visible');
  }

  function toggleAppBar() {
    appbar.classList.toggle('appbar--visible');
  }

  // Right-click → toggle AppBar, block system context menu
  document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    toggleAppBar();
  });

  // Click outside AppBar → hide it
  document.addEventListener('click', function (e) {
    if (appbar.classList.contains('appbar--visible') && !appbar.contains(e.target)) {
      hideAppBar();
    }
  });

  /* -----------------------------------------------
     Mobile: long tap (500ms) on document → toggle AppBar
  ----------------------------------------------- */
  var longTapTimer = null;

  document.addEventListener('touchstart', function (e) {
    // Start timer
    longTapTimer = setTimeout(function () {
      longTapTimer = null;
      toggleAppBar();
    }, 500);
  }, { passive: true });

  document.addEventListener('touchend', function () {
    if (longTapTimer) {
      clearTimeout(longTapTimer);
      longTapTimer = null;
    }
  }, { passive: true });

  document.addEventListener('touchmove', function () {
    if (longTapTimer) {
      clearTimeout(longTapTimer);
      longTapTimer = null;
    }
  }, { passive: true });

  /* -----------------------------------------------
     Horizontal scroll buttons
     <button data-scroll="track_id" data-dir="1|-1">
  ----------------------------------------------- */
  var SCROLL_STEP = 240; // px per click

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-scroll]');
    if (!btn) return;

    var trackId = btn.getAttribute('data-scroll');
    var dir = parseInt(btn.getAttribute('data-dir'), 10) || 1;
    var track = document.getElementById(trackId);

    if (track) {
      track.scrollBy({ left: dir * SCROLL_STEP, behavior: 'smooth' });
    }
  });

  /* -----------------------------------------------
     Star ratings
     Reads data-reviews="[4,5,3,...]" from .stars elements,
     computes average, renders filled/empty stars.
  ----------------------------------------------- */
  function renderStars(avg) {
    var full  = Math.floor(avg);
    var half  = (avg - full) >= 0.5 ? 1 : 0;
    var empty = 5 - full - half;
    return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
  }

  document.querySelectorAll('.stars[data-reviews]').forEach(function (el) {
    try {
      var ratings = JSON.parse(el.getAttribute('data-reviews'));
      if (!ratings.length) {
        el.textContent = '☆☆☆☆☆';
        el.classList.add('stars--empty');
        return;
      }
      var sum = ratings.reduce(function (a, b) { return a + b; }, 0);
      var avg = sum / ratings.length;
      el.textContent = renderStars(avg);
      el.setAttribute('title', 'Рейтинг: ' + avg.toFixed(1) + ' / 5');
    } catch (err) {
      el.textContent = '☆☆☆☆☆';
      el.classList.add('stars--empty');
    }
  });

})();
