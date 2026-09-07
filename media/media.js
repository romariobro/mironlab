(() => {
  const cards = [...document.querySelectorAll('.all-grid .media-card')];
  const buttons = [...document.querySelectorAll('[data-filter-group]')];
  const topic = document.querySelector('#topic');
  const count = document.querySelector('#results-count');
  if (!count) return;
  let group = 'All';
  const apply = () => {
    let visible = 0;
    cards.forEach(card => {
      card.hidden = !((group === 'All' || card.dataset.group === group) &&
        (topic.value === 'All' || card.dataset.topics.split('|').includes(topic.value)));
      if (!card.hidden) visible++;
    });
    document.querySelectorAll('.media-group').forEach(section => {
      section.hidden = ![...section.querySelectorAll('.media-card')].some(card => !card.hidden);
    });
    count.textContent = document.documentElement.lang === 'ru' ? 'Материалов: ' + visible : 'Materials: ' + visible;
    document.querySelector('#empty').hidden = visible !== 0;
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    group = button.dataset.filterGroup;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    apply();
  }));
  topic.addEventListener('change', apply);
  apply();
})();
