/*** Sort Mense ***/

// 1. prendi la lista
const list = document.querySelector('.mense-list');

// 2. funzione che ritorna sempre il set corrente di card
const getCards = () => Array.from(list.querySelectorAll('.mensa-card'));

function sortAndAnimate(key, asc = true) {
  const cards = getCards();                                // snapshot attuale
  const first = new Map(cards.map(c => [c, c.getBoundingClientRect()]));

  // ordina leggendo i data-*
  cards.sort((a, b) => {
    const av = +a.dataset[key], bv = +b.dataset[key];
    return asc ? av - bv : bv - av;
  });

  // riappendi la colonna (il padre .col-*)
  cards.forEach(c => list.appendChild(c.parentElement));

  const last = new Map(cards.map(c => [c, c.getBoundingClientRect()]));

  // FLIP
  cards.forEach(card => {
    const f = first.get(card), l = last.get(card);
    const dx = f.left - l.left, dy = f.top - l.top;

    card.style.transform  = `translate(${dx}px,${dy}px)`;
    card.style.transition = 'transform 0s';

    requestAnimationFrame(() => {
      card.style.transform  = '';
      card.style.transition = 'transform 400ms cubic-bezier(.4,.2,.2,1)';
    });

    card.addEventListener('transitionend', () => card.style.transition = '');
  });
}

// 3. bind dei bottoni
document.querySelectorAll('.tag-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelector('.tag-btn.active')?.classList.remove('active');
    btn.classList.add('active');

    const key = btn.dataset.sort;
    const asc = btn.dataset.dir === 'asc';
	console.log(`Sorting by ${key} in ${asc ? 'ascending' : 'descending'} order`);
    sortAndAnimate(key, asc);
  });
});
