/**
 * Cypress Hills — small front-end enhancements for the Elementor build.
 * Everything here hooks onto CSS classes set on Elementor elements, so the
 * content itself stays editable in Elementor.
 */
(function () {
	'use strict';

	var body = document.body;
	var inEditor = body.classList.contains('elementor-editor-active');
	var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	body.classList.add('ch-js');

	function onVisible(el, cb, threshold) {
		if (!('IntersectionObserver' in window)) { cb(); return; }
		var io = new IntersectionObserver(function (entries) {
			if (entries[0].isIntersecting) { cb(); io.disconnect(); }
		}, { threshold: threshold || 0.3 });
		io.observe(el);
	}

	/* Hero: image wipe + slow zoom, then the navy panel slides in and its text reveals. */
	function initHero() {
		if (inEditor) { return; }
		document.querySelectorAll('.ch-hero').forEach(function (stage) {
			var slides = Array.prototype.filter.call(stage.children, function (el) { return el.classList.contains('ch-slide'); });
			if (!slides.length) { return; }
			var wrap = stage.closest('.ch-hero-wrap') || stage.parentElement;
			var curEl = wrap.querySelector('.ch-hero-cur .elementor-heading-title');
			var totalEl = wrap.querySelector('.ch-hero-total .elementor-heading-title');
			var bar = wrap.querySelector('.ch-hero-bar');
			var prevBtn = wrap.querySelector('.ch-hero-prev .elementor-button');
			var nextBtn = wrap.querySelector('.ch-hero-next .elementor-button');
			var IMG_ONLY = 2000, HOLD = 5000, N = slides.length;
			var cur = 0, tPanel = 0, tNext = 0;
			function pad(n) { return (n < 10 ? '0' : '') + n; }
			if (totalEl) { totalEl.textContent = pad(N); }
			if (prevBtn) { prevBtn.setAttribute('aria-label', 'Previous slide'); }
			if (nextBtn) { nextBtn.setAttribute('aria-label', 'Next slide'); }

			function ring() {
				if (!nextBtn) { return; }
				var old = nextBtn.querySelector('.ch-hero-ring');
				if (old) { old.remove(); }
				if (reduceMotion) { return; }
				nextBtn.insertAdjacentHTML('beforeend', '<svg class="ch-hero-ring" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="28"></circle></svg>');
				nextBtn.style.setProperty('--ch-ring', (IMG_ONLY + HOLD) + 'ms');
			}
			function arm() {
				clearTimeout(tPanel); clearTimeout(tNext);
				tPanel = setTimeout(function () { slides[cur].classList.add('is-panel'); }, reduceMotion ? 0 : IMG_ONLY);
				if (!reduceMotion) { tNext = setTimeout(function () { go((cur + 1) % N); }, IMG_ONLY + HOLD); }
				ring();
			}
			function paint() {
				if (curEl) { curEl.textContent = pad(cur + 1); }
				if (bar) { bar.style.setProperty('--ch-progress', ((cur + 1) / N * 100) + '%'); }
			}
			function go(i) {
				if (i === cur) { return; }
				var prev = cur;
				slides.forEach(function (sl, k) {
					sl.classList.remove('is-prev', 'is-panel');
					if (k !== prev && k !== i) { sl.classList.remove('is-current'); }
				});
				slides[prev].classList.remove('is-current');
				slides[prev].classList.add('is-prev');
				void slides[i].offsetWidth; // restart the wipe from the left edge
				slides[i].classList.add('is-current');
				cur = i;
				paint();
				arm();
			}
			function click(dir) {
				return function (e) { e.preventDefault(); go((cur + dir + N) % N); };
			}
			if (prevBtn) { prevBtn.addEventListener('click', click(-1)); }
			if (nextBtn) { nextBtn.addEventListener('click', click(1)); }

			paint();
			setTimeout(function () { slides[0].classList.add('is-current'); arm(); }, 120);
		});
	}

	/* Recent work: the active panel expands; auto-advance every 6s with a progress bar; hover/focus picks. */
	function initWork() {
		if (inEditor) { return; }
		var mq = window.matchMedia('(max-width: 819px)');
		document.querySelectorAll('.ch-work-acc').forEach(function (acc) {
			var cards = Array.prototype.filter.call(acc.children, function (el) { return el.classList.contains('ch-work-card'); });
			if (!cards.length) { return; }
			var cur = 0, timer = 0;
			cards.forEach(function (c) {
				if (!c.querySelector('.ch-work-bar')) { c.insertAdjacentHTML('beforeend', '<span class="ch-work-bar" aria-hidden="true"></span>'); }
			});
			function go(i) {
				clearTimeout(timer);
				cur = i;
				cards.forEach(function (c, k) {
					c.classList.toggle('is-active', mq.matches || k === i);
					c.classList.remove('is-running');
				});
				if (mq.matches || reduceMotion) { return; }
				requestAnimationFrame(function () {
					requestAnimationFrame(function () { cards[i].classList.add('is-running'); });
				});
				timer = setTimeout(function () { go((cur + 1) % cards.length); }, 6000);
			}
			cards.forEach(function (c, k) {
				function pick() { if (!mq.matches && k !== cur) { go(k); } }
				c.addEventListener('mouseenter', pick);
				c.addEventListener('focusin', pick);
			});
			if (mq.addEventListener) { mq.addEventListener('change', function () { go(cur); }); }
			go(0);
		});
	}

	/* Marquee: duplicate each track's chips once so translateX(-50%) loops seamlessly. */
	function initMarquee() {
		if (inEditor) { return; }
		document.querySelectorAll('.ch-marq-track').forEach(function (track) {
			if (track.dataset.chCloned) { return; }
			Array.prototype.slice.call(track.children).forEach(function (chip) {
				var copy = chip.cloneNode(true);
				copy.setAttribute('aria-hidden', 'true');
				copy.querySelectorAll('a, button').forEach(function (a) { a.setAttribute('tabindex', '-1'); });
				track.appendChild(copy);
			});
			track.dataset.chCloned = '1';
		});
	}

	/* Sketch / finished-yard compare: drag to move the divider; gentle sweep until touched. */
	function initCompare() {
		document.querySelectorAll('.ch-compare').forEach(function (el) {
			var after = el.querySelector('.ch-cmp-after');
			if (!after || el.querySelector('.ch-cmp-handle')) { return; }
			var handle = document.createElement('div');
			handle.className = 'ch-cmp-handle';
			handle.innerHTML = '<span aria-hidden="true">‹ ›</span>';
			el.appendChild(handle);

			var user = false, raf = 0;
			function set(p) {
				p = Math.max(2, Math.min(98, p));
				after.style.clipPath = 'inset(0 0 0 ' + p + '%)';
				handle.style.left = p + '%';
			}
			function sweep() {
				if (reduceMotion || inEditor) { set(50); return; }
				var t0 = performance.now();
				(function go(now) {
					if (user) { return; }
					set(50 + Math.sin((now - t0) / 1000 * 0.9) * 28);
					raf = requestAnimationFrame(go);
				})(t0);
			}
			el.addEventListener('pointerdown', function (e) {
				user = true;
				cancelAnimationFrame(raf);
				var r = el.getBoundingClientRect();
				function mv(ev) { set((ev.clientX - r.left) / r.width * 100); }
				function up() {
					window.removeEventListener('pointermove', mv);
					window.removeEventListener('pointerup', up);
				}
				mv(e);
				window.addEventListener('pointermove', mv);
				window.addEventListener('pointerup', up);
			});
			onVisible(el, sweep, 0.2);
		});
	}

	/* Services: rotate the highlighted service every few seconds; hover/focus takes over. */
	function initServices() {
		document.querySelectorAll('.ch-services').forEach(function (sec) {
			var items = sec.querySelectorAll('.ch-svc-item');
			var imgs = sec.querySelectorAll('.ch-svc-img');
			var label = sec.querySelector('.ch-svc-label .elementor-heading-title');
			if (!items.length) { return; }
			var cur = 0, timer = 0;
			function set(i) {
				cur = i;
				items.forEach(function (it, k) { it.classList.toggle('is-active', k === i); });
				imgs.forEach(function (im, k) { im.classList.toggle('is-active', k === i); });
				if (label) {
					var name = items[i].querySelector('.ch-svc-name .elementor-heading-title');
					if (name) { label.textContent = name.textContent.trim(); }
				}
			}
			function arm() {
				clearInterval(timer);
				if (reduceMotion || inEditor) { return; }
				timer = setInterval(function () { set((cur + 1) % items.length); }, 3800);
			}
			items.forEach(function (it, k) {
				it.addEventListener('mouseenter', function () { set(k); arm(); });
				it.addEventListener('focusin', function () { set(k); arm(); });
			});
			set(0);
			arm();
		});
	}

	/* Process: light the steps up in sequence once the section is on screen, then loop. */
	function initProcess() {
		document.querySelectorAll('.ch-process').forEach(function (sec) {
			var steps = sec.querySelectorAll('.ch-step');
			if (!steps.length) { return; }
			steps.forEach(function (s) {
				var c = s.querySelector('.ch-step-circle');
				if (c && !c.querySelector('.ch-step-ring')) {
					c.insertAdjacentHTML('afterbegin', '<svg class="ch-step-ring" viewBox="0 0 100 100" aria-hidden="true">' +
						'<circle class="ch-ring-track" cx="50" cy="50" r="48"></circle>' +
						'<circle class="ch-ring-arc" cx="50" cy="50" r="48" pathLength="100"></circle></svg>');
				}
			});
			function paint(g) {
				steps.forEach(function (s, i) {
					s.classList.toggle('is-on', g >= i);
					s.classList.toggle('is-current', g === i);
				});
			}
			if (reduceMotion || inEditor) { paint(steps.length); return; }
			paint(-1);
			onVisible(sec, function () {
				var g = -1;
				(function tick() {
					g = g >= steps.length ? -1 : g + 1;
					paint(g);
					setTimeout(tick, g === steps.length ? 1800 : g === -1 ? 700 : 2400);
				})();
			}, 0.3);
		});
	}

	function init() {
		initHero();
		initWork();
		initMarquee();
		initCompare();
		initServices();
		initProcess();
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
