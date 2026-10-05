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
					setTimeout(tick, g === steps.length ? 2600 : g === -1 ? 700 : 2400);
				})();
			}, 0.3);
		});
	}

	function init() {
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
