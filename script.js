document.getElementById('year').textContent = new Date().getFullYear();

// Highlight the section currently in view, without changing navigation behavior.
const links = document.querySelectorAll('nav a');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      links.forEach((link) => {
        if (link.hash === `#${entry.target.id}`) {
          link.setAttribute('aria-current', 'location');
        } else {
          link.removeAttribute('aria-current');
        }
      });
    }
  }, { rootMargin: '-10% 0px -60% 0px', threshold: 0 });
  document.querySelectorAll('main section[id]').forEach((section) => observer.observe(section));
}

const pronunciationButton = document.querySelector('.pronunciation-button');
const pronunciationAudio = document.getElementById('una-pronunciation');
pronunciationButton.addEventListener('click', async () => {
  try {
    if (pronunciationAudio.readyState > 0) pronunciationAudio.currentTime = 0;
    await pronunciationAudio.play();
    pronunciationButton.classList.add('is-playing');
  } catch {
    pronunciationButton.title = 'Audio could not play. Please try again.';
  }
});
pronunciationAudio.addEventListener('ended', () => {
  pronunciationButton.classList.remove('is-playing');
});
