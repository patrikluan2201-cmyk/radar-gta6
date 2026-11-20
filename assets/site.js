/* Radar GTA 6 — busca local, categorias e vídeo de fonte oficial. */
(function () {
  'use strict';
  const input = document.getElementById('story-search');
  const cards = Array.from(document.querySelectorAll('.story-card[data-categories]'));
  const chips = Array.from(document.querySelectorAll('[data-filter]'));
  const result = document.getElementById('search-result');
  const noResults = document.getElementById('no-results');
  const clear = document.getElementById('search-clear');
  let filter = 'tudo';
  const normalize = value => (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  function update() {
    if (!input) return;
    const term = normalize(input.value);
    let visible = 0;
    for (const card of cards) {
      const categories = (card.dataset.categories || '').split(' ');
      const matchesCategory = filter === 'tudo' || categories.includes(filter);
      const matchesSearch = normalize(card.textContent + ' ' + (card.dataset.keywords || '')).includes(term);
      card.hidden = !(matchesCategory && matchesSearch);
      if (!card.hidden) visible++;
    }
    if (result) result.textContent = visible === 1 ? '1 matéria encontrada' : visible + ' matérias encontradas';
    if (noResults) noResults.hidden = visible !== 0;
    if (clear) clear.hidden = !input.value;
  }
  if (input) {
    const params = new URLSearchParams(location.search);
    const prior = params.get('busca');
    if (prior) input.value = prior.slice(0, 120);
    input.addEventListener('input', update);
    if (clear) clear.addEventListener('click', () => { input.value = ''; input.focus(); update(); });
  }
  chips.forEach(chip => chip.addEventListener('click', () => {
    filter = chip.dataset.filter;
    chips.forEach(item => item.setAttribute('aria-pressed', String(item === chip)));
    update();
  }));
  update();
  const play = document.getElementById('play-video');
  if (play) play.addEventListener('click', () => {
    const container = document.getElementById('video-player');
    if (!container || container.querySelector('iframe')) return;
    const iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/tJbzMqJGH4k?autoplay=1';
    iframe.title = 'Grand Theft Auto VI: An Extended Look — vídeo oficial da Rockstar Games';
    iframe.loading = 'eager';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    container.replaceChildren(iframe);
  });
})();
